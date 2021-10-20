from init import *
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MyWin()
    mw.show()
    sys.exit(app.exec_())
