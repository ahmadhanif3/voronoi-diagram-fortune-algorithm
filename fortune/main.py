from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGraphicsView, QFileDialog
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from Canvas import Canvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.points = []
        self.circles = []
        self.showFullScreen()

        # Setup GUI
        widget = QWidget()
        layout = QHBoxLayout()
        layoutBtn = QVBoxLayout()
        layoutBtn.setAlignment(Qt.AlignVCenter)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.canvas = Canvas()
        self.view = QGraphicsView(self.canvas)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setFixedSize(1400, 1100)
        self.view.setMouseTracking(False)
        self.view.viewport().installEventFilter(self)
        layout.addWidget(self.view)

        # Setup Buttons
        self.calculateBtn = QPushButton("Calculate Voronoi")
        self.calculateBtn.clicked.connect(self.canvas.calculate)
        self.largestCircleBtn = QPushButton("Largest Circle")
        self.largestCircleBtn.clicked.connect(self.canvas.addCircle)
        self.fileBtn = QPushButton("Load Points")
        self.fileBtn.clicked.connect(self.loadPoints)
        self.clearBtn = QPushButton("Clear Canvas")
        self.clearBtn.clicked.connect(self.canvas.clearCanvas)
        layoutBtn.addWidget(self.calculateBtn)
        layoutBtn.addWidget(self.largestCircleBtn)
        layoutBtn.addWidget(self.fileBtn)
        layoutBtn.addWidget(self.clearBtn)
        layout.addLayout(layoutBtn)

    # Catch mouse button click
    def eventFilter(self, source, event):
        if event.type() == event.MouseButtonPress:
            pos = event.pos()
            p = self.view.mapToScene(pos)
            self.canvas.addPoint(p)
            return True
        return super().eventFilter(source, event)

    # Load points from files
    def loadPoints(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Points File", "", "Text Files (*.txt)")
        if filename:
            with open(filename, 'r') as file:
                self.canvas.loadPoints(file)

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
