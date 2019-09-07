import pickle
import numpy as np
from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QButtonGroup, QLineEdit


class signal_padding_GUI_main(QtWidgets.QWidget):

    def __init__(self):
        super(signal_padding_GUI_main, self).__init__()
        # Initialize necessary stuff
        self.items = []
        self.export_buttons = []
        self.dim_texts = []
        self.noise_texts = []
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
            str += '<<<<bound ' + (idx + 1).__str__() + '>>>>' + '\n'
            str += 'Shape of bounded region: '
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
            info_text.setFixedSize(1280, 720)
            layout.addWidget(info_text)

            #label2
            label2 = QtWidgets.QLabel()
            label2.setText('type your comma separated custom dimension, for example: 200,1200')
            layout.addWidget(label2)

            #dimension input
            dim_text = QLineEdit()
            self.dim_texts.append(dim_text)
            layout.addWidget(dim_text)

            #label3
            label3 = QtWidgets.QLabel()
            label3.setText('custom noise level(upper limit) for padding in scientific notation\n'
                           'for example: 1.2e-4 -> smallest number python provides < random new noise < 1.2e-4')
            layout.addWidget(label3)

            #nosie level input
            noise_text = QLineEdit()
            self.noise_texts.append(noise_text)
            layout.addWidget(noise_text)

            #export button
            push_button = QtWidgets.QPushButton(group_box)
            push_button.setText(idx.__str__()+'_'+ 'export')
            push_button.setFixedSize(300, 32)
            layout.addWidget(push_button)

            self.export_buttons.append(push_button)
            top_layout.addWidget(group_box)

        #button listener
        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        for button in self.export_buttons:
            self.btn_grp.addButton(button)
        self.btn_grp.buttonClicked.connect(self.export_button_pressed)

        #add widgets to main window
        top_widget.setLayout(top_layout)
        scrollArea.setWidget(top_widget)
        self.resize(1600, 900)

    #this is called when export button pressed
    def export_button_pressed(self, btn):
        #read meta info
        target = btn.text().split('_')
        idx = int(target[0])
        item = self.items[idx]
        dims = self.dim_texts[idx].text().split(',')
        dims = [int(x.strip()) for x in dims]
        fnames = self.fnames[0]
        curr_name = fnames[idx].split('_')
        custom_noise = float(self.noise_texts[idx].text().strip())
        del curr_name[-1]
        new_name =''
        for str in curr_name:
            new_name+=str
            new_name+='_'
        new_name+='padded.pickle'
        # print(dims)
        # print(item)
        # print(new_name)
        # print(custom_noise)

        #read current target data
        raw_bounded = item['bounded']
        #only if dims are right and input noise upper limit is valid
        if dims[0] > raw_bounded.shape[1] and dims[1] > raw_bounded.shape[2] and custom_noise > np.nextafter(0, 1):
            #padding
            padded = np.random.uniform(low=np.nextafter(0,1), high=custom_noise, size=(2,dims[0],dims[1]))
            padded[:,:raw_bounded.shape[1],:raw_bounded.shape[2]] = raw_bounded
            #create new pickle
            with open(new_name, 'wb') as f:
                pickle.dump(padded, f)

#run main
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = signal_padding_GUI_main()
    widget.show()
    sys.exit(app.exec_())

