import heapq

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class SweepQueue:
  def __init__(self):
    self.queue = []

  def add(self, i):
    return


class Voronoi:
  def __init__(self, points):
    self.points = SweepQueue()

    for point in points:
      p = Point(point.x(), point.y())
      self.points.add(p)
    
    for point in self.points:
      print(f"{point.x}, {point.y}")