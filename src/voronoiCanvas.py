from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor
from voronoiIncremental2 import Voronoi

class VoronoiCanvas(QWidget):
    H = 1100

    def __init__(self):
        super().__init__()
        self.points = []
        self.edges = []
        self.circles = []
        self.setObjectName("VoronoiCanvas")
        self.setStyleSheet("""
            #VoronoiCanvas {
                background-color: #ffffff;  
                border: 5px solid #000000; 
            }
        """)
        self.setMaximumSize(1400, 1100)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.addPoint(event.pos())

    def addPoint(self, pos):
        self.points.append(pos)
        self.update()

    def addCircle(self, center, radius):
        self.circles.append((center, radius))
        self.update()

    def clearPoints(self):
        self.points.clear()
        self.edges.clear()
        self.circles.clear()
        self.update()

    def loadPoints(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Points File", "", "Text Files (*.txt)")
        if filename:
            self.points.clear()
            with open(filename, 'r') as file:
                for line in file:
                    x, y = line.strip().split(',')
                    self.points.append(QPoint(int(x), 1100-int(y)))
            self.update()

    def paintEvent(self, event):
        """Render the points and Voronoi diagram."""
        painter = QPainter(self)

        # Draw seed points
        pen = QPen(QColor(0, 0, 0), 10, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        for point in self.points:
            painter.drawPoint(point.x(), point.y())

        # Draw edges
        if self.edges:
            pen = QPen(QColor(255, 0, 0), 2, Qt.SolidLine)
            painter.setPen(pen)
            for edge in self.edges:
                p1, p2 = edge
                painter.drawLine(
                    int(p1[0]), int(self.H - p1[1]),  # Flip y-axis for drawing
                    int(p2[0]), int(self.H - p2[1])
                )
        
        # Draw circle (update when voronoi algorithm is done)
        for center, radius in self.circles:
            pen = QPen(QColor(21, 171, 31), 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawEllipse(center, radius, radius)

        painter.end()

    def computeVoronoi(self):
        """Compute the Voronoi diagram."""
        if len(self.points) < 2:
            return  # Not enough points to compute the diagram

        # Convert QPoint objects to tuples
        point_list = [(p.x(), self.H - p.y()) for p in self.points]

        # Instantiate and compute the Voronoi diagram
        voronoi = Voronoi(point_list)
        self.edges = voronoi.compute_diagram()  # Get the edges
        self.update()
