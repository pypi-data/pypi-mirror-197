"""F-distribution, also known as Snedecor's F distribution or the Fisher–Snedecor distribution.

For more information read:

* `scipy.stats.f <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f.html>`__
* `The F-distribution Wikipedia page <https://en.wikipedia.org/wiki/F-distribution>`__

"""

from __future__ import annotations

from ..._measure_convertible import NonConstantMeasureConvertible
from ..._measure_description import MeasureDescription, convert_to_measure_description
from ..._measures.calculated_measure import CalculatedMeasure, Operator
from ._utils import NumericMeasureConvertible, ensure_strictly_positive


def _validate_args(
    numerator_degrees_of_freedom: NumericMeasureConvertible,
    denominator_degrees_of_freedom: NumericMeasureConvertible,
) -> None:
    ensure_strictly_positive(
        numerator_degrees_of_freedom, "numerator_degrees_of_freedom"
    )
    ensure_strictly_positive(
        denominator_degrees_of_freedom, "denominator_degrees_of_freedom"
    )


def pdf(
    point: NonConstantMeasureConvertible,
    /,
    *,
    numerator_degrees_of_freedom: NumericMeasureConvertible,
    denominator_degrees_of_freedom: NumericMeasureConvertible,
) -> MeasureDescription:
    r"""Probability density function for a F-distribution.

    The pdf for a F-distributions with parameters :math:`d1` et :math:`d2` is

    .. math::

        \operatorname {pdf}(x) = \frac
          {\sqrt {\frac {(d_{1}x)^{d_{1}}\,\,d_{2}^{d_{2}}}{(d_{1}x+d_{2})^{d_{1}+d_{2}}}}}
          {x\,\mathrm {B} \!\left(\frac {d_{1}}{2},\frac {d_{2}}{2}\right)}

    Where :math:`\mathrm {B}` is the beta function.

    Args:
        point: The point where the function is evaluated.
        numerator_degrees_of_freedom: Numerator degrees of freedom.
            Must be positive.
        denominator_degrees_of_freedom: Denominator degrees of freedom.
            Must be positive.

    See Also:
        `The F-distribution Wikipedia page <https://en.wikipedia.org/wiki/F-distribution>`__

    """
    _validate_args(numerator_degrees_of_freedom, denominator_degrees_of_freedom)
    return CalculatedMeasure(
        Operator(
            "F_density",
            [
                convert_to_measure_description(arg)
                for arg in [
                    point,
                    numerator_degrees_of_freedom,
                    denominator_degrees_of_freedom,
                ]
            ],
        )
    )


def cdf(
    point: NonConstantMeasureConvertible,
    /,
    *,
    numerator_degrees_of_freedom: NumericMeasureConvertible,
    denominator_degrees_of_freedom: NumericMeasureConvertible,
) -> MeasureDescription:
    r"""Cumulative distribution function for a F-distribution.

    The cdf for a F-distributions with parameters :math:`d1` et :math:`d2` is

    .. math::

        \operatorname {cdf}(x) = I_{\frac {d_{1}x}{d_{1}x+d_{2}}} \left(\tfrac {d_{1}}{2},\tfrac {d_{2}}{2}\right)

    where I is the `regularized incomplete beta function <https://en.wikipedia.org/wiki/Beta_function#Incomplete_beta_function>`__.

    Args:
        point: The point where the function is evaluated.
        numerator_degrees_of_freedom: Numerator degrees of freedom.
            Must be positive.
        denominator_degrees_of_freedom: Denominator degrees of freedom.
            Must be positive.

    See Also:
        `The F-distribution Wikipedia page <https://en.wikipedia.org/wiki/F-distribution>`__

    """
    _validate_args(numerator_degrees_of_freedom, denominator_degrees_of_freedom)
    return CalculatedMeasure(
        Operator(
            "F_cumulative_probability",
            [
                convert_to_measure_description(arg)
                for arg in [
                    point,
                    numerator_degrees_of_freedom,
                    denominator_degrees_of_freedom,
                ]
            ],
        )
    )


def ppf(
    point: NonConstantMeasureConvertible,
    /,
    *,
    numerator_degrees_of_freedom: NumericMeasureConvertible,
    denominator_degrees_of_freedom: NumericMeasureConvertible,
) -> MeasureDescription:
    """Percent point function for a F-distribution.

    Also called inverse cumulative distribution function.

    Args:
        point: The point where the function is evaluated.
        numerator_degrees_of_freedom: Numerator degrees of freedom.
            Must be positive.
        denominator_degrees_of_freedom: Denominator degrees of freedom.
            Must be positive.

    See Also:
        `The F-distribution Wikipedia page <https://en.wikipedia.org/wiki/F-distribution>`__

    """
    _validate_args(numerator_degrees_of_freedom, denominator_degrees_of_freedom)
    return CalculatedMeasure(
        Operator(
            "F_ppf",
            [
                convert_to_measure_description(arg)
                for arg in [
                    point,
                    numerator_degrees_of_freedom,
                    denominator_degrees_of_freedom,
                ]
            ],
        )
    )
