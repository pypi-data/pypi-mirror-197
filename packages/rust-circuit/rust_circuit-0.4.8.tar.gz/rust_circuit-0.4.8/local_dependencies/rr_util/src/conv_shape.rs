use std::iter::zip;

use anyhow::{bail, Context, Result};
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyValueError, prelude::*};
use thiserror::Error;

use crate::{
    python_error_exception,
    shape::{broadcast_shapes, Shape, Size},
};

pub fn conv_shape(
    input_shape: &Shape,
    filter_shape: &Shape,
    stride: &[usize],
    padding: &[(usize, usize)],
) -> Result<Shape> {
    if stride.len() != padding.len() {
        bail!(ConvError::ConvStridePaddingNotFull {
            stride: stride.len(),
            padding: padding.len(),
        });
    }
    if stride.len() > 3 {
        bail!(ConvError::NotSupportedYet {
            string: "Conv over more than 3 dims not supported".into(),
        });
    }

    let dims = stride.len();
    let input_batch_shape: Shape =
        if let Some(input_batch_rank) = input_shape.len().checked_sub(dims + 1) {
            input_shape[..input_batch_rank].into()
        } else {
            bail!(ConvError::ConvInputWrongShape {});
        };

    let filter_batch_shape: Shape =
        if let Some(filter_batch_rank) = filter_shape.len().checked_sub(dims + 2) {
            input_shape[..filter_batch_rank].into()
        } else {
            bail!(ConvError::ConvFilterWrongShape {});
        };
    let output_batch_shape = broadcast_shapes(&[&input_batch_shape[..], &filter_batch_shape[..]])
        .context("input and filter batch shapes dont broadcast")?;

    if !filter_batch_shape.is_empty() {
        bail!(ConvError::NotSupportedYet {
            string: format!(
                "Batch dims on filter aren't supported yet, found {:?}",
                filter_batch_shape
            ),
        });
    }
    let out_channels = filter_shape[filter_batch_shape.len()];
    let in_channels = filter_shape[filter_shape.len() - 1];
    if !in_channels.eq_if_known(input_shape[input_shape.len() - 1]) {
        bail!(ConvError::ConvInputFilterDifferentNumInputChannels {
            filter: in_channels,
            input: input_shape[input_shape.len() - 1],
        });
    }
    let input_conv_shape = &input_shape[input_batch_shape.len()..input_batch_shape.len() + dims];
    let filter_kernel_shape = &filter_shape[filter_shape.len() - dims - 1..filter_shape.len() - 1];
    let input_conv_shape_padded_minus_edges: Shape =
        zip(input_conv_shape, zip(padding, filter_kernel_shape))
            .map(|(input_l, (padding, kernel_l))| input_l - (kernel_l - 1) + padding.0 + padding.1)
            .collect();
    let new_conv_shape: Shape = zip(&input_conv_shape_padded_minus_edges, stride)
        .map(|(i, s)| {
            if !(i % *s).is_if_known(0) {
                Err(ConvError::ConvStrideMustDivide {
                    shape: input_conv_shape_padded_minus_edges.clone(),
                    stride: stride.to_vec(),
                })
                .context("hi")
            } else {
                Ok(i / *s)
            }
        })
        .collect::<Result<Shape>>()?;

    Ok(output_batch_shape
        .into_iter()
        .chain(new_conv_shape)
        .chain(std::iter::once(out_channels))
        .collect())
}

#[apply(python_error_exception)]
#[base_error_name(Conv)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ConvError {
    #[error("{string} ({e_name})")]
    NotSupportedYet { string: String },

    #[error("Conv requires stride and padding to be full size, got stride len {stride} padding len {padding} ({e_name})")]
    ConvStridePaddingNotFull { stride: usize, padding: usize },

    #[error("Conv input wrong shape ({e_name})")]
    ConvInputWrongShape {},

    #[error("Conv input wrong shape ({e_name})")]
    ConvFilterWrongShape {},

    #[error("Conv kernel shape must be all odd, got ({e_name})")]
    ConvFilterMustBeOddLength { shape: Shape },

    #[error("Conv stride must evenly divide ({e_name})")]
    ConvStrideMustDivide { shape: Shape, stride: Vec<usize> },

    #[error("Conv groups ({groups}) must divide input channels ({in_channels}) and output channels ({out_channels}) ({e_name})")]
    ConvGroupsMustDivide {
        groups: usize,
        in_channels: usize,
        out_channels: usize,
    },

    #[error(
        "Conv input and filter must have same number of input channels, got {input} and {filter} ({e_name})"
    )]
    ConvInputFilterDifferentNumInputChannels { input: Size, filter: Size },
}
