# Delivery Route Optimizer

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A desktop application that solves the **Travelling Salesperson Problem (TSP)** for a small delivery round. It generates a depot and three customer locations on a 2D grid, then lets you run three different routing algorithms over the same graph and compare their results side by side.

Built for the **502IT** coursework as a demonstration of graph data structures, greedy heuristics, local search, and exhaustive search.

## Features

- **Randomised scenarios** — click *Set D, A, B, C Nodes* to generate a fresh depot and three customers with random coordinates, then rebuild the complete distance graph.
- **Three routing algorithms** run on demand against the same node set.
- **Live distance matrix** showing every pairwise leg (Depot→A, Depot→B, Depot→C, A→B, B→C, A→C) in kilometres.
- **Algorithm comparison panel** that tracks each algorithm's total distance as you run it and highlights the current best.
- **Route trace output** printing the full node sequence and total distance for the most recent run.
- **Zero dependencies** — Python standard library only.

## Implemented algorithms

### 1. Nearest Neighbour — greedy heuristic, O(n²)

Starts at the depot and repeatedly hops to the closest unvisited node, then returns to the depot. Fast and usually decent, but it commits to early choices it cannot undo, so the tour can end up with crossed legs.

### 2. 2-Opt Refinement — local search

Takes the Nearest Neighbour tour and repeatedly reverses route segments, keeping any reversal that shortens the total distance. This untangles crossed paths. It restarts the sweep after each accepted improvement and stops when no reversal helps. **Run Nearest Neighbour first** — 2-Opt refines an existing route rather than building one.

### 3. Brute Force — exact solution, O(n!)

Enumerates every permutation of the customer nodes and keeps the shortest closed tour. This is guaranteed optimal, which makes it the yardstick the two heuristics are measured against. With the default four nodes that is only 3! = 6 tours; the factorial growth is why the heuristics exist at all.

The comparison panel makes the trade-off concrete: on most random layouts Nearest Neighbour and 2-Opt land on the same distance as Brute Force, but on the awkward ones the greedy tour is visibly worse and 2-Opt closes the gap.

## Architecture

The routing engine is fully decoupled from the GUI, so every class below can be imported and tested without Tkinter.

```
Location          A delivery address: id, name, and (x, y) coordinates.
                  distance_to() gives straight-line distance via math.hypot.

DistanceMatrix    The graph. Holds the nodes and a nested dictionary of
                  pairwise distances for O(1) lookup, with self-distance
                  defined as 0 and missing edges as infinity.

RoutePlanner      The algorithms — nearest_neighbour, optimize_2opt and
                  brute_force — plus calculate_total_distance, which every
                  one of them scores against.

UltimateDeliveryApp   Tkinter front end: control panel and distance matrix
                      on the left, route output and comparison panel on the right.
```

## Running it

Requires Python 3.8+ with Tkinter (bundled with the standard Windows and macOS installers; on Debian/Ubuntu install `python3-tk`).

```bash
git clone https://github.com/sebastiansiju/delivery-route-optimizer.git
```

Then run the script inside the `delivery route optimizer` folder:

```bash
python "delivery route optimizer/delivery route optimizer.py"
```

## Usage

1. The app opens with a depot and three customers already generated. Click **Set D, A, B, C Nodes** at any time for a new random layout — this also resets the comparison panel.
2. Click **Run Nearest Neighbour** to build a greedy tour.
3. Click **Apply 2-Opt Refinement** to improve that tour. (Running this first shows an error — 2-Opt needs a route to refine.)
4. Click **Run Brute Force (Exact)** for the guaranteed optimum.
5. Compare the three distances in the **Algorithm Comparison & Best Route** panel at the bottom right; the starred line names the current winner.

Distances are straight-line (Euclidean) and reported in kilometres. The depot sits at the origin `(0, 0)`; customers are placed at random integer coordinates between 10 and 50 on both axes.

## Repository contents

```
delivery-route-optimizer/
├── delivery route optimizer/
│   ├── delivery route optimizer.py   # Routing engine + Tkinter GUI
│   ├── UML diagram                   # Class diagram for the routing engine
│   └── pseudocode                    # Pseudocode for all three algorithms
├── README.md
├── LICENSE
└── .gitignore
```

## License

MIT
