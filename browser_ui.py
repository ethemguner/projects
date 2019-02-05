from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets
import sys





class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
            
        self.setWindowTitle("Exc-X")
            
    def init_ui(self):

        ## Forex Graph view.
        self.eksi_biri = QtWebEngineWidgets.QWebEngineView()
        self.eksi_biri.load(QtCore.QUrl('https://eksisozluk.com/biri/ssg'))
        
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.eksi_biri)
        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v_box)
        
        self.setLayout(h_box)
        self.show()
        
        
app = QtWidgets.QApplication(sys.argv)
window = Window()
window.move(200, 120)
app.setStyle("Fusion")
window.setFixedSize(1355, 590)
sys.exit(app.exec_())