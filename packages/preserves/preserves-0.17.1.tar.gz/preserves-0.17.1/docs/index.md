# Overview

```shell
pip install preserves
```

This package ([`preserves` on pypi.org](https://pypi.org/project/preserves/)) implements
[Preserves](https://preserves.dev/) for Python 3.x. It provides the core [semantics][] as well
as both the [human-readable text syntax](https://preserves.dev/preserves-text.html) (a superset
of JSON) and [machine-oriented binary format](https://preserves.dev/preserves-binary.html)
(including canonicalization) for Preserves. It also implements [Preserves
Schema](https://preserves.dev/preserves-schema.html) and [Preserves
Path](https://preserves.dev/preserves-path.html).

 - Main package API: [preserves](/api)

## What is Preserves?

{% include "what-is-preserves.md" %}

## Mapping between Preserves values and Python values

Preserves `Value`s are categorized in the following way:

{% include "value-grammar.md" %}

Python's strings, byte strings, integers, booleans, and double-precision floats stand directly
for their Preserves counterparts. Small wrapper classes for `Float` and `Symbol` complete the
suite of atomic types.

Python's lists and tuples correspond to Preserves `Sequence`s, and dicts and sets to
`Dictionary` and `Set` values, respectively. Preserves `Record`s are represented by a `Record`
class. Finally, embedded values are represented by a small `Embedded` wrapper class.

[semantics]: https://preserves.dev/preserves.html#semantics
