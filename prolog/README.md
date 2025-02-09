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

## Result of parsing

There is no output file, facts are added in to Prolog interactive program dynamiccally using predicate `assertz/1`.

Each single line of the input file is parsed into fact like this:

```prolog
male('Александр')
female('Дана (Ж)')
spouse('Богдан', 'Мария')
parent('Павел', 'Александра')
```

## How to Run

### Prerequisites

- Ensure you have **SWI Prolog** installed on your system.

### Steps to Execute

1. Prepare an input file with the specified format (e.g., `input.txt`) or use `input_short.txt` for testing.
2. Open a terminal and navigate to the directory containing `parser.pl` and `input.txt`.
3. Start GNU Prolog:

   ```bash
   swipl
   ```

4. Load the Prolog program:

   ```prolog
   [parser].
    ```

5. Run the parsing process by invoking:

   ```prolog
   parse_input_file('input.txt').
    ```

6. Check the generated rules are available by typing:

   ```prolog
   father(X, Y).
   ```

### How to add new relation

For example we want to add a new relation, great uncle (двоюродный дедушка), how would we proceed?

1. Rezlize if you have a great uncle at all. For this we can use already defined relations and call from CLI where `swipl` running:

```bash
grandfather(GF, Name), brother(GB, GF).
```

This wil give us all the possible matches for this predicate, for example:

```bash
grandfather(GF, ME), brother(GB, GF).
GF = 'Константин',
ME = 'Марина',
GB = 'Сильвестр' ;
GF = 'Константин',
ME = 'Урбан',
GB = 'Сильвестр' ;
GF = 'Ярослав',
ME = 'Анфиса',
GB = 'Максим' .
```

2. We can see that, `Урбан` for example has a great uncle `Сильвестр`, then we can verify in `input.txt`, if it was a valid predicate.
3. After we just add to `relations.pl` an entry: `great_uncle(Name, GU) :- grandfather(GF, Name), brother(GU, GF).`
4. After re-compiling, we call `great_uncle('Урбан', RESULT).` and make sure RESULT is `Сильвестр`.
