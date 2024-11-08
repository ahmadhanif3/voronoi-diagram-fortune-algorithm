"""
Voronoi Diagram Class

Initiate with (points) inside the diagram

Edges will be generated and obtained

"""

class VoronoiDiagram:
    def __init__(self, points):
        self.points = points
        self.voronoi_edges = []

    def construct(self):
        # Initialize the sweep line and the beach line
        self.initialize_sweep_line()

        # Sweep the plane and update the beach line
        while self.sweep_line_has_not_reached_end():
            self.handle_next_event()

        # Construct the Voronoi cells from the final beach line
        self.construct_voronoi_cells()

    def initialize_sweep_line(self):
        # Set up the initial beach line and sweep line
        return

    def handle_next_event(self):
        # Process the next event (point appearance or arc intersection)
        # and update the beach line accordingly
        return

    def construct_voronoi_cells(self):
        # Use the final beach line to construct the Voronoi cells
        # and store them in self.voronoi_cells
        return