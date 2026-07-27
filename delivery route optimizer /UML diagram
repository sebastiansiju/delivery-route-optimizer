+-------------------------------------------------------------+
|                          Location                           |
+-------------------------------------------------------------+
| - loc_id: str                                               |
| - name: str                                                 |
| - x: float                                                  |
| - y: float                                                  |
+-------------------------------------------------------------+
| + distance_to(other: Location): float                       |
+-------------------------------------------------------------+
                               ^
                               | (stores 1..*)
+-------------------------------------------------------------+
|                       DistanceMatrix                        |
+-------------------------------------------------------------+
| - locations: Dict[str, Location]                            |
| - matrix: Dict[str, Dict[str, float]]                       |
+-------------------------------------------------------------+
| + add_location(loc: Location): void                         |
| + get_distance(u: str, v: str): float                       |
+-------------------------------------------------------------+
                               ^
                               | (queries 1)
+-------------------------------------------------------------+
|                        RoutePlanner                         |
+-------------------------------------------------------------+
| - dist_matrix: DistanceMatrix                               |
+-------------------------------------------------------------+
| + calculate_total_distance(route: List[str]): float         |
| + nearest_neighbour(start_id: str): Tuple[List[str], float] |
| + optimize_2opt(route: List[str]): Tuple[List[str], float]  |
| + brute_force(start_id: str): Tuple[List[str], float]       |
+-------------------------------------------------------------+
                               ^
                               | (uses 1)
+-------------------------------------------------------------+
|                     UltimateDeliveryApp                     |
+-------------------------------------------------------------+
| - root: tk.Tk                                               |
| - dist_matrix: DistanceMatrix                               |
| - planner: RoutePlanner                                     |
| - current_route: List[str]                                  |
| - results: Dict[str, float]                                 |
+-------------------------------------------------------------+
| + setup_ui(): void                                          |
| + get_next_alphabetical_id(): str                           |
| + update_matrix_display(): void                             |
| + add_custom_location(): void                               |
| + generate_locations(): void                                |
| + update_best_dialogue(): void                              |
| + run_nn(): void                                            |
| + run_2opt(): void                                          |
| + run_brute_force(): void                                   |
+-------------------------------------------------------------+
