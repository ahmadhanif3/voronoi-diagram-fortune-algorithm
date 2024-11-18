import math
import heapq
from typing import List, Tuple, Optional

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return self.x < other.x

class Event:
    def __init__(self, x: float, p: Optional[Point] = None, a=None, valid=True):
        self.x = x
        self.p = p
        self.a = a
        self.valid = valid

    def __lt__(self, other):
        return self.x < other.x

class Arc:
    def __init__(self, p, pprev=None, pnext=None):
        self.p = p  # site point
        self.pprev = pprev  # previous arc
        self.pnext = pnext  # next arc
        self.s0 = None  # left edge
        self.s1 = None  # right edge
        self.e = None  # circle event

class Segment:
    def __init__(self, start):
        self.start = start
        self.end = None

    def finish(self, end):
        self.end = end

class VoronoiDiagram:
    def __init__(self, points):
        self.output = []  # line segments
        self.circles = [] # store circles
        self.arc = None        
        self.points = []
        self.event = []
        
        # Insert points
        for x, y in points:
            p = Point(x, y)
            heapq.heappush(self.points, (p.x, p))

        # Bounding box
        self.x0  = -100
        self.y0 = -100
        self.x1 = 1500
        self.y1 = 1200
        
        # Add margins to bounding box
        dx = (self.x1 - self.x0 + 1) / 5.0
        dy = (self.y1 - self.y0 + 1) / 5.0

    def process(self):
        # Process site and circle events
        while self.points:
            if self.event and self.event[0].x <= self.points[0][0]:
                self.process_event()
            else:
                self.process_point()
        
        # Process remaining circle events
        while self.event:
            self.process_event()
        
        self.finish_edges()

    def process_point(self):
        # Get next site event
        _, p = heapq.heappop(self.points)
        self.arc_insert(p)

    def process_event(self):
        # Get next circle event
        e = heapq.heappop(self.event)
        
        if e.valid:
            # Start new edge
            s = Segment(e.p)
            self.output.append(s)

            # Remove associated arc
            a = e.a
            if a.pprev:
                a.pprev.pnext = a.pnext
                a.pprev.s1 = s
            if a.pnext:
                a.pnext.pprev = a.pprev
                a.pnext.s0 = s

            # Finish edges
            if a.s0: a.s0.finish(e.p)
            if a.s1: a.s1.finish(e.p)

            # Recheck circle events
            if a.pprev: self.check_circle_event(a.pprev, e.x)
            if a.pnext: self.check_circle_event(a.pnext, e.x)

    def arc_insert(self, p):
        if not self.arc:
            self.arc = Arc(p)
            return

        # Find arc to split
        i = self.arc
        while i:
            flag, z = self.intersect(p, i)
            if flag:
                # Split existing arc
                flag, zz = self.intersect(p, i.pnext)
                if i.pnext and not flag:
                    i.pnext.pprev = Arc(i.p, i, i.pnext)
                    i.pnext = i.pnext.pprev
                else:
                    i.pnext = Arc(i.p, i)
                i.pnext.s1 = i.s1

                # Add new arc
                i.pnext.pprev = Arc(p, i, i.pnext)
                i.pnext = i.pnext.pprev

                i = i.pnext

                # Add new half-edges
                seg = Segment(z)
                self.output.append(seg)
                i.pprev.s1 = i.s0 = seg

                seg = Segment(z)
                self.output.append(seg)
                i.pnext.s0 = i.s1 = seg

                # Check for new circle events
                self.check_circle_event(i, p.x)
                self.check_circle_event(i.pprev, p.x)
                self.check_circle_event(i.pnext, p.x)
                return
            
            i = i.pnext

        # Append to end of arc list
        i = self.arc
        while i.pnext:
            i = i.pnext
        i.pnext = Arc(p, i)
        
        # Insert new segment
        x = self.x0
        y = (i.pnext.p.y + i.p.y) / 2.0
        start = Point(x, y)

        seg = Segment(start)
        i.s1 = i.pnext.s0 = seg
        self.output.append(seg)

    def check_circle_event(self, i, x0):
        # Remove previous invalid event
        if i.e and i.e.x != self.x0:
            i.e.valid = False
        i.e = None

        if not i.pprev or not i.pnext:
            return

        flag, x, o = self.circle(i.pprev.p, i.p, i.pnext.p)
        if flag and x > self.x0:
            i.e = Event(x, o, i)
            heapq.heappush(self.event, i.e)

    def circle(self, a, b, c):
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

        self.circles.append((ox, oy, radius))
           
        return True, x, o
        
    def intersect(self, p, i):
        if not i or i.p.x == p.x:
            return False, None

        a = b = 0.0

        if i.pprev:
            a = self.intersection(i.pprev.p, i.p, 1.0*p.x).y
        if i.pnext:
            b = self.intersection(i.p, i.pnext.p, 1.0*p.x).y

        if ((not i.pprev or a <= p.y) and (not i.pnext or p.y <= b)):
            py = p.y
            px = 1.0 * ((i.p.x)**2 + (i.p.y-py)**2 - p.x**2) / (2*i.p.x - 2*p.x)
            res = Point(px, py)
            return True, res
        return False, None

    def intersection(self, p0, p1, l):
        # Compute parabola intersection
        p = p0
        if p0.x == p1.x:
            py = (p0.y + p1.y) / 2.0
        elif p1.x == l:
            py = p1.y
        elif p0.x == l:
            py = p0.y
            p = p1
        else:
            # Quadratic formula
            z0 = 2.0 * (p0.x - l)
            z1 = 2.0 * (p1.x - l)

            a = 1.0/z0 - 1.0/z1
            b = -2.0 * (p0.y/z0 - p1.y/z1)
            c = 1.0 * (p0.y**2 + p0.x**2 - l**2) / z0 - 1.0 * (p1.y**2 + p1.x**2 - l**2) / z1

            py = 1.0 * (-b-math.sqrt(b*b - 4*a*c)) / (2*a)
            
        px = 1.0 * (p.x**2 + (p.y-py)**2 - l**2) / (2*p.x-2*l)
        res = Point(px, py)
        return res

    def finish_edges(self):
        l = self.x1 + (self.x1 - self.x0) + (self.y1 - self.y0)
        i = self.arc
        while i.pnext:
            if i.s1:
                p = self.intersection(i.p, i.pnext.p, l*2.0)
                i.s1.finish(p)
            i = i.pnext

    def get_output(self):
        res = []
        for o in self.output:
            if o.start and o.end:
                res.append((o.start.x, o.start.y, o.end.x, o.end.y))
        return res, self.circles

def generate_voronoi(points):
    """Generate Voronoi diagram for given points"""
    voronoi = VoronoiDiagram(points)
    voronoi.process()
    return voronoi.get_output()