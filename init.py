from form import Ui_Widget
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from re import search, I


class ReMap:
    def __init__(self, n_dic, val):
        self._items = n_dic
        self.__val = val
        self._tempkey_ = None

    def __getitem__(self, key):
        for regex in self._items.keys():
            if search(regex, key, I):
                self._tempkey_ = key
                return self._items[regex]
        return self.__val

plt.rcParams['font.sans-serif'] = ['SimHei']


class MyWin(QMainWindow, Ui_Widget):
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.setupUi(self)
        self.max_x = int(self.x_max.toPlainText())
        self.min_x = int(self.x_min.toPlainText())
        self.max_y = int(self.y_max.toPlainText())
        self.min_y = int(self.y_min.toPlainText())
        self.function = self.comboBox.currentText()
        self.pushButton.clicked.connect(self.calculate)
        self.comboBox.activated.connect(self.expressionshow)
        self.expression.hide()
        self.label_8.hide()

    def expressionshow(self):
        if(self.comboBox.currentText() == "多项式"):
            self.label_8.show()
            self.expression.show()
        else:
            self.label_8.hide()
            self.expression.hide()

    def calculate(self):
        self.max_x = int(self.x_max.toPlainText())
        self.min_x = int(self.x_min.toPlainText())
        self.max_y = int(self.y_max.toPlainText())
        self.min_y = int(self.y_min.toPlainText())
        combox_text = self.comboBox.currentText()
        self.function = combox_text if combox_text != "多项式" else "polynomial "+ self.expression.text()
        if self.max_x <= self.min_x:
            print("x range wrong!!!")
            return 0
        if self.max_y <= self.min_y :
            print("y range wrong!!!")
            return 0

        myfunction = Myfunction(self.min_x, self.max_x)
        myfunction.func_dict.__getitem__(self.function)()
        if(self.clear.isChecked()):
            plt.close()
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))
        plt.title("Function img")
        plt.xlim(self.min_x, self.max_x)
        plt.ylim(self.min_y, self.max_y)
        plt.plot(myfunction.x, myfunction.y)
        plt.savefig('./output.jpg')

        jpg = QtGui.QPixmap('./output.jpg').scaled(self.imgshow.width(), self.imgshow.height())
        self.imgshow.setPixmap(jpg)

class Myfunction:
    def __init__(self, min_x: int, max_x: int):
        self.point_count = 300
        x = []
        area_point_count = self.point_count // (max_x - min_x)
        for i in range(min_x, max_x):
            temp = np.arange(i, i+1,
                      round(1 / area_point_count, 2))
            x += list(temp)

        self.x = x
        self.y = []
        self.func_dict = ReMap({"sin\(x\)": self.sin, "cos\(x\)": self.cos, "ln\(x\)": self.log,
                                "1/x": self.inverse, "polynomial .*": self.polynomial}, None)

    def sin(self):
        # self.y = math.sin(self.x)
        for i in self.x:
            y = math.sin(i)
            self.y.append(y)

    def cos(self):
        for i in self.x:
            y = math.cos(i)
            self.y.append(y)

    def log(self):
        for i in self.x:
            if i <= 0:
                print("illegal element")
                y = None
            else:
                y = math.log(i)
            self.y.append(y)

    def inverse(self):
        for i in self.x:
            if i == 0:
                print("illegal element")
                y = None
            else:
                y = 1/i
            self.y.append(y)

    def polynomial(self):
        for i in self.x:
            try:
                y = eval(self.func_dict._tempkey_.split(' ')[1].replace('x', '(' + str(i) + ')'))
            except:
                print("expression wrong")
                y = None
            self.y.append(y)


