"""Unit tests for the RoutePlanner/DistanceMatrix/Location engine.

The engine lives in a single file alongside the Tkinter GUI, inside a
directory whose name ends with a space ("delivery route optimizer /").
It is loaded here via importlib so the tests do not depend on that
directory being an importable package.
"""
import importlib.util
import itertools
import math
import random
import sys
import unittest
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "delivery route optimizer "
    / "delivery route optimizer.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("route_optimizer", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


try:
    engine = _load_module()
except ImportError as exc:  # pragma: no cover - environment without Tkinter
    engine = None
    _import_error = exc


@unittest.skipIf(engine is None, f"module could not be imported: {globals().get('_import_error')}")
class LocationTests(unittest.TestCase):
    def test_distance_to_is_euclidean(self):
        a = engine.Location("A", "A", 0, 0)
        b = engine.Location("B", "B", 3, 4)
        self.assertAlmostEqual(a.distance_to(b), 5.0)

    def test_distance_to_self_is_zero(self):
        a = engine.Location("A", "A", 7, 9)
        self.assertAlmostEqual(a.distance_to(a), 0.0)

    def test_distance_is_symmetric(self):
        a = engine.Location("A", "A", 1, 2)
        b = engine.Location("B", "B", -3, 5)
        self.assertAlmostEqual(a.distance_to(b), b.distance_to(a))


@unittest.skipIf(engine is None, f"module could not be imported: {globals().get('_import_error')}")
class DistanceMatrixTests(unittest.TestCase):
    def setUp(self):
        self.matrix = engine.DistanceMatrix()
        self.matrix.add_location(engine.Location("D", "Depot", 0, 0))
        self.matrix.add_location(engine.Location("A", "A", 3, 4))
        self.matrix.add_location(engine.Location("B", "B", 6, 8))
        self.matrix.add_edge("D", "A")
        self.matrix.add_edge("D", "B")
        self.matrix.add_edge("A", "B")

    def test_get_distance_matches_euclidean_distance(self):
        self.assertAlmostEqual(self.matrix.get_distance("D", "A"), 5.0)
        self.assertAlmostEqual(self.matrix.get_distance("D", "B"), 10.0)
        self.assertAlmostEqual(self.matrix.get_distance("A", "B"), 5.0)

    def test_get_distance_is_symmetric(self):
        self.assertAlmostEqual(
            self.matrix.get_distance("D", "A"), self.matrix.get_distance("A", "D")
        )

    def test_self_distance_is_zero(self):
        self.assertAlmostEqual(self.matrix.get_distance("D", "D"), 0.0)

    def test_missing_edge_is_infinite(self):
        self.matrix.add_location(engine.Location("C", "C", 1, 1))
        self.assertEqual(self.matrix.get_distance("D", "C"), float("inf"))


@unittest.skipIf(engine is None, f"module could not be imported: {globals().get('_import_error')}")
class RoutePlannerTests(unittest.TestCase):
    def _build_matrix(self, coords):
        matrix = engine.DistanceMatrix()
        for loc_id, (x, y) in coords.items():
            matrix.add_location(engine.Location(loc_id, loc_id, x, y))
        ids = list(coords.keys())
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                matrix.add_edge(ids[i], ids[j])
        return matrix

    def _assert_valid_tour(self, route, node_ids, start_id):
        self.assertEqual(route[0], start_id)
        self.assertEqual(route[-1], start_id)
        # Every node visited exactly once between the two depot bookends.
        self.assertEqual(sorted(route[1:-1]), sorted(node_ids - {start_id}))

    def test_calculate_total_distance_sums_consecutive_legs(self):
        matrix = self._build_matrix({"D": (0, 0), "A": (3, 0), "B": (3, 4)})
        planner = engine.RoutePlanner(matrix)
        total = planner.calculate_total_distance(["D", "A", "B", "D"])
        self.assertAlmostEqual(total, 3 + 4 + 5)

    def test_nearest_neighbour_produces_valid_tour(self):
        coords = {"D": (0, 0), "A": (10, 0), "B": (10, 10), "C": (0, 10)}
        matrix = self._build_matrix(coords)
        planner = engine.RoutePlanner(matrix)
        route, distance = planner.nearest_neighbour("D")
        self._assert_valid_tour(route, set(coords), "D")
        self.assertAlmostEqual(distance, planner.calculate_total_distance(route))

    def test_optimize_2opt_never_worsens_the_route(self):
        random.seed(42)
        for _ in range(20):
            coords = {
                node: (random.randint(0, 50), random.randint(0, 50))
                for node in ("D", "A", "B", "C", "E")
            }
            matrix = self._build_matrix(coords)
            planner = engine.RoutePlanner(matrix)
            nn_route, nn_dist = planner.nearest_neighbour("D")
            opt_route, opt_dist = planner.optimize_2opt(nn_route)
            self._assert_valid_tour(opt_route, set(coords), "D")
            self.assertLessEqual(opt_dist, nn_dist + 1e-9)
            self.assertAlmostEqual(opt_dist, planner.calculate_total_distance(opt_route))

    def test_optimize_2opt_reaches_local_optimum(self):
        # No single reversal of the returned route should shorten it further.
        coords = {"D": (0, 0), "A": (10, 10), "B": (10, 0), "C": (0, 10)}
        matrix = self._build_matrix(coords)
        planner = engine.RoutePlanner(matrix)
        nn_route, _ = planner.nearest_neighbour("D")
        opt_route, opt_dist = planner.optimize_2opt(nn_route)

        for i in range(1, len(opt_route) - 2):
            for k in range(i + 1, len(opt_route) - 1):
                candidate = opt_route[:i] + opt_route[i:k + 1][::-1] + opt_route[k + 1:]
                candidate_dist = planner.calculate_total_distance(candidate)
                self.assertGreaterEqual(candidate_dist, opt_dist - 1e-9)

    def test_brute_force_matches_manual_optimum(self):
        coords = {"D": (0, 0), "A": (10, 0), "B": (10, 10), "C": (0, 10)}
        matrix = self._build_matrix(coords)
        planner = engine.RoutePlanner(matrix)
        route, distance = planner.brute_force("D")
        self._assert_valid_tour(route, set(coords), "D")

        expected_best = min(
            planner.calculate_total_distance(["D", *perm, "D"])
            for perm in itertools.permutations(["A", "B", "C"])
        )
        self.assertAlmostEqual(distance, expected_best)

    def test_brute_force_is_at_least_as_good_as_nearest_neighbour(self):
        random.seed(7)
        for _ in range(10):
            coords = {
                node: (random.randint(0, 50), random.randint(0, 50))
                for node in ("D", "A", "B", "C", "E")
            }
            matrix = self._build_matrix(coords)
            planner = engine.RoutePlanner(matrix)
            _, nn_dist = planner.nearest_neighbour("D")
            _, bf_dist = planner.brute_force("D")
            self.assertLessEqual(bf_dist, nn_dist + 1e-9)


if __name__ == "__main__":
    unittest.main()
