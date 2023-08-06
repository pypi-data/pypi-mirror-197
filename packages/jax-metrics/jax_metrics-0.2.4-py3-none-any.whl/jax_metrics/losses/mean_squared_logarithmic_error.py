import typing as tp

import jax
import jax.numpy as jnp

from jax_metrics import types, utils
from jax_metrics.losses.loss import Loss, Reduction


def mean_squared_logarithmic_error(target: jax.Array, preds: jax.Array) -> jax.Array:
    """
    Computes the mean squared logarithmic error between target and predictions.

    ```python
    loss = mean(square(log(target + 1) - log(preds + 1)), axis=-1)
    ```

    Usage:

    ```python
    rng = jax.random.PRNGKey(42)

    target = jax.random.randint(rng, shape=(2, 3), minval=0, maxval=2)
    preds = jax.random.uniform(rng, shape=(2, 3))

    loss = jm.losses.mean_squared_logarithmic_error(target, preds)

    assert loss.shape == (2,)

    first_log = jnp.log(jnp.maximum(target, types.EPSILON) + 1.0)
    second_log = jnp.log(jnp.maximum(preds, types.EPSILON) + 1.0)
    assert jnp.array_equal(loss, jnp.mean(jnp.square(first_log - second_log), axis=-1))
    ```

    Arguments:
        target: Ground truth values. shape = `[batch_size, d0, .. dN]`.
        preds: The predicted values. shape = `[batch_size, d0, .. dN]`.

    Returns:
        Mean squared logarithmic error values. shape = `[batch_size, d0, .. dN-1]`.
    """

    target = target.astype(preds.dtype)
    first_log = jnp.log(jnp.maximum(target, types.EPSILON) + 1.0)
    second_log = jnp.log(jnp.maximum(preds, types.EPSILON) + 1.0)

    return jnp.mean(jnp.square(first_log - second_log), axis=-1)


class MeanSquaredLogarithmicError(Loss):
    """
    Computes the mean squared logarithmic errors between target and predictions.

    `loss = mean(square(log(target + 1) - log(preds + 1)), axis=-1)`

    Usage:

    ```python
    target = jnp.array([[0.0, 1.0], [0.0, 0.0]])
    preds = jnp.array([[1.0, 1.0], [1.0, 0.0]])

    # Using 'auto'/'sum_over_batch_size' reduction type.
    msle = jm.losses.MeanSquaredLogarithmicError()

    assert msle(target, preds) == 0.24022643

    # Calling with 'sample_weight'.
    assert msle(target, preds, sample_weight=jnp.array([0.7, 0.3])) = 0.12011322

    # Using 'sum' reduction type.
    msle = jm.losses.MeanSquaredLogarithmicError(reduction=jm.losses.Reduction.SUM)

    assert msle(target, preds) == 0.48045287

    # Using 'none' reduction type.
    msle = jm.losses.MeanSquaredLogarithmicError(reduction=jm.losses.Reduction.NONE)

    assert jnp.equal(msle(target, preds), jnp.array([0.24022643, 0.24022643])).all()
    ```
    Usage with the Elegy API:

    ```python
    model = elegy.Model(
        module_fn,
        loss=jm.losses.MeanSquaredLogarithmicError(),
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
        Invokes the `MeanSquaredLogarithmicError` instance.

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
        return mean_squared_logarithmic_error(target, preds)
