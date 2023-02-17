import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore,QtGui

from PyQt5.QtGui import QPalette





import cv2
import numpy as np 


class MainWindow(QWidget):
    weight=230
    def __init__(self):
        super().__init__()        
        self.setGeometry(800, 370, 330, 500)
        
        self.globalLayout = QVBoxLayout(self)
        self.Label=QLabel(self)
        self.feedLabel = QLabel(self)
        self.saga_kaydir_btn=QPushButton("", self)
        self.sola_kaydir_btn=QPushButton("", self)
        self.start_btn=QPushButton("", self)
        self.cancel_btn = QPushButton("", self)
        self.foto_cek_btn=QPushButton("", self)
        
        self.select_camera=QComboBox(self)
        
        self.start_btn.setIcon(QIcon("Start-icon.png"))
        self.cancel_btn.setIcon(QIcon("stop.png"))
        self.sola_kaydir_btn.setIcon(QIcon("sol.png"))
        self.saga_kaydir_btn.setIcon(QIcon("sag.png"))
        self.foto_cek_btn.setIcon(QIcon("kamera.png"))
               
        buttons_widget=QWidget(self)
        buttons_layout=QHBoxLayout(buttons_widget)
        

        buttons_layout.addWidget(self.start_btn,alignment=Qt.AlignBottom)
        buttons_layout.addWidget(self.cancel_btn,alignment=Qt.AlignBottom)
        buttons_layout.addWidget(self.foto_cek_btn,alignment=Qt.AlignBottom)
        buttons_layout.addWidget(self.select_camera,alignment=Qt.AlignBottom)
        buttons_layout.addWidget(self.sola_kaydir_btn,alignment=Qt.AlignBottom)
        buttons_layout.addWidget(self.saga_kaydir_btn,alignment=Qt.AlignBottom)
  
        
       
        self.globalLayout.addWidget(self.Label,alignment=Qt.AlignCenter)

        self.globalLayout.addWidget(self.feedLabel,alignment=Qt.AlignCenter)
        


        ## Butonlarımızın tıklama eventine tanımladığımız fonksiyonları entegre ettik.

        self.globalLayout.addWidget(buttons_widget)
        
        self.setLayout(self.globalLayout)
        
        self.start_btn.clicked.connect(self.start_feed)
        self.cancel_btn.clicked.connect(self.stop_feed)
        
        
       
                
               
        # thread oluşturuldu

        self.thread = QThread()
        # worker oluşturuldu
        self.worker = Worker()
        #workeri thread e taşıdık.
        self.worker.moveToThread(self.thread)
        #methodları run lıyoruz
        self.thread.started.connect(self.worker.run)
    

        self.worker.imageUpdate.connect(self.set_new_img)
        
        self.worker.finished.connect(self.worker_done)
    
   
    def start_feed(self):
        #self.worker.camera=cv2.VideoCapture(0)

        self.worker.camera=cv2.VideoCapture("rtsp://192.168.1.10:554/user=admin&password=EXLXEXKX&channel=1&stream=0.sdp")
        self.worker.running=True
       
        # thread başlatılıyor.
        self.thread.start()


    def sola_kaydir(self):
        print("sola kaydırıldı.")
    def saga_kaydir(self):
        print("Saga kaydır")
    def stop_feed(self):
        self.worker.running = False
        
        
    def worker_done(self):
        print("Çalışan Uygulamlar kapandı")
        self.worker.camera.release()
        self.thread.quit()
        
    def thread_done(self):
        print("Program sonlandırıldı")
    def set_new_img(self,Image):
        
        print("Video akışı geliyor.")
        Image=Image.scaled(800, 410, QtCore.Qt.KeepAspectRatio)
        self.Label.setPixmap(QPixmap.fromImage(Image))          
        #self.feedLabel.setPixmap(QPixmap.fromImage(Image))    
    def foto_cek(self):
        print("foto cekildi")

class Worker(QObject):
    finished = pyqtSignal() # Main sayfa ile iletişim
    imageUpdate = pyqtSignal(QImage) 
   
    
    def __init__(self):
        super().__init__()
        self.camera=None
        self.running=None

        self._srcW = 1920   
        self._srcH = 1080       
        self._destW = 290   # 290 dan çekildi. 
        self._destH = 850                     # pencere size ayarları 
        
        self._zoom = 1
    
 





    def run(self):
        
        self._mapX=np.loadtxt("BetaX0.txt",delimiter=",",dtype=np.float32)
        self._mapY=np.loadtxt("Betay0.txt",delimiter=",",dtype=np.float32)
        
        def getImage(img):

            
            output=cv2.remap(img,self._mapX,self._mapY,cv2.INTER_LINEAR)
            return output



       

        while True:
                        
            ret, frame = self.camera.read() 

            if ret:
                frame=cv2.resize(frame,(1920,1080))
                Image=getImage(frame)
                Image=Image[70:Image.shape[0]-100,0:Image.shape[1]]
                print(Image.shape[0])
                print(Image.shape[1])

                ConvertToQtFormat = QImage(Image.data,Image.shape[1],Image.shape[0],3*Image.shape[1],QImage.Format_BGR888)

                self.imageUpdate.emit(ConvertToQtFormat)
                
      
        
        
if __name__ == "__main__":
    App = QApplication(sys.argv)

    Root = MainWindow()


    palette = Root.palette()
   # palette.setColor(QtGui.QPalette.Window, QtGui.QColor("orange"))
    Root.setPalette(palette)
    Root.show()
    sys.exit(App.exec())