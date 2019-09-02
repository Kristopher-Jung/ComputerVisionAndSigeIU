from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import RectangleSelector


class qt_play1(QWidget):

    def __init__(self, parent=None):
        super(qt_play1,self).__init__(parent)
        # initialize GUI stuff
        self.fname = None
        self.data_IQ_list = None
        self.I_t = None
        self.I_f = None
        self.figureI, self.axI = plt.subplots(1)
        self.canvasI = FigureCanvas(self.figureI)
        self.toolbarI = NavigationToolbar(self.canvasI, self)
        self.figure_bounded, self.ax_bounded = plt.subplots(2)
        self.canvas_bounded = FigureCanvas(self.figure_bounded)
        win = QMainWindow()
        win.setFixedSize(1280,900)
        menu_widget = QWidget()

        #buttons
        button = QPushButton('read data', menu_widget)
        boundIbutton = QPushButton('bounding I data', menu_widget)
        refresh_button = QPushButton('refreseh plot', menu_widget)
        export_button = QPushButton('export data', menu_widget)
        metagen_button = QPushButton('gen meta', menu_widget)
        layout = QHBoxLayout(menu_widget)
        layout.addWidget(button)
        layout.addWidget(boundIbutton)
        layout.addWidget(refresh_button)
        layout.addWidget(export_button)
        layout.addWidget(metagen_button)
        button.clicked.connect(self.button_pressed)
        boundIbutton.clicked.connect(self.boundIbutton_pressed)
        refresh_button.clicked.connect(self.refresh_pressed)
        export_button.clicked.connect(self.export_pressed)
        metagen_button.clicked.connect(self.metagen_pressed)

        #plot widgets
        plotWidget = QWidget()
        plotLayout = QVBoxLayout(plotWidget)
        plotLayout.addWidget(self.toolbarI)
        plotLayout.addWidget(self.canvasI)
        plotLayout.addWidget(self.canvas_bounded)
        win.setMenuWidget(menu_widget)
        win.setCentralWidget(plotWidget)
        win.show()
        app.exit(app.exec_())


    #read iq data from sigmf data file and saved it to this class
    def iq_read(self, file):
        Fs = 1000000
        data_IQ_list = []
        data_IQ_temp = []
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

    #read sigmf data file
    def button_pressed(self):
        fname = QFileDialog.getOpenFileName(self,'Open Files','./')
        try:
            self.data_IQ_list, self.I_f, self.I_t = self.iq_read(fname[0])
            self.plot_I_initial(self.data_IQ_list, self.I_f, self.I_t)
        except FileNotFoundError:
            return

    #this is called when bbox pressed
    def boundIbutton_pressed(self):
        self.spanI = RectangleSelector(self.axI, self.onselectI, interactive=True)

    #this is called when refreseh pressed
    def refresh_pressed(self):
        if (self.data_IQ_list is not None) and (self.I_f is not None) and (self.I_t is not None):
            self.plot_I_initial(self.data_IQ_list, self.I_f, self.I_t)
            self.figure_bounded.clear()

    #this is called when export data pressed
    def export_pressed(self):
        print('not implemented yet')

    #this is called to generate new custom metadata sigmf
    def metagen_pressed(self):
        print('not implemented yet')

    #this is called for bounding box region, and its data
    def onselectI(self, eclick, erelease):
        xmin = eclick.xdata
        xmax = erelease.xdata
        ymin = eclick.ydata
        ymax = erelease.ydata
        Idata = self.I[0,:,:]
        Qdata = self.I[1,:,:]
        xindmin, xindmax = np.searchsorted(self.I_t, (xmin, xmax))
        yindmin, yindmax = np.searchsorted(self.I_f, (ymin, ymax))
        print('I_t X Index Min to max = ', self.I_t[xindmin:xindmax].shape)
        print('I_t X index min = ', xindmin, ' xindex max = ', xindmax)
        print('I_f y Index min to max = ', self.I_f[yindmin:yindmax].shape)
        print('I_f y index min = ', yindmin, ' y index max = ', yindmax)
        print('I data x min_to_max, y min_to_max = ', Idata[xindmin:xindmax, yindmin:yindmax].shape)
        self.figure_bounded.clear()
        self.ax_bounded = self.figure_bounded.subplots(2)
        self.ax_bounded[0].plot(10 * np.log10(Idata[xindmin:xindmax, yindmin:yindmax]))
        self.ax_bounded[0].set_title('I-region')
        self.ax_bounded[1].plot(10 * np.log10(Qdata[xindmin:xindmax, yindmin:yindmax]))
        self.ax_bounded[1].set_title('Q-region')
        self.canvas_bounded.draw()

    #plotting Initial Inphase data
    def plot_I_initial(self,data_IQ_list, I_f, I_t):
        self.figureI.clear()
        self.I = data_IQ_list[0]
        self.axI = self.figureI.add_subplot(111)
        self.axI.pcolormesh(I_t, I_f, 10 * np.log10(self.I[0, :, :]))
        self.axI.set_xlabel('Time [sec]')
        self.axI.set_ylabel('Frequency [Hz]')
        self.axI.set_title('Inphase STFT Magnitude')
        self.canvasI.draw()


if __name__ == '__main__':
    app = QApplication([])
    qt = qt_play1()