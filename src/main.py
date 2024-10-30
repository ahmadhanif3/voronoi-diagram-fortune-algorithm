import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QFileDialog)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QMouseEvent

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
        self.points.append(event.pos())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0), 10, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        for point in self.points:
            painter.drawPoint(point.x(), point.y())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Voronoi Diagram with Fortune's Algorithm")
        self.showFullScreen()

        self.minimizeButton = QPushButton("-")
        self.exitButton = QPushButton("x")
        self.minimizeButton.clicked.connect(self.showMinimized)
        self.exitButton.clicked.connect(self.close)
        self.minimizeButton.setFixedSize(30, 30)
        self.exitButton.setFixedSize(30, 30)

        windowControls = QHBoxLayout()
        windowControls.addWidget(self.minimizeButton)
        windowControls.addWidget(self.exitButton)
        windowControls.setAlignment(Qt.AlignTop | Qt.AlignRight)

        mainLayout = QHBoxLayout()

        self.canvas = VoronoiCanvas()
        canvasLayout = QVBoxLayout()
        canvasLayout.addWidget(self.canvas)

        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)

        inputLayout = QVBoxLayout()
        self.inputLabel = QLabel("Enter seed point coordinates or load from a file:")
        self.loadButton = QPushButton("Load Points from File")
        self.loadButton.clicked.connect(self.loadPoints)
        self.infoXLabel = QLabel("X axis maximum coordinate: 1400")
        self.infoYLabel = QLabel("Y axis maximum coordinate: 1100")

        inputLayout.addWidget(self.inputLabel)
        inputLayout.addWidget(self.loadButton)
        inputLayout.addWidget(self.infoXLabel)
        inputLayout.addWidget(self.infoYLabel)
        inputLayout.addStretch()

        mainLayout.addLayout(canvasLayout, 4)
        mainLayout.addWidget(separator)
        mainLayout.addLayout(inputLayout, 1)

        centralWidget = QWidget()
        centralFrame = QVBoxLayout(centralWidget)
        centralFrame.addLayout(windowControls)
        centralFrame.addLayout(mainLayout)

        self.setCentralWidget(centralWidget)

    def loadPoints(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Points File", "", "Text Files (*.txt)")
        if filename:
            with open(filename, 'r') as file:
                self.canvas.points.clear()
                for line in file:
                    x, y = line.strip().split(',')
                    self.canvas.points.append(QPoint(int(x), int(y)))
                self.canvas.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
