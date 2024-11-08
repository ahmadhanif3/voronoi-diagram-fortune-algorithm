"""

Test for voronoi diagram with fortune algorithm

"""

import heapq
import math
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

class Event:
    def __init__(self, point, event_type, arc=None):
        self.point = point
        self.event_type = event_type 
        self.arc = arc
        self.y = point.y

    def __lt__(self, other):
        return self.y < other.y

class Edge:
    def __init__(self, start):
        self.start = start
        self.end = None
        self.direction = None

class Arc:
    def __init__(self, site):
        self.site = site
        self.edge = None
        self.circle_event = None

class VoronoiDiagram:
    def __init__(self, points):
        self.points = points
        self.edges = []
        self.event_queue = []
        self.beachline = None

        for point in points:
            event = Event(point, "site")
            heapq.heappush(self.event_queue, event)

    def process_events(self):
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            if event.event_type == "site":
                self.handle_site_event(event)
            elif event.event_type == "circle":
                self.handle_circle_event(event)

    def handle_site_event(self, event):
        site = event.point
        if not self.beachline:
            self.beachline = Arc(site)
            return

        arc = self.get_arc_above(site)
        if arc is None:
            print("Warning: No arc found above the site.")
            return

        if arc.circle_event:
            arc.circle_event = None

        left_edge, right_edge = self.create_breakpoints(site, arc)

        new_arc = Arc(site)
        new_arc.edge = right_edge
        arc.edge = left_edge

        self.check_circle_event(arc)
        self.check_circle_event(new_arc)
        self.check_circle_event(arc)


    def handle_circle_event(self, event):
        arc = event.arc
        if not arc or arc.circle_event != event:
            return 

        vertex = event.point

        arc.edge.end = vertex
        arc.edge = None

        self.check_circle_event(arc)

    def create_breakpoints(self, site, arc):
        left_edge = Edge(arc.site)
        right_edge = Edge(site)
        self.edges.extend([left_edge, right_edge])
        return left_edge, right_edge

    def get_arc_above(self, point):
        arc = self.beachline
        while arc:
            if arc.site.x < point.x < arc.site.x + 1:
                return arc
            arc = arc.edge
        return None

    def check_circle_event(self, arc):
        if not arc:
            return
        arc.circle_event = None

    def get_edges(self):
        return [(edge.start, edge.end) for edge in self.edges if edge.end]
