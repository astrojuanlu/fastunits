from npytypes.rational import rational as R


def superscript(n: int) -> str:
    # https://stackoverflow.com/a/62987096/554319
    return "".join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[ord(c) - ord("0")] for c in str(n)])


def rational_exponent_str(r: R) -> str:
    # str(R(1)) raises TypeError: __str__ returned non-string (type bytes)
    if r.d == 1:
        return superscript(r.n)
    else:
        # There is no "superscript slash", so we will use a hack
        # See https://stackoverflow.com/a/49325148/554319
        return f"{superscript(r.n)}⸍{superscript(r.d)}"
