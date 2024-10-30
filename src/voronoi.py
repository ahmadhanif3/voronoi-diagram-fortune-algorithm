from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor

class VoronoiCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.setObjectName("VoronoiCanvas")
        self.setStyleSheet("""
            #VoronoiCanvas {
                background-color: #ffffff;  
                border: 5px solid #000000; 
            }
        """)
        self.setMaximumSize(1400, 1100)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # Ensure the left button is pressed
            self.addPoint(event.pos())

    def addPoint(self, pos):
        """Adds a point at the specified position."""
        self.points.append(pos)
        self.update()

    def loadPoints(self):
        """Opens a file dialog to select and load points from a text file."""
        filename, _ = QFileDialog.getOpenFileName(self, "Open Points File", "", "Text Files (*.txt)")
        if filename:
            self.points.clear()
            with open(filename, 'r') as file:
                for line in file:
                    x, y = line.strip().split(',')
                    self.points.append(QPoint(int(x), int(y)))
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0), 10, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        for point in self.points:
            painter.drawPoint(point.x(), point.y())