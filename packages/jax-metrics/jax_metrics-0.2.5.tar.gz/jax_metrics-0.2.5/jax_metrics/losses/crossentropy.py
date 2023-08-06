import typing as tp

import jax
import jax.numpy as jnp
import optax

from jax_metrics import types
from jax_metrics.losses.loss import Loss, Reduction


def crossentropy(
    target: jax.Array,
    preds: jax.Array,
    *,
    binary: bool = False,
    from_logits: bool = True,
    label_smoothing: tp.Optional[float] = None,
    check_bounds: bool = True,
) -> jax.Array:
    n_classes = preds.shape[-1]
    integer_labels = False

    if target.ndim == preds.ndim - 1:
        if target.shape != preds.shape[:-1]:
            raise ValueError(
                f"Target shape '{target.shape}' does not match preds shape '{preds.shape}'"
            )
        if label_smoothing is not None or not from_logits:
            target = jax.nn.one_hot(target, n_classes)
        else:
            integer_labels = True
    elif target.ndim != preds.ndim:
        raise ValueError(
            f"Target shape '{target.shape}' does not match preds shape '{preds.shape}'"
        )

    if label_smoothing is not None:
        target = optax.smooth_labels(target, label_smoothing)

    loss: jax.Array
    if from_logits:
        if binary:
            loss = optax.sigmoid_binary_cross_entropy(preds, target).mean(axis=-1)
        elif integer_labels:
            loss = optax.softmax_cross_entropy_with_integer_labels(preds, target)
        else:
            loss = optax.softmax_cross_entropy(preds, target)
    else:
        preds = jnp.clip(preds, types.EPSILON, 1.0 - types.EPSILON)

        if binary:
            loss = -jnp.mean(
                target * jnp.log(preds) + (1 - target) * jnp.log(1 - preds), axis=-1
            )
        else:
            loss = -(target * jnp.log(preds)).sum(axis=-1)

    return loss


class Crossentropy(Loss):
    """
    Computes the crossentropy loss between the target and predictions.

    Use this crossentropy loss function when there are two or more label classes.
    We expect target to be provided as integers. If you want to provide target
    using `one-hot` representation, please use `CategoricalCrossentropy` loss.
    There should be `# classes` floating point values per feature for `preds`
    and a single floating point value per feature for `target`.
    In the snippet below, there is a single floating point value per example for
    `target` and `# classes` floating pointing values per example for `preds`.
    The shape of `target` is `[batch_size]` and the shape of `preds` is
    `[batch_size, num_classes]`.

    Usage:
    ```python
    target = jnp.array([1, 2])
    preds = jnp.array([[0.05, 0.95, 0], [0.1, 0.8, 0.1]])

    # Using 'auto'/'sum_over_batch_size' reduction type.
    scce = jm.losses.Crossentropy()
    result = scce(target, preds)  # 1.177
    assert np.isclose(result, 1.177, rtol=0.01)

    # Calling with 'sample_weight'.
    result = scce(target, preds, sample_weight=jnp.array([0.3, 0.7]))  # 0.814
    assert np.isclose(result, 0.814, rtol=0.01)

    # Using 'sum' reduction type.
    scce = jm.losses.Crossentropy(
        reduction=jm.losses.Reduction.SUM
    )
    result = scce(target, preds)  # 2.354
    assert np.isclose(result, 2.354, rtol=0.01)

    # Using 'none' reduction type.
    scce = jm.losses.Crossentropy(
        reduction=jm.losses.Reduction.NONE
    )
    result = scce(target, preds)  # [0.0513, 2.303]
    assert jnp.all(np.isclose(result, [0.0513, 2.303], rtol=0.01))
    ```

    Usage with the `Elegy` API:

    ```python
    model = elegy.Model(
        module_fn,
        loss=jm.losses.Crossentropy(),
        metrics=elegy.metrics.Accuracy(),
        optimizer=optax.adam(1e-3),
    )

    ```
    """

    def __init__(
        self,
        *,
        from_logits: bool = True,
        binary: bool = False,
        label_smoothing: tp.Optional[float] = None,
        reduction: tp.Optional[Reduction] = None,
        weight: tp.Optional[float] = None,
    ):
        """
        Initializes `SparseCategoricalCrossentropy` instance.

        Arguments:
            from_logits: Whether `preds` is expected to be a logits tensor. By
                default, we assume that `preds` encodes a probability distribution.
                **Note - Using from_logits=True is more numerically stable.**
            reduction: (Optional) Type of `jm.losses.Reduction` to apply to
                loss. Default value is `SUM_OVER_BATCH_SIZE`. For almost all cases
                this defaults to `SUM_OVER_BATCH_SIZE`.
            weight: Optional weight contribution for the total loss. Defaults to `1`.
        """
        super().__init__(reduction=reduction, weight=weight)

        self._from_logits = from_logits
        self._binary = binary
        self._label_smoothing = label_smoothing

    def call(
        self,
        target,
        preds,
        sample_weight: tp.Optional[jax.Array] = None,
        **_,
    ) -> jax.Array:
        """
        Invokes the `SparseCategoricalCrossentropy` instance.

        Arguments:
            target: Ground truth values.
            preds: The predicted values.
            sample_weight: Acts as a
                coefficient for the loss. If a scalar is provided, then the loss is
                simply scaled by the given value. If `sample_weight` is a tensor of size
                `[batch_size]`, then the total loss for each sample of the batch is
                rescaled by the corresponding element in the `sample_weight` vector. If
                the shape of `sample_weight` is `[batch_size, d0, .. dN-1]` (or can be
                broadcasted to this shape), then each loss element of `preds` is scaled
                by the corresponding value of `sample_weight`. (Note on`dN-1`: all loss
                functions reduce by 1 dimension, usually axis=-1.)

        Returns:
            Loss values per sample.
        """

        return crossentropy(
            target,
            preds,
            binary=self._binary,
            from_logits=self._from_logits,
            label_smoothing=self._label_smoothing,
        )
