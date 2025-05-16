# NOTES

## What is a functional programming?

### Pure functions

A pure function’s output depends only on its inputs, and it has no side effects (no modifying globals, no I/O, no
changing state).

### Immutability

Data structures are never changed in place. Instead, operations create new versions.

### First-Class and Higher-Order Functions

1. Functions are values: you can pass them as arguments, return them from other functions, and assign them to variables.
2. A higher-order function either takes one or more functions as arguments or returns a function.

### Declarative Style?

You describe what you want done, not how to do it step by step.

### Benefits

1. Simple predictable behavior and testing: pure functions are predictable.
2. Concurrency-friendly: No shared mutable state avoids race conditions.

#### Installation

For Mac

1. install rmagick: `brew install imagemagick`
2. then execute from root: `bundle install`

#### TODO:

1. Try other Metrics (for example, NCC)
2. 