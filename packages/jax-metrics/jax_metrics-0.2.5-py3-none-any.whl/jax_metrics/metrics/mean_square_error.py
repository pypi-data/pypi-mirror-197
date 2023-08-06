import typing as tp

import jax
import jax.numpy as jnp

from jax_metrics import types
from jax_metrics.metrics.mean import Mean

M = tp.TypeVar("M", bound="MeanSquareError")


def _mean_square_error(preds: jax.Array, target: jax.Array) -> jax.Array:
    """Calculates values required to update/compute Mean Square Error. Cast preds to have the same type as target.

    Args:
        preds: Predicted tensor
        target: Ground truth tensor

    Returns:
        jax.Array values needed to update Mean Square Error
    """

    target = target.astype(preds.dtype)
    return jnp.square(preds - target)


class MeanSquareError(Mean):
    def __init__(
        self,
        dtype: tp.Optional[jnp.dtype] = None,
    ):
        """
        `Computes Mean Square Error`_ (MSE):
        .. math:: \text{MSE} = \frac{1}{N}\sum_i^N(y_i - \hat{y_i})^2
        Where :math:`y` is a tensor of target values, and :math:`\hat{y}` is a tensor of predictions.

        Args:
            name:
                Module name
            dtype:
                Metrics states initialization dtype


        Example:
        >>> import jax.numpy as jnp
        >>> from jax_metrics.metrics.mean_square_error import MeanSquareError

        >>> target = jnp.array([3.0, -0.5, 2.0, 7.0])
        >>> preds = jnp.array([3.0, -0.5, 2.0, 7.0])

        >>> mse = MeanSquareError()
        >>> mse(preds, target)

        """
        super().__init__(dtype=dtype)

    def update(
        self: M,
        target: jax.Array,
        preds: jax.Array,
        sample_weight: tp.Optional[jax.Array] = None,
        **_,
    ) -> M:
        """
        Accumulates metric statistics. `target` and `preds` should have the same shape.

        Arguments:
            target:
                Ground truth values. shape = `[batch_size, d0, .. dN]`.
            preds:
                The predicted values. shape = `[batch_size, d0, .. dN]`
            sample_weight:
                Optional weighting of each example. Defaults to 1. shape = `[batch_size, d0, .. dN]`

        Returns:
            MeanSquareError instance with updated state
        """
        values = _mean_square_error(preds, target)
        return super().update(values, sample_weight)
