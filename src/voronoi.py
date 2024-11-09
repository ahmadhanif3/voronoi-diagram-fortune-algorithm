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

  def is_empty(self):
      return len(self.queue) == 0

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

    def is_empty(self):
        return not self.queue or all(entry[-1] == self.REMOVED for entry in self.queue)



class Voronoi:
  def __init__(self, points):
    self.sites = SiteQueue()
    self.circles = CircleQueue()
    self.lines = []
    self.arc = None

    for point in points:
      p = Point(point.x(), point.y())
      self.sites.add(p)
    
    for point in self.sites:
      print(f"{point.x}, {point.y}")