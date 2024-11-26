from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt, QPointF
from Voronoi import Voronoi


class Canvas(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.points = []
        self.circles = []
        self.setSceneRect(0, 0, 1300, 1000)

    def addPoint(self, point):
        """Add a point"""
        self.addEllipse(point.x()-5, point.y()-5, 10, 10, QPen(Qt.black), Qt.black)
        self.points.append((point.x(), point.y()))

    def drawEdges(self, edges):
        """Draw edges of voronoi """
        for edge in edges:
            self.addLine(edge[0], edge[1], edge[2], edge[3], QPen(Qt.red))

    def clearCanvas(self):
        """Clear the canvas"""
        self.clear()
        self.points = []
        self.circles = []

    def loadPoints(self, file):
        """Load points from file"""
        for line in file:
            x, y = line.strip().split(',')
            x, y = float(x),1000 - float(y)
            self.addPoint(QPointF(x, y))
    
    def addCircle(self):
        """Draw largest empty circle"""
        if not self.circles:
            return
        list_largest_circle = []

        largest_circle = max(self.circles, key=lambda c: c[2])
        for circle in self.circles:
            if circle[2] == largest_circle[2]:
                list_largest_circle.append(circle)

        for largest_circle in list_largest_circle:
            cx, cy, radius = largest_circle

            pen = QPen(Qt.blue)
            self.addEllipse(
                cx - radius, cy - radius,
                2 * radius, 2 * radius,
                pen
            )

    def removeDuplicatesPoints(self):
        """Remove duplicate points"""
        temp_points = []
        for point in self.points:
            if point not in temp_points:
                temp_points.append(point)
        self.points = temp_points

    def calculate(self):
        """Calculate voronoi"""
        if self.points:
            self.clear()
            self.removeDuplicatesPoints()
            for x, y in self.points:
                self.addEllipse(x-5, y-5, 10, 10, QPen(Qt.black), Qt.black)
            voronoi = Voronoi(self.points)
            voronoi.process()
            temp = voronoi.get_output()
            edges = temp[0]
            self.circles = temp[1] 
            self.drawEdges(edges)