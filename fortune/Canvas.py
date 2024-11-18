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

    # Add a point
    def addPoint(self, point):
        self.addEllipse(point.x()-5, point.y()-5, 10, 10, QPen(Qt.black), Qt.black)
        self.points.append((point.x(), point.y()))

    # Draw edges of voronoi 
    def drawEdges(self, edges):
        for edge in edges:
            self.addLine(edge[0], edge[1], edge[2], edge[3], QPen(Qt.red))

    # Clear the canvas
    def clearCanvas(self):
        self.clear()
        self.points = []

    # Load points from file
    def loadPoints(self, file):
        for line in file:
            x, y = line.strip().split(',')
            x, y = float(x), 1100-float(y)
            self.addPoint(QPointF(x, y))
    
    # Draw largest empty circle
    def addCircle(self):
        if not self.circles:
            return

        largest_circle = max(self.circles, key=lambda c: c[2])
        cx, cy, radius = largest_circle

        pen = QPen(Qt.blue)
        self.addEllipse(
            cx - radius, cy - radius,
            2 * radius, 2 * radius,
            pen
        )

    # Calculate voronoi
    def calculate(self):
        if self.points:
            self.clear()
            for x, y in self.points:
                self.addEllipse(x-5, y-5, 10, 10, QPen(Qt.black), Qt.black)
            voronoi = Voronoi(self.points)
            voronoi.process()
            temp = voronoi.get_output()
            edges = temp[0]
            self.circles = temp[1] 
            self.drawEdges(edges)