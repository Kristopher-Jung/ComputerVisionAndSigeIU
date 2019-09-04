from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout, \
    QLineEdit
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import RectangleSelector
import json
import pickle


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
        metagen_button = QPushButton('edit metadata', menu_widget)
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
        self.I_f, self.I_t, self.I_stft = signal.stft(I, Fs, nperseg=4096)
        Q_f, Q_t, self.Q_stft = signal.stft(Q, Fs, nperseg=4096)
        data_IQ_temp.append(np.abs(self.I_stft))
        data_IQ_temp.append(np.abs(self.Q_stft))
        data_IQ_list.append(data_IQ_temp)
        self.data_IQ_list = np.array(data_IQ_list)
        return self.data_IQ_list, self.I_f, self.I_t

    #read sigmf data file
    def button_pressed(self):
        self.fname = QFileDialog.getOpenFileName(self,'Open Files','./')
        try:
            self.data_IQ_list, self.I_f, self.I_t = self.iq_read(self.fname[0])
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
        if (self.I_t is not None) and (self.I_f is not None) and (self.I is not None):
            export_data_raw = {'I_t': self.I_t, 'I_f':self.I_f, 'I': self.I_bounded, 'Q': self.Q_bounded}
            I_padded = np.zeros((self.I.shape[1], self.I.shape[2]))
            I_padded[:self.I_bounded.shape[0], :self.I_bounded.shape[1]] = self.I_bounded
            Q_padded = np.zeros((self.I.shape[1], self.I.shape[2]))
            Q_padded[:self.Q_bounded.shape[0], :self.Q_bounded.shape[1]] = self.Q_bounded
            export_data_bounded = np.zeros(self.I.shape)
            export_data_bounded[0] = I_padded
            export_data_bounded[1] = Q_padded
            print(I_padded.shape, Q_padded.shape, export_data_bounded.shape)
            print(export_data_bounded)
            with open(self.fname[0]+ '_bounded_raw.pickle', 'wb') as f:
                pickle.dump(export_data_raw, f)

            with open(self.fname[0]+'_bounded_padded.pickle', 'wb') as f:
                pickle.dump(export_data_bounded, f)
        else:
            print('read sigmf and plot it first')


    #this is called to generate new custom metadata sigmf
    def metagen_pressed(self):
        self.metadata_name = QFileDialog.getOpenFileName(self, 'Open Files', './')[0]
        try:
            with open(self.metadata_name) as f:
                self.metadata = json.load(f)
                self.textbox1 = QLineEdit(self)
                self.textbox1.move(20, 20)
                self.textbox1.resize(280, 40)
                self.tb1 = QPushButton('field selection', self)
                self.tb1.move(20, 80)
                self.show()
                self.tb1.clicked.connect(self.textbox_clicked)
        except FileNotFoundError:
            return

    def textbox_clicked(self):
        if self.textbox1.text() == "global":
            self.textbox2 = QLineEdit(self)
            self.textbox2.move(20, 20)
            self.textbox2.resize(280, 40)
            self.tb2 = QPushButton('in_field', self)
            self.tb2.move(20, 80)
            print('himsdfklj')
            self.show()
            self.tb2.clicked.connect(self.textbox_clicked)
        if self.textbox1.text() == "core:class":
            print('')
        if self.textbox1.text() == "captures":
            print('')
        if self.textbox1.text() == "annotations":
            print('')

    def textbox2_clicked(self):
        print('here!')

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
        #print('I_t X Index Min to max = ', self.I_t[xindmin:xindmax].shape)
        #print('I_t X index min = ', xindmin, ' xindex max = ', xindmax)
        #print('I_f y Index min to max = ', self.I_f[yindmin:yindmax].shape)
        #print('I_f y index min = ', yindmin, ' y index max = ', yindmax)
        #print('I data x min_to_max, y min_to_max = ', Idata[xindmin:xindmax, yindmin:yindmax].shape)
        self.figure_bounded.clear()
        self.ax_bounded = self.figure_bounded.subplots(2)
        self.I_bounded_SNR = 10 * np.log10(Idata[xindmin:xindmax, yindmin:yindmax])
        self.Q_bounded_SNR = 10 * np.log10(Qdata[xindmin:xindmax, yindmin:yindmax])
        self.I_bounded = Idata[xindmin:xindmax, yindmin:yindmax]
        print(self.I_bounded)
        self.Q_bounded = Idata[xindmin:xindmax, yindmin:yindmax]
        self.ax_bounded[0].plot(self.I_bounded_SNR)
        self.ax_bounded[0].set_title('I-region-SNR')
        self.ax_bounded[1].plot(self.Q_bounded_SNR)
        self.ax_bounded[1].set_title('Q-region-SNR')
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