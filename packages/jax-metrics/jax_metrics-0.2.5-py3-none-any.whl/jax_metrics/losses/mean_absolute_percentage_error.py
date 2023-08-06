import typing as tp

import jax
import jax.numpy as jnp

from jax_metrics import types, utils
from jax_metrics.losses.loss import Loss, Reduction


def mean_absolute_percentage_error(target: jax.Array, preds: jax.Array) -> jax.Array:
    """
    Computes the mean absolute percentage error (MAPE) between target and predictions.

    After computing the absolute distance between the true value and the prediction value
    and divide by the true value, the mean value over the last dimension is returned.

    Usage:

    ```python
    rng = jax.random.PRNGKey(42)

    target = jax.random.randint(rng, shape=(2, 3), minval=0, maxval=2)
    preds = jax.random.uniform(rng, shape=(2, 3))

    loss = jm.losses.mean_absolute_percentage_error(target, preds)

    assert loss.shape == (2,)

    assert jnp.array_equal(loss, 100. * jnp.mean(jnp.abs((preds - target) / jnp.clip(target, types.EPSILON, None))))
    ```

    Arguments:
        target: Ground truth values. shape = `[batch_size, d0, .. dN]`.
        preds: The predicted values. shape = `[batch_size, d0, .. dN]`.

    Returns:
        Mean absolute percentage error values. shape = `[batch_size, d0, .. dN-1]`.
    """
    target = target.astype(preds.dtype)
    diff = jnp.abs((preds - target) / jnp.maximum(jnp.abs(target), types.EPSILON))
    return 100.0 * jnp.mean(diff, axis=-1)


class MeanAbsolutePercentageError(Loss):
    """
    Computes the mean absolute errors between target and predictions.

    `loss = mean(abs((target - preds) / target))`

    Usage:

    ```python
    target = jnp.array([[1.0, 1.0], [0.9, 0.0]])
    preds = jnp.array([[1.0, 1.0], [1.0, 0.0]])

    # Using 'auto'/'sum_over_batch_size' reduction type.
    mape = jm.losses.MeanAbsolutePercentageError()
    result = mape(target, preds)
    assert np.isclose(result, 2.78, rtol=0.01)

    # Calling with 'sample_weight'.
    assert np.isclose(mape(target, preds, sample_weight=jnp.array([0.1, 0.9])), 2.5, rtol=0.01)

    # Using 'sum' reduction type.
    mape = jm.losses.MeanAbsolutePercentageError(reduction=jm.losses.Reduction.SUM)

    assert np.isclose(mape(target, preds), 5.6, rtol=0.01)

    # Using 'none' reduction type.
    mape = jm.losses.MeanAbsolutePercentageError(reduction=jm.losses.Reduction.NONE)

    assert jnp.all(np.isclose(result, [0. , 5.6], rtol=0.01))

    ```
    Usage with the Elegy API:

    ```python
    model = elegy.Model(
        module_fn,
        loss=jm.losses.MeanAbsolutePercentageError(),
        metrics=elegy.metrics.Mean(),
    )
    ```
    """

    def call(
        self,
        target: jax.Array,
        preds: jax.Array,
        sample_weight: tp.Optional[
            jax.Array
        ] = None,  # not used, __call__ handles it, left for documentation purposes.
        **_,
    ) -> jax.Array:
        """
        Invokes the `MeanAbsolutePercentageError` instance.

        Arguments:
            target: Ground truth values. shape = `[batch_size, d0, .. dN]`, except
                sparse loss functions such as sparse categorical crossentropy where
                shape = `[batch_size, d0, .. dN-1]`
            preds: The predicted values. shape = `[batch_size, d0, .. dN]`
            sample_weight: Optional `sample_weight` acts as a
                coefficient for the loss. If a scalar is provided, then the loss is
                simply scaled by the given value. If `sample_weight` is a tensor of size
                `[batch_size]`, then the total loss for each sample of the batch is
                rescaled by the corresponding element in the `sample_weight` vector. If
                the shape of `sample_weight` is `[batch_size, d0, .. dN-1]` (or can be
                broadcasted to this shape), then each loss element of `preds` is scaled
                by the corresponding value of `sample_weight`. (Note on`dN-1`: all loss
                functions reduce by 1 dimension, usually axis=-1.)

        Returns:
            Weighted loss float `Tensor`. If `reduction` is `NONE`, this has
                shape `[batch_size, d0, .. dN-1]`; otherwise, it is scalar. (Note `dN-1`
                because all loss functions reduce by 1 dimension, usually axis=-1.)

        Raises:
            ValueError: If the shape of `sample_weight` is invalid.
        """
        return mean_absolute_percentage_error(target, preds)
