import tkinter as tk
import math
import random
import itertools
from typing import List, Tuple, Dict

# CORE LOGIC (OOP Data Structures & Algorithms)


class Location:
    """Represents a delivery address with 2D coordinates."""
    def __init__(self, loc_id: str, name: str, x: float, y: float):
        self.loc_id = loc_id
        self.name = name
        self.x = x
        self.y = y

    def distance_to(self, other: 'Location') -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


class DistanceMatrix:
    """Dictionary-based lookup for pairwise distances."""
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.matrix: Dict[str, Dict[str, float]] = {}

    def add_location(self, loc: Location) -> None:
        self.locations[loc.loc_id] = loc
        self.matrix[loc.loc_id] = {}

    def add_edge(self, id1: str, id2: str) -> None:
        dist = self.locations[id1].distance_to(self.locations[id2])
        self.matrix[id1][id2] = dist
        self.matrix[id2][id1] = dist

    def get_distance(self, u: str, v: str) -> float:
        if u == v:
            return 0.0
        return self.matrix.get(u, {}).get(v, float('inf'))


class RoutePlanner:
    """Executes Nearest Neighbour, 2-Opt, and Brute Force TSP algorithms."""
    def __init__(self, dist_matrix: DistanceMatrix):
        self.dist_matrix = dist_matrix

    def calculate_total_distance(self, route: List[str]) -> float:
        total = 0.0
        for i in range(len(route) - 1):
            total += self.dist_matrix.get_distance(route[i], route[i + 1])
        return total

    def nearest_neighbour(self, start_id: str) -> Tuple[List[str], float]:
        """O(n^2) Greedy Approach"""
        all_nodes = set(self.dist_matrix.locations.keys())
        route = [start_id]
        current = start_id
        unvisited = all_nodes - {start_id}

        while unvisited:
            nearest = None
            min_dist = float('inf')
            for candidate in unvisited:
                dist = self.dist_matrix.get_distance(current, candidate)
                if dist < min_dist:
                    min_dist = dist
                    nearest = candidate
            
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest

        route.append(start_id)
        return route, self.calculate_total_distance(route)

    def optimize_2opt(self, route: List[str]) -> Tuple[List[str], float]:
        """2-Opt Local Search Refinement"""
        best_route = route[:]
        best_distance = self.calculate_total_distance(best_route)
        improved = True

        while improved:
            improved = False
            for i in range(1, len(best_route) - 2):
                for k in range(i + 1, len(best_route) - 1):
                    new_route = best_route[:i] + best_route[i:k + 1][::-1] + best_route[k + 1:]
                    new_distance = self.calculate_total_distance(new_route)

                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True
                        break
                if improved:
                    break

        return best_route, best_distance

    def brute_force(self, start_id: str) -> Tuple[List[str], float]:
        """Exact Permutation Search O(n!)"""
        other_nodes = [loc for loc in self.dist_matrix.locations.keys() if loc != start_id]
        best_route = []
        min_distance = float('inf')

        for perm in itertools.permutations(other_nodes):
            current_tour = [start_id] + list(perm) + [start_id]
            tour_dist = self.calculate_total_distance(current_tour)

            if tour_dist < min_distance:
                min_distance = tour_dist
                best_route = current_tour

        return best_route, min_distance


# =====================================================================
# GUI APPLICATION
# =====================================================================

class UltimateDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("502IT Problem 1: Delivery Route Optimizer")
        self.root.geometry("850x650")
        self.root.configure(bg="#f4f6f7")

        self.dist_matrix = DistanceMatrix()
        self.planner = RoutePlanner(self.dist_matrix)
        self.current_route = []

        # Track distances for bottom-right comparison box
        self.results = {
            "Nearest Neighbour": None,
            "2-Opt Refined": None,
            "Brute Force": None
        }

        self.setup_ui()
        self.generate_locations()

    def setup_ui(self):
        # -------------------------------------------------------------
        # LEFT PANEL
        # -------------------------------------------------------------
        left_panel = tk.Frame(self.root, width=270, bg="#2c3e50", padx=10, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left_panel, text="Route Planner", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50").pack(pady=(0, 10))
        
        # The setup button stays where it is
        tk.Button(left_panel, text=" Set D, A, B, C Nodes", command=self.generate_locations, width=24, bg="#f9fafc", fg="#2c3e50").pack(pady=4)
        tk.Button(left_panel, text=" Run Nearest Neighbour", command=self.run_nn, width=24, bg="#ff000d", fg="#03050a").pack(pady=(30, 4))
        tk.Button(left_panel, text=" Apply 2-Opt Refinement", command=self.run_2opt, width=24, bg="#00e5ff", fg="#03050a").pack(pady=4)
        tk.Button(left_panel, text=" Run Brute Force (Exact)", command=self.run_brute_force, width=24, bg="#39e622", fg="#03050a").pack(pady=4)

        # BOTTOM-LEFT BOX: GRAPH DISTANCES MATRIX (D, A, B, C)
        self.matrix_frame = tk.LabelFrame(left_panel, text=" Graph Distances (D, A, B, C) ", font=("Arial", 9, "bold"), fg="#f1c40f", bg="#34495e", padx=8, pady=8)
        self.matrix_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.lbl_d_a = tk.Label(self.matrix_frame, text="Depot -> A: --", font=("Arial", 9), fg="white", bg="#34495e", anchor="w")
        self.lbl_d_a.pack(fill=tk.X)

        self.lbl_d_b = tk.Label(self.matrix_frame, text="Depot -> B: --", font=("Arial", 9), fg="white", bg="#34495e", anchor="w")
        self.lbl_d_b.pack(fill=tk.X)

        self.lbl_d_c = tk.Label(self.matrix_frame, text="Depot -> C: --", font=("Arial", 9), fg="white", bg="#34495e", anchor="w")
        self.lbl_d_c.pack(fill=tk.X)

        self.lbl_a_b = tk.Label(self.matrix_frame, text="A -> B: --", font=("Arial", 9), fg="#ecf0f1", bg="#34495e", anchor="w")
        self.lbl_a_b.pack(fill=tk.X, pady=(3, 0))

        self.lbl_b_c = tk.Label(self.matrix_frame, text="B -> C: --", font=("Arial", 9), fg="#ecf0f1", bg="#34495e", anchor="w")
        self.lbl_b_c.pack(fill=tk.X)

        self.lbl_a_c = tk.Label(self.matrix_frame, text="A -> C: --", font=("Arial", 9), fg="#ecf0f1", bg="#34495e", anchor="w")
        self.lbl_a_c.pack(fill=tk.X)

        self.lbl_d_d = tk.Label(self.matrix_frame, text="Depot -> Depot: 0.00 km", font=("Arial", 9, "bold"), fg="#f1c40f", bg="#34495e", anchor="w")
        self.lbl_d_d.pack(fill=tk.X, pady=(4, 0))

        # -------------------------------------------------------------
        # RIGHT PANEL (Split into Top Logs & Bottom-Right Comparison)
        # -------------------------------------------------------------
        right_panel = tk.Frame(self.root, bg="#f4f6f7", padx=15, pady=15)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(right_panel, text="Calculated Route Results", font=("Arial", 12, "bold"), bg="#f4f6f7", fg="#2c3e50").pack(anchor="w")

        # Upper Text Box for Route Logs
        self.txt_output = tk.Text(right_panel, font=("Consolas", 10), bg="white", relief=tk.SOLID, bd=1, height=18)
        self.txt_output.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        # NEW BOTTOM-RIGHT BOX: BEST ALGORITHM COMPARISON DIALOGUE
        self.best_frame = tk.LabelFrame(right_panel, text=" Algorithm Comparison & Best Route ", font=("Arial", 10, "bold"), fg="#2c3e50", bg="#e8f8f5", padx=10, pady=10, relief=tk.GROOVE)
        self.best_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_res_nn = tk.Label(self.best_frame, text="Nearest Neighbour : Not Calculated", font=("Arial", 9), bg="#e8f8f5", anchor="w")
        self.lbl_res_nn.pack(fill=tk.X)

        self.lbl_res_2opt = tk.Label(self.best_frame, text="2-Opt Refinement   : Not Calculated", font=("Arial", 9), bg="#e8f8f5", anchor="w")
        self.lbl_res_2opt.pack(fill=tk.X)

        self.lbl_res_bf = tk.Label(self.best_frame, text="Brute Force (Exact): Not Calculated", font=("Arial", 9), bg="#e8f8f5", anchor="w")
        self.lbl_res_bf.pack(fill=tk.X)

        self.lbl_best_winner = tk.Label(self.best_frame, text="★ BEST ALGORITHM: Run algorithms to compare", font=("Arial", 10, "bold"), fg="#27ae60", bg="#e8f8f5", anchor="w")
        self.lbl_best_winner.pack(fill=tk.X, pady=(6, 0))

    def generate_locations(self):
        """Generates nodes for Depot (D), Customer A, Customer B, and Customer C."""
        self.dist_matrix = DistanceMatrix()
        self.planner = RoutePlanner(self.dist_matrix)
        self.current_route = []

        # Reset Results Tracker
        self.results = {"Nearest Neighbour": None, "2-Opt Refined": None, "Brute Force": None}

        self.dist_matrix.add_location(Location("D", "Depot", 0, 0))
        self.dist_matrix.add_location(Location("A", "Customer A", random.randint(10, 50), random.randint(10, 50)))
        self.dist_matrix.add_location(Location("B", "Customer B", random.randint(10, 50), random.randint(10, 50)))
        self.dist_matrix.add_location(Location("C", "Customer C", random.randint(10, 50), random.randint(10, 50)))

        ids = list(self.dist_matrix.locations.keys())
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                self.dist_matrix.add_edge(ids[i], ids[j])

        # Distances
        d_a = self.dist_matrix.get_distance("D", "A")
        d_b = self.dist_matrix.get_distance("D", "B")
        d_c = self.dist_matrix.get_distance("D", "C")
        a_b = self.dist_matrix.get_distance("A", "B")
        b_c = self.dist_matrix.get_distance("B", "C")
        a_c = self.dist_matrix.get_distance("A", "C")
        d_d = self.dist_matrix.get_distance("D", "D")

        # Update Bottom-Left Matrix Box
        self.lbl_d_a.config(text=f"Depot -> A: {d_a:.2f} km")
        self.lbl_d_b.config(text=f"Depot -> B: {d_b:.2f} km")
        self.lbl_d_c.config(text=f"Depot -> C: {d_c:.2f} km")
        self.lbl_a_b.config(text=f"A -> B:     {a_b:.2f} km")
        self.lbl_b_c.config(text=f"B -> C:     {b_c:.2f} km")
        self.lbl_a_c.config(text=f"A -> C:     {a_c:.2f} km")
        self.lbl_d_d.config(text=f"Depot -> Depot: {d_d:.2f} km")

        # Reset Bottom-Right Box UI
        self.lbl_res_nn.config(text="Nearest Neighbour : Not Calculated")
        self.lbl_res_2opt.config(text="2-Opt Refinement   : Not Calculated")
        self.lbl_res_bf.config(text="Brute Force (Exact): Not Calculated")
        self.lbl_best_winner.config(text="★ BEST ALGORITHM: Run algorithms to compare", fg="#7f8c8d")

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, "Nodes Loaded: Depot (D), Customer A, Customer B, Customer C.\n\n")
        # Display the generated coordinates
        self.txt_output.insert(tk.END, "Run algorithms to see the live comparison in the bottom-right dialogue box.")

    def update_best_dialogue(self):
        """Updates the bottom-right dialogue box with calculated distances and determines the best algorithm."""
        nn_d = self.results["Nearest Neighbour"]
        opt_d = self.results["2-Opt Refined"]
        bf_d = self.results["Brute Force"]

        self.lbl_res_nn.config(text=f"Nearest Neighbour : {nn_d:.2f} km" if nn_d else "Nearest Neighbour : Not Calculated")
        self.lbl_res_2opt.config(text=f"2-Opt Refinement   : {opt_d:.2f} km" if opt_d else "2-Opt Refinement   : Not Calculated")
        self.lbl_res_bf.config(text=f"Brute Force (Exact): {bf_d:.2f} km" if bf_d else "Brute Force (Exact): Not Calculated")

        # Find the algorithm with the minimum distance
        valid_results = {k: v for k, v in self.results.items() if v is not None}
        if valid_results:
            best_alg = min(valid_results, key=valid_results.get)
            best_val = valid_results[best_alg]
            self.lbl_best_winner.config(text=f"★ BEST ALGORITHM: {best_alg} ({best_val:.2f} km)", fg="#27ae60")

    def run_nn(self):
        """Runs Nearest Neighbour."""
        self.current_route, nn_dist = self.planner.nearest_neighbour("D")
        self.results["Nearest Neighbour"] = nn_dist
        self.update_best_dialogue()

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, "=== 1. NEAREST NEIGHBOUR ROUTE ===\n\n")
        self.txt_output.insert(tk.END, " -> ".join(self.current_route) + "\n\n")
        self.txt_output.insert(tk.END, f"Total Calculated Distance: {nn_dist:.2f} km\n")

    def run_2opt(self):
        """Runs 2-Opt."""
        if not self.current_route:
            self.txt_output.insert(tk.END, "\n[Error] Please run Nearest Neighbour first!")
            return

        opt_route, opt_dist = self.planner.optimize_2opt(self.current_route)
        self.results["2-Opt Refined"] = opt_dist
        self.update_best_dialogue()

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, "=== 2. 2-OPT REFINED ROUTE ===\n\n")
        self.txt_output.insert(tk.END, " -> ".join(opt_route) + "\n\n")
        self.txt_output.insert(tk.END, f"Optimized Distance: {opt_dist:.2f} km\n")

    def run_brute_force(self):
        """Runs Brute Force."""
        bf_route, bf_dist = self.planner.brute_force("D")
        self.results["Brute Force"] = bf_dist
        self.update_best_dialogue()

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, "=== 3. BRUTE FORCE EXACT OPTIMAL ROUTE ===\n\n")
        self.txt_output.insert(tk.END, " -> ".join(bf_route) + "\n\n")
        self.txt_output.insert(tk.END, f"Absolute Minimum Distance: {bf_dist:.2f} km\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateDeliveryApp(root)
    root.mainloop()