import pytest
from typing import Union, Optional, Type
from range import Range, a_lt_b, a_gt_b, lower_end_in, upper_end_in, is_empty, union

inf_bracket_error = "Infinite end can only go with a non-inclusive bracket"

test_cases: list[tuple] = []
for i in ["[]", "()", "[)", "(]"]:
    test_cases.append((1, 5, i, None, None))
    test_cases.append((1, 5., i, None, None))
    test_cases.append((5., 1., i, "Start has to be greater then end", ValueError))
    if i[0] == '(':
        test_cases.append((None, 5, i, None, None))
    if i[0] == '[':
        test_cases.append((None, 5, i, inf_bracket_error, ValueError))
        test_cases.append((None, None, i, inf_bracket_error, ValueError))
    if i[-1] == ')':
        test_cases.append((5, None, i, None, None))
    if i[-1] == ']':
        test_cases.append((5, None, i, inf_bracket_error, ValueError))

for i in ('', 3), (-2, "3.0"), (4, False):
    test_cases.append((i[0], i[1], "[)", "Start and the end of the range have to be of the same type", TypeError))
for i in ["sdfgjhs", 45, None]:
    test_cases.append((3, 7, i, "Available brackets are", ValueError))


@pytest.mark.parametrize(('start', 'end', 'brackets', 'message', 'error_type'), test_cases)
def test_create(start: Union[int, float, str, None],
                end: Union[int, float, str, None],
                brackets: Optional[str],
                message: Optional[str],
                error_type: Optional[None],
                capfd) -> None:
    if error_type:
        with pytest.raises(error_type) as excinfo:
            r = Range(start, end, brackets)
        assert excinfo.type is error_type
        assert message in str(excinfo.value)
    else:
        r = Range(start, end, brackets)

        assert type(r) == Range
        if isinstance(start, int):
            assert r.start == float(start)
        else:
            assert r.start == start
        if isinstance(end, int):
            assert r.end == float(end)
        else:
            assert r.end == end
        assert r.brackets == brackets

        print(r)
        out, err = capfd.readouterr()
        if start is None:
            start = "-inf"
        elif isinstance(start, int):
            start = float(start)
        if end is None:
            end = "+inf"
        elif isinstance(end, int):
            end = float(end)
        assert out == f'{brackets[0]}{start}, {end}{brackets[-1]}\n'


test_cases = [((None, None, "()"), (None, None, "()"), True),
              ((None, None, None), (None, None, "()"), False),
              ((None, None, None), (2, 5, "[]"), False),
              ]
variations = [[None, None], [4., None], [1., 5.5], [1, 5.5], [1, 4],
              [5., 5.5], [4., 4.], [None, 5.]] + [[i, i] for i in (5, 5., -4., -843765834756.234)]

for i in ["[]", "()", "[)", "(]"]:
    for j in ["[]", "()", "[)", "(]"]:
        for vi in variations:
            for vj in variations:
                if vi[0] is None and i[0] != '(' or vi[-1] is None and i[-1] != ')':
                    m = inf_bracket_error
                else:
                    m = True if vi == vj and i == j else False
                    # Empty ranges equality
                    if (vi[0] == vi[-1] and i != '[]') and (vj[0] == vj[-1] and j != '[]')\
                            and [None, None] not in (vi, vj):
                        m = True
                    try:
                        v1_r = Range(vi[0], vi[-1], i)
                        v2_r = Range(vj[0], vj[-1], j)
                    except (ValueError, TypeError) as e:
                        m = e
                test_cases.append(((vi[0], vi[-1], i), (vj[0], vj[-1], j), m))


@pytest.mark.parametrize(('first', 'second', 'message'), test_cases)
def test_eq(first: tuple,
            second: tuple,
            message: Union[bool, str, Type[TypeError], Type[ValueError]]
            ) -> None:
    if isinstance(message, bool):
        r1 = Range(first[0], first[1], first[2])
        r2 = second
        if isinstance(r2, tuple):
            r2 = Range(second[0], second[1], second[2])
        comparison = r1 == r2
        assert comparison is message
    else:
        with pytest.raises((TypeError, ValueError)) as excinfo:
            r1 = Range(first[0], first[1], first[2])
            r2 = second
            if isinstance(r2, tuple):
                r2 = Range(second[0], second[1], second[2])
            comparison = r1 == r2
        assert str(message) in str(excinfo.value.args[0])


test_cases = [
    ((None, None, '()'), (None, None, '()'), False),
    ((None, None, '()'), (4, None, '()'), True),
    ((None, None, '()'), (4, 5, '()'), True),
    ((None, None, '()'), (None, 5, '()'), False),
]
for i in ["[]", "()", "[)", "(]"]:
    for j in ["[]", "()", "[)", "(]"]:
        test_cases.append(((1, 4, i), (5, 6, j), True))
        test_cases.append(((1, 6, i), (5, 6, j), True))
        test_cases.append(((7., 9.5, i), (5, 6, j), False))
        test_cases.append(((7., 9.5, i), (5, 123, j), False))

        if i[0] == '[' and j[0] == '(':
            test_cases.append(((1., 5.5, i), (1., 6., j), True))
            test_cases.append(((1., 5.5, i), (1., 4., j), True))
            test_cases.append(((1., 5.5, i), (1., 5.5, j), True))
        elif i[0] == j[0]:
            m1 = False if i[-1] == j[-1] or (i[-1] == ']' and j[-1] == ')') else True
            test_cases.append(((1., 5.5, i), (1., 5.5, j), m1))
            test_cases.append(((1., 4.5, i), (1., 5.5, j), True))
            test_cases.append(((1., 4.5, i), (1., 3.5, j), False))
            if j[-1] == ')':
                test_cases.append(((1., 2., i), (1., None, j), True))
            m2 = True if i[-1] == ')' and j[-1] == ']' else False
            test_cases.append(((1., 4.5, i), (1., 4.5, j), m2))
        else:
            test_cases.append(((1., 4.5, i), (1., 4.5, j), False))
            test_cases.append(((1., 5.5, i), (1., 4.5, j), False))
            test_cases.append(((1., 5.5, i), (1., 6.5, j), False))

        if i[0] == '(':
            test_cases.append(((None, 4.5, i), (1., 4.5, j), True))
            test_cases.append(((None, 4.5, i), (1., 2.5, j), True))
            test_cases.append(((None, 4.5, i), (1., 5.5, j), True))
            if j == '()':
                test_cases.append(((None, 4.5, i), (None, None, j), True))
            if j[-1] == ')':
                test_cases.append(((None, 4.5, i), (1., None, j), True))
            if j[0] == '(':
                test_cases.append(((None, 4.5, i), (None, 5.4, j), True))
                test_cases.append(((None, 4.5, i), (None, 6.5, j), True))
                m3 = True if i[-1] == ')' and j[-1] == ']' else False
                test_cases.append(((None, 4.5, i), (None, 4.5, j), m3))
        if i[-1] == ')':
            test_cases.append(((4., None, i), (5., 6., j), True))
            if j[0] == "(":
                test_cases.append(((4., None, i), (None, 6., j), False))
        if i == j:
            for s, e in (1, 4), (4., 6.), (-1.76, 99999999999999.999999999999):
                test_cases.append(((s, e, i), (s, e, j), False))


@pytest.mark.parametrize(('first', 'second', 'message'), test_cases)
def test_comparison_lt(first: tuple,
            second: tuple,
            message: bool,
            ) -> None:
    r1 = Range(first[0], first[1], first[2])
    r2 = Range(second[0], second[1], second[2])
    comparison = r1 < r2
    assert comparison is message


test_cases = [
    ((5, 6, "[)"), 5, True),
    ((5, 6, "[)"), 6, False),
    ((None, None, "()"), None, True),
    ((None, 5, "()"), None, False),
    ((None, 5, "()"), "None", "'<' not supported between instances of 'str' and 'int'"),

]
variations = [[None, None], [4., None], [4., 5.], [5., 5.5], [6., 7.], [4., 4.], [None, 5.], {}, "", None, 5.]
for i in ["[]", "()", "[)", "(]"]:
    for j in ["[]", "()", "[)", "(]"]:
        for vi in variations[:-4]:
            m = ""
            first_0 = tuple(vi + [i])
            if vi[0] is None and i[0] != '(' or vi[-1] is None and i[-1] != ')':
                m = inf_bracket_error
                test_cases.append((first_0, None, m))
            else:

                vi_r = Range(vi[0], vi[1], i)
                for vj in variations:
                    if vj == {}:
                        m = "not supported between instances of"
                        second = vj
                        test_cases.append((first_0, second, m))
                    elif vj == "":
                        m = "not supported between instances of"
                        second = vj
                        if vi == [4., 4.] and i in ("(]", "[)", "()"):
                            m = False
                        elif vi == [None, None]:
                            m = True
                        test_cases.append((first_0, second, m))
                    elif vj is None:
                        m = True if vi + [i] == [None, None, "()"] else False
                        second = vj
                        test_cases.append((first_0, second, m))
                    elif vj == 5.:
                        second = vj
                        m = True if (
                            vi[-1] is None or
                            (vi[-1] == vj and i[-1] == "]") or
                            (vi[0] == vj and i[0] == "[")
                        ) else False
                        test_cases.append((first_0, second, m))
                    elif not (vj[0] is None and j[0] != '(' or
                              vj[-1] is None and j[-1] != ')'):
                        second = tuple(vj + [j])
                        vj_r = Range(vj[0], vj[1], j)
                        m = False
                        if (lower_end_in(vi_r, vj_r) or a_lt_b(vi_r.start, vj_r.start, "start")) and\
                                (upper_end_in(vi_r, vj_r) or a_gt_b(vi_r.end, vj_r.end, "end")):
                            m = True
                        elif is_empty(vj_r):
                            m = True
                        test_cases.append((first_0, second, m))


@pytest.mark.parametrize(('first', 'second', 'message'), test_cases)
def test_contains(first: tuple,
                  second: Union[tuple, dict, str, None, float],
                  message: Union[bool, str],
                  ) -> None:
    if (first[0], first[2][0]) == (None, "[") or (first[1], first[2][1]) == (None, "]"):
        with pytest.raises(ValueError) as excinfo0:
            r1 = Range(first[0], first[1], first[2])
        assert message in str(excinfo0.value)
    else:
        r1 = Range(first[0], first[1], first[2])
        r2 = second
        if isinstance(second, tuple):
            r2 = Range(second[0], second[1], second[2])

        if isinstance(message, bool):
            comparison = r2 in r1
            assert comparison is message
        else:
            with pytest.raises(TypeError) as excinfo:
                comparison = r2 in r1
            assert message in str(excinfo.value)


test_cases = []
variations = [[None, None], [4., None], [4., 5.], [5., 5.5], [6., 7.], [4., 4.], [3., 8.], [-3, -2], [-3, 8],
              [None, 5.], {}, None, 5.
              ]
for i in ["[]", "()", "[)", "(]"]:
    for j in ["[]", "()", "[)", "(]"]:
        for vi in variations[:-3]:
            res = None
            first_0 = tuple(vi + [i])
            if vi[0] is None and i[0] != '(' or vi[-1] is None and i[-1] != ')':
                res = inf_bracket_error
                test_cases.append((first_0, None, res))
            else:
                vi_r = Range(vi[0], vi[1], i)
                for vj in variations:
                    if vj in ({}, None, 5.):
                        second_0, res = vj, False
                        test_cases.append((first_0, second_0, res))
                    elif vj[0] is None and j[0] != '(' or vj[-1] is None and j[-1] != ')':
                        second_0, res = tuple(vj + [j]), inf_bracket_error
                        test_cases.append((first_0, second_0, res))
                    else:
                        vj_r = Range(vj[0], vj[1], j)
                        res = Range(empty=True)
                        first, second = sorted([vi_r, vj_r])
                        if second in first:
                            res = second
                        elif first in second:
                            res = first
                        elif second.start < first.end:
                            res = Range(second.start, first.end, brackets=second.brackets[0] + first.brackets[-1])
                        elif second.start == first.end and (second.brackets[0], first.brackets[-1]) == ('[', ']'):
                            res = Range(second.start, second.start, "[]")
                        if is_empty(res):
                            res = Range(empty=True)
                        first_0, second_0 = tuple(vars(first).values()), tuple(vars(second).values())
                        test_cases.append((first_0, second_0, res))


@pytest.mark.parametrize(('first', 'second', 'message'), test_cases)
def test_intersect(first: tuple,
                   second: Union[tuple, None],
                   message: Union[Range, str, bool]) -> None:

    if type(message) == str:

        r2 = second
        if (first[0], first[2]) in [(None, "[)"), (None, '[]')] or (first[1], first[2]) in [(None, "(]"), (None, '[]')]:
            with pytest.raises(ValueError) as excinfo_00:
                r1 = Range(first[0], first[1], first[2])
            assert message in str(excinfo_00.value)
        if isinstance(second, tuple):
            r1 = Range(first[0], first[1], first[2])
            if second[0: 2] == (None, None) and second[2] != "()":
                with pytest.raises(ValueError) as excinfo_01:
                    Range(second[0], second[1], second[2])
                assert message in str(excinfo_01.value)
            else:
                with pytest.raises(ValueError) as excinfo:
                    r2 = Range(second[0], second[1], second[2])
                    intersection = r1.intersect(r2)
                assert message in str(excinfo.value)
    else:
        r1 = Range(first[0], first[1], first[2])
        r2 = second
        if isinstance(second, tuple):
            r2 = Range(second[0], second[1], second[2])
        intersection = r1.intersect(r2)

        assert intersection == message


test_cases = []
variations = [[None, None], [4., None], [4., 5.], [5., 5.5], [6., 7.], [4., 4.], [3., 8.], [-3, -2], [-3, 8],
              [None, 5.], {}, None, 5.]
for i in ["[]", "()", "[)", "(]"]:
    for j in ["[]", "()", "[)", "(]"]:
        for vi in variations[:-3]:
            first_0 = tuple(vi + [i])
            res = None
            if vi[0] is None and i[0] != '(' or vi[-1] is None and i[-1] != ')':
                res = inf_bracket_error
                test_cases.append((first_0, None, res))
            else:
                vi_r = Range(vi[0], vi[1], i)
                for vj in variations:
                    if vj in ({}, None, 5.):
                        second_0, res = vj, "unsupported operand type(s) for"
                        test_cases.append((first_0, second_0, res))
                    elif vj[0] is None and j[0] != '(' or vj[-1] is None and j[-1] != ')':
                        second_0, res = tuple(vj + [j]), inf_bracket_error
                        test_cases.append((first_0, second_0, res))
                    else:
                        vj_r = Range(vj[0], vj[1], j)
                        res = Range(empty=True)
                        first, second = sorted([vi_r, vj_r])
                        if second in first:
                            res = first
                        elif first in second:
                            res = second
                        elif second.start < first.end:
                            res = Range(first.start, second.end, brackets=first.brackets[0] + second.brackets[-1])
                        elif second.start == first.end and \
                                ((second.brackets[0], first.brackets[-1]) in [('(', ']'), ("[", ")"), ("[", "]")]):
                            res = Range(first.start, second.end, first.brackets[0] + second.brackets[-1])
                        elif first.end < second.start:
                            res = first, second
                        else:
                            res = first + second
                        if isinstance(res, Range) and is_empty(res):
                            res = Range(empty=True)
                        first_0, second_0 = tuple(vars(first).values()), tuple(vars(second).values())
                        test_cases.append((first_0, second_0, res))


@pytest.mark.parametrize(('first', 'second', 'message'), test_cases)
def test_add(first: tuple,
             second: Union[tuple, None],
             message: Union[str, Range, bool]):
    # if second is None:
    #     with pytest.raises(TypeError) as excinfo_0:
    #         Range(first[0], first[1], first[2]) + second
    #     assert message in str(excinfo_0.value)

    r2 = second
    if type(message) == str:

        if isinstance(second, tuple) or (first[0], first[2]) in [(None, "[)"), (None, '[]')] or (first[1], first[2]) in [(None, "(]"), (None, '[]')]:
            with pytest.raises(ValueError) as excinfo:
                r1 = Range(first[0], first[1], first[2])
                r2 = Range(second[0], second[1], second[2])
                total = r1 + r2
            assert message in str(excinfo.value)
        elif isinstance(r2, (float, int)) or r2 is None:
            r1 = Range(first[0], first[1], first[2])
            with pytest.raises(TypeError) as excinfo:
                total = r1 + r2
            assert message in str(excinfo.value)
    else:
        r1 = Range(first[0], first[1], first[2])
        if isinstance(second, tuple):
            r2 = Range(second[0], second[1], second[2])
        total = r1 + r2
        if isinstance(total, tuple):
            i = 0
            for t in total:
                if isinstance(message, tuple):
                    assert vars(t) == vars(message[i])
                else:
                    assert vars(t) == vars(message)
                i += 1
        assert total == message
        assert (Range(3, 4), Range(3.5, 3.8), Range(3.9, 6), Range(7, 8), Range(7.5, 9, "(]")) + Range(2, 3.5)\
               == (Range(2, 6), Range(7, 9, "[]"))


def test_union():
    a = Range(3, 4)
    b = Range(5, 6)
    bb = Range(5, 6, "()")
    d = Range(5, 9, "()")
    e = Range(5.5, 10)
    g = Range(5.5, 6)
    f = Range(None, None, "()")
    h = Range(0, None, "()")
    assert union(a, b, f) == f
    assert union(a, e, b) == (a, Range(b.start, e.end))
    assert union(a, e, b, b, b, a) == (a, Range(b.start, e.end))
    assert union(a, b, g) == (a, b)
    assert union(b, d) == Range(b.start, d.end)
    assert union(b, bb) == b
    assert union(g, h) == h
    with pytest.raises(TypeError) as excinfo:
        _ = union(a, e, b, b, b, "")
    assert "'<' not supported between instances of" in str(excinfo.value.args[0])


test_cases = [
    [(Range(2, 3) + Range(3, 4)) + Range(5, 6), Range(2, 4) + Range(5, 6), True],
    [Range(1, 2) + (Range(2, 3) + Range(3, 4)), Range(1, 4), True],
]


@pytest.mark.parametrize(('first', 'second', 'message'), test_cases)
def test_radd(first, second, message):
    if isinstance(message, bool):
        assert (first == second) is True


test_cases = [
    [Range(5, 7) - Range(5.5, 6), (Range(5, 5.5), Range(6, 7)), True],
    [Range(5, 7, "[]") - Range(6, 8, "(]"), (Range(5, 6, "[]"), Range(7, 8, "(]")), True],
    [Range(5.5, 6) - Range(5, 7), (Range(5, 5.5), Range(6, 7)), True],
    [Range(6, 8, "(]") - Range(5, 7, "[]"), (Range(5, 6, "[]"), Range(7, 8, "(]")), True],
    [Range(empty=True) - Range(5, 6, "[]"), Range(5, 6, "[]"), True],
    [Range(5, 6, "[]") - Range(empty=True), Range(5, 6, "[]"), True],
    [Range(empty=True) - Range(empty=True), Range(empty=True), True],
    [Range(5, 6, "[]") - Range(7, 8), (Range(5, 6, "[]"), Range(7, 8)), True],
    [Range(7, 8) - Range(5, 6, "[]"), (Range(5, 6, "[]"), Range(7, 8)), True],
]


@pytest.mark.parametrize(('first', 'second', 'message'), test_cases)
def test_sub(first, second, message):
    if isinstance(message, bool):
        assert (first == second) is True
