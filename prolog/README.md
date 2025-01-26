# Input File Parser

This Prolog program parses a given text file containing relationship data and generates Prolog rules from it. The program reads an input file, processes each line, and writes corresponding Prolog predicates to an output file.

## Features

- Detects and processes gender lines (e.g., `Авдей (М)` or `Аврора (Ж)`).
- Detects and processes spouse relationships (`Назар <-> Кира`).
- Detects and processes parent-child relationships (`Богдан -> Целестина`).
- Generates Prolog predicates for `male/1`, `female/1`, `spouse/2`, and `parent/2`.

## Input File Format

The input file should contain lines in one of the following formats:

1. **Gender information:**
   - `Авдей (М)` for male.
   - `Целестина (Ж)` for female.

2. **Spouse relationship:**
   - `Назар <-> Кира` to indicate that John and Jane are spouses.

3. **Parent-child relationship:**
   - `Богдан -> Целестина` to indicate that John is a parent of Mary.

## Output File Format

The output file will contain Prolog predicates corresponding to the input data, such as:

```prolog
male('Александр').
female('Дана (Ж)').
spouse('Богдан', 'Мария').
parent('Павел', 'Александра').
```

## How to Run

### Prerequisites

- Ensure you have **GNU Prolog** installed on your system.

### Steps to Execute

1. Prepare an input file with the specified format (e.g., `input.txt`) or use `input_short.txt` for testing.
2. Open a terminal and navigate to the directory containing `parser.pl` and `input.txt`.
3. Start GNU Prolog:

   ```bash
   gprolog
   ```

4. Load the Prolog program:

   ```prolog
   [parser].
    ```

5. Run the parsing process by invoking:

   ```prolog
   parse_input_file('input.txt', 'people.pl').
    ```

6. Check the generated `people.pl` file for the output predicates.

### Example

#### Input File (`input.txt`)

```text
Авдей (М)
Александра (Ж)
Ростислав <-> Александра
Корнилий -> Владимир
```

#### Generated Output File (`people.pl`)

```prolog
male('Авдей').
female('Александра').
spouse('Ростислав', 'Александра').
parent('Корнилий', 'Владимир').
```
