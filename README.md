# Battleship Solitaire CSP Solver

A Python solver for the Battleship Solitaire puzzle using Constraint Satisfaction Problem (CSP) techniques with Generalized Arc Consistency (GAC) and backtracking search.

## Summary

This project solves Battleship Solitaire puzzles by modeling them as a CSP. It uses GAC propagation with backtracking search and the Minimum Remaining Values (MRV) heuristic for variable ordering. The solver enforces row/column ship counts, diagonal adjacency rules, and ship shape constraints to find valid fleet placements.

## Features

- **GAC Propagation**: Efficient domain pruning using Generalized Arc Consistency
- **Backtracking Search**: Systematic exploration with pruning of invalid branches
- **MRV Heuristic**: Selects variables with smallest remaining domains first
- **Multiple Constraint Types**: Table constraints, NValues constraints, and custom ship constraints
- **Ship Validation**: Verifies correct fleet composition (submarines, destroyers, cruisers, battleships)

## Puzzle Format

Input files use the following format:
```
32140231        # Row constraints (ships per row)
12301212        # Column constraints (ships per column)
4321            # Fleet: 4 subs, 3 destroyers, 2 cruisers, 1 battleship
........        # Grid with hints (. = unknown, S = sub, < > ^ v = ship ends, M = middle)
...^....
...v....
........
```

## Cell Symbols

| Symbol | Meaning |
|--------|---------|
| `.` | Water (empty) |
| `S` | Submarine (1×1) |
| `<` | Ship left end |
| `>` | Ship right end |
| `^` | Ship top end |
| `v` | Ship bottom end |
| `M` | Ship middle segment |

## Usage

```bash
python battleship.py --inputfile puzzle.txt --outputfile solution.txt
```

## Constraints Implemented

| Constraint | Description |
|------------|-------------|
| `TableConstraint` | Explicit enumeration of valid tuples |
| `NValuesConstraint` | Bounds on count of specific values in a set of variables |
| `IfAllThenOneConstraint` | Conditional constraint for ship continuity |
| Row/Column constraints | Exact ship segment counts per line |
| Diagonal constraints | No ships adjacent diagonally |
| Shape constraints | Valid ship piece adjacencies |

## Search Algorithms

| Algorithm | Description |
|-----------|-------------|
| `BT` | Basic backtracking |
| `GAC` | GAC propagation + backtracking |

## Variable Heuristics

| Heuristic | Description |
|-----------|-------------|
| `fixed` | Follow CSP variable ordering |
| `random` | Random unassigned variable |
| `mrv` | Minimum Remaining Values (smallest domain first) |

## File Structure

```
├── battleship.py      # Main solver and puzzle parser
├── backtracking.py    # BT and GAC search algorithms
├── constraints.py     # Constraint implementations
└── csp.py             # Variable, Constraint, and CSP base classes
```

## Example

```bash
python battleship.py --inputfile input1.txt --outputfile output1.txt
```

Output:
```
....S...
...<M>..
...^....
...v..S.
........
--------------
```

## Requirements

- Python 3.7+
- No external dependencies

## License

Educational use.
