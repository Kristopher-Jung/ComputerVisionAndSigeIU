import pickle
from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class load_pic_v2_2(QtWidgets.QWidget):

    def __init__(self):
        super(load_pic_v2_2, self).__init__()
        # Initialize necessary stuff
        self.items = []
        self.images = []
        #read multiple files
        self.fnames = QFileDialog.getOpenFileNames(self, 'Open Files', './data')
        for fname in self.fnames[0]:
            print(fname)
            with open(fname, 'rb') as f:
                self.items.append(pickle.load(f))

        #Initialize scrollarea widget
        lay = QtWidgets.QVBoxLayout(self)
        scrollArea = QtWidgets.QScrollArea()
        lay.addWidget(scrollArea)
        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout()


        #read all the data and initialize necessary GUI widgets
        for idx, item in enumerate(self.items):
            path = self.fnames[0]
            fname = path[idx]
            group_box = QtWidgets.QGroupBox()
            group_box.setTitle(fname)
            layout = QtWidgets.QVBoxLayout(group_box)

            #label1
            label1 = QtWidgets.QLabel()
            label1.setText('data overview: ')
            layout.addWidget(label1)

            #info text
            info_text = QTextEdit()
            str = ''
            str += '<<<<IQbound ' + (idx + 1).__str__() + '>>>>' + '\n'
            str += 'Shape of bounded IQ sample: '
            str += item['bounded'].shape.__str__()
            str += '\n'
            for k, v in item.items():
                str += '<<' + k + '>>'
                str += '\n'
                str += v.__str__()
                str += '\n'
            str += '\n'
            info_text.setText(str)
            info_text.setReadOnly(True)
            info_text.setFixedSize(1600, 360)
            layout.addWidget(info_text)

            fig = plt.figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.pcolormesh(item['bounded'])
            layout.addWidget(canvas)
            canvas.draw()
            plt.savefig(fname+'.png')

            top_layout.addWidget(group_box)

        #add widgets to main window
        top_widget.setLayout(top_layout)
        scrollArea.setWidget(top_widget)
        self.resize(1900, 900)

#run main
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = load_pic_v2_2()
    widget.show()
    sys.exit(app.exec_())

