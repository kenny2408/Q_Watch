import sys
from datetime import datetime

import pytz
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QButtonGroup, QLabel, QHBoxLayout, QVBoxLayout, QApplication

from q_watch.qt_watch import QWatch


class MainWindow(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        self.internal_pity()
        self.initiator()
        self.styles()
        self.structure()
        self.connections()
        self.update_date_time()
        self.start()

    def internal_pity(self):
        self.setMinimumSize(250, 250)

    # noinspection PyAttributeOutsideInit
    def initiator(self):
        self.button_local = QPushButton('Local')
        self.button_bogota = QPushButton('Bogotá')
        self.button_caracas = QPushButton('Caracas')
        self.button_mexico_city = QPushButton('Mexico City')
        self.button_new_york = QPushButton('New York')
        self.button_london = QPushButton('London')
        self.button_los_angeles = QPushButton('Los Angeles')
        self.button_santiago = QPushButton('Santiago')
        self.button_sydney = QPushButton('Sydney')
        self.button_tokyo = QPushButton('Tokyo')

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.button_local, 0)
        self.button_group.addButton(self.button_bogota, 1)
        self.button_group.addButton(self.button_caracas, 2)
        self.button_group.addButton(self.button_mexico_city, 3)
        self.button_group.addButton(self.button_new_york, 4)
        self.button_group.addButton(self.button_london, 5)
        self.button_group.addButton(self.button_los_angeles, 6)
        self.button_group.addButton(self.button_santiago, 7)
        self.button_group.addButton(self.button_sydney, 8)
        self.button_group.addButton(self.button_tokyo, 9)

        self.watch = QWatch()
        self.meridian = QLabel('AM')
        self.sec = self.min = self.hr = 0
        self.day = self.month = self.year = 0

        self.Time = QtCore.QTimer()

        self.selected_city = 0
        self.city = ('Local', 'Colombia: Bogotá', 'Venezuela: Caracas', 'Mexico: Mexico City',
                     'United States: New York', 'United Kingdom: London', 'United States: Los Angeles',
                     'Chile: Santiago', 'Australia: Sydney', 'Japan: Tokyo')

        self.tag = QLabel('WATCH')

    def styles(self):
        self.setStyleSheet('background-color:#1A293E')
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor('#707986'))
        palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('#707986'))
        self.tag.setPalette(palette)
        self.meridian.setPalette(palette)
        self.meridian.setAlignment(QtCore.Qt.AlignCenter)
        self.button_local.setPalette(palette)
        self.button_local.setFlat(True)
        self.button_bogota.setPalette(palette)
        self.button_bogota.setFlat(True)
        self.button_caracas.setPalette(palette)
        self.button_caracas.setFlat(True)
        self.button_mexico_city.setPalette(palette)
        self.button_mexico_city.setFlat(True)
        self.button_new_york.setPalette(palette)
        self.button_new_york.setFlat(True)
        self.button_london.setPalette(palette)
        self.button_london.setFlat(True)
        self.button_los_angeles.setPalette(palette)
        self.button_los_angeles.setFlat(True)
        self.button_santiago.setPalette(palette)
        self.button_santiago.setFlat(True)
        self.button_sydney.setPalette(palette)
        self.button_sydney.setFlat(True)
        self.button_tokyo.setPalette(palette)
        self.button_tokyo.setFlat(True)

    def structure(self):
        h1 = QHBoxLayout()
        h1.addWidget(self.tag)
        h1.addWidget(self.meridian)

        div_watch = QHBoxLayout()
        div_watch.addWidget(self.watch)

        div_buttons = QHBoxLayout()
        div_buttons.addWidget(self.button_local)
        div_buttons.addWidget(self.button_bogota)
        div_buttons.addWidget(self.button_caracas)
        div_buttons.addWidget(self.button_mexico_city)
        div_buttons.addWidget(self.button_new_york)
        div_buttons.addWidget(self.button_london)
        div_buttons.addWidget(self.button_los_angeles)
        div_buttons.addWidget(self.button_santiago)
        div_buttons.addWidget(self.button_sydney)
        div_buttons.addWidget(self.button_tokyo)

        # noinspection PyAttributeOutsideInit
        self.body = QVBoxLayout(self)
        self.body.addLayout(h1)
        self.body.addLayout(div_watch)
        self.body.addLayout(div_buttons)

    def connections(self):
        self.button_group.buttonClicked[int].connect(self.__push__)
        self.watch.date_change.connect(self.update_date_time)
        self.Time.timeout.connect(self.watch.RunTime)
        self.watch.meridian_change.connect(self.meridian.setText)

    def start(self):
        self.Time.start(1000)

    def __push__(self, chosen_city):
        self.selected_city = chosen_city
        self.update_date_time()

    # noinspection PyAttributeOutsideInit
    def update_date_time(self):
        current_location = self.city[self.selected_city]
        time_zone = None

        if current_location == 'Colombia: Bogotá':
            time_zone = pytz.timezone('America/Bogota')
        elif current_location == 'Venezuela: Caracas':
            time_zone = pytz.timezone('America/Caracas')
        elif current_location == 'Mexico: Mexico City':
            time_zone = pytz.timezone('America/Mexico_City')
        elif current_location == 'United States: New York':
            time_zone = pytz.timezone('America/New_York')
        elif current_location == 'United Kingdom: London':
            time_zone = pytz.timezone('Europe/London')
        elif current_location == 'United States: Los Angeles':
            time_zone = pytz.timezone('America/Los_Angeles')
        elif current_location == 'Chile: Santiago':
            time_zone = pytz.timezone('America/Santiago')
        elif current_location == 'Australia: Sydney':
            time_zone = pytz.timezone('Australia/Sydney')
        elif current_location == 'Japan: Tokyo':
            time_zone = pytz.timezone('Asia/Tokyo')

        date_time = datetime.now(time_zone)
        self.hr = date_time.hour
        self.min = date_time.minute
        self.sec = int(date_time.second)
        self.day = date_time.date().day
        self.month = date_time.date().month
        self.year = date_time.date().year

        self.__update_calendar__()
        self.__update_clock__()

    def __update_clock__(self):
        self.watch.UpdateFullTime(self.hr, self.min, self.sec)

    def __update_calendar__(self):
        self.tag.setText(f'{self.day}/{self.month}/{self.year} : City {self.city[self.selected_city]}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
