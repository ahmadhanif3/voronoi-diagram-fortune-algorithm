import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QFileDialog)
from PyQt5.QtCore import Qt, QPoint
from voronoiCanvas import VoronoiCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Voronoi Diagram with Fortune's Algorithm")
        self.showFullScreen()

        #Window Controls
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

        #Canvas
        self.canvas = VoronoiCanvas()
        canvasLayout = QVBoxLayout()
        canvasLayout.addWidget(self.canvas)

        #Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)

        #Input Controls
        inputLayout = QVBoxLayout()
        self.inputLabel = QLabel("Enter seed point coordinates or load from a file:")
        self.loadButton = QPushButton("Load Points from File")
        self.loadButton.clicked.connect(self.canvas.loadPoints)
        self.clearButton = QPushButton("Clear Points")
        self.clearButton.clicked.connect(self.canvas.clearPoints)
        self.computeButton = QPushButton("Compute Voronoi Diagram")
        self.computeButton.clicked.connect(self.canvas.computeVoronoi)
        self.infoXLabel = QLabel("X axis maximum coordinate: 1400")
        self.infoYLabel = QLabel("Y axis maximum coordinate: 1100")

        inputLayout.addWidget(self.inputLabel)
        inputLayout.addWidget(self.loadButton)
        inputLayout.addWidget(self.clearButton)
        inputLayout.addWidget(self.computeButton)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
