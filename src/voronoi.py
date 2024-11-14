import heapq
import itertools

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class CircleEvent:
  def __init__(self, x, point, arc):
    self.x = x
    self.point = point
    self.arc = arc
    self.valid = True

  def invalidate(self):
    self.valid = False

class Arc:
  def __init__(self, point, prev, next):
    self.point = point
    self.prev = prev
    self.next = next
    self.circle_event = None
    self.edge_left = None
    self.edge_right = None

class Edge:
  def __init__(self, start):
    self.start = start
    self.end = None
    self.flag = False

  def complete(self, end):
    if not self.flag:
       self.flag = True
       self.end = end

class SiteQueue:
  def __init__(self):
      self.queue = []
      self.point_set = set()  

  def push(self, point):
      p = (point.x, point.y)
      if p not in self.point_set:
          heapq.heappush(self.queue, (point.x, point.y, point))
          self.point_set.add(p)  

  def pop(self):
      _, _, point = heapq.heappop(self.queue)
      self.point_set.remove((point.x, point.y))  
      return point
  
  def peek(self):
    if self.queue:
        return self.queue[0][2]
    return None

  def not_empty(self):
      return len(self.queue) != 0

class CircleQueue:
    def __init__(self):
        self.queue = []
        self.entry_finder = {}
        self.REMOVED = '<removed>'
        self.counter = itertools.count()

    def push(self, event):
        if event in self.entry_finder:
            self.remove(event)
        count = next(self.counter)
        entry = [event.x, count, event]
        self.entry_finder[event] = entry
        heapq.heappush(self.queue, entry)

    def remove(self, event):
        entry = self.entry_finder.pop(event, None)
        if entry is not None:
            entry[-1] = self.REMOVED

    def pop(self):
        while self.queue:
            _, _, event = heapq.heappop(self.queue)
            if event is not self.REMOVED:
                del self.entry_finder[event]
                return event
        raise KeyError("pop from an empty priority queue")

    def peek(self):
        while self.queue:
            _, _, event = self.queue[0]
            if event is not self.REMOVED:
                return event
            heapq.heappop(self.queue) 
            del self.entry_finder[event]
        raise KeyError("peek from an empty priority queue")

    def not_empty(self):
        return any(entry[-1] != self.REMOVED for entry in self.queue) if self.queue else False

class Voronoi:
  def __init__(self, points):
    self.sites = SiteQueue()
    self.circles = CircleQueue()
    self.edges = []
    self.arc = None
    self.x0 = 0
    self.y0 = 0
    self.x1 = 1400
    self.y1 = 1100

    for point in points:
      p = Point(point.x(), point.y())
      self.sites.add(p)
    
  def process(self):
    while self.sites.not_empty():
      if self.circles.not_empty() and (self.circles.peek().x <= self.sites.peek().x):
        self.circle_iter()
      else:
        self.site_iter()

    while self.circles.not_empty():
      self.circle_iter()

    self.finish_edges()
  
  def site_iter():
    return

  def circle_iter():
    return
  
  def arc_insert():
    return
  
  def circle_event():
    return
  
  def circle():
    return
  
  def intersect():
    return
  
  def intersection():
    return
  
  def finish_edges():
    return
  
  def output():
    return
  