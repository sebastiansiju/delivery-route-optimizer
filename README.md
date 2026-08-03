# 🚚 Delivery Route Optimizer

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A Python-based desktop application designed to solve the **Travelling Salesperson Problem (TSP)** for delivery logistics. This project features an interactive GUI that allows users to plot delivery nodes and visually compare the efficiency and execution time of different pathfinding and heuristic algorithms.

## ✨ Features

* **Interactive GUI (Tkinter):** Visually plot delivery locations (nodes) on a 2D coordinate grid.
* **Algorithm Comparison:** Run multiple algorithms side-by-side to compare total distance and computation time.
* **Combinatorial Safeguards:** Built-in threshold warnings to prevent application freezing when running $O(n!)$ exact algorithms on large datasets.
* **Object-Oriented Architecture:** Clean encapsulation of Graph Data Structures (`Location`, `DistanceMatrix`, and `RoutePlanner`).

## 🧠 Implemented Algorithms

1. **Nearest Neighbour (Greedy Heuristic):** 
   * **Time Complexity:** $O(n^2)$
   * Rapidly calculates a highly efficient route by always moving to the closest unvisited node. Excellent for large datasets where exact computation is impossible.
2. **2-Opt Refinement:** 
   * Iteratively untangles crossed paths in the Nearest Neighbour route by reversing segments, significantly optimizing the final distance.
3. **Brute Force (Exact Solution):** 
   * **Time Complexity:** $O(n!)$
   * Calculates every possible permutation to guarantee the absolute shortest path. *Note: Limited to $n \le 10$ nodes to prevent CPU overloading.*

## 📸 Screenshots

*(Replace these placeholder links with actual images of your app once uploaded to GitHub)*

| Main Interface & Map | Algorithm Comparison Output |
|:---:|:---:|
| `<img src="path/to/interface.png" width="400">` | `<img src="path/to/results.png" width="400">` |

## 🚀 Installation & Setup

This application is built using purely Python standard libraries. No external `pip` installations are required!

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/Delivery-Route-Optimizer.git](https://github.com/YourUsername/Delivery-Route-Optimizer.git)
   cd Delivery-Route-Optimizer
   
