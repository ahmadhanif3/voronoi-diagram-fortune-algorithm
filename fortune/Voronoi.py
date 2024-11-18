import math
import heapq
from typing import Optional

class Point:
    """
    Represents a 2D point in the plane.
    
    Attributes:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return self.x < other.x

class Event:
    """
    Represents an event in Fortune's algorithm (site or circle).

    Attributes:
        x (float): The x-coordinate of the event.
        p (Optional[Point]): The point associated with the event (for site events).
        a (Optional[Arc]): The arc associated with the event (for circle events).
        valid (bool): Whether the event is valid.
    """
    def __init__(self, x: float, p: Optional[Point] = None, a=None, valid=True):
        self.x = x
        self.p = p
        self.a = a
        self.valid = valid

    def __lt__(self, other):
        return self.x < other.x

class Arc:
    """
    Represents a parabolic arc in the beachline.

    Attributes:
        p (Point): The focus point of the parabola.
        pprev (Optional[Arc]): The previous arc in the linked list.
        pnext (Optional[Arc]): The next arc in the linked list.
        s0 (Optional[Segment]): The left edge of the arc.
        s1 (Optional[Segment]): The right edge of the arc.
        e (Optional[Event]): The circle event associated with the arc.
    """
    def __init__(self, p, pprev=None, pnext=None):
        self.p = p  # site point
        self.pprev = pprev  # previous arc
        self.pnext = pnext  # next arc
        self.s0 = None  # left edge
        self.s1 = None  # right edge
        self.e = None  # circle event

class Segment:
    """
    Represents an edge of the Voronoi diagram.

    Attributes:
        start (Point): The starting point of the segment.
        end (Optional[Point]): The ending point of the segment.
    """
    def __init__(self, start):
        self.start = start
        self.end = None

    def finish(self, end):
        self.end = end

class Voronoi:
    def __init__(self, points):
        """Initializes the Voronoi diagram with a set of points."""
        self.output = []  # line segments
        self.circles = [] # store circles
        self.arc = None        
        self.points = []
        self.event = []
        
        for x, y in points:
            p = Point(x, y)
            heapq.heappush(self.points, (p.x, p))

        self.x0  = -100
        self.y0 = -100
        self.x1 = 1500
        self.y1 = 1200

    def process(self):
        """Processes all site and circle events to compute the Voronoi diagram."""
        # Process site and circle events
        while self.points:
            if self.event and self.event[0].x <= self.points[0][0]:
                self._process_event()
            else:
                self._process_point()
        
        # Process remaining circle events
        while self.event:
            self._process_event()
        
        self._finish_edges()

    def _process_point(self):
        """Processes a site event by adding a new arc to the beachline."""
        # Get next site event
        _, p = heapq.heappop(self.points)
        self._arc_insert(p)

    def _process_event(self):
        """Process the next circle event."""
        # Get the next circle event
        e = heapq.heappop(self.event)

        if e.valid:
            # Handle the valid circle event
            self._handle_valid_event(e)

    def _handle_valid_event(self, e):
        """Handle the logic for a valid circle event."""
        # Start a new edge and add it to the output
        new_segment = self._start_new_edge(e)

        # Remove the arc associated with the event and update neighbors
        arc = e.a
        self._remove_arc(arc, new_segment)

        # Finish the edges of the removed arc
        self._finish_arc_edges(arc, e)

        # Recheck circle events for neighboring arcs
        self._recheck_neighbors(arc, e)

    def _start_new_edge(self, e):
        """Start a new edge for the circle event."""
        segment = Segment(e.p)
        self.output.append(segment)
        return segment

    def _remove_arc(self, arc, new_segment):
        """Remove the arc associated with the event and update neighbor pointers."""
        if arc.pprev:
            arc.pprev.pnext = arc.pnext
            arc.pprev.s1 = new_segment
        if arc.pnext:
            arc.pnext.pprev = arc.pprev
            arc.pnext.s0 = new_segment

    def _finish_arc_edges(self, arc, e):
        """Finish the edges of the removed arc."""
        if arc.s0:
            arc.s0.finish(e.p)
        if arc.s1:
            arc.s1.finish(e.p)

    def _recheck_neighbors(self, arc, e):
        """Recheck circle events for the neighboring arcs."""
        if arc.pprev:
            self._check_circle_event(arc.pprev, e.x)
        if arc.pnext:
            self._check_circle_event(arc.pnext, e.x)

    def _arc_insert(self, p):
        if not self.arc:
            self.arc = Arc(p)
            return

        i = self.arc
        while i:
            flag, z = self._intersect(p, i)
            if flag:
                self._split_arc(i, p, z)
                return
            i = i.pnext

        self._append_arc_to_end(p)

    def _split_arc(self, arc, p, intersection_point):
        """Split an existing arc at the given point and add the new arc."""
        flag, zz = self._intersect(p, arc.pnext)
        if arc.pnext and not flag:
            arc.pnext.pprev = Arc(arc.p, arc, arc.pnext)
            arc.pnext = arc.pnext.pprev
        else:
            arc.pnext = Arc(arc.p, arc)
        arc.pnext.s1 = arc.s1

        arc.pnext.pprev = Arc(p, arc, arc.pnext)
        arc.pnext = arc.pnext.pprev

        arc = arc.pnext

        # Add new half-edges
        self._add_new_segments(arc, intersection_point)

        # Check for new circle events
        self._check_new_circle_events(arc, p.x)

    def _add_new_segments(self, arc, intersection_point):
        """Add new segments for the split arcs."""
        seg1 = Segment(intersection_point)
        self.output.append(seg1)
        arc.pprev.s1 = arc.s0 = seg1

        seg2 = Segment(intersection_point)
        self.output.append(seg2)
        arc.pnext.s0 = arc.s1 = seg2

    def _check_new_circle_events(self, arc, x):
        """Check for new circle events for the split arcs."""
        self._check_circle_event(arc, x)
        self._check_circle_event(arc.pprev, x)
        self._check_circle_event(arc.pnext, x)

    def _append_arc_to_end(self, p):
        """Append a new arc to the end of the arc list."""
        i = self.arc
        while i.pnext:
            i = i.pnext
        i.pnext = Arc(p, i)

        x = self.x0
        y = (i.pnext.p.y + i.p.y) / 2.0
        start = Point(x, y)

        seg = Segment(start)
        i.s1 = i.pnext.s0 = seg
        self.output.append(seg)

    def _check_circle_event(self, i, x0):
        # Remove previous invalid event
        if i.e and i.e.x != self.x0:
            i.e.valid = False
        i.e = None

        if not i.pprev or not i.pnext:
            return

        flag, x, o = self._circle(i.pprev.p, i.p, i.pnext.p)
        if flag and x > self.x0:
            i.e = Event(x, o, i)
            heapq.heappush(self.event, i.e)

    def _circle(self, a, b, c):
        # Check right turn
        if ((b.x - a.x)*(c.y - a.y) - (c.x - a.x)*(b.y - a.y)) > 0:
            return False, None, None

        # Compute circumcircle
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A*(a.x + b.x) + B*(a.y + b.y)
        F = C*(a.x + c.x) + D*(a.y + c.y)
        G = 2*(A*(c.y - b.y) - B*(c.x - b.x))

        if G == 0:
            return False, None, None

        # Circle center
        ox = 1.0 * (D*E - B*F) / G
        oy = 1.0 * (A*F - C*E) / G
        radius = math.sqrt((a.x - ox) ** 2 + (a.y - oy) ** 2)
        x = ox + radius
        o = Point(ox, oy)

        if self._check_circle_empty(ox, oy, radius):
            self.circles.append((ox, oy, radius)) 
           
        return True, x, o
        
    def _intersect(self, p, i):
        if not i or i.p.x == p.x:
            return False, None

        a = b = 0.0

        if i.pprev:
            a = self._intersection(i.pprev.p, i.p, 1.0*p.x).y
        if i.pnext:
            b = self._intersection(i.p, i.pnext.p, 1.0*p.x).y

        if ((not i.pprev or a <= p.y) and (not i.pnext or p.y <= b)):
            py = p.y
            px = 1.0 * ((i.p.x)**2 + (i.p.y-py)**2 - p.x**2) / (2*i.p.x - 2*p.x)
            res = Point(px, py)
            return True, res
        return False, None

    def _intersection(self, p0, p1, l):
        """Compute the intersection of two parabolas."""
        if p0.x == p1.x:
            return self._handle_vertical_parabolas(p0, p1, l)
        if p1.x == l:
            return Point(p1.x, p1.y)  # p1 lies on the directrix
        if p0.x == l:
            return Point(p0.x, p0.y)  # p0 lies on the directrix

        # General case: Use quadratic formula
        return self._solve_quadratic_intersection(p0, p1, l)

    def _handle_vertical_parabolas(self, p0, p1, l):
        """Handle the special case where parabolas are vertically aligned."""
        py = (p0.y + p1.y) / 2.0
        px = self._compute_px(p0, py, l)
        return Point(px, py)

    def _solve_quadratic_intersection(self, p0, p1, l):
        """Solve the intersection using the quadratic formula"""
        z0 = 2.0 * (p0.x - l)
        z1 = 2.0 * (p1.x - l)

        a = 1.0 / z0 - 1.0 / z1
        b = -2.0 * (p0.y / z0 - p1.y / z1)
        c = (
            (p0.y**2 + p0.x**2 - l**2) / z0
            - (p1.y**2 + p1.x**2 - l**2) / z1
        )

        py = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
        px = self._compute_px(p0, py, l)
        return Point(px, py)

    def _compute_px(self, p, py, l):
        """Compute the x-coordinate of the intersection"""
        return (p.x**2 + (p.y - py)**2 - l**2) / (2 * p.x - 2 * l)

    def _finish_edges(self):
        """Finishes the edges of a removed arc."""
        l = self.x1 + (self.x1 - self.x0) + (self.y1 - self.y0)
        i = self.arc
        while i.pnext:
            if i.s1:
                p = self._intersection(i.p, i.pnext.p, l*2.0)
                i.s1.finish(p)
            i = i.pnext

    def _check_circle_empty(self, ox, oy, radius):
        """Check if the circle is empty (contains no points)."""
        for _, point in self.points:
            distance = math.sqrt((point.x - ox) ** 2 + (point.y - oy) ** 2)
            if distance <= radius:
                return False
        return True 

    def get_output(self):
        """Retrieves the results of the Voronoi diagram computation."""
        res = []
        for o in self.output:
            if o.start and o.end:
                res.append((o.start.x, o.start.y, o.end.x, o.end.y))
        return res, self.circles