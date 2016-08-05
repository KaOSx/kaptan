from PyQt5.QtWidgets import QWizardPage, QLabel, QGroupBox, QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout,\
    QComboBox, QPushButton, QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtMultimedia import QCamera, QCameraInfo, QCameraImageCapture, QCameraImageProcessing

import os
import shutil


class AvatarWidget(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSubTitle(self.tr("<h2>Create Your Avatar</h2>"))

        vlayout = QVBoxLayout(self)

        labelLayout = QHBoxLayout()
        labelImage = QLabel()
        labelImage.setPixmap(QIcon.fromTheme("preferences-desktop-user").pixmap(64, 64))
        labelImage.setMaximumSize(64, 64)
        labelLayout.addWidget(labelImage)

        label = QLabel(self)
        label.setWordWrap(True)
        label.setText(self.tr("<p>This screen helps you set your <strong>user picture</strong>. You can either choose an image from a \
        file or you can capture an image from your camera. Select an option from the <strong>options</strong> menu.</p>"))
        labelLayout.addWidget(label)
        vlayout.addLayout(labelLayout)

        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))

        centerLayout = QHBoxLayout()
        centerLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Preferred))

        groupBox = QGroupBox()
        groupBox.setMaximumWidth(500)
        vlayout2 = QVBoxLayout(groupBox)
        hlayout = QHBoxLayout()

        comboBox = QComboBox()
        comboBox.setMinimumWidth(250)
        comboBox.addItems([self.tr("Options"), self.tr("Choose an image...")])

        #Camera control
        self.cameraInfo = None
        self.camera = None
        self.cameraImageCapture = None
        cameras = QCameraInfo.availableCameras()

        if len(cameras):
            self.cameraInfo = cameras[0]
            comboBox.addItem(self.tr("Camera ") + self.cameraInfo.deviceName())
            self.camera = QCamera(self.cameraInfo)
            self.camera.setCaptureMode(QCamera.CaptureStillImage)
            self.cameraImageCapture = QCameraImageCapture(self.camera)
            self.imageProcessing = self.camera.imageProcessing()
            self.imageProcessing.setWhiteBalanceMode(QCameraImageProcessing.WhiteBalanceSunlight)
            self.imageProcessing.setContrast(1)
            self.imageProcessing.setSaturation(1)
            self.imageProcessing.setSharpeningLevel(1)
            self.imageProcessing.setDenoisingLevel(1)
            #self.imageProcessing.setColorFilter(QCameraImageProcessing.ColorFilterWhiteboard) #FIXME Qt5.5
            self.cameraImageCapture.imageCaptured.connect(self.imageCapture)

        self.buttonCam = QPushButton()
        self.buttonCam.setText(self.tr("Capture"))
        self.buttonCam.setIcon(QIcon.fromTheme("camera-web"))
        self.buttonCam.setVisible(False)

        self.buttonReplay = QPushButton()
        self.buttonReplay.setText(self.tr("Recapture"))
        self.buttonReplay.setIcon(QIcon.fromTheme("view-refresh"))
        self.buttonReplay.setVisible(False)

        hlayout.addWidget(comboBox)
        hlayout.addItem(QSpacerItem(300, 20, QSizePolicy.Preferred, QSizePolicy.Preferred))
        hlayout.addWidget(self.buttonCam)
        hlayout.addWidget(self.buttonReplay)

        vlayout2.addLayout(hlayout)

        hlayout2 = QHBoxLayout()

        hlayout2.addItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Preferred))

        self.cameraLabel = QLabel()
        self.cameraLabel.setScaledContents(True)
        self.cameraLabel.setStyleSheet("background-color: black;")
        self.cameraLabel.setMinimumSize(320, 240)
        self.cameraLabel.setMaximumSize(320, 240)

        self.cameraView = QCameraViewfinder()
        self.cameraView.setMaximumSize(320,240)
        self.cameraView.setMinimumSize(320,240)
        self.cameraView.hide()

        hlayout2.addWidget(self.cameraLabel)
        hlayout2.addWidget(self.cameraView)

        hlayout2.addItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Preferred))
        vlayout2.addLayout(hlayout2)

        centerLayout.addWidget(groupBox)
        centerLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Preferred))
        vlayout.addLayout(centerLayout)
        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))

        comboBox.currentIndexChanged.connect(self.avatarSelect)
        self.buttonCam.clicked.connect(self.buttonCamChanged)
        self.buttonReplay.clicked.connect(self.buttonReplayChanged)

        self.userAvatar = None

    def avatarSelect(self, index):
        if index == 0:
            if self.camera != None:
                self.camera.stop()
            self.buttonReplay.hide()
            self.buttonCam.hide()
            self.cameraView.hide()
            self.cameraLabel.show()
        elif index == 1:
            if self.camera != None:
                self.camera.stop()
            self.userAvatar = None
            self.buttonReplay.hide()
            self.buttonCam.hide()
            self.cameraView.hide()
            self.cameraLabel.show()
            file_url, file_type = QFileDialog.getOpenFileName(self, self.tr("Choose Avatar"), QDir.homePath(), "Image (*.png *.jpg)")
            if file_url != "":
                p = QPixmap(file_url)
                self.cameraLabel.setPixmap(p)
                self.userAvatar = file_url
        elif index == 2:
            self.userAvatar = None
            self.cameraLabel.hide()
            self.cameraView.show()
            self.camera.setViewfinder(self.cameraView)
            self.camera.start()
            self.buttonCam.setVisible(True)
            self.buttonReplay.hide()

    def buttonCamChanged(self):
        self.buttonCam.hide()
        self.buttonReplay.show()
        self.camera.searchAndLock()
        self.cameraImageCapture.capture("/tmp/avatar")
        self.camera.unlock()
        self.userAvatar = "/tmp/avatar.jpg"

    def buttonReplayChanged(self):
        self.userAvatar = None
        self.buttonReplay.hide()
        self.buttonCam.show()
        self.camera.start()
        self.cameraLabel.hide()
        self.cameraView.show()

    def imageCapture(self, id, preview):
        pixmap = QPixmap.fromImage(preview)
        self.camera.stop()
        self.cameraView.hide()
        self.cameraLabel.show()
        self.cameraLabel.setPixmap(pixmap)

    def execute(self):
        try:
            if self.userAvatar:
                if os.path.exists(os.path.join(os.environ["HOME"], ".face.icon")):
                    os.remove(os.path.join(os.environ["HOME"], ".face.icon"))
                shutil.copy(self.userAvatar, os.path.join(os.environ["HOME"], ".face.icon"))
                os.remove(self.userAvatar)
        except:
            with open("/tmp/.kaptan.bug", "w") as d:
                d.write("avatar değiştirilemedi.")
                d.close()