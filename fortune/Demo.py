from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPointF
from Voronoi import Voronoi


class MainWindow(QMainWindow):
    # radius of drawn points on canvas
    RADIUS = 3

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voronoi Diagram")
        self.setGeometry(100, 100, 600, 600)

        # State variables
        self.points = []
        self.LOCK_FLAG = False

        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Canvas setup
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        main_layout.addWidget(self.view)

        # Buttons
        self.btnCalculate = QPushButton("Calculate")
        self.btnCalculate.clicked.connect(self.onClickCalculate)
        main_layout.addWidget(self.btnCalculate)

        self.btnClear = QPushButton("Clear")
        self.btnClear.clicked.connect(self.onClickClear)
        main_layout.addWidget(self.btnClear)

        # Mouse event handling
        self.view.setMouseTracking(True)
        self.view.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        """Handle mouse events on the canvas."""
        if event.type() == event.MouseButtonDblClick and not self.LOCK_FLAG:
            if source == self.view.viewport():
                pos = event.pos()
                scene_pos = self.view.mapToScene(pos)
                self.addPoint(scene_pos)
        return super().eventFilter(source, event)

    def addPoint(self, point):
        """Add a point to the canvas."""
        self.scene.addEllipse(
            point.x() - self.RADIUS, point.y() - self.RADIUS,
            self.RADIUS * 2, self.RADIUS * 2,
            QPen(Qt.black), Qt.black
        )
        self.points.append((point.x(), point.y()))

    def onClickCalculate(self):
        """Calculate and draw the Voronoi diagram."""
        if not self.LOCK_FLAG:
            self.LOCK_FLAG = True

            vp = Voronoi(self.points)
            vp.process()
            lines = vp.get_output()
            self.drawLinesOnCanvas(lines)
            
            print(lines)

    def onClickClear(self):
        """Clear the canvas and reset."""
        self.LOCK_FLAG = False
        self.scene.clear()
        self.points = []

    def drawLinesOnCanvas(self, lines):
        """Draw Voronoi edges on the canvas."""
        pen = QPen(Qt.blue)
        for line in lines:
            self.scene.addLine(line[0], line[1], line[2], line[3], pen)


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
