import typing as tp

import jax
import jax.numpy as jnp

from jax_metrics import types
from jax_metrics.metrics.mean import Mean


def _mean_absolute_error(preds: jax.Array, target: jax.Array) -> jax.Array:
    """Calculates values required to update/compute Mean Absolute Error. Cast preds to have the same type as target.

    Args:
        preds: Predicted tensor
        target: Ground truth tensor

    Returns:
        jax.Array values needed to update Mean Absolute Error
    """

    target = target.astype(preds.dtype)
    return jnp.abs(preds - target)


class MeanAbsoluteError(Mean):
    def __init__(
        self,
        name: tp.Optional[str] = None,
        dtype: tp.Optional[jnp.dtype] = None,
    ):
        """
        `Computes Mean Absolute Error`_ (MAE):
        .. math:: \text{MAE} = \frac{1}{N}\sum_i^N | y_i - \hat{y_i} |
        Where :math:`y` is a tensor of target values, and :math:`\hat{y}` is a tensor of predictions.

        Args:
            name:
                Module name
            dtype:
                Metrics states initialization dtype


        Example:
        >>> import jax.numpy as jnp
        >>> from jax_metrics.metrics.mean_absolute_error import MeanAbsolutError

        >>> target = jnp.array([3.0, -0.5, 2.0, 7.0])
        >>> preds = jnp.array([3.0, -0.5, 2.0, 7.0])

        >>> mae = MeanAbsolutError()
        >>> mae(preds, target)

        """
        super().__init__(dtype=dtype)

    def update(
        self,
        target: jax.Array,
        preds: jax.Array,
        sample_weight: tp.Optional[jax.Array] = None,
        **_,
    ) -> tp.Any:
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
            MeanAbsoluteError instance with updated state
        """
        values = _mean_absolute_error(preds, target)
        return super().update(values, sample_weight)
