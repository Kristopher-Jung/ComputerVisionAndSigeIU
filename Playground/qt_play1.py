from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QFileDialog, QLabel
import cv2
from PyQt5.QtGui import QPixmap
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import SpanSelector

class qt_play1(QWidget):

    def __init__(self, parent=None):
        super(qt_play1,self).__init__(parent)
        self.fname = None
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        win = QMainWindow()
        win.setFixedSize(1280,720)
        menu_widget = QWidget()
        button = QPushButton('read data', menu_widget)
        horiz_button = QPushButton('horizontal cut', menu_widget)
        layout = QVBoxLayout(menu_widget)
        layout.addWidget(button)
        layout.addWidget(horiz_button)
        #self.label = QLabel()
        #pixmap = QPixmap(self.fname)
        #self.label.setPixmap(pixmap)

        plotWidget = QWidget()
        plotLayout = QVBoxLayout(plotWidget)
        plotLayout.addWidget(self.toolbar)
        plotLayout.addWidget(self.canvas)

        win.setMenuWidget(menu_widget)
        win.setCentralWidget(plotWidget)
        button.clicked.connect(self.button_pressed)

        win.show()
        app.exit(app.exec_())

    def button_pressed(self):
        fname = QFileDialog.getOpenFileName(self,'Open Files','./')

        #self.img = cv2.imread(fname[0])
        #print(self.img.shape)
        data_IQ_list, I_f, I_t = self.iq_read(fname[0])
        self.plot_I(data_IQ_list, I_f, I_t)

    def horiz_button_pressed(self):
        print('')

    def iq_read(self, file):
        Fs = 1000000
        data_IQ_list = []
        data_IQ_temp = []
        #for file in data_files:
        UHF_dat = np.fromfile(file, dtype="float32")
        I = UHF_dat[0::2]
        Q = UHF_dat[1::2]
        I_f, I_t, I_stft = signal.stft(I, Fs, nperseg=4096)
        Q_f, Q_t, Q_stft = signal.stft(Q, Fs, nperseg=4096)
        data_IQ_temp.append(np.abs(I_stft))
        data_IQ_temp.append(np.abs(Q_stft))
        data_IQ_list.append(data_IQ_temp)
        data_IQ_temp = []
        data_IQ_list = np.array(data_IQ_list)
        return data_IQ_list, I_f, I_t

    def plot_I(self,data_IQ_list, I_f, I_t):
        self.figure.clear()
        for I in data_IQ_list:
            self.ax = self.figure.add_subplot(111)
            self.ax.pcolormesh(I_t, I_f, 10 * np.log10(I[0, :, :]))
            #ax.title('Inphase STFT Magnitude')
            #ax.ylabel('Frequency [Hz]')
            #ax.xlabel('Time [sec]')
            # set useblit True on gtkagg for enhanced performance
            figure, ax = plt.subplots()
            self.span = SpanSelector(self.ax, self.onselect_horiz, 'horizontal', useblit=True,
                                     rectprops=dict(alpha=0.5, facecolor='red'))
            self.canvas.draw()




    def onselect_horiz(sekf, xmin, xmax):
        print(xmin, xmax)




    def plot_Q(self,data_IQ_list,I_f,I_t):
        for Q in data_IQ_list:
            plt.pcolormesh(I_t, I_f, 10 * np.log10(Q[1, :, :]))
            plt.title('Quadrature STFT Magnitude')
            plt.ylabel('Frequency [Hz]')
            plt.xlabel('Time [sec]')




if __name__ == '__main__':
    app = QApplication([])
    qt = qt_play1()