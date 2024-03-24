import sys
from PIL import Image
import numpy as np
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
    QGraphicsPixmapItem,
)
from PySide6.QtGui import QPixmap, QColor, QKeyEvent, QMouseEvent, QPainter
from PySide6.QtCore import Qt


class RGB:
    def __init__(self, rgb=(0, 0, 0)) -> None:
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]

    def toQColor(self):
        return QColor(self.red, self.green, self.blue)


def toIntPos(pos):
    return (int(pos.x()), int(pos.y()))


def setPalette(palette: np.ndarray, dial):
    for i in range(palette.size):
        color: RGB = palette[i]
        dial.setCustomColor(i, color.toQColor())


def readPalette(path):
    image = Image.open(path)
    rgbim = image.convert("RGB")
    pixdict = {}
    for y in range(rgbim.size[1]):
        for x in range(rgbim.size[0]):
            pixdict[rgbim.getpixel((x, y))] = True
    pixlist = []
    for rgb in pixdict:
        pixlist.append(RGB(rgb))
    return np.array(pixlist)


class PixmapItem(QGraphicsPixmapItem):
    def __init__(self, w=16, h=16, rgb=RGB()):
        super().__init__()
        pixmap = QPixmap(w, h)
        pixmap.fill(rgb.toQColor())
        self.setPixmap(pixmap)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            # Emit custom signal for left-click event
            print(toIntPos(event.pos()))


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.scene = QGraphicsScene()
        # scene.addText("Hello, world!")
        self.pixmap = PixmapItem()
        self.clrpalette = readPalette("palettes/steam-lords-1x.png")
        self.palpix = PixmapItem(self.clrpalette.size)
        self.palpainter = QPainter(self.palpix.pixmap())
        for i in range(self.clrpalette.size):
            self.palpainter.setPen(self.clrpalette[i].toQColor())
            self.palpainter.drawPoint(i, 0)
        self.scene.addItem(self.pixmap)
        self.scene.addItem(self.clrpalette)
        self.view = QGraphicsView(self.scene)
        self.view.scale(24, 24)
        self.setCentralWidget(self.view)
        self.resize(512, 512)

    def keyPressEvent(self, event: QKeyEvent):
        pass


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
