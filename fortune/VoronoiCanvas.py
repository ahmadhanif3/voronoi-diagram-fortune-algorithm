from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor
import Voronoi

class VoronoiCanvas(QWidget):
    H = 1100

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
        if event.button() == Qt.LeftButton:
            self.addPoint(event.pos())

    def addPoint(self, pos):
        self.points.append(pos)
        self.update()

    def clearPoints(self):
        self.points.clear()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0), 10, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        for point in self.points:
            painter.drawPoint(point.x(), point.y())

    def onClickCalculate(self):
        """Calculate and draw the Voronoi diagram."""
        if not self.LOCK_FLAG:
            self.LOCK_FLAG = True

            vp = Voronoi(self.points)
            vp.process()
            lines = vp.get_output()
            self.drawLinesOnCanvas(lines)

    def loadPoints(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Points File", "", "Text Files (*.txt)")
        if filename:
            self.points.clear()
            with open(filename, 'r') as file:
                for line in file:
                    x, y = line.strip().split(',')
                    x, y = float(x), float(y)
                    self.scene.addEllipse(
                        x - self.RADIUS, y - self.RADIUS,
                        self.RADIUS * 2, self.RADIUS * 2,
                        QPen(Qt.black), Qt.black
                    )
                    self.points.append((x,y))
            self.update()