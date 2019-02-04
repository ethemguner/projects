from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError   ## internet bağlantısı kontrol etmek amaçlı


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
            
        self.setWindowTitle("Anlık Kur")
            
    def init_ui(self):
        
            self.information_label = QtWidgets.QLabel("Bütün veriler bloomberght.com'dan alınmıştır.") ## çok bahtsızım ben, başımıza bir şey gelmesin diye bu bilgiyi ekliyoruz. :*)
            ## bir zamanlyııc ayarı. her 30 saniyede bir programın fonksiyonları ve çekilen değerleri yeniler.
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.refreshData) ## functiona gidiyoruzi.
            self.timer.start(30000)
            
            ## Veriler çekiliyor. (değişken isimlerine çok takmadım programı yazarken, burda da değiştirmeye gerek duymadım.)
            page = requests.get('https://www.bloomberght.com')
            soup = BeautifulSoup(page.content, 'html.parser')
            currency = soup.find(class_='col-md-10 col-sm-12 col-xs-12 marketsWrap')
            currency_dolar = currency.find(id = "dolar")
            currency_euro = currency.find(id = "euro")
            currency_euro_usd = currency.find(id="eur-usd")
            currency_value_eurusd = currency_euro_usd.select(".LastPrice")
            currency_value_dolar = currency_dolar.select(".LastPrice")
            currency_value_euro = currency_euro.select(".LastPrice")
            getting_closer = currency.find_all(class_="marketsCol")   ## yüzdesel değişim verisi çekiliyor.
            
            
            ## Try-except blokları, gelen değerleri kontrol ediyor. Bloomberght'de yüzdesel değişim 0'ın altına inince downRed PercentChange class'ından değer alınır.
            ## Bu durumda artık yeşil (upGreen PercentChange)'den alınan veri, kullanılamaz. Uygulama, kendini yenilediğinde AttributeError verir.
            ## Bu try-except bloklarında, her bir yüzdesel değişimin yeşil,kırmızı ve 0 olma durumunu kontrol ediyoruz.
            ## 0.00 değerini kendimiz verdik. Renk değişimi sağlamadık.
            try:
                self.usd_try_percantal_ratio = getting_closer[1].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.usd_try_percantal_ratio = getting_closer[1].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.usd_try_percantal_ratio = "0.00"
                
            try:
                self.euro_try_percantal_ratio = getting_closer[2].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.euro_try_percantal_ratio = getting_closer[2].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.euro_try_percantal_ratio = "0.00"
    
            try:
                self.euro_usd_percantal_ratio = getting_closer[3].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.euro_usd_percantal_ratio = getting_closer[3].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.euro_usd_percantal_ratio = "0.00"
                    
            
            ## Internet gittiğinde programın kapanmaması için bir error mesaj kutusu göstermemiz gerek, onu tanımladım:
            self.msgBox = QtWidgets.QMessageBox()
            
            ## Table'lar tanımlanıyor. (Row ve column sayıları ile birlikte.)
            self.currency_table = QtWidgets.QTableWidget()
            self.currency_table.setRowCount(3)
            self.currency_table.setColumnCount(2)
            self.currency_table.setColumnWidth(0,152)
                
            self.currency_ratio_table = QtWidgets.QTableWidget()
            self.currency_ratio_table.setRowCount(3)
            self.currency_ratio_table.setColumnCount(2)
            self.currency_ratio_table.setColumnWidth(0,152)
            
            ## Yukarıda çekilen liste şeklinde gelen veriler, bu table'lar için kullanılabilir hale getiriliyor.
            ## get_text() gereksiz html kodlarından arındırıyor verimizi.
            self.dolar_try = currency_value_dolar[0].get_text()
            self.euro_try = currency_value_euro[0].get_text()
            self.euro_usd = currency_value_eurusd[0].get_text()

            ## Tablolara verilerimiz ekleniyor.
            
            ## exchange values -->>>
            self.currency_table.setItem(0,0, QtWidgets.QTableWidgetItem("USD/TRY"))
            self.currency_table.setItem(0,1, QtWidgets.QTableWidgetItem(self.dolar_try))
            
            self.currency_table.setItem(1,0, QtWidgets.QTableWidgetItem("EUR/TRY"))
            self.currency_table.setItem(1,1, QtWidgets.QTableWidgetItem(self.euro_try))
            
            self.currency_table.setItem(2,0, QtWidgets.QTableWidgetItem("EUR/USD"))
            self.currency_table.setItem(2,1, QtWidgets.QTableWidgetItem(self.euro_usd))
            
            ## percantal ratios -->>
            self.currency_ratio_table.setItem(0,0, QtWidgets.QTableWidgetItem("USD/TRY"))
            self.currency_ratio_table.setItem(0,1, QtWidgets.QTableWidgetItem(self.usd_try_percantal_ratio))
            
            self.currency_ratio_table.setItem(1,0, QtWidgets.QTableWidgetItem("EURO/TRY"))
            self.currency_ratio_table.setItem(1,1, QtWidgets.QTableWidgetItem(self.euro_try_percantal_ratio))
            
            self.currency_ratio_table.setItem(2,0, QtWidgets.QTableWidgetItem("EURO/USD"))
            self.currency_ratio_table.setItem(2,1, QtWidgets.QTableWidgetItem(self.euro_usd_percantal_ratio))
            
            ## Set tables as uneditable. ## Kullanıcı tabloların üzerine tıklayıp değiştirme/silme yapmasın diye bir NoTrigger tanımlaması yaptık.
            self.currency_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.currency_ratio_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            
            ## Row ve column'ların counterlarını gizledik. (bunu öğrenmek zor olmuştu)
            self.currency_table.verticalHeader().setVisible(False)  ## for hide the row-column counter.
            self.currency_table.horizontalHeader().setVisible(False) ## for hide the row-column counter.
            

            self.currency_ratio_table.verticalHeader().setVisible(False)
            self.currency_ratio_table.horizontalHeader().setVisible(False)
            
            
            ## Vertical boxımız.
            v_box = QtWidgets.QVBoxLayout()
            
            ## Widget'lar, (tablolar) ekleniyor vertical boxa.
            v_box.addWidget(self.currency_table)
            v_box.addWidget(self.currency_ratio_table)
            v_box.addWidget(self.information_label)
            
            ##horizontal box. onun içine de vertical boxımızı ekliyoruz böylelikle arayüzle oynanınca kaymalar engelleniyor.
            ## hoş ben boyutu fixledim ama adettendir.
            h_box = QtWidgets.QHBoxLayout()
            h_box.addLayout(v_box)
            
            ## Yüzdesel değişimlerin renklerini ayarlamak için funciton çağırıyoruz.
            self.colorRatios()
            
            ## Son adım, layout ayarlandı.
            self.setLayout(h_box)
            self.show() ## arayüz yüklendi.
            
    ## Verilerimiz yenileniyor.
    def refreshData(self):
        
        ## Try except içerisine almamız sebebi, internet bağlantısı hatasını yakalamaktan ibaret. Except kısmında msgBox'ı editlediğimi göreceksiniz.
        try: 
            page = requests.get('https://www.bloomberght.com')
            soup = BeautifulSoup(page.content, 'html.parser')
            currency = soup.find(class_='col-md-10 col-sm-12 col-xs-12 marketsWrap')
            currency_dolar = currency.find(id = "dolar")
            currency_euro = currency.find(id = "euro")
            currency_euro_usd = currency.find(id="eur-usd")
            currency_value_eurusd = currency_euro_usd.select(".LastPrice")
            currency_value_dolar = currency_dolar.select(".LastPrice")
            currency_value_euro = currency_euro.select(".LastPrice")
            getting_closer = currency.find_all(class_="marketsCol")
            
            ## Yukardakinin aynı mantığı.
            try:
                self.usd_try_percantal_ratio = getting_closer[1].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.usd_try_percantal_ratio = getting_closer[1].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.usd_try_percantal_ratio = "0.00"

            try:
                self.euro_try_percantal_ratio = getting_closer[2].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.euro_try_percantal_ratio = getting_closer[2].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.euro_try_percantal_ratio = "0.00"
    
            try:
                self.euro_usd_percantal_ratio = getting_closer[3].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.euro_usd_percantal_ratio = getting_closer[3].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.euro_usd_percantal_ratio = "0.00"
                
            self.dolar_try = currency_value_dolar[0].get_text()
            self.euro_try = currency_value_euro[0].get_text()
            self.euro_dolar = currency_value_eurusd[0].get_text()

            self.currency_table.setItem(0,0, QtWidgets.QTableWidgetItem("USD/TRY"))
            self.currency_table.setItem(0,1, QtWidgets.QTableWidgetItem(self.dolar_try))
            
            self.currency_table.setItem(1,0, QtWidgets.QTableWidgetItem("EUR/TRY"))
            self.currency_table.setItem(1,1, QtWidgets.QTableWidgetItem(self.euro_try))
            
            self.currency_table.setItem(2,0, QtWidgets.QTableWidgetItem("EUR/USD"))
            self.currency_table.setItem(2,1, QtWidgets.QTableWidgetItem(self.euro_dolar))
            
            self.currency_ratio_table.setItem(0,0, QtWidgets.QTableWidgetItem("USD/TRY"))
            self.currency_ratio_table.setItem(0,1, QtWidgets.QTableWidgetItem(self.usd_try_percantal_ratio))
            
            self.currency_ratio_table.setItem(1,0, QtWidgets.QTableWidgetItem("EURO/TRY"))
            self.currency_ratio_table.setItem(1,1, QtWidgets.QTableWidgetItem(self.euro_try_percantal_ratio))
            
            self.currency_ratio_table.setItem(2,0, QtWidgets.QTableWidgetItem("EURO/USD"))
            self.currency_ratio_table.setItem(2,1, QtWidgets.QTableWidgetItem(self.euro_usd_percantal_ratio))
            
            self.colorRatios() ## renklerimiz de yenilensin
        
        except ConnectionError:
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.setText("ERROR! No connection. Check your internet connection please.")
            self.msgBox.setWindowTitle("Critical")
            self.msgBox.exec_()
            
    def colorRatios(self):
        
        ## replace metodunu kullandık. Çünkü bir if sorgulaması ile gelen yüzdesel değişimlerin
        ## 0'dan büyüklüğünü küçüklüğünü sorgulamamız gerek. Gelen değerler %4,3 gibi geldiği için
        ## sorgulamada kullanamazdık. Dolayısıyla , yerine . replace ediyoruz.
        new_usd_try_ratio_temp = self.usd_try_percantal_ratio.replace("% ","")
        new_usd_try_ratio = new_usd_try_ratio_temp.replace(",",".")
        
        new_euro_try_ratio_temp = self.euro_try_percantal_ratio.replace("% ","")
        new_euro_try_ratio = new_euro_try_ratio_temp.replace(",",".")

        new_euro_usd_ratio_temp = self.euro_usd_percantal_ratio.replace("% ","")
        new_euro_usd_ratio = new_euro_usd_ratio_temp.replace(",",".")

        if float(new_usd_try_ratio) < 0:
            self.currency_ratio_table.item(0,1).setBackground(QtGui.QColor(100,0,0)) ## GREEN

        if float(new_euro_try_ratio) < 0:
            self.currency_ratio_table.item(1,1).setBackground(QtGui.QColor(100,0,0))

        if float(new_euro_usd_ratio) < 0:
            self.currency_ratio_table.item(2,1).setBackground(QtGui.QColor(100,0,0))
            
        if float(new_usd_try_ratio) > 0:
            self.currency_ratio_table.item(0,1).setBackground(QtGui.QColor(0,100,0)) ## RED

        if float(new_euro_try_ratio) > 0:
            self.currency_ratio_table.item(1,1).setBackground(QtGui.QColor(0,100,0))

        if float(new_euro_usd_ratio) > 0:
            self.currency_ratio_table.item(2,1).setBackground(QtGui.QColor(0,100,0))
            
        ## WHEN PERCENTAL CHANGE VALUE BE %0.00, THERE IS NO COLOR ASSIGNED.
        
app = QtWidgets.QApplication(sys.argv)
window = Window()
window.move(200, 120) ## pencerenin ekranda başlangıç yeri
app.setStyle("Fusion") ## stil ayarı (vazgeçilmezim)
window.setFixedSize(276, 235) ## boyut fixledik.
sys.exit(app.exec_())