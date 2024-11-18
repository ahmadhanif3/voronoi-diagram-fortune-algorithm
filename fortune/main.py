from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QGraphicsScene, QGraphicsView, QFileDialog
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPointF
from Voronoi import Voronoi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.points = []
        self.circles = []
        self.showFullScreen()

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Canvas setup
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setFixedSize(1400, 1100)
        self.scene.setSceneRect(0, 0, 1300, 1000) 
        main_layout.addWidget(self.view)

        # Buttons
        self.btnCalculate = QPushButton("Calculate Voronoi")
        self.btnCalculate.clicked.connect(self.calculate)
        main_layout.addWidget(self.btnCalculate)

        self.btnLargestCircle = QPushButton("Largest Circle")
        self.btnLargestCircle.clicked.connect(self.largestCircle)
        main_layout.addWidget(self.btnLargestCircle)

        self.btnLoad = QPushButton("Load Points")
        self.btnLoad.clicked.connect(self.loadPoints)
        main_layout.addWidget(self.btnLoad)

        self.btnClear = QPushButton("Clear Canvas")
        self.btnClear.clicked.connect(self.clear)
        main_layout.addWidget(self.btnClear)

        self.view.setMouseTracking(False)
        self.view.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == event.MouseButtonPress:
            pos = event.pos()
            scene_pos = self.view.mapToScene(pos)
            self.addPoint(scene_pos)
            return True
        return super().eventFilter(source, event)
    
    def loadPoints(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Points File", "", "Text Files (*.txt)")
        if filename:
            with open(filename, 'r') as file:
                for line in file:
                    x, y = line.strip().split(',')
                    x, y = float(x), 1100-float(y)
                    self.addPoint(QPointF(x, y))

    def addPoint(self, point):
        self.scene.addEllipse(point.x()-5, point.y()-5, 10, 10, QPen(Qt.black), Qt.black)
        self.points.append((point.x(), point.y()))

    def calculate(self):
        self.scene.clear()
        for x, y in self.points:
            self.scene.addEllipse(x-5, y-5, 10, 10, QPen(Qt.black), Qt.black)
        voronoi = Voronoi(self.points)
        voronoi.process()
        temp = voronoi.get_output()
        edges = temp[0]
        self.circles = temp[1] 
        self.drawEdges(edges)

    def largestCircle(self):
        if not self.circles:
            return

        largest_circle = max(self.circles, key=lambda c: c[2])
        cx, cy, radius = largest_circle

        pen = QPen(Qt.blue)
        self.scene.addEllipse(
            cx - radius, cy - radius,
            2 * radius, 2 * radius,
            pen
        )

    def clear(self):
        self.scene.clear()
        self.points = []

    def drawEdges(self, edges):
        for edge in edges:
            self.scene.addLine(edge[0], edge[1], edge[2], edge[3], QPen(Qt.red))


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()