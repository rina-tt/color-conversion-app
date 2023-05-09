import sys, os
import pathlib
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import cv2
import numpy as np

class MainWindow(QMainWindow):
    
    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        """ UIの初期化 """
        self.resize(1000, 500) # リサイズ
        self.setWindowTitle('間違い探し作成アプリ') # タイトル
        self.statusBar = QStatusBar()
        message = QLabel('画像をクリックして変更箇所を指定')
        self.statusBar.addWidget(message)
        self.setStatusBar(self.statusBar)
        self.original_img_path = False
        
        self.MakeMenubar()      #メニューバー作成
        self.MakeButtonSpace()  #ボタンスペース作成
        self.MakeImgSpace()     #画像表示スペース作成
        
        ### ボタンスペースと画像スペース縦につなげる
        view = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(self.button_space)
        vbox.addWidget(self.img_space)
        view.setLayout(vbox)
        
        ### MainWindowにセット
        self.setCentralWidget(view)
        self.show()
        
    def MakeMenubar(self):
        '''メニューバー作成'''
        def Openfile():
            # ファイルダイアログを呼び出し、選択したファイルのファイルパスを取得
            filepath = QFileDialog.getOpenFileName(self, 'open file')[0]
            #print("Openfile:",filepath)

            # 画像以外の時エラーメッセージ
            if self.original_img_space.SetImg(filepath) == False:
                QMessageBox.warning(self, "Warning", "画像ファイルを入力してください。")
                return
            # 画像ならoriginal_img_pathを更新
            self.original_img_path = filepath

            # 画像をセット
            if self.original_img_path:
                self.original_img_space.SetImg(self.original_img_path)

        def Saveimg():
            #保存
            filepath = QFileDialog.getSaveFileName(self, "save file")[0]
            filepath = str(pathlib.Path(filepath).with_suffix(".png"))
            saveimg = self.changed_img_space.changed_qimg #保存する画像
            saveimg.save(filepath)
                
        # (ファイルを)開くアクション
        openAction = QAction('&開く', self)
        openAction.triggered.connect(Openfile)        
        
        # 保存アクション
        saveAction = QAction('&保存', self)
        saveAction.triggered.connect(Saveimg)
        
        # メニューバーオブジェクトを取得
        self.menubar = self.menuBar()
        
        # ファイルメニュー
        fileMenu = self.menubar.addMenu('&ファイル')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        self.menubar.setNativeMenuBar(False) #macは必要
        
    def MakeButtonSpace(self):
        '''ボタンスペース作成'''
        def Start():
            if self.original_img_path == False:
                QMessageBox.warning(self, "Warning", "画像を指定していません。")
            elif self.original_img_space.view.zahyou == False:
                QMessageBox.warning(self, "Warning", "変更場所を指定していません。")
            else:
                self.changed_img_space.ChangeImg(1)

        def Noutan():
            if self.original_img_path == False:
                QMessageBox.warning(self, "Warning", "画像を指定していません。")
            elif self.original_img_space.view.zahyou == False:
                QMessageBox.warning(self, "Warning", "変更場所を指定していません。")
            else:
                self.changed_img_space.ChangeImg(2)

        def ShowAnswer():
            pass

        def Reset():
            self.menubar.clear() #メニューバー削除
            self.initUI()
            
        def showDialog():
            # カラー選択画面のダイアログ表示
            col = QColorDialog.getColor()
            # 選択された色をメインウィンドウへ表示
            if col.isValid():
                self.col_btn.setStyleSheet("QWidget { background-color: %s }" % col.name())  
                self.red = int(col.name()[1:3], 16)
                self.green = int(col.name()[3:5], 16)
                self.blue = int(col.name()[5:7], 16)
        
        self.button_space = QWidget()
        
        # 実行ボタン
        self.start_button = QPushButton('任意の色に変更') 
        self.start_button.clicked.connect(Start)
        self.noutan_button = QPushButton('濃淡変換')
        self.noutan_button.clicked.connect(Noutan) 
        
        # リセットボタン
        self.reset_button = QPushButton('リセット')
        self.reset_button.clicked.connect(Reset)      
        
        # 実行＆リセットを縦に連結
        vbox = QVBoxLayout()
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.noutan_button)
        vbox.addWidget(self.reset_button)
        
        # 正解表示チェックボックス
        self.ans_check = QCheckBox("正解表示")
        self.ans_check.clicked.connect(ShowAnswer) 
        
        # 間違い数選択
        self.miss_combo = QComboBox()
        for i in range(1,6):           #纏めて設定できるように変更
            self.miss_combo.addItem(str(i))
        self.miss_label = QLabel("間違い数")
        
        miss_space = QHBoxLayout()
        miss_space.addWidget(self.miss_label)
        miss_space.addWidget(self.miss_combo)

        # 色の初期設定（黒にする）
        col_space = QHBoxLayout()
        self.col_label = QLabel("色変更")
        col = QtGui.QColor(0, 0, 0) 
        self.col_btn = QPushButton()
        self.col_btn.clicked.connect(showDialog)
        self.col_btn.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.red = int(col.name()[1:3], 16)
        self.green = int(col.name()[3:5], 16)
        self.blue = int(col.name()[5:7], 16)
        col_space.addWidget(self.col_label)
        col_space.addWidget(self.col_btn)
        
        #一番右のスペース
        right_space = QVBoxLayout()
        right_space.addLayout(miss_space)
        right_space.addLayout(col_space)
        
        # 横に連結
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox) #実行＆リセット
        hbox.addStretch(1)
        hbox.addWidget(self.ans_check) #正解表示
        hbox.addStretch(1)
        hbox.addLayout(right_space) #間違い数
        hbox.addStretch(1)
        self.button_space.setLayout(hbox) #ボタンスペースの作成
        
    def MakeImgSpace(self):
        '''画像表示スペース作成'''
        self.img_space = QWidget()
        self.original_img_space = ImgSpace(self,1) #元画像
        self.changed_img_space = ImgSpace(self,0)  #加工後画像 
        
        # 横に連結
        hbox = QHBoxLayout()
        hbox.addWidget(self.original_img_space) #元画像
        self.arrow = QLabel("→")
        hbox.addWidget(self.arrow)
        hbox.addWidget(self.changed_img_space)  #加工後画像
        self.img_space.setLayout(hbox) #画像スペースの作成
        
    
class ImgSpace(QWidget):
    def __init__(self,parent,original): #original = 元画像領域なら1,加工後領域なら0
        """ ImgSpaceのインスタンスが生成されたときに呼び出されるメソッド """
        super(ImgSpace, self).__init__()
        self.parent = parent #MainWindowのこと
        self.original= original 
        
        # canvasのレイアウト
        self.canvas_layout = QGridLayout()
        
        # canvas_layoutをQWidget(self)にセット
        self.setLayout(self.canvas_layout)

        # 画像を表示するためのviewをレイアウトにセット
        widget = QWidget(None)
        self.view = MyGraphicsView(self.parent, widget)

        # original = 1 のときはMyScene呼び出し、そうでないときはQGraphicsSceneを呼び出す
        if self.original == 1:
            self.scene = MyScene(self,self.parent)#引数に自クラスselfと親クラスMainWindow
            self.text = QGraphicsTextItem("Drag and drop a file here")
            self.scene.addItem(self.text)
            self.original_img = QtGui.QImage()
        else:
            self.scene = QGraphicsScene()
            self.changed_img = QtGui.QImage()
            
        self.view.setScene(self.scene)  
        self.canvas_layout.addWidget(self.view)


    def SetImg(self,filepath):
        changed_img = QtGui.QImage()

        # 画像ファイルの読み込み
        if not self.original_img.load(filepath):
            return False
        changed_img.load(filepath) #changed_imgに画像の内容を保存(追加分)
        
        #print("SetImg:",filepath)

        def qimage_to_cv(qimage):
            w, h, d = qimage.size().width(), qimage.size().height(), qimage.depth()
            bytes_ = qimage.bits().asstring(w * h * d // 8)
            arr = np.frombuffer(bytes_, dtype=np.uint8).reshape((h, w, d // 8))
            return arr

        #透過部分白塗り
        def white(img):
            # columnとrowがそれぞれ格納されたタプル(長さ２)となっている
            index = np.where(img[:, :, 3] == 0)
            white_img = img.copy()
            # 白塗りする
            white_img[index] = [255, 255, 255, 255]
            return white_img
        
        #qimageをcvに変換、透過部分を白塗り
        changed_img = white(qimage_to_cv(changed_img)) 
        #カラー画像のときは、RGBからBGRへ変換する
        if changed_img.ndim == 3:
            changed_img = cv2.cvtColor(changed_img, cv2.COLOR_RGB2BGR) 
        self.parent.changed_img_space.changed_img =changed_img

        # sceneの初期化
        self.scene.clear()        
        # QImage -> QPixmap
        self.pixmap = QtGui.QPixmap.fromImage(self.original_img)        
        # pixmapをsceneに追加
        self.scene.addPixmap(self.pixmap)
        # ウィジェットを更新
        self.update()
        
    def ChangeImg(self, mode = 1):
        #print("実行")
        #print(self.parent.original_img_space.view.zahyou)
        self.point = self.parent.original_img_space.view.zahyou
        
        def cv_to_qimage(cv_image):
            height, width, bytesPerComponent = cv_image.shape
            bytesPerLine = bytesPerComponent * width
            cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB, cv_image)
            image = QtGui.QImage(cv_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            return image

        #色を変える領域の決定
        def color_change_region(img):
            # エッジ検出
            img = cv2.Canny(img, 50, 110)
            # カーネルを作成する。
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
            # 2値画像を収縮する。
            img = cv2.dilate(img, kernel)

            #輪郭抽出
            h, w = img.shape
            mask = np.zeros((h+2, w+2), np.uint8)
            retval,img,mask,rect = cv2.floodFill(img, mask, (int(self.point[0]),int(self.point[1])), 100)#変更位置
            return img

        #色を変える/濃淡変換
        def change(original,edges):
            edges=color_change_region(edges)
            img=original.copy() #エラーが出たのでcopyを追加
            h, w ,x = img.shape
            for i in range(h):
                for j in range(w):
                    if edges[i,j]==100:
                        if mode == 1:
                            img[i,j]=[self.parent.red,self.parent.green,self.parent.blue]#色
                        elif mode == 2:
                            img[i,j] = img[i,j]//5*4
            return img
        
        edges = cv2.cvtColor(self.changed_img, cv2.COLOR_BGR2GRAY)
        #選択領域色変更andRGBからBGRに変換
        self.changed_img = cv2.cvtColor(change(self.changed_img,edges) , cv2.COLOR_RGB2BGR) 

        #cvをqimageに変換
        self.changed_qimg = cv_to_qimage(self.changed_img)
        # sceneの初期化
        self.scene.clear()        
        # QImage -> QPixmap
        self.pixmap = QtGui.QPixmap.fromImage(self.changed_qimg)  
        # pixmapをsceneに追加
        self.scene.addPixmap(self.pixmap)
        # ウィジェットを更新
        self.update()

class MyScene(QGraphicsScene):
    def __init__(self,parent,window): #parent(ImgSpace)とMainwindowクラス
        """ MySceneのインスタンスが生成されたときに呼び出されるメソッド """
        super(MyScene, self).__init__()
        self.parent = parent
        self.window = window # MainWindowの変数や関数を参照するため
        
    def dragEnterEvent(self, e): #ドラッグされたとき
        mimeData = e.mimeData()

        # パスの有無で判定
        if mimeData.hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e): #ドロップされたとき
        # ファイルパス取得
        urls = e.mimeData().urls()
        filepath = urls[0].toLocalFile()
        #print("dropEvent:",filepath)       
        
        # 画像以外の時エラーメッセージ
        self.img = QtGui.QImage()
        if self.img.load(filepath) == False:
            # MainWindowクラスにおいて表示
            QMessageBox.warning(self.window, "Warning", "画像ファイルを入力してください。")
            return
        
        # 画像ファイルならoriginal_img_pathを更新
        self.window.original_img_path = filepath

        # 画像をセット
        if self.window.original_img_path:
            self.window.original_img_space.SetImg(self.window.original_img_path)
        
    def dragMoveEvent(self, e): #ドラッグの受け入れに必要
        e.acceptProposedAction()

#拡大縮小・クリック座標取得
class MyGraphicsView(QGraphicsView):
    def __init__(self, window, *argv, **keywords):
        super(MyGraphicsView, self).__init__(*argv, **keywords)
        self._numScheduledScalings = 0
        self.coordinates = []
        self.zahyou = False
        self.window = window

    def wheelEvent(self, event):
        numDegrees = event.angleDelta().y() / 8
        numSteps = numDegrees / 15
        self._numScheduledScalings += numSteps
        if self._numScheduledScalings * numSteps < 0:
            self._numScheduledScalings = numSteps
        anim = QtCore.QTimeLine(350, self)
        anim.setUpdateInterval(20)
        anim.valueChanged.connect(self.scalingTime)
        anim.finished.connect(self.animFinished)
        anim.start()

    def scalingTime(self, x):
        factor = 1.0 + float(self._numScheduledScalings) / 300.0
        self.scale(factor, factor)

    def animFinished(self):
        if self._numScheduledScalings > 0:
            self._numScheduledScalings -= 1
        else:
            self._numScheduledScalings += 1

    def mousePressEvent(self, event):
        p = self.mapToScene(event.pos())
        
        if event.button() == QtCore.Qt.MidButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)

            event = QtGui.QMouseEvent(
                QtCore.QEvent.GraphicsSceneDragMove, 
                event.pos(), 
                QtCore.Qt.MouseButton.LeftButton, 
                QtCore.Qt.MouseButton.LeftButton, 
                QtCore.Qt.KeyboardModifier.NoModifier
                )

        elif event.button() == QtCore.Qt.LeftButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)

        self.coordinates = [p.x(), p.y()]
        QGraphicsView.mousePressEvent(self, event)
   
    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)
        self.setDragMode(QGraphicsView.NoDrag)
        if event.button() == QtCore.Qt.LeftButton:
            p = self.mapToScene(event.pos())
            self.coordinates.extend([p.x(), p.y()])
            #取得した座標の表示
            #text = 'select area : ' + ','.join([ str(int(c)) for c in self.coordinates])

            self.zahyou = self.coordinates[0:2] #クリックした瞬間の座標のみ（coordinatesは放した瞬間の座標も含む）
            
            message = QLabel('画像をクリックして変更箇所を指定  ' + 'select_point：' + str(self.zahyou[0]) + ', ' + str(self.zahyou[1]))
            self.window.statusBar = QStatusBar()
            self.window.statusBar.addWidget(message)
            self.window.setStatusBar(self.window.statusBar)
        
def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()

if __name__ == '__main__':
    main()
