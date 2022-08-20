import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication

from q_watch.cartesian_tools import circular_coordinates


class QWatch(QtWidgets.QWidget):
    date_change = QtCore.pyqtSignal(bool)
    meridian_change = QtCore.pyqtSignal(str)

    # noinspection PyMissingConstructor
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        self.internal_properties()
        self.indicator()

    def internal_properties(self):
        self.setMinimumSize(200, 200)

    def pixmap_verification(self):
        self.panel = QPixmap(self.rect().size())
        return self.panel.isNull()

    def indicator(self):
        self.panel = None
        self.CENTER = None
        self.max_window_length = 0
        self.min_window_length = 0

        self.sec = self.min = 59
        self.hr = 11
        self.hr_24 = 11

        self.__Abort__ = self.pixmap_verification()

    def __center(self):
        center_x = self.size().width() / 2
        center_y = self.size().height() / 2

        if center_x > center_y:
            self.max_window_length = self.size().width()
            self.min_window_length = self.size().height()

        else:
            self.max_window_length = self.size().height()
            self.min_window_length = self.size().width()

        return center_x, center_y

    def paintEvent(self, event):
        self.__beginning__()

    def __beginning__(self):
        if self.__Abort__:
            return

        self.CENTER = self.__center()
        # background color
        self.panel.fill(QtGui.QColor('#2f4f4f'))
        # create panel
        paint = QPainter(self)
        paint.drawPixmap(0, 0, self.panel)
        self.drawContent(paint)

    # noinspection PyPep8Naming
    def drawContent(self, paint):
        paint.setRenderHint(QPainter.Antialiasing, True)
        self._drawClockOutline(paint)
        self._drawHand(paint, self.min_window_length * .35, self.sec, 60, 2, '#e6faf0')
        self._drawHand(paint, self.min_window_length * .30, self.min, 60, 5, '#e6faf0')
        self._drawHand(paint, self.min_window_length * .20, self.hr, 12, 7, '#a2b3ab')

    def resizeEvent(self, event):
        # redraw on window resize
        self.__reset__()

    def __reset__(self):
        if self.__Abort__:
            return

        del self.panel
        self.panel = None
        self.__Abort__ = self.pixmap_verification()
        self.__Recalculate__ = True

    def __center_dimension(self, watch_size):
        size_x = self.size().width()
        size_y = self.size().height()
        return QRectF((size_x - watch_size) / 2, (size_y - watch_size) / 2, watch_size, watch_size)

    def _drawClockOutline(self, paint):
        Pen = QtGui.QPen()
        Pen.setWidth(3)
        Pen.setColor(QtGui.QColor('#a9aac2'))
        paint.setPen(Pen)
        paint.drawEllipse(self.__center_dimension(self.min_window_length - 20))
        self.__minute_second(paint)

    def __minute_second(self, paint):
        Pen = paint.pen()
        Pen.setColor(QtGui.QColor('#ffadad'))
        paint.setPen(Pen)

        for i in range(60):
            p1 = circular_coordinates(self.CENTER, self.min_window_length * .45, 60, i)
            p2 = circular_coordinates(self.CENTER, self.min_window_length * .44, 60, i)
            paint.drawLine(QPointF(p1['x'], p1['y']), QPointF(p2['x'], p2['y']))

        Pen.setColor(QtGui.QColor('#9bf6ff'))
        paint.setPen(Pen)

        for i in range(12):
            p1 = circular_coordinates(self.CENTER, self.min_window_length * .45, 12, i)
            p2 = circular_coordinates(self.CENTER, self.min_window_length * .40, 12, i)
            p3 = circular_coordinates(self.CENTER, self.min_window_length * .35, 12, i, 'time')
            paint.drawLine(QPointF(p1['x'], p1['y']), QPointF(p2['x'], p2['y']))
            paint.drawText(QPointF(p3['x'] - 3, p3['y'] + 3), str(i + 1))

    # noinspection PyPep8Naming,PyMethodMayBeStatic
    def _drawHand(self, paint, length, time_unit, cycles, thickness=1, color='#000000'):
        Pen = paint.pen()
        Pen.setWidth(thickness)
        Pen.setCapStyle(QtCore.Qt.RoundCap)
        Pen.setColor(QtGui.QColor(color))
        paint.setPen(Pen)

        XY = circular_coordinates(self.CENTER, length, cycles, time_unit, 'time')
        coor_XY = QPointF(XY['x'], XY['y'])
        paint.drawLine(QPointF(self.CENTER[0], self.CENTER[1]), coor_XY)

    def RunTime(self):
        self.UpdateSec(self.sec + 2)

    def UpdateSec(self, sec):
        self.sec = sec - 1

        if self.sec > 59:
            self.sec = 0
            self.UpdateMin(self.min + 2)

        else:
            self.update()

    # noinspection PyShadowingBuiltins
    def UpdateMin(self, min):
        self.min = min - 1

        if self.min > 59:
            self.min = 0
            self.updateHr(self.hr + 2)

        else:
            self.update()

    def updateHr(self, hr):
        self.hr_24 = hr - 1

        if self.hr_24 > 23:
            self.hr_24 = 0
            self.date_change.emit(True)
            self.meridian_change.emit('AM')

        if self.hr_24 > 11:
            self.hr = self.hr_24 - 12
            self.meridian_change.emit('PM')

        else:
            self.hr = self.hr_24

        self.update()

    def UpdateFullTime(self, Hr, Min, Sec):
        self.hr_24 = Hr - 1

        if self.hr_24 > 11:
            self.hr = self.hr_24 -12
            self.meridian_change.emit('PM')

        else:
            self.hr = self.hr_24
            self.meridian_change.emit('AM')

        self.min = Min - 1
        self.sec = int(Sec) - 1
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = QWatch()
    v.UpdateFullTime(12, 17, 37)
    v.show()
    sys.exit(app.exec())
