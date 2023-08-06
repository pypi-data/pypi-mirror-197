import typing as tp

import jax
import jax.numpy as jnp

from jax_metrics import types
from jax_metrics.metrics.reduce import Reduce, Reduction

M = tp.TypeVar("M", bound="Mean")


class Mean(Reduce):
    """
    Computes the (weighted) mean of the given values.

    For example, if values is `[1, 3, 5, 7]` then the mean is `4`.
    If the weights were specified as `[1, 1, 0, 0]` then the mean would be `2`.
    This metric creates two variables, `total` and `count` that are used to
    compute the average of `values`. This average is ultimately returned as `mean`
    which is an idempotent operation that simply divides `total` by `count`.
    If `sample_weight` is `None`, weights default to 1.
    Use `sample_weight` of 0 to mask values.

    Usage:

    ```python
    mean = elegy.metrics.Mean()
    result = mean([1, 3, 5, 7])  # 16 / 4
    assert result == 4.0


    result = mean([4, 10])  # 30 / 6
    assert result == 5.0
    ```

    Usage with elegy API:

    ```python
    model = elegy.Model(
        module_fn,
        loss=jm.losses.MeanSquaredError(),
        metrics=elegy.metrics.Mean(),
    )
    ```
    """

    def __init__(
        self,
        dtype: tp.Optional[jnp.dtype] = None,
    ):
        """Creates a `Mean` instance.
        Arguments:
            dtype: (Optional) data type of the metric result. Defaults to `float32`.
        """
        super().__init__(
            reduction=Reduction.weighted_mean,
            dtype=dtype,
        )

    def update(
        self: M,
        values: jax.Array,
        sample_weight: tp.Optional[jax.Array] = None,
        **_,
    ) -> M:
        """
        Accumulates the mean statistic over various batches.

        Arguments:
            values: Per-example value.
            sample_weight: Optional weighting of each example.

        Returns:
            Mean instance with updated state.
        """

        return super().update(
            values=values,
            sample_weight=sample_weight,
        )
