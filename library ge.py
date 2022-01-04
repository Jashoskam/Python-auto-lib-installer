from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import threading
import sys
import imp
import subprocess

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(390, 150)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        #MainWindow.setWindowFlag(Qt.FramelessWindowHint)
        #MainWindow.setWindowFlags(Qt.CustomizeWindowHint)
        css = """
                    QWidget{
                        Background: #000000;
                        color:black;
                        font:12px bold;
                        font-weight:bold;
                        border-radius: 1px;
                        height: 11px;
                    }
                    """
        MainWindow.setStyleSheet("""background-color:rgba(60,63,65,255);""")
		
		# adding pushbutton
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(290, 10, 93, 28))

        self.textbox = QtWidgets.QLineEdit(self.centralwidget)
        self.textbox.setGeometry(QtCore.QRect(10, 10, 280, 28))
        self.textbox.setStyleSheet("""color:white;
                                            font-size:13px;
                                            border-style:none;""")
		
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 370, 100))
        self.listWidget.setWordWrap(True)
        self.listWidget.setStyleSheet("""color:white;
                                            font-size:13px;
                                            border-style:none;
                                            background-color:rgba(43,43,43,255);}
                                            QScrollBar:vertical {           
            border: none;
            background:white;
            width:3px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop: 0 black, stop: 0.5 black, stop:1 black);
            min-height: 0px;
        }
        QScrollBar::add-line:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop: 0 black, stop: 0.5 black,  stop:1 black);
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop: 0  black, stop: 0.5 black,  stop:1 black);
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
                                    
                                    """)

		# adding signal and slot
        self.pushButton.clicked.connect(self.changelabeltext)
	
		
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
        self.pushButton.setText("Push Button")
    def checkFileExistance(self):
        fileName = self.textbox.text()
        try:
                with open(fileName) as file:
                    listWidgetItem = QtWidgets.QListWidgetItem(("import of "+fileName+" successful"))
                    self.listWidget.addItem(listWidgetItem)
                    for line in file:
                        lineContext = line.rstrip()
                        if "import" in lineContext:
                            x = lineContext.split()
                            try:
                                imp.find_module(str(x[1]))
                                listWidgetItem = QtWidgets.QListWidgetItem(("module "+x[1]+" already exists"))
                                self.listWidget.addItem(listWidgetItem)
                            except ImportError:
                                errorMsg = QtWidgets.QListWidgetItem(("error while installing "+x[1]))
                                errorMsg.setForeground(QtCore.Qt.red)
                                self.listWidget.addItem(errorMsg)
                                subproces=subprocess.check_call([sys.executable, "-m", "pip", "install", x[1]])
                                subprocess_return = subproces.stdout.read()
                    errorMsg2 = QtWidgets.QListWidgetItem(("*process finished*"))
                    self.listWidget.addItem(errorMsg2)
        except Exception as e:
            errorMsg2 = QtWidgets.QListWidgetItem(("error while importing "+fileName))
            errorMsg2.setForeground(QtCore.Qt.red)
            self.listWidget.addItem(errorMsg2)
            errorMsg2 = QtWidgets.QListWidgetItem(str(e))
            errorMsg2.setForeground(QtCore.Qt.red)
            self.listWidget.addItem(errorMsg2)
    def changelabeltext(self):
        try:
            
            listWidgetItem = QtWidgets.QListWidgetItem("importing file")
            self.listWidget.addItem(listWidgetItem)
            t1 = threading.Thread(target=self.checkFileExistance)
            t1.start()
        except Exception as e:
            print(e)
            
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()

	sys.exit(app.exec_())
