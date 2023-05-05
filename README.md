# range class


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
