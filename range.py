from functools import total_ordering


def a_lt_b(a, b, pos):
    try:
        return (a is not None and b is not None and a < b) or\
            (a is None and b is not None and pos == "start") or \
            (a is not None and b is None and pos == "end")
    except TypeError as e:
        raise TypeError(e)


def a_gt_b(a, b, pos):
    return a_lt_b(b, a, pos)


def upper_end_in(self, other):
    return other.end == self.end and (self.brackets[-1] == ']' or other.brackets[-1] == ')')


def upper_end_eq_non_incl(self, other):
    return self.end == other.end and (self.brackets[-1], other.brackets[-1]) == (')', ']')


def lower_end_in(self, other):
    return self.start == other.start and (self.brackets[0] == '[' or other.brackets[0] == '(')


def is_empty(a):
    return type(a) == Range and (a.start == a.end and a.start is not None and a.brackets != "[]") \
        or (a.brackets is None)


def good_num_types(r, s):
    return type(s) in (int, float) and (type(r.start) in (int, float) or type(r.end) in (int, float))


def good_types(r, s):
    return type(s) in {type(r.start), type(r.end)} or good_num_types(r, s)


def normalise_tuple_of_range(t):
    t = sorted(t)
    i = 1
    res = [t[0]]
    while i <= len(t) - 1:
        if res[-1].intersect(t[i]) != Range(empty=True):
            res[-1] += t[i]

        else:
            res.append(t[i])
        i += 1
    return tuple(res)


def union(*args):
    if len(args) == 1:
        return args
    args = sorted(args)
    res = args[0]
    for j in range(len(args[1:])):
        arg = args[1:][j]
        if isinstance(res, Range):
            res += arg  # can become tuple here
            if isinstance(res, (tuple, list)):
                res = sorted(list(res))
        elif isinstance(res, (tuple, list)):
            res = list(res)
            res[-1] += arg
            if isinstance(res[-1], tuple):
                res = res[:-1] + list(res[-1])
                res = sorted(res)
                # print("3 res res", res)
        else:
            return False
    return res if isinstance(res, Range) else tuple(res)


def reverse_bracket(a):
    lib = {"(": ")", ")": "(", "[": "]", "]": "["}
    return lib[a]


def reverse_n_swap_bracket(a):
    lib = {"(": "[", ")": "]", "[": "(", "]": ")"}
    return lib[reverse_bracket(a)]


@total_ordering
class Range:
    def __init__(self, start=None, end=None, brackets="[)", empty=False):
        if not empty and not (start == end == brackets and start is None):
            available_brackets = ["[]", "()", "[)", "(]"]
            if brackets not in available_brackets:
                raise ValueError(f'Available brackets are {str(available_brackets)}, got {brackets} instead')

            if None not in (start, end):
                if type(start) != type(end):
                    if type(start) in (int, float) and type(end) in (int, float):
                        start, end = float(start), float(end)
                    else:
                        raise TypeError(f"Start and the end of the range have to be of the same type, currently\n"
                                        f"type_start={type(start)}, type_end={type(end)}")
                if start > end:
                    raise ValueError(f"Start has to be greater then end, currently start={start}, end={end}")
            if (start is None and brackets[0] != '(') or (end is None and brackets[-1] != ')'):
                raise ValueError(f'Infinite end can only go with a non-inclusive bracket:'
                                 f'{brackets}, {start}, {end}')
            self.start = start
            self.end = end
            self.brackets = brackets
        else:
            self.start = self.end = self.brackets = None

    def __eq__(self, other):
        if not isinstance(other, Range):
            return NotImplemented
        if is_empty(other):
            if is_empty(self):
                return True
            else:
                return False
        if vars(self) == vars(other):
            return True
        return False

    def __lt__(self, other):
        # self < other
        if not isinstance(other, Range):
            return NotImplemented
        if is_empty(other):
            if is_empty(self):
                return False
            else:
                return True
        if a_lt_b(self.start, other.start, "start"):
            return True
        if self.start == other.start:
            if (self.brackets[0], other.brackets[0]) == ('[', '('):
                return True
            if self.brackets[0] == other.brackets[0]:
                if a_lt_b(self.end, other.end, "end") or upper_end_eq_non_incl(self, other):
                    return True
        if self.start is None and self.end is not None:
            if a_lt_b(self.end, other.end, "end") or upper_end_eq_non_incl(self, other):
                return True
        if good_types(self, other) and a_lt_b(self.start, other, "start"):
            return True
        return False

    def __contains__(self, other):
        # other in self
        if not isinstance(other, Range):
            other = Range(other, other, "()") if other is None else Range(other, other, "[]")
        if is_empty(other):
            return True
        if is_empty(self) and not is_empty(other):
            return False

        if (lower_end_in(self, other) or a_lt_b(self.start, other.start, "start")) \
                and (upper_end_in(self, other) or a_lt_b(other.end, self.end, "end")):
            return True

        if good_types(self, other) and \
                (
                     (a_lt_b(self.start, other, "start") or lower_end_in(self, Range(other, None, "[)"))) and
                     (a_lt_b(other, self.end, "end") or upper_end_in(self, Range(None, other, "(]")))
                ):
            return True
        return False

    def intersect(self, other):
        if not isinstance(other, Range):
            return False
        if is_empty(self) or is_empty(other):
            return Range(empty=True)
        a, b = self, other
        # guarantee that a <= b
        if b in a:
            return b
        elif a in b:
            return a
        if self > other:
            a, b = other, self
        if a_lt_b(b.start, a.end, pos="start") or b.start == a.end:
            res = Range(b.start, a.end, brackets=b.brackets[0] + a.brackets[-1])
            if is_empty(res):
                return Range(empty=True)
            else:
                return res
        return Range(empty=True)

    def is_single_element(self):
        return self.start == self.end and self.brackets == "[]"

    def __sub__(self, other):
        if not isinstance(other, Range):
            return NotImplemented
        if is_empty(other) or is_empty(self) or self.intersect(other) == Range(empty=True):
            return self + other
        sm, lg = sorted([self, other])
        intersection = self.intersect(other)
        if intersection and intersection != Range(empty=True):
            if lg in sm:
                if lg.is_single_element():
                    return sm
                return Range(sm.start, lg.start, sm.brackets[0] + reverse_n_swap_bracket(lg.brackets[0])),\
                    Range(lg.end, sm.end, reverse_n_swap_bracket(lg.brackets[-1]) + sm.brackets[-1])
            return Range(sm.start, lg.start, sm.brackets[0] + reverse_n_swap_bracket(lg.brackets[0])),\
                Range(sm.end, lg.end, reverse_n_swap_bracket(sm.brackets[-1]) + lg.brackets[-1])
        return Range(empty=True)

    def __rsub__(self, other):
        if isinstance(other, tuple):
            res = self
            for i in other:
                res -= i
            return res
        return self - other

    def __add__(self, other):
        if not isinstance(other, Range):
            # check that every element of the tuple is a Range
            if isinstance(other, tuple) and sum([isinstance(i, Range) for i in other]) == len(other):
                return normalise_tuple_of_range(tuple([self] + list(other)))
            return NotImplemented
        a, b = self, other
        # guarantee that a <= b
        if b in a:
            return a
        elif a in b:
            return b
        if self > other:
            a, b = other, self
        intersection = a.intersect(b)
        if intersection:
            if intersection == Range(empty=True):
                if Range(empty=True) in (a, b):
                    return b if self == Range(empty=True) else self
                elif a.end == b.start and a.brackets[-1] + b.brackets[0] in ("](", ")["):
                    return Range(a.start, b.end, brackets=a.brackets[0] + b.brackets[-1])
                else:
                    return a, b
            else:
                return Range(a.start, b.end, brackets=a.brackets[0] + b.brackets[-1])
        else:
            return a, b

    def __radd__(self, other):
        return self + other

    def format_single_range(self):
        if isinstance(self.start, int):
            self.start = float(self.start)
        if isinstance(self.end, int):
            self.end = float(self.end)
        start, end = f"{self.brackets[0]}{self.start}", f"{self.end}{self.brackets[-1]}"
        if self.brackets[0] == "(" and self.start is None:
            start = "(-inf"
        if self.brackets[-1] == ")" and self.end is None:
            end = "+inf)"
        return f"{start}, {end}"

    def __str__(self):
        if is_empty(self):
            return 'empty'
        else:
            return self.format_single_range()

    def __hash__(self):
        return hash((self.start, self.end, self.brackets))
