from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QFileDialog
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import RectangleSelector


class qt_play1(QWidget):

    def __init__(self, parent=None):
        super(qt_play1,self).__init__(parent)
        self.fname = None
        self.figureI, self.axI = plt.subplots(1)
        self.canvasI = FigureCanvas(self.figureI)
        self.toolbarI = NavigationToolbar(self.canvasI, self)

        self.figureQ, self.axQ = plt.subplots(1)
        self.canvasQ = FigureCanvas(self.figureQ)
        self.toolbarQ = NavigationToolbar(self.canvasQ, self)

        win = QMainWindow()
        win.setFixedSize(1280,720)
        menu_widget = QWidget()
        button = QPushButton('read data', menu_widget)
        boundIbutton = QPushButton('bounding I data', menu_widget)
        boundQbutton = QPushButton('bounding Q data', menu_widget)
        layout = QVBoxLayout(menu_widget)
        layout.addWidget(button)
        layout.addWidget(boundIbutton)
        layout.addWidget(boundQbutton)

        plotWidget = QWidget()
        plotLayout = QVBoxLayout(plotWidget)
        plotLayout.addWidget(self.toolbarI)
        plotLayout.addWidget(self.canvasI)
        plotLayout.addWidget(self.toolbarQ)
        plotLayout.addWidget(self.canvasQ)

        win.setMenuWidget(menu_widget)
        win.setCentralWidget(plotWidget)
        button.clicked.connect(self.button_pressed)
        boundIbutton.clicked.connect(self.boundIbutton_pressed)
        boundQbutton.clicked.connect(self.boundQbutton_pressed)

        win.show()
        app.exit(app.exec_())

    def button_pressed(self):
        fname = QFileDialog.getOpenFileName(self,'Open Files','./')
        data_IQ_list, I_f, I_t = self.iq_read(fname[0])
        self.plot_I(data_IQ_list, I_f, I_t)
        self.plot_Q(data_IQ_list, I_f, I_t)

    def boundIbutton_pressed(self):
        self.spanI = RectangleSelector(self.axI, self.onselectI, interactive=True)

    def boundQbutton_pressed(self):
        self.spanQ = RectangleSelector(self.axQ, self.onselectQ, interactive=True)

    def onselectI(self, eclick, erelease):
        print(eclick, erelease)

    def onselectQ(self, eclick, erelease):
        print(eclick, erelease)


    def iq_read(self, file):
        Fs = 1000000
        data_IQ_list = []
        data_IQ_temp = []
        #for file in data_files:
        UHF_dat = np.fromfile(file, dtype="float32")
        I = UHF_dat[0::2]
        Q = UHF_dat[1::2]
        self.I_f, self.I_t, I_stft = signal.stft(I, Fs, nperseg=4096)
        Q_f, Q_t, Q_stft = signal.stft(Q, Fs, nperseg=4096)
        data_IQ_temp.append(np.abs(I_stft))
        data_IQ_temp.append(np.abs(Q_stft))
        data_IQ_list.append(data_IQ_temp)
        self.data_IQ_list = np.array(data_IQ_list)
        return self.data_IQ_list, self.I_f, self.I_t

    def plot_I(self,data_IQ_list, I_f, I_t):
        self.figureI.clear()
        I = data_IQ_list[0]
        self.axI = self.figureI.add_subplot(111)
        self.axI.pcolormesh(I_t, I_f, 10 * np.log10(I[0, :, :]))
        self.canvasI.draw()


    def plot_Q(self,data_IQ_list,I_f,I_t):
        self.figureQ.clear()
        Q = data_IQ_list[0]
        self.axQ = self.figureQ.add_subplot(111)
        self.axQ.pcolormesh(I_t, I_f, 10 * np.log10(Q[1, :, :]))
        self.canvasQ.draw()


if __name__ == '__main__':
    app = QApplication([])
    qt = qt_play1()