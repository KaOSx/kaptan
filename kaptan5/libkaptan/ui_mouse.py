from PyQt5.QtWidgets import QWizardPage, QLabel, QGroupBox, QRadioButton, QHBoxLayout, QVBoxLayout, QCheckBox, \
    QSpacerItem, QSizePolicy, QButtonGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

from os.path import join

class MouseWidget(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSubTitle(self.tr("<h2>Setup Mouse Behavior</h2>"))

        vlayout = QVBoxLayout(self)

        labelLayout = QHBoxLayout()
        imageLabel = QLabel()
        imageLabel.setPixmap(QIcon.fromTheme("preferences-desktop-mouse").pixmap(64, 64))
        imageLabel.setMaximumSize(64, 64)
        labelLayout.addWidget(imageLabel)

        mouseLabel = QLabel(self)
        mouseLabel.setText(self.tr("""<p>The <strong>clicking behavior</strong> defines how many times you want
        to click when you are opening a file. If you are <strong>left handed</strong>, you may prefer to
        swap the left and right buttons of your pointing device.</p>"""))
        mouseLabel.setWordWrap(True)
        labelLayout.addWidget(mouseLabel)
        vlayout.addLayout(labelLayout)

        vlayout.addItem(QSpacerItem(20, 100, QSizePolicy.Preferred, QSizePolicy.Preferred))

        hlayout = QHBoxLayout()
        vlayout.addLayout(hlayout)

        self.createGroupBox(hlayout)

        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))

        self.folderSingleClick = True
        self.mouseButtonMap = "RightHanded"
        self.reverseScrollPolarity = False


    def createGroupBox(self, layout):
        group1 = QGroupBox(self)
        group1.setTitle(self.tr("Clicking Behavior"))
        group1.setMinimumHeight(150)
        group1.setMaximumWidth(300)
        layout.addWidget(group1)

        vlayout1 = QVBoxLayout(group1)
        buttonGroup = QButtonGroup(group1)

        self.radiobutton1 = QRadioButton(group1)
        self.radiobutton1.setText(self.tr("Double-click to open files and folders."))
        self.radiobutton1.setChecked(False)
        vlayout1.addWidget(self.radiobutton1)

        self.radiobutton2 = QRadioButton(group1)
        self.radiobutton2.setText(self.tr("Single-click to open files and folders."))
        self.radiobutton2.setChecked(True)
        vlayout1.addWidget(self.radiobutton2)

        buttonGroup.addButton(self.radiobutton1)
        buttonGroup.addButton(self.radiobutton2)

        buttonGroup.buttonClicked.connect(self.folderClick)

        group2 = QGroupBox(self)
        group2.setTitle(self.tr("Button Order"))
        group2.setMinimumHeight(150)
        group2.setMaximumWidth(300)
        layout.addWidget(group2)

        vlayout2 = QVBoxLayout(group2)
        buttonGroup2 = QButtonGroup(group2)

        self.radiobutton3 = QRadioButton(group2)
        self.radiobutton3.setText(self.tr("Right hand."))
        self.radiobutton3.setChecked(True)
        vlayout2.addWidget(self.radiobutton3)

        self.radiobutton4 = QRadioButton(group2)
        self.radiobutton4.setText(self.tr("Left hand."))
        vlayout2.addWidget(self.radiobutton4)

        buttonGroup2.addButton(self.radiobutton3)
        buttonGroup2.addButton(self.radiobutton4)

        buttonGroup2.buttonClicked.connect(self.mouseButton)

        self.checkbox = QCheckBox(group2)
        self.checkbox.setText(self.tr("Reverse scrolling."))
        self.checkbox.clicked.connect(self.reverseScroll)
        vlayout2.addWidget(self.checkbox)

    def folderClick(self, button):
        if button == self.radiobutton1:
            self.folderSingleClick = False
        else:
            self.folderSingleClick = True

    def mouseButton(self, button):
        if button == self.radiobutton3:
            self.mouseButtonMap = "RightHanded"
        else:
            self.mouseButtonMap = "LeftHanded"

    def reverseScroll(self):
        if self.checkbox.isChecked():
            self.reverseScrollPolarity = True
        else:
            self.reverseScrollPolarity = False

    def execute(self):
        settings1 = QSettings(join(QDir.homePath(), ".config", "kcminputrc"), QSettings.IniFormat)
        settings2 = QSettings(join(QDir.homePath(), ".config", "kdeglobals"), QSettings.IniFormat)

        settings1.setValue("Mouse/MouseButtonMapping", self.mouseButtonMap)
        settings1.setValue("Mouse/ReverseScrollPolarity", self.reverseScrollPolarity)
        settings1.sync()

        settings2.setValue("KDE/SingleClick", self.folderSingleClick)
        settings2.sync()
