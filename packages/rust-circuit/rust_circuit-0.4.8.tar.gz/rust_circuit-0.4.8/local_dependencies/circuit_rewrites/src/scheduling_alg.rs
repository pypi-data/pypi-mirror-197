use std::{
    cmp::max,
    sync::{
        atomic::{AtomicBool, AtomicUsize, Ordering},
        mpsc::channel,
        Arc,
    },
    time::Instant,
};

use anyhow::{bail, Result};
use itertools::Itertools;
use rand::{rngs::SmallRng, Rng, SeedableRng};
use rr_util::{print::oom_fmt, python_println, sv, timed, timed_value, util::HashBytes};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use smallvec::SmallVec as Sv;

use crate::scheduled_execution::SchedulingOOMError;

#[derive(Clone, Debug)]
pub struct DagSimpSettings {
    pub same_ratio: f64,
    pub tiny_size: usize,
    pub exhaustive_settle_ns: usize,
    pub exhaustive_give_up_ns: usize,
    pub mem_limit: usize,
    pub verbose: usize,
    pub parallelism: Option<usize>,
}

impl Default for DagSimpSettings {
    fn default() -> Self {
        Self {
            same_ratio: 0.25,
            tiny_size: 200_000,
            mem_limit: 100_000_000, // overridden by OptimizationSettings.max_memory
            exhaustive_settle_ns: 8_000_000,
            exhaustive_give_up_ns: 400_000_000, /* overridden by OptimizationSettings.scheduling_timeout */
            verbose: 0,
            parallelism: Some(8),
        }
    }
}

// rule: there can be only one edge between each pair of nodes
#[derive(Default, Clone, Debug)]
pub struct Dag {
    pub children: Vec<Sv<[u32; 6]>>,
    pub parents: Vec<Sv<[u32; 6]>>,
    pub node_costs: Vec<usize>,
    pub node_to_orig: HashMap<u32, Sv<[u32; 6]>>,
    pub node_hashes: Vec<HashBytes>,
    pub hash_to_node: HashMap<HashBytes, usize>,
    pub pre_root_nodes: Vec<u32>,
}
impl Dag {
    pub fn get_outputs(&self) -> Vec<usize> {
        let result = rr_util::util::filter_to_idx(self.parents.iter(), |y: &&Sv<_>| y.is_empty());
        result
    }

    pub fn expand_order(&self, order: Vec<u32>) -> Vec<u32> {
        self.pre_root_nodes
            .iter()
            .chain(order.iter().flat_map(|x| self.node_to_orig[x].iter()))
            .cloned()
            .collect()
    }

    pub fn cost(&self) -> usize {
        self.node_to_orig
            .iter()
            .map(|x| self.node_costs[*x.0 as usize])
            .max()
            .unwrap_or(0)
    }

    pub fn compute_schedule(&self, settings: &DagSimpSettings) -> Result<Vec<u32>> {
        let mut self_useds = self.clone();
        self_useds.used_to_beginning();
        Ok(
            self_useds.expand_order(if self_useds.node_to_orig.len() <= 1 {
                self_useds.node_to_orig.keys().cloned().collect::<Vec<_>>()
            } else {
                ExhaustiveScheduler::new(self_useds.clone(), None, settings.clone(), None)
                    .run_portfolio_maybe()?
                    .into_iter()
                    .map(|(a, _b)| a)
                    .collect()
            }),
        )
    }

    // Renumbers everything! breaks all node references!
    pub fn used_to_beginning(&mut self) {
        let new_to_old: Vec<u32> = self.node_to_orig.keys().cloned().collect();
        let old_to_new: HashMap<u32, u32> = new_to_old
            .iter()
            .enumerate()
            .map(|(i, j)| (*j, i as u32))
            .collect();
        self.node_to_orig = new_to_old
            .iter()
            .enumerate()
            .map(|(i, o)| (i as u32, self.node_to_orig[o].clone()))
            .collect();
        self.children = new_to_old
            .iter()
            .map(|i| {
                self.children[*i as usize]
                    .iter()
                    .map(|j| old_to_new[j])
                    .collect()
            })
            .collect();
        self.parents = new_to_old
            .iter()
            .map(|i| {
                self.parents[*i as usize]
                    .iter()
                    .map(|j| old_to_new[j])
                    .collect()
            })
            .collect();
        self.node_costs = new_to_old
            .iter()
            .map(|x| self.node_costs[*x as usize])
            .collect();
    }

    // UNFINISHED

    // simplify all

    pub fn simplify(&mut self, simp_settings: &DagSimpSettings) -> Result<bool> {
        let mut result = false;
        while self.simplify_pass(simp_settings, false)? {
            if simp_settings.verbose > 2 {
                println!("did pass {}", self.node_to_orig.len());
                self.print_cytoscape_link();
            }
            result = true;
        }
        while self.simplify_pass(simp_settings, true)? {
            if simp_settings.verbose > 2 {
                self.print_cytoscape_link();
                println!("did pass {}", self.node_to_orig.len());
            }
            result = true;
        }
        Ok(result)
    }

    // warning: I'm modifying the graph as I'm traversing it. edits must not mess with topo frontier
    pub fn simplify_pass(
        &mut self,
        simp_settings: &DagSimpSettings,
        do_isolated: bool,
    ) -> Result<bool> {
        // simplify bottom_up
        let mut did_anything = false;
        if do_isolated {
            did_anything |= self.schedule_isolated(simp_settings)?;
        }
        // we don't re-check whether leaves are still leaves, so
        // no rewrite can add children to an int which previously had no children
        let mut nodes_visited: HashSet<u32> = Default::default();
        let mut bottom_frontier: Vec<u32> = self.get_bottom_frontier();
        let mut parenties: Vec<u32> = vec![];
        while !bottom_frontier.is_empty() {
            let popped = bottom_frontier.pop().unwrap();
            nodes_visited.insert(popped);
            if !self.node_to_orig.contains_key(&popped) {
                continue;
            }
            macro_rules! and_namer {
                ($fnident:expr) => {
                    (stringify!($fnident), $fnident)
                };
            }
            let simps: [(
                &'static str,
                fn(&mut Dag, u32, &DagSimpSettings) -> Option<Vec<u32>>,
            ); 8] = [
                and_namer!(Dag::try_inline_lone_sibling),
                and_namer!(Dag::try_merge_simple_diamond),
                and_namer!(Dag::try_merge_chain_close),
                and_namer!(Dag::try_elim_middle_monotonic),
                and_namer!(Dag::try_merge_half_diamond),
                and_namer!(Dag::try_elim_small_leaf),
                and_namer!(Dag::try_merge_descending_peaks),
                and_namer!(Dag::try_merge_multi_diamond_below),
            ];
            for (simp_name, simplification) in simps {
                if let Some(the_parenties) = simplification(self, popped, simp_settings) {
                    parenties = the_parenties;
                    did_anything = true;
                    if simp_settings.verbose > 2 {
                        println!("did simp {}", simp_name);
                    }
                    break;
                }
            }
            // println!("frontier {:?}", &bottom_frontier);
            if self.node_to_orig.contains_key(&popped) {
                for parent in &self.parents[popped as usize] {
                    if self.children[*parent as usize]
                        .iter()
                        .all(|x| nodes_visited.contains(x))
                        && !nodes_visited.contains(parent)
                    {
                        bottom_frontier.push(*parent);
                    }
                }
            } else {
                for parent in &parenties {
                    if self.children[*parent as usize]
                        .iter()
                        .all(|x| nodes_visited.contains(x))
                        && !nodes_visited.contains(parent)
                    {
                        bottom_frontier.push(*parent);
                    }
                }
            }
        }
        if nodes_visited.len() < self.node_to_orig.len() {
            println!("didnt visit enough nodes {:?}", &self);
        }

        // println!("did it {:?}", self.node_to_orig);
        Ok(did_anything)
    }

    // try simplification at point

    pub fn try_elim_small_leaf(
        &mut self,
        node: u32,
        simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if self.children[node as usize].is_empty() && self.is_tiny(node, simp_settings) {
            let result = Some(self.parents[node as usize].iter().cloned().collect());
            self.seperate_integrate_node(node);
            return result;
        }
        None
    }

    pub fn try_merge_half_diamond(
        &mut self,
        node: u32,
        _simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if let [a, b] = self.parents[node as usize][..] {
            if let Some(parent) = self.get_sole_parent(a) && self.parents[b as usize].iter().contains(&parent){
                self.merge_add(node, b, false);
                return Some(Default::default());
            }
            if let Some(parent) = self.get_sole_parent(b) && self.parents[a as usize].iter().contains(&parent){
                self.merge_add(node, a, false);
                return Some(Default::default());
            }
        }
        None
    }

    pub fn try_merge_simple_diamond(
        &mut self,
        node: u32,
        _simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if let [a, b] = self.parents[node as usize][..] && a!=b && self.parents[a as usize].len() == 1
                && self.parents[b as usize].len() == 1 && self.parents[a as usize][0] == self.parents[b as usize][0] {
            let top = self.parents[a as usize][0];
            let new_cost = self.node_costs[a as usize] + self.node_costs[b as usize];
            let intermediate = self.split_node_extra_below(top);
            self.merge_add(intermediate, a, true);
            self.merge_add(intermediate, b, true);
            self.node_costs[intermediate as usize] = new_cost;
            return Some(Default::default());
        }
        None
    }

    pub fn try_merge_multi_diamond_below(
        &mut self,
        node: u32,
        _simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if self.children[node as usize].len() <= 1 {
            return None;
        }
        if self.children[node as usize]
            .iter()
            .all(|&c| self.parents[c as usize].len() == 1 && self.children[c as usize].len() == 1)
            && self.children[node as usize].iter().all(|&c| {
                self.children[c as usize][0]
                    == self.children[self.children[node as usize][0] as usize][0]
            })
        {
            let mut new_cost = 0;
            let intermediate = self.split_node_extra_below(node);
            for c in self.children[intermediate as usize].clone() {
                self.merge_add(intermediate, c, true);
                new_cost += self.node_costs[c as usize];
            }
            self.node_costs[intermediate as usize] = new_cost;
            return Some(Default::default());
        }
        None
    }

    pub fn try_merge_chain_close(
        &mut self,
        node: u32,
        simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if let Some(parent_node) = self.get_sole_parent(node) {
            if self.are_node_memories_similar(parent_node, node, simp_settings)
                || self.is_tiny(parent_node, simp_settings) && self.is_tiny(node, simp_settings)
            {
                self.merge_larger(node, parent_node, false);
                return Some(Default::default());
            }
        }
        None
    }

    pub fn try_elim_middle_monotonic(
        &mut self,
        node: u32,
        _simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if let Some(parent_node) = self.get_sole_parent(node) {
            if let Some(grandparent_node) = self.get_sole_parent(parent_node) {
                if self.node_costs[node as usize] <= self.node_costs[parent_node as usize]
                    && self.node_costs[parent_node as usize]
                        < self.node_costs[grandparent_node as usize]
                {
                    self.merge_larger(parent_node, grandparent_node, false);
                    return Some(Default::default());
                }
                if self.node_costs[node as usize] >= self.node_costs[parent_node as usize]
                    && self.node_costs[parent_node as usize]
                        >= self.node_costs[grandparent_node as usize]
                {
                    self.merge_larger(node, parent_node, false);
                    return Some(Default::default());
                }
            }
        }
        None
    }

    pub fn try_inline_lone_sibling(
        &mut self,
        node: u32,
        simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if self.parents[node as usize].len() == 1
            && self.children[self.parents[node as usize][0] as usize].len() > 1
            && self.children[node as usize].is_empty()
        {
            let parent_node = self.parents[node as usize][0];
            if self.node_costs[parent_node as usize] as f64 * simp_settings.same_ratio
                >= self.node_costs[node as usize] as f64
            {
                self.merge_add(node, parent_node, false);
            } else {
                self.inline_sibling(self.parents[node as usize][0], node);
            }
            return Some(Default::default());
        }
        None
    }

    pub fn try_merge_descending_peaks(
        &mut self,
        node: u32,
        _simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        let mut chain = self.get_parent_chain(node);
        if chain.len() <= 3 {
            return None;
        }
        let mut did_anything = false;
        // self.print_cytoscape_link();
        let mut counter = 0;
        while !chain.is_empty() {
            // println!(
            //     "merging descending peaks {:?}",
            //     chain
            //         .iter()
            //         .map(|x| (*x, self.node_costs[*x as usize]))
            //         .collect::<Vec<_>>()
            // );
            let max_val = chain
                .iter()
                .map(|x| self.node_costs[*x as usize])
                .max()
                .unwrap();
            let max_pos = chain
                .iter()
                .position(|x| self.node_costs[*x as usize] == max_val)
                .unwrap();
            // println!("max pos {}", max_pos);
            if counter != 0 {
                for i in 1..max_pos + 1 {
                    did_anything = true;
                    self.merge_larger(chain[0], chain[i], false);
                }
            }
            chain.drain(0..max_pos + 1);
            if chain.is_empty() {
                break;
            }
            let min_val = chain
                .iter()
                .map(|x| self.node_costs[*x as usize])
                .min()
                .unwrap();
            let min_pos = chain.len()
                - 1
                - chain
                    .iter()
                    .rev()
                    .position(|x| self.node_costs[*x as usize] == min_val)
                    .unwrap();
            // println!("min pos {}", min_pos);
            for i in 1..min_pos {
                did_anything = true;
                self.merge_larger(chain[0], chain[i], false);
            }
            chain.drain(0..min_pos + 1);
            counter += 1;
        }
        if did_anything {
            // self.print_cytoscape_link();
            return Some(vec![]);
        }
        None
    }

    // composite rewrites
    pub fn inline_sibling(&mut self, parent: u32, child: u32) {
        let new_lower = self.split_node_extra_below(parent);
        self.merge_add(child, new_lower, false);
    }

    // raw rewrites

    pub fn merge_add(&mut self, target: u32, absorbed: u32, is_target_top: bool) {
        let to_add = self.node_costs[absorbed as usize];
        self.merge_nodes(target, absorbed, is_target_top);
        self.node_costs[target as usize] += to_add;
    }

    pub fn merge_larger(&mut self, target: u32, absorbed: u32, is_target_top: bool) {
        let new_node_cost = max(
            self.node_costs[absorbed as usize],
            self.node_costs[target as usize],
        );
        self.merge_nodes(target, absorbed, is_target_top);
        self.node_costs[target as usize] = new_node_cost;
    }

    // doesn't change node_costs. you have to change this yourself
    pub fn merge_nodes(&mut self, target: u32, absorbed: u32, is_target_top: bool) {
        assert!(target != absorbed);
        if !self.node_to_orig.contains_key(&target) {
            self.print_cytoscape_link();
            dbg!(self);
            panic!("target not in graph")
        }
        self.children[target as usize] = self.children[target as usize]
            .iter()
            .chain(self.children[absorbed as usize].iter())
            .filter(|x| **x != absorbed && **x != target)
            .unique()
            .cloned()
            .collect();
        self.parents[target as usize] = self.parents[target as usize]
            .iter()
            .chain(self.parents[absorbed as usize].iter())
            .filter(|x| **x != absorbed && **x != target)
            .unique()
            .cloned()
            .collect();
        for absorbed_child in &self.children[absorbed as usize] {
            self.parents[*absorbed_child as usize] = self.parents[*absorbed_child as usize]
                .iter()
                .map(|x| if *x == absorbed { target } else { *x })
                .unique()
                .collect();
        }
        for absorbed_parent in &self.parents[absorbed as usize] {
            self.children[*absorbed_parent as usize] = self.children[*absorbed_parent as usize]
                .iter()
                .map(|x| if *x == absorbed { target } else { *x })
                .unique()
                .collect();
        }

        let removed_to_orig = if is_target_top {
            self.node_to_orig
                .remove(&absorbed)
                .unwrap()
                .into_iter()
                .chain(self.node_to_orig[&target].clone())
                .collect()
        } else {
            self.node_to_orig[&target]
                .clone()
                .into_iter()
                .chain(self.node_to_orig.remove(&absorbed).unwrap())
                .collect()
        };
        self.node_to_orig.insert(target, removed_to_orig);
    }

    pub fn split_node_extra_below(&mut self, node: u32) -> u32 {
        let new_id = self.node_costs.len() as u32;
        assert_eq!(self.node_costs.len(), self.children.len());
        assert_eq!(self.node_costs.len(), self.parents.len());
        self.node_costs.push(self.node_costs[node as usize]);
        self.node_to_orig.insert(new_id, sv![]);
        self.children.push(self.children[node as usize].clone());
        self.parents.push(sv![node]);
        self.children[node as usize] = sv![new_id];
        for child in &self.children[new_id as usize] {
            for x in self.parents[*child as usize].iter_mut() {
                if *x == node {
                    *x = new_id;
                }
            }
        }
        new_id
    }

    pub fn seperate_integrate_node(&mut self, node: u32) {
        assert!(self.children[node as usize].is_empty());
        let cost = self.node_costs[node as usize];
        for parent in &self.parents[node as usize] {
            self.children[*parent as usize] = self.children[*parent as usize]
                .iter()
                .filter(|x| **x != node)
                .cloned()
                .collect();
            self.node_costs[*parent as usize] += cost;
        }
        self.pre_root_nodes
            .extend(self.node_to_orig.remove(&node).unwrap());
    }

    pub fn seperate_node(&mut self, node: u32) {
        assert!(self.children[node as usize].is_empty());
        for parent in &self.parents[node as usize] {
            self.children[*parent as usize] = self.children[*parent as usize]
                .iter()
                .filter(|x| **x != node)
                .cloned()
                .collect();
        }
        self.pre_root_nodes
            .extend(self.node_to_orig.remove(&node).unwrap());
    }

    // passes

    // schedule isolated pass
    pub fn schedule_isolated(&mut self, settings: &DagSimpSettings) -> Result<bool> {
        let isolated = self.find_isolated(settings);
        // self.print_cytoscape_link();
        // println!("{:?} ", &isolated);
        let mut did_anything = false;
        for iso in &isolated {
            let direct_only_sub = self.get_direct_only_sub(&iso.2);
            // direct_only_sub.print_cytoscape_link();
            let required_first = Some(
                *direct_only_sub
                    .node_to_orig
                    .iter()
                    .find(|(_k, v)| v[0] == iso.1)
                    .unwrap()
                    .0,
            );
            let resy = ExhaustiveScheduler::new(
                direct_only_sub.clone(),
                required_first,
                settings.clone(),
                None,
            )
            .run_portfolio_maybe();

            if resy.is_err() && did_anything {
                return Ok(true);
            }

            let order = resy?
                .iter()
                .map(|(k, v)| (direct_only_sub.node_to_orig[k][0], *v))
                .collect();
            // assert!(order[0].0==iso.1 && order.last().unwrap().0==iso.0);
            self.replace_isolated_with_linear(&order);
            if settings.verbose > 2 {
                println!("did isolated");
            }
            did_anything = true;
            // println!("FINISHED ISOLATED SCHEDULE");
        }
        // self.print_cytoscape_link();
        Ok(!isolated.is_empty())
    }

    pub fn find_isolated(&self, _settings: &DagSimpSettings) -> Vec<(u32, u32, HashSet<u32>)> {
        let mut result = vec![];
        for &upper in self.node_to_orig.keys() {
            let mut done: HashSet<u32> = HashSet::from_iter([upper]);
            let mut frontier: Vec<u32> = self.children[upper as usize]
                .iter()
                .filter(|x| self.parents[**x as usize].len() == 1)
                .cloned()
                .collect();
            let mut children: HashSet<u32> =
                self.children[upper as usize].iter().cloned().collect();
            while !frontier.is_empty() {
                let popped = frontier.pop().unwrap();
                done.insert(popped);
                children.remove(&popped);
                if self.parents[popped as usize]
                    .iter()
                    .any(|x| !done.contains(x))
                {
                    break;
                }
                if children.is_empty() {
                    if done.len() > 3 {
                        result.push((upper, popped, done.clone()));
                    }
                    break;
                }
                // if self.children[popped as usize].is_empty() {
                //     break;
                // }
                children.extend(&self.children[popped as usize]);
                for &child in &self.children[popped as usize] {
                    if self.parents[child as usize]
                        .iter()
                        .all(|x| done.contains(x))
                    {
                        frontier.push(child);
                    }
                }
            }
        }
        result.sort_unstable_by(|a, b| a.2.len().cmp(&b.2.len()));
        result
    }

    pub fn replace_isolated_with_linear(&mut self, order: &Vec<(u32, usize)>) {
        // println!("linearizing order {:?}", order);
        // because this is isolated except for first children and last parents,
        // we don't need to fix up any backrefs
        for (i, (node, cost)) in order.iter().enumerate() {
            if i != 0 {
                self.children[*node as usize] = sv![order[i - 1_usize].0];
            }
            if i != order.len() - 1 {
                self.parents[*node as usize] = sv![order[i + 1_usize].0];
                self.node_costs[*node as usize] = *cost;
            }
        }
    }

    // util

    pub fn are_node_memories_similar(
        &self,
        a: u32,
        b: u32,
        simp_settings: &DagSimpSettings,
    ) -> bool {
        (self.node_costs[a as usize] as f64 - self.node_costs[b as usize] as f64).abs()
            < simp_settings.same_ratio
                * (self.node_costs[a as usize] as f64 + self.node_costs[b as usize] as f64)
                / 2.0
    }

    pub fn get_sole_parent(&self, node: u32) -> Option<u32> {
        if self.parents[node as usize].len() == 1
            && self.children[self.parents[node as usize][0] as usize].len() == 1
        {
            return Some(self.parents[node as usize][0]);
        }
        None
    }

    pub fn is_tiny(&self, node: u32, settings: &DagSimpSettings) -> bool {
        self.node_costs[node as usize] < settings.tiny_size
    }

    pub fn get_bottom_frontier(&self) -> Vec<u32> {
        self.node_to_orig
            .iter()
            .filter(|(k, _n)| self.children[**k as usize].is_empty())
            .map(|(k, _n)| *k)
            .collect()
    }

    pub fn get_parent_chain(&self, node: u32) -> Vec<u32> {
        let mut result = vec![node];
        while self.parents[*result.last().unwrap() as usize].len() == 1
            && self.children[self.parents[*result.last().unwrap() as usize][0] as usize].len() == 1
        {
            result.push(self.parents[*result.last().unwrap() as usize][0]);
        }
        result
    }

    pub fn get_direct_only_sub(&self, set: &HashSet<u32>) -> Dag {
        let ordered: Vec<u32> = set.iter().cloned().collect();
        Dag {
            children: set
                .iter()
                .map(|x| {
                    self.children[*x as usize]
                        .iter()
                        .filter_map(|y| ordered.iter().position(|z| z == y).map(|z| z as u32))
                        .collect()
                })
                .collect(),
            parents: ordered
                .iter()
                .map(|x| {
                    self.parents[*x as usize]
                        .iter()
                        .filter_map(|y| ordered.iter().position(|z| z == y).map(|z| z as u32))
                        .collect()
                })
                .collect(),
            node_costs: ordered
                .iter()
                .map(|x| self.node_costs[*x as usize])
                .collect(),
            node_to_orig: ordered
                .iter()
                .enumerate()
                .map(|(i, x)| (i as u32, sv![*x]))
                .collect(),
            node_hashes: vec![],
            hash_to_node: Default::default(),
            pre_root_nodes: vec![],
        }
    }

    pub fn get_costs_of_order(&self, order: &[u32]) -> Vec<(u32, usize)> {
        let mut children: Vec<i32> = self.children.iter().map(|x| x.len() as i32).collect();
        let mut parents: Vec<i32> = self.parents.iter().map(|x| x.len() as i32).collect();
        let mut result = vec![];
        for o in order {
            children[*o as usize] -= 1;
            for parent in &self.parents[*o as usize] {
                children[*parent as usize] -= 1;
            }
            for child in &self.children[*o as usize] {
                parents[*child as usize] -= 1;
            }
            result.push((
                *o,
                self.node_to_orig
                    .keys()
                    .filter_map(|i| {
                        if children[*i as usize] < 0 && parents[*i as usize] >= 1 {
                            Some(self.node_costs[*i as usize])
                        } else {
                            None
                        }
                    })
                    .sum(),
            ));
        }
        result
    }

    // misc
    pub fn print_cytoscape_link(&self) {
        python_println!("{}", self.repr_cytoscape_link());
    }
    pub fn repr_cytoscape_link(&self) -> String {
        let not_excaped = format!(
            "{{\"graphName\":\"\",\"graphValue\":[{},{}]}}",
            self.node_to_orig
                .keys()
                .map(|i| format!(
                    "{{\"id\":\"{}\",\"name\":{:?},\"label\": \"{}: {}\"}}",
                    i,
                    "",
                    *i,
                    oom_fmt(self.node_costs[*i as usize])
                ))
                .collect::<Vec<_>>()
                .join(","),
            self.node_to_orig
                .keys()
                .flat_map(|i| self.children[*i as usize]
                    .iter()
                    .map(|j| format!(
                        "{{\"source\":\"{}\",\"target\":\"{}\",\"label\": \"\"}}",
                        i, j
                    ))
                    .collect::<Vec<_>>())
                .collect::<Vec<_>>()
                .join(",")
        );
        format!(
            "http://interp-tools.redwoodresearch.org/#/networkgraph/{}",
            url_escape::encode_fragment(&not_excaped)
        )
    }
}

pub fn filter_to_idx<'a, T, F>(col: &'a [T], f: F) -> impl Iterator<Item = u32> + 'a
where
    F: Fn(&T) -> bool + 'a,
{
    col.iter()
        .enumerate()
        .filter(move |(_i, x)| f(x))
        .map(|(i, _x)| i as u32)
}

#[derive(Clone, Debug)]
struct VecStack<T> {
    storage: Vec<T>,
    levels: Vec<usize>,
    start: usize,
}
impl<T> VecStack<T> {
    fn new() -> Self {
        Self {
            storage: vec![],
            levels: vec![],
            start: 0,
        }
    }
    #[inline]
    fn pop_level(&mut self) {
        let n = self.levels.pop().unwrap();
        self.storage.truncate(n);
        self.start = self.levels.last().copied().unwrap_or(0);
    }
    #[inline]
    fn push_level(&mut self) {
        self.levels.push(self.storage.len());
        self.start = self.storage.len();
    }

    fn clear(&mut self) {
        self.storage.clear();
        self.levels.clear();
        self.start = 0;
    }

    fn push_copy_last(&mut self)
    where
        T: Copy,
    {
        let l = self.storage.len();
        self.storage.extend_from_within(self.start..);
        self.levels.push(l);
        self.start = l;
    }

    #[inline]
    fn extend(&mut self, x: impl IntoIterator<Item = T>) {
        self.storage.extend(x)
    }
    #[inline]
    fn last_swap_remove(&mut self, ix: usize) -> T {
        self.storage.swap_remove(self.start + ix)
    }
    #[inline]
    fn last(&self) -> &[T] {
        &self.storage[self.start..]
    }
    #[inline]
    fn last_mut(&mut self) -> &mut [T] {
        &mut self.storage[self.start..]
    }
    #[inline]
    fn last_len(&self) -> usize {
        self.storage.len() - self.start
    }
    #[inline]
    fn push(&mut self, x: T) {
        self.storage.push(x)
    }
}

#[derive(Clone, Debug)]
struct ExhaustiveScheduler {
    dag: Dag,
    parents_left: Vec<u16>,
    num_parents: Vec<u16>,
    entry_point: Option<u32>, // alive at start of schedule
    best: (Vec<(u32, usize)>, usize),
    order_nodes: VecStack<(u32, usize)>, /* (node, max cost) for chosen node & propagations. max cost always <= max_cost_so_far. stack has a level per entry in order */
    order: Vec<(u32, usize, usize)>, /* (choice ix in options_stack entry, alive cost before choice, max cost so far before choice) */
    alive_cost: usize,
    max_cost_so_far: usize,
    options_stack: VecStack<u32>,
    settings: DagSimpSettings,
    rng: Option<SmallRng>,
    found_anything: bool,
    numiters: usize,
}

// todo:
// nogoods: (S, x): S alive => no solution of cost < x
// learn a nogood when backtracking due to checked all alternatives, x = min of achieveable cost returned from failed alternatives (when backtrack keep track of actual cost achieved), S = set alive before backtracking
// do one watch literal scheme on nogoods
// might be interesting to figure out proof rules and/or clause minimization:
// - log nogood size diff assuming we can delete from both sides? to see potential for minimization
// - maybe can delete leaves from S (if nothing else in S depends on them) & subtract their cost from x I think? not totally sure this is valid, and probably won't implement it for now anyways
// - machanical way to dervie proof rules: look at MIP/PB proofs of learned clauses for MIP/pesudo boolean encoding

impl ExhaustiveScheduler {
    pub fn new(
        dag: Dag,
        entry_point: Option<u32>,
        settings: DagSimpSettings,
        random_seed: Option<u64>,
    ) -> Self {
        let mut result = Self {
            parents_left: vec![],
            num_parents: dag
                .parents
                .iter()
                .map(|x| {
                    x.len()
                        .try_into()
                        .expect("node with more than 2^16-1 parents!")
                })
                .collect(),
            entry_point,
            best: (vec![], usize::MAX),
            order: vec![],
            order_nodes: VecStack::new(),
            options_stack: VecStack::new(),
            alive_cost: 0,
            max_cost_so_far: 0,
            dag,
            settings,
            found_anything: false,
            rng: random_seed.map(|rs| SmallRng::seed_from_u64(rs)),
            numiters: 0,
        };
        entry_point.map(|x| {
            // ensure x is alive at start, special cased
            result.num_parents[x as usize] += 1;
        });
        result.reset();
        result
    }
    fn reset(&mut self) {
        self.parents_left = self.num_parents.clone();
        self.order.clear();
        self.order_nodes.clear();
        self.options_stack.clear();
        self.alive_cost = 0;
        self.max_cost_so_far = 0;

        self.options_stack.push_level();
        self.options_stack
            .extend(filter_to_idx(&self.parents_left, |x| *x == 0).map(|x| {
                self.alive_cost += self.dag.node_costs[x as usize];
                x
            }));
        self.max_cost_so_far = self.alive_cost;
    }

    #[inline]
    fn upd_alive_cost(&mut self, x: u32) {
        for &child in &self.dag.children[x as usize] {
            if self.parents_left[child as usize] == self.num_parents[child as usize] {
                self.alive_cost += self.dag.node_costs[child as usize];
            }
        }
    }
    #[inline]
    fn upd_rest(&mut self, x: u32) {
        for &child in &self.dag.children[x as usize] {
            self.parents_left[child as usize] -= 1;
            if self.parents_left[child as usize] == 0 {
                self.options_stack.push(child)
            }
        }
    }

    fn choose(&mut self, i: u32) -> bool {
        let choice = self.options_stack.last()[i as usize] as u32;
        let cost_before = self.alive_cost;
        let max_cost_so_far_before = self.max_cost_so_far;

        self.upd_alive_cost(choice);

        if self.alive_cost >= self.best.1 {
            self.alive_cost = cost_before;
            return false;
        }
        self.max_cost_so_far = self.max_cost_so_far.max(self.alive_cost);

        self.order_nodes.push_level();
        self.order_nodes.push((choice, self.alive_cost));

        self.alive_cost -= self.dag.node_costs[choice as usize];

        self.options_stack.push_copy_last();
        self.options_stack.last_swap_remove(i as usize);

        self.upd_rest(choice);

        loop {
            let mut did_anything = false;
            for ix in (0..self.options_stack.last_len()).into_iter().rev() {
                let x = self.options_stack.last()[ix];
                let cost: usize = self.dag.children[x as usize]
                    .iter()
                    .map(|&ch| {
                        if self.parents_left[ch as usize] == self.num_parents[ch as usize] {
                            self.dag.node_costs[ch as usize]
                        } else {
                            0
                        }
                    })
                    .sum();
                if (cost <= self.dag.node_costs[x as usize])
                    && (cost + self.alive_cost <= self.max_cost_so_far)
                {
                    did_anything = true;
                    self.options_stack.last_swap_remove(ix);
                    self.upd_alive_cost(x);
                    self.order_nodes.push((x, self.alive_cost));
                    assert!(self.alive_cost <= self.max_cost_so_far);
                    self.alive_cost -= self.dag.node_costs[x as usize];
                    self.upd_rest(x);
                }
            }
            if !did_anything {
                break;
            }
        }

        self.order.push((i, cost_before, max_cost_so_far_before));

        // todo maybe take choice here when options_stack.last_len() == 1?

        if let Some(rng) = &mut self.rng {
            let rand_byte: u8 = rng.gen_range(0..5);
            if rand_byte == 0 {
                self.options_stack
                    .last_mut()
                    .sort_unstable_by_key(|&x| -(x as i32));
                return true;
            } else if rand_byte == 1 {
                self.options_stack.last_mut().sort_unstable();
                return true;
            } else if rand_byte == 2 {
                self.options_stack
                    .last_mut()
                    .sort_by_cached_key(|&x| self.dag.parents[x as usize].len());
                return true;
            } else if rand_byte == 3 {
                // alive_cost diff
                self.options_stack.last_mut().sort_by_cached_key(|&x| {
                    self.dag.children[x as usize]
                        .iter()
                        .map(|&ch| {
                            if self.parents_left[ch as usize] == self.num_parents[ch as usize] {
                                self.dag.node_costs[ch as usize]
                            } else {
                                0
                            }
                        })
                        .sum::<usize>() as i64
                        - self.dag.node_costs[x as usize] as i64
                });
                return true;
            }
        }

        self.options_stack.last_mut().sort_by_cached_key(|&x| {
            // lower means tried sooner
            self.dag.children[x as usize]
                .iter()
                .map(|&child| self.parents_left[child as usize])
                .max()
                .unwrap_or(0)
        });
        return true;
    }
    #[inline]
    fn pop(&mut self) -> u32 {
        let popped = self.order.pop().unwrap();
        for (x, _) in self.order_nodes.last().iter().rev() {
            for child in &self.dag.children[*x as usize] {
                self.parents_left[*child as usize] += 1;
            }
        }
        self.order_nodes.pop_level();
        self.options_stack.pop_level();
        self.alive_cost = popped.1;
        self.max_cost_so_far = popped.2;
        popped.0
    }
    fn search_loop(
        &mut self,
        halt_signal: Option<Arc<AtomicBool>>,
        best_cost: Option<Arc<AtomicUsize>>,
        max_cost: usize,
    ) {
        let start_instant = std::time::Instant::now();
        loop {
            // println!("{} {:?}", self.alive_cost, self.order);
            // if self.
            // println!(
            //     "{} {} {}",
            //     self.alive_cost,
            //     self.order.len(),
            //     self.options_stack.last().unwrap().len()
            // );
            if self.options_stack.last_len() == 0 {
                let max_cost = self
                    .order_nodes
                    .storage
                    .iter()
                    .map(|(_, a)| *a)
                    .max()
                    .unwrap();
                assert!(max_cost < self.best.1);
                self.best = (self.order_nodes.storage.clone(), max_cost);
                self.found_anything = true;
                best_cost
                    .as_ref()
                    .map(|x| x.fetch_min(max_cost, std::sync::atomic::Ordering::SeqCst));
                // println!(
                //     "backjump {} {}",
                //     oom_fmt(max_cost),
                //     self.order.len(),
                //     // self.options_stack.levels
                // );
            }
            let best_cost = best_cost
                .as_ref()
                .map_or(usize::MAX, |x| x.load(std::sync::atomic::Ordering::Relaxed))
                .min(self.best.1)
                .min(max_cost);
            // loop until we make a successful choice
            let mut i = 0;
            loop {
                while !self.order.is_empty()
                    && (i >= self.options_stack.last_len() as u32
                        || self.max_cost_so_far >= best_cost)
                {
                    i = self.pop() + 1;
                }
                if self.order.len() == 0 && i != 0 {
                    break;
                }
                if !self.choose(i) {
                    i += 1;
                } else {
                    break;
                }
            }
            if self.done(start_instant, &halt_signal) {
                break;
            }
            self.numiters += 1;
        }
        // println!(
        //     "dag size {} numiters {} cur order len {} best cost {}{}",
        //     self.dag.node_costs.len(),
        //     self.numiters,
        //     self.order.len(),
        //     if self.best.0.len() == 0 {
        //         "no solution".to_owned()
        //     } else {
        //         oom_fmt(self.best.1)
        //     },
        //     if self.order.len() == 0 {
        //         " exhaustive"
        //     } else {
        //         ""
        //     }
        // );
    }
    fn done(&mut self, start_instant: Instant, halt_signal: &Option<Arc<AtomicBool>>) -> bool {
        (self.numiters % 100 == 0
            && ((self.best.1 <= self.settings.mem_limit
                && start_instant.elapsed().as_nanos()
                    > self.settings.exhaustive_settle_ns as u128)
                || (start_instant.elapsed().as_nanos()
                    > self.settings.exhaustive_give_up_ns as u128)
                || (halt_signal
                    .as_ref()
                    .map(|h| h.load(std::sync::atomic::Ordering::Relaxed))
                    .unwrap_or(false))))
            || self.order.len() == 0
    }
    fn get_out(self, halt_signal: Option<Arc<AtomicBool>>) -> Result<(Vec<(u32, usize)>, usize)> {
        halt_signal.map(|x| x.swap(true, std::sync::atomic::Ordering::Relaxed));
        if self.found_anything {
            let mut o = self.best.0;
            self.entry_point.map(|x| {
                let last = o.last().unwrap();
                let last_cost = self.dag.node_costs[last.0 as usize];
                o.push((x, last.1 - last_cost))
            });
            o.reverse();
            assert_eq!(o.len(), self.parents_left.len());
            return Ok((o, self.best.1));
        }
        bail!(SchedulingOOMError::ExhaustiveTimeout {
            iters: self.numiters,
            size: self.dag.node_to_orig.len(),
        })
    }

    fn run(
        mut self,
        halt_signal: Option<Arc<AtomicBool>>,
        best_cost: Option<Arc<AtomicUsize>>,
    ) -> Result<(Vec<(u32, usize)>, usize)> {
        self.search_loop(halt_signal.clone(), best_cost, usize::MAX);
        self.get_out(halt_signal)
        // println!("{}", self.dag.repr_cytoscape_link());
    }

    pub fn run_binary_search(
        mut self,
        halt_signal: Option<Arc<AtomicBool>>,
        best_cost: Option<Arc<AtomicUsize>>,
    ) -> Result<(Vec<(u32, usize)>, usize)> {
        let mut failed_cost = 0;
        let mut best_so_far = usize::MAX;
        let start_instant = std::time::Instant::now();
        let real_timeout = self.settings.exhaustive_settle_ns;
        let mut prev_mid = usize::MAX;
        loop {
            let top = best_cost
                .as_ref()
                .map_or(self.best.1, |x| x.load(Ordering::Relaxed));
            let mid = failed_cost + (top - failed_cost) / 2;
            let remaining_steps = (prev_mid as f64 - mid as f64).log2() - 16.0; // 2^16 = 64kb
            if mid > prev_mid {
                self.reset();
            }
            prev_mid = mid;

            self.settings.exhaustive_settle_ns = real_timeout / (remaining_steps as usize).max(1);
            self.search_loop(halt_signal.clone(), best_cost.clone(), mid);
            self.settings.exhaustive_settle_ns = real_timeout;

            if self.best.1 == best_so_far {
                failed_cost = mid;
            } else {
                // println!("binary search {} -> {}", oom_fmt(mid), oom_fmt(self.best.1));
                best_so_far = self.best.1;
            }
            if self.done(start_instant, &halt_signal) {
                break;
            }
        }
        self.get_out(halt_signal)
    }

    pub fn run_portfolio_raw(self) -> Result<Vec<(u32, usize)>> {
        // println!("portfolio!");
        let halt_signal: Arc<AtomicBool> = Arc::new(AtomicBool::from(false));
        let best_cost: Arc<AtomicUsize> = Arc::new(AtomicUsize::from(usize::MAX));
        let (tx, rx) = channel();
        for i in 0..self.settings.parallelism.unwrap() {
            let tx = tx.clone();
            let mut self_here = self.clone();
            self_here.rng = if i == 0 {
                None
            } else {
                Some(SmallRng::seed_from_u64(i as u64))
            };
            let halt_signal_clone = halt_signal.clone();
            let best_cost = best_cost.clone();
            std::thread::spawn(move || {
                // let randy = self_here.use_rand;
                let (result, _time) = timed_value!(if i < 2 {
                    self_here.run_binary_search(Some(halt_signal_clone), Some(best_cost))
                } else {
                    self_here.run(Some(halt_signal_clone), Some(best_cost))
                });
                // println!("finished {} took {:.2?}", result.is_ok(), _time);
                tx.send(result).unwrap_or(());
            });
        }
        let results = rx
            .iter()
            .take(self.settings.parallelism.unwrap())
            .collect::<Vec<_>>();
        if results.iter().any(|x| x.is_ok()) {
            let x = results
                .into_iter()
                .filter_map(|x| x.ok())
                .min_by_key(|t| t.1)
                .unwrap();
            // println!("best {}", oom_fmt(x.1));
            Ok(x.0)
        } else {
            Ok(results.into_iter().next().unwrap()?.0)
        }
    }

    pub fn run_portfolio_maybe(self) -> Result<Vec<(u32, usize)>> {
        let v = self.settings.verbose >= 2;
        pyo3::Python::with_gil(|py| {
            py.allow_threads(move || {
                if self.dag.node_to_orig.len() > 30
                    && self.settings.parallelism.is_some()
                    && self.settings.parallelism.unwrap() > 1
                {
                    timed!(self.run_portfolio_raw(), 10, v)
                } else {
                    timed!(self.run_binary_search(None, None).map(|x| x.0), 10, v)
                }
            })
        })
    }
}
