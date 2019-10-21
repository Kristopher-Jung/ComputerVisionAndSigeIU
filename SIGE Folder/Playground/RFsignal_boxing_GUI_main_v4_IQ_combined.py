import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout, \
    QTextEdit, QInputDialog, QLineEdit
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import RectangleSelector
import pickle
import time


class signal_boxing_GUI_main(QWidget):

    def __init__(self, parent=None):
        super(signal_boxing_GUI_main, self).__init__(parent)
        # initialize GUI stuff
        self.fname = None
        self.IQ_t = None
        self.IQ_f = None
        self.IQ_bounded = None
        self.figureIQ, self.ax = plt.subplots(1)
        self.canvasIQ = FigureCanvas(self.figureIQ)
        self.toolbarIQ = NavigationToolbar(self.canvasIQ, self)
        self.figure_bounded, self.ax_bounded = plt.subplots(2)
        self.canvas_bounded = FigureCanvas(self.figure_bounded)
        self.index = 0
        self.all_bounded_data_raw = []
        self.all_bounded = []
        self.setWindowTitle('signal boxing GUI')

        win = QMainWindow()
        win.setFixedSize(1280, 900)
        menu_widget = QWidget()

        # buttons
        button = QPushButton('read data', menu_widget)
        read_bound_button = QPushButton('save current bound', menu_widget)
        overview_button = QPushButton('bounds overview', menu_widget)
        remove_last_button = QPushButton('remove last bound', menu_widget)
        export_raw_button = QPushButton('export raw', menu_widget)

        layout = QHBoxLayout(menu_widget)
        layout.addWidget(button)
        layout.addWidget(read_bound_button)
        layout.addWidget(remove_last_button)
        layout.addWidget(overview_button)
        layout.addWidget(export_raw_button)

        button.clicked.connect(self.button_pressed)
        read_bound_button.clicked.connect(self.read_bound_button_pressed)
        overview_button.clicked.connect(self.overview_pressed)
        remove_last_button.clicked.connect(self.remove_last_pressed)
        export_raw_button.clicked.connect(self.export_raw_pressed)

        # plot widgets
        plotWidget = QWidget()
        plotLayout = QVBoxLayout(plotWidget)
        plotLayout.addWidget(self.toolbarIQ)
        plotLayout.addWidget(self.canvasIQ)
        plotLayout.addWidget(self.canvas_bounded)
        win.setMenuWidget(menu_widget)
        win.setCentralWidget(plotWidget)
        win.show()
        app.exit(app.exec_())

    # read iq data from sigmf data file and saved it to this class
    def iq_read(self, file):
        Fs = 25000000
        fft = 25000
        UHF_dat = np.fromfile(file, dtype="float32")
        max = 25000000
        IQ_temp = UHF_dat[0:max]
        IQ = IQ_temp.astype(np.float32).view(np.complex64)
        self.IQ_f, self.IQ_t, self.Z = signal.stft(IQ, fs=Fs, nperseg=fft, return_onesided=False)
        PSD = 10 * np.log10(np.abs(self.Z) + 1e-30)
        self.flipped = np.vstack([PSD[fft // 2:], PSD[:fft // 2]])
        return self.flipped, self.IQ_f, self.IQ_t

    # read sigmf data file
    def button_pressed(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open Files', './')
        try:
            self.iq_read(self.fname[0])
            self.plot_IQ_initial(self.flipped, self.IQ_f, self.IQ_t)
            self.IQ_bounded = None
            self.all_bounded = []
            self.spanIQ = RectangleSelector(self.ax, self.onselectIQ, interactive=True, useblit=True)
            self.figure_bounded.clear()
            self.ax_bounded = self.figure_bounded.subplots(2)
            self.canvas_bounded.draw()
        except FileNotFoundError:
            return

    def read_bound_button_pressed(self):
        if self.IQ_bounded is not None:
            curr_bound_data = {'IQ_bounded': self.IQ_bounded}
            self.all_bounded.append(curr_bound_data)

    def overview_pressed(self):
        text = QTextEdit(self)
        text.setFixedSize(1280, 720)
        str = ''
        for idx, item in enumerate(self.all_bounded):
            str += '<<<<bound ' + (idx + 1).__str__() + '>>>>'
            str += '\n'
            for k, v in item.items():
                str += '<<' + k + '>>'
                str += '\n'
                str += v.__str__()
                str += '\n'
            str += '\n'
        text.setText(str)
        text.setReadOnly(True)
        self.show()

    def export_raw_pressed(self):
        if self.all_bounded.__len__() == 0:
            print('you do not have any bounded data yet')
        else:
            ts = time.time()
            time_stamp = time.ctime(ts).replace(' ', '_')
            for idx, bound in enumerate(self.all_bounded):
                names = self.fname[0].split('.')
                fname = names[0]
                paths = fname.split('/')
                real_fname = paths[-1]
                if not os.path.exists('./data'):
                    os.mkdir('./data')
                fullpath = './data/' + real_fname + '_' + time_stamp + '_' + 'bound_' + str(idx) + '_raw'
                IQ_bounded = bound['IQ_bounded']
                full = {'bounded': IQ_bounded}
                with open(fullpath + '.pickle', 'wb') as f:
                    pickle.dump(full, f)

    def remove_last_pressed(self):
        if self.all_bounded.__len__() >= 1:
            del self.all_bounded[-1]

    # this is called for bounding box region, and its data
    def onselectIQ(self, eclick, erelease):
        xmin = int(eclick.xdata)
        xmax = int(erelease.xdata)
        ymin = int(eclick.ydata)
        ymax = int(erelease.ydata)
        # xindmin, xindmax = np.searchsorted(self.IQ_t, (xmin, xmax))
        # yindmin, yindmax = np.searchsorted(self.IQ_f, (ymin, ymax))

        self.figure_bounded.clear()
        self.ax_bounded = self.figure_bounded.subplots(2)
        # self.IQ_t_bounded = self.IQ_t[xindmin:xindmax]
        # self.IQ_f_bounded = self.IQ_f[yindmin:yindmax]
        self.IQ_bounded = self.IQ[ymin:ymax, xmin:xmax]
        self.ax_bounded[0].pcolormesh(self.IQ_bounded)
        self.ax_bounded[1].plot(self.IQ_bounded)
        self.canvas_bounded.draw()

    # plotting Initial Inphase data
    def plot_IQ_initial(self, flipped, IQ_f, IQ_t):
        self.figureIQ.clear()
        self.IQ = flipped
        self.ax = self.figureIQ.add_subplot(111)
        self.ax.pcolormesh(flipped)
        self.canvasIQ.draw()


if __name__ == '__main__':
    app = QApplication([])
    qt = signal_boxing_GUI_main()
