from __future__ import annotations

from fractions import Fraction
from typing import Any


def superscript(n: int) -> str:
    # https://stackoverflow.com/a/62987096/554319
    number_sup = "".join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[ord(c) - ord("0")] for c in str(abs(n))])
    if n < 0:
        return f"⁻{number_sup}"
    else:
        return number_sup


def rational_exponent_str(exponent: Any) -> str:
    try:
        # We first assume this is a npytypes.rational.rational object
        # Notice that str(R(1)) raises TypeError: __str__ returned non-string
        num = exponent.n
        den = exponent.d
    except AttributeError:
        # We try to convert it to a Fraction
        exponent_f = Fraction(exponent)
        num = exponent_f.numerator
        den = exponent_f.denominator

    if den == 1:
        return superscript(num)
    else:
        # There is no "superscript slash", so we will use a hack
        # See https://stackoverflow.com/a/49325148/554319
        return f"{superscript(num)}⸍{superscript(den)}"
