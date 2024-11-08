"""

Test for voronoi diagram with fortune algorithm

"""

import heapq
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

    def set_direction(self, dx, dy):
        self.direction = Point(dx, dy)

class Arc:
    def __init__(self, site):
        self.site = site
        self.edge = None
        self.circle_event = None
        self.prev = None
        self.next = None

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

        arc_above = self.get_arc_above(site.x)
        if arc_above is None:
            print("Warning: No arc found above the site.")
            return

        if arc_above.circle_event:
            arc_above.circle_event = None

        left_edge, right_edge = self.create_breakpoints(site, arc_above)

        new_arc = Arc(site)
        new_arc.edge = right_edge
        arc_above.edge = left_edge

        self.insert_arc_between(arc_above, new_arc)

        self.check_circle_event(arc_above.prev)
        self.check_circle_event(new_arc)
        self.check_circle_event(arc_above.next)

    def handle_circle_event(self, event):
        arc = event.arc
        if not arc or arc.circle_event != event:
            return 

        vertex = event.point

        if arc.edge:
            arc.edge.end = vertex
        if arc.prev:
            arc.prev.next = arc.next
        if arc.next:
            arc.next.prev = arc.prev

        self.check_circle_event(arc.prev)
        self.check_circle_event(arc.next)

    def create_breakpoints(self, site, arc):
        left_edge = Edge(arc.site)
        right_edge = Edge(site)
        left_edge.set_direction(site.x - arc.site.x, site.y - arc.site.y)
        right_edge.set_direction(arc.site.x - site.x, arc.site.y - site.y)
        self.edges.extend([left_edge, right_edge])
        return left_edge, right_edge


    # TODO: Fix logic here
    def get_arc_above(self, x):
        arc = self.beachline
        while arc:
            if arc.site.x < x < arc.site.x + 1: 
                return arc
            arc = arc.next
        return None

    def insert_arc_between(self, arc_left, arc_new):
        arc_right = arc_left.next
        arc_left.next = arc_new
        arc_new.prev = arc_left
        arc_new.next = arc_right
        if arc_right:
            arc_right.prev = arc_new

    # TODO: Check circle event event
    def check_circle_event(self, arc):
        if not arc:
            return
        arc.circle_event = None  

    def get_edges(self):
        return [(edge.start, edge.end) for edge in self.edges if edge.end]
