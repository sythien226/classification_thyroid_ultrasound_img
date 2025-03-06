from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
import tkinter as tk
from tkinter import filedialog
import sys
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import tensorflow as tf

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(951, 670)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(10)

        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("UTM Akashi")
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setMouseTracking(False)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setFixedSize(800, 600)  # Đặt kích thước cố định cho QLabel
        self.verticalLayout.addWidget(self.label_2, alignment=QtCore.Qt.AlignCenter)

        self.horizontalLayout = QHBoxLayout()
        self.input = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("UTM Akashi")
        font.setPointSize(10)
        self.input.setFont(font)
        self.input.setObjectName("input")
        self.horizontalLayout.addWidget(self.input)

        self.output = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("UTM Akashi")
        font.setPointSize(10)
        self.output.setFont(font)
        self.output.setObjectName("output")
        self.horizontalLayout.addWidget(self.output)

        self.resultLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("UTM Akashi")
        font.setPointSize(10)
        self.resultLabel.setFont(font)
        self.resultLabel.setObjectName("resultLabel")
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.resultLabel.setFixedSize(200, 30)
        self.horizontalLayout.addWidget(self.resultLabel)

        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 951, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Kết nối các nút với các hàm xử lý
        self.input.clicked.connect(self.load_image)
        self.output.clicked.connect(self.show_result)

        # Load the trained model
        self.model = load_model('D:/web_demo/demo/model.keras')


    def retranslateUi(self, MainWindow):
        #cập nhật các văn bản h thị trên các widget trong giao diện ng dùng
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Công cụ phân loại u nang tuyến giáp"))
        self.input.setText(_translate("MainWindow", "Load Image"))
        self.output.setText(_translate("MainWindow", "Result"))

    def load_image(self):
        # Sử dụng Tkinter để mở hộp thoại chọn file
        root = tk.Tk()
        root.withdraw()  # Ẩn cửa sổ Tkinter chính
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            # Hiển thị ảnh đã chọn trên QLabel với kích thước lớn hơn
            pixmap = QPixmap(self.file_path)
            self.label_2.setPixmap(pixmap.scaled(self.label_2.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            # Reset resultLabel
            self.resultLabel.setText("")

    def preprocess_image(self, image_path):
        img = load_img(image_path, target_size=(299, 299))
        img_array = img_to_array(img)/255.0
        img_array = np.expand_dims(img_array, axis=0)  # Thêm chiều batch
        return img_array

    def show_result(self):
        if hasattr(self, 'file_path'):
            img = self.preprocess_image(self.file_path)
            predictions = self.model.predict(img).flatten()
            predictions = tf.nn.sigmoid(predictions)  # Áp dụng hàm sigmoid
            prediction = tf.where(predictions < 0.6, 0, 1).numpy()[0]  # Điều chỉnh ngưỡng giống như trong code kiểm thử
            result = 'Lành tính' if prediction == 0 else 'Ác tính'
            self.resultLabel.setText(f"Kết quả: {result}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
