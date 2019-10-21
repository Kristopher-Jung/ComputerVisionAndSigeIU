import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider, QTextEdit)

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

    def setting(self):
        if self.all_bounded is not None and self.all_bounded.__len__() >= 1:
            grid = QVBoxLayout()
            for idx, item in enumerate(self.all_bounded):
                grid.addWidget(self.createExampleGroup(idx, item))
            export_button = QPushButton('export')
            grid.addWidget(export_button)
            export_button.clicked.connect(self.export_button_pressed)
            self.setLayout(grid)
            self.setWindowTitle("PyQt5 Sliders")
            self.resize(1280, 720)

    def set_data(self, all_bounded):
        self.all_bounded = all_bounded

    def createExampleGroup(self, idx, item):
        groupBox = QGroupBox("Slider Example")

        radio1 = QRadioButton("&Radio horizontal slider")

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(10)
        slider.setSingleStep(1)
        radio1.setChecked(True)

        text = QTextEdit(self)
        str = ''
        str += '<<<<bound ' + (idx + 1).__str__() + '>>>>' + '\n'
        str += 'Shape of bounded region: '
        str += item['I_bounded'].shape.__str__()
        str += '\n'
        for k, v in item.items():
            str += '<<' + k + '>>'
            str += '\n'
            str += v.__str__()
            str += '\n'
        str += '\n'
        text.setText(str)
        text.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(slider)
        vbox.addWidget(text)



        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def export_button_pressed(self):
        print('exporting begins!')