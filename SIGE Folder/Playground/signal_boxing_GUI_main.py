import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout, \
    QTextEdit
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
        self.data_IQ_list = None
        self.I_t = None
        self.I_f = None
        self.I_t_bounded = None
        self.I_f_bounded = None
        self.I_bounded = None
        self.Q_bounded = None
        self.figureI, self.axI = plt.subplots(1)
        self.canvasI = FigureCanvas(self.figureI)
        self.toolbarI = NavigationToolbar(self.canvasI, self)
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
        plotLayout.addWidget(self.toolbarI)
        plotLayout.addWidget(self.canvasI)
        plotLayout.addWidget(self.canvas_bounded)
        win.setMenuWidget(menu_widget)
        win.setCentralWidget(plotWidget)
        win.show()
        app.exit(app.exec_())

    # read iq data from sigmf data file and saved it to this class
    def iq_read(self, file):
        Fs = 1000000
        data_IQ_list = []
        data_IQ_temp = []
        UHF_dat = np.fromfile(file, dtype="float32")
        I = UHF_dat[0::2]
        Q = UHF_dat[1::2]
        self.I_f, self.I_t, self.I_stft = signal.stft(I, Fs, nperseg=1024)
        Q_f, Q_t, self.Q_stft = signal.stft(Q, Fs, nperseg=1024)
        data_IQ_temp.append(np.abs(self.I_stft))
        data_IQ_temp.append(np.abs(self.Q_stft))
        data_IQ_list.append(data_IQ_temp)
        self.data_IQ_list = np.array(data_IQ_list)
        return self.data_IQ_list, self.I_f, self.I_t

    # read sigmf data file
    def button_pressed(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open Files', './')
        try:
            self.data_IQ_list, self.I_f, self.I_t = self.iq_read(self.fname[0])
            self.plot_I_initial(self.data_IQ_list, self.I_f, self.I_t)
            self.I_t_bounded = None
            self.I_f_bounded = None
            self.I_bounded = None
            self.Q_bounded = None
            self.all_bounded = []
            self.spanI = RectangleSelector(self.axI, self.onselectI, interactive=True, useblit=False)
            self.figure_bounded.clear()
            self.ax_bounded = self.figure_bounded.subplots(2)
            self.canvas_bounded.draw()
        except FileNotFoundError:
            return

    # this is called when refreseh pressed
    def read_bound_button_pressed(self):
        if (self.I_t_bounded is not None) and \
                (self.I_f_bounded is not None) and \
                (self.I_bounded is not None) and \
                (self.Q_bounded is not None):
            curr_bound_data = {'I_t': self.I_t_bounded, 'I_f': self.I_f_bounded, 'I_bounded': self.I_bounded,
                               'Q_bounded': self.Q_bounded}
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
                I_bounded = bound['I_bounded']
                Q_bounded = bound['Q_bounded']
                I_t = bound['I_t']
                I_f = bound['I_f']
                bounded = np.zeros((2, I_bounded.shape[0], I_bounded.shape[1]))
                bounded[0] = I_bounded
                bounded[1] = Q_bounded
                full = {'I_t': I_t, 'I_f': I_f, 'bounded':bounded}
                with open(fullpath + '.pickle', 'wb') as f:
                    pickle.dump(full, f)

                # fwith open(fullpath+ '.pickle', 'rb') as ff:
                #     print(pickle.load(ff))

    def remove_last_pressed(self):
        if self.all_bounded.__len__() >= 1:
            del self.all_bounded[-1]

    # this is called for bounding box region, and its data
    def onselectI(self, eclick, erelease):
        xmin = eclick.xdata
        xmax = erelease.xdata
        ymin = eclick.ydata
        ymax = erelease.ydata

        # is this right way to read I and Q? both looks identical in overview.
        Idata = self.I[0, :, :]
        Qdata = self.I[1, :, :]

        xindmin, xindmax = np.searchsorted(self.I_t, (xmin, xmax))
        yindmin, yindmax = np.searchsorted(self.I_f, (ymin, ymax))

        self.I_t_bounded = self.I_t[xindmin:xindmax]
        self.I_f_bounded = self.I_f[yindmin:yindmax]

        I_bounded_SNR = 10 * np.log10(Idata[yindmin:yindmax, xindmin:xindmax])
        Q_bounded_SNR = 10 * np.log10(Qdata[yindmin:yindmax, xindmin:xindmax])
        self.I_bounded = Idata[yindmin:yindmax, xindmin:xindmax]
        self.Q_bounded = Qdata[yindmin:yindmax, xindmin:xindmax]

        self.figure_bounded.clear()
        self.ax_bounded = self.figure_bounded.subplots(2)
        self.ax_bounded[0].plot(I_bounded_SNR)
        self.ax_bounded[0].set_title('I-region-SNR')
        self.ax_bounded[1].plot(Q_bounded_SNR)
        self.ax_bounded[1].set_title('Q-region-SNR')
        self.canvas_bounded.draw()

    # plotting Initial Inphase data
    def plot_I_initial(self, data_IQ_list, I_f, I_t):
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
    qt = signal_boxing_GUI_main()
