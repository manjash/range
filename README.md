# range class

Range is a class for operations with mathematical ranges (eg (0, 5] or (-Inf, -3)). It's not related to the standard python range function.
Range object has to be hashable and can be used as a dictionary key.

## Syntax
Range has to have a start, an end and brakets indicating whether the start / end are included. `start` must be greater or equal to `end`.

By default brackets are `[)`: `Range(5, 8.5)` represents `[5.0, 8.5)` range of floats.
Custom brackets are defined as folllows: `Range(5, 8.5, "[]")` representing `[5.0, 8.5]`.

### Infinite borders
`None` represents `+/- Inf` for Range object:
  - `Range(None, None, "()")` represents (-Inf, Inf)
  - `Range(None, 5, "(]")` represents (-Inf, 5]

Inf border requires an exclusive bracket, otherwise throws an error.
As far as non-numerical range operations are possible, any range is included into `Range(None, None, "()")`, eg `"" in Range(None, None, "()") is True`

### Empty Range object
  - `Range(empty=True)` or `Range(None, None, None)`
  - `Range(start, end, brackets)` object with `start == end` and at least one of the brackets being non-inclusive, eg `Range(5, 5, "(]")`.
Exception: `None` represents `+/- Inf` for Range object, hence `Range(None, None, "()")` or Range(5, None) are not empty.
  - `print(Range(empty=True) == 'empty'`

## Supported opeations between 2 Range objects:
  - equal: `Range(5, 6.5, "[)") == Range(5, 6.5) is True`
  - not equal: `Range(5, 6.5, "[]") != Range(5, 6.5) is True`
  - comparison (<, >, >=, <=). Algorithm for comparison:
    - First try to order by `start`, if equal by `end` (both take brackets into account) 
  - 'contains' operation ('in'):
    - 1 element in the Range object: `5 in Range(5, 6) is True`
    - 1 range object is fully included in another range object: `Range(3, 4) in Range(3, 4, "[]") is True`
  - Intersection:
    - `Range(3, 4).intersect(Range(3.5, 5)) == Range(3.5, 4.)`
    - `Range(3, 4).intersect(Range(5, 6)) == Range(empty=True)`
  - Union returns a `Range` object is objects intersect otherwise - a tuple of `Range` objects: 
    - `Range(3, 4) + Range(4, 5) == Range(3., 5.)`
    - `Range(3, 4) + Range(4.1, 5) == (Range(3, 5), Range(4.1, 5))`
    - `Range(3, 4) + Range(empty=True) == Range(3., 4.)`
  - Difference is defined as union without intersection:
    - `Range(3, 4) - Range(4.1, 5) == (Range(3, 5), Range(4.1, 5))`
    - `Range(3, 4) - Range(3.5, 3.6) == (Range(3., 3.5), Range(3.6, 4.))`
    - `Range(3, 4) - Range(empty=True) == Range(3., 4.)`

## Operations on multiple objects:
Union and difference of multiple Range objects and a tuple of Range objects is also supported, for example:
  - `Range(3, 4) - Range(3.5, 7) + Range(2.7, 2.9) == Range(2.7, 2.9), Range(3., 3.5), Range(4, 7)`
  - `Range(3, 4) + (Range(3.5, 7), Range(3.6, 3.7), Range(7.5, 9)) + Range(2.7, 2.9) == (Range(2.7, 2.9), Range(3, 7), Range(7.5, 9))`

**!NB:** difference for Range and tuple_of_Range_objects (eg `Range(3, 4) - (Range(5, 6), Range(7, 8)`) is not supported.

## Requirements:

- Make a Range class with business logic similar to https://www.postgresql.org/docs/current/rangetypes.html.
- Start with learning about python [typing](https://docs.python.org/3/library/typing.html) (everything will be strongly typed, learn mypy too). Additionally, take a look at [Generics](https://docs.python.org/3/library/typing.html#generics).
- Start with Float (continuous type)
- Request to create a range with start >= finish is invalid, throw an exception
- Supported operations between 2 range class objects:
  - equal / not
  - comparison (more, less, and with equals). Python has a decorator total_ordering (or similar), use it for simplification.
  - range object has to be hashable. Range has to be immutable and when changes happen, this creates a new range obect all the time.

- Algorithmic part (like SET functionality):
  - 'contains' operation ('in'):
    - 1 element in the range object
    - 1 range object is fully included in another range object
  - Intersection of 2 range objects
  - union (has intersection - return range object, no intersection - return list)
  - difference (similar)

- More complicated:
  - Union for multiple range objects

- examples of ranges: `[0, 5), [0, 5], (0, 5), (0, 5], (-inf, 5], (-inf, inf), [5, inf), empty`
- beautiful print (like above), read `__str__` vs `__repr__`

- tests
