"""
    This is the implementation for constructing voronoi diagram given sets of points in the plane
    The reference used for this implementation is https://github.com/khuyentran1401/Voronoi-diagram/
"""

import numpy as np
from sklearn.neighbors import NearestNeighbors


class Voronoi:
    def __init__(self, points, xmin=None, xmax=None, ymin=None, ymax=None):
        self.points = list(set(points))  # Ensure unique points
        self.edges = []  # List of edges [(p1, p2), ...]
        self.regions = []  # List of regions (polygons)

        # Determine bounding box
        if xmin is None or xmax is None or ymin is None or ymax is None:
            self.xmin, self.xmax, self.ymin, self.ymax = self._calculate_bounding_box()
        else:
            self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax

    def _calculate_bounding_box(self):
        """Calculate a bounding box with a margin around the points."""
        points_array = np.array(self.points)
        margin = 1
        xmin = points_array[:, 0].min() - margin
        xmax = points_array[:, 0].max() + margin
        ymin = points_array[:, 1].min() - margin
        ymax = points_array[:, 1].max() + margin
        return xmin, xmax, ymin, ymax

    def _perpendicular_bisector(self, p1, p2):
        """Calculate the perpendicular bisector of two points p1 and p2."""
        midpoint = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        if p1[0] == p2[0]:  # Vertical line, perpendicular bisector is horizontal
            return ((self.xmin, midpoint[1]), (self.xmax, midpoint[1]))
        if p1[1] == p2[1]:  # Horizontal line, perpendicular bisector is vertical
            return ((midpoint[0], self.ymin), (midpoint[0], self.ymax))

        slope = -(p2[0] - p1[0]) / (p2[1] - p1[1])  # Negative reciprocal
        intercept = midpoint[1] - slope * midpoint[0]
        return ((self.xmin, slope * self.xmin + intercept), (self.xmax, slope * self.xmax + intercept))

    def _do_intersect(self, p1, q1, p2, q2):
        """Check if line segments (p1, q1) and (p2, q2) intersect."""
        def orientation(a, b, c):
            val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
            if val == 0:
                return 0  # Collinear
            return 1 if val > 0 else 2  # Clockwise or counterclockwise

        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True
        return False  # Simplified for clarity

    def compute_diagram(self):
        """Construct the Voronoi diagram incrementally."""
        n = len(self.points)
        if n < 2:
            return []

        # Sort points relative to a reference point
        reference = (self.xmin, self.ymin)
        self.points.sort(key=lambda p: ((p[0] - reference[0]) ** 2 +
                                        (p[1] - reference[1]) ** 2) ** 0.5, reverse=True)

        cur_points = [self.points.pop()]
        for _ in range(n - 1):
            new_point = self.points.pop()
            cur_points.append(new_point)

            # Find the closest point to the new one
            nbrs = NearestNeighbors(n_neighbors=2).fit(np.array(cur_points))
            indices = nbrs.kneighbors(np.array(new_point).reshape(1, -1), return_distance=False)
            closest_point = cur_points[indices[0][1]]

            # Calculate the perpendicular bisector
            bisector_start, bisector_end = self._perpendicular_bisector(new_point, closest_point)

            # Add the bisector as a new edge
            self.edges.append((bisector_start, bisector_end))

            # Check intersections with existing edges
            intersected_edges = []
            for edge in self.edges:
                if self._do_intersect(bisector_start, bisector_end, edge[0], edge[1]):
                    intersected_edges.append(edge)

            # Add new edges formed by intersections
            for edge in intersected_edges:
                self.edges.remove(edge)
                intersection_point = self._find_intersection(bisector_start, bisector_end, edge[0], edge[1])
                self.edges.append((intersection_point, edge[0]))
                self.edges.append((intersection_point, bisector_start))


        return self.edges

    def _find_intersection(self, p1, q1, p2, q2):
        """Find the intersection point of two lines."""
        a1 = q1[1] - p1[1]
        b1 = p1[0] - q1[0]
        c1 = a1 * p1[0] + b1 * p1[1]

        a2 = q2[1] - p2[1]
        b2 = p2[0] - q2[0]
        c2 = a2 * p2[0] + b2 * p2[1]

        determinant = a1 * b2 - a2 * b1
        if determinant == 0:
            return None  # Lines are parallel or collinear

        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        return (x, y)
