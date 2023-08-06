"""Beta distribution.

For more information read:

* `scipy.stats.beta <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html>`__
* `The beta distribution Wikipedia page <https://en.wikipedia.org/wiki/Beta_distribution>`__

"""

from __future__ import annotations

from ..._measure_convertible import NonConstantMeasureConvertible
from ..._measure_description import MeasureDescription, convert_to_measure_description
from ..._measures.calculated_measure import CalculatedMeasure, Operator
from ._utils import NumericMeasureConvertible


def pdf(
    point: NonConstantMeasureConvertible,
    /,
    *,
    alpha: NumericMeasureConvertible,
    beta: NumericMeasureConvertible,
) -> MeasureDescription:
    r"""Probability density function for a beta distribution.

    The pdf of the beta distribution with shape parameters :math:`\alpha` and :math:`\beta` is given by the formula

    .. math::

        \operatorname {pdf}(x) = \frac {x^{\alpha -1}(1-x)^{\beta -1}}{ \mathrm {B}(\alpha ,\beta )}

    With :math:`\mathrm {B}` the beta function:

    .. math::

        \mathrm {B} (\alpha ,\beta )=\int _{0}^{1}t^{\alpha -1}(1-t)^{\beta-1}dt = \frac {\Gamma (\alpha )\Gamma (\beta )}{\Gamma (\alpha +\beta )}


    Where :math:`\Gamma` is the `Gamma function <https://en.wikipedia.org/wiki/Gamma_function>`__.

    Args:
        point: The point where the function is evaluated.
        alpha: The alpha parameter of the distribution.
        beta: The beta parameter of the distribution.

    See Also:
        `The beta distribution Wikipedia page <https://en.wikipedia.org/wiki/Beta_distribution>`__

    """
    return CalculatedMeasure(
        Operator(
            "beta_density",
            [convert_to_measure_description(arg) for arg in [point, alpha, beta]],
        )
    )


def cdf(
    point: NonConstantMeasureConvertible,
    /,
    *,
    alpha: NumericMeasureConvertible,
    beta: NumericMeasureConvertible,
) -> MeasureDescription:
    r"""Cumulative distribution function for a beta distribution.

    The cdf of the beta distribution with shape parameters :math:`\alpha` and :math:`\beta` is

    .. math::

        \operatorname {cdf}(x) = I_x(\alpha,\beta)


    Where :math:`I` is the `regularized incomplete beta function <https://en.wikipedia.org/wiki/Beta_function#Incomplete_beta_function>`__.

    Args:
        point: The point where the function is evaluated.
        alpha: The alpha parameter of the distribution.
        beta: The beta parameter of the distribution.

    See Also:
        `The beta distribution Wikipedia page <https://en.wikipedia.org/wiki/Beta_distribution>`__

    """
    return CalculatedMeasure(
        Operator(
            "beta_cumulative_probability",
            [convert_to_measure_description(arg) for arg in [point, alpha, beta]],
        )
    )


def ppf(
    point: NonConstantMeasureConvertible,
    /,
    *,
    alpha: NumericMeasureConvertible,
    beta: NumericMeasureConvertible,
) -> MeasureDescription:
    """Percent point function for a beta distribution.

    Also called inverse cumulative distribution function.

    Args:
        point: The point where the density function is evaluated.
        alpha: The alpha parameter of the distribution.
        beta: The beta parameter of the distribution.

    See Also:
        `The beta distribution Wikipedia page <https://en.wikipedia.org/wiki/Beta_distribution>`__

    """
    return CalculatedMeasure(
        Operator(
            "beta_ppf",
            [convert_to_measure_description(arg) for arg in [point, alpha, beta]],
        )
    )
