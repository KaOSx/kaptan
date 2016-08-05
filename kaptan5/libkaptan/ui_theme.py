from PyQt5.QtWidgets import QWizardPage, QLabel, QGroupBox, QCheckBox, QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout,\
    QSpinBox, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from os.path import join
import os
from .tools import Parser
from .tabwidget import ThemeTabWidget

class ThemeWidget(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSubTitle(self.tr("<h2>Customize Your Desktop</h2>"))

        vlayout = QVBoxLayout(self)

        labelLayout = QHBoxLayout()
        imageLabel = QLabel()
        imageLabel.setMaximumSize(64, 64)
        imageLabel.setPixmap(QIcon.fromTheme("preferences-desktop-color").pixmap(64, 64))
        labelLayout.addWidget(imageLabel)

        label = QLabel(self)
        label.setText(self.tr("<p>Choose your favorite theme and desktop type. Customize KaOS with different styles and themes.</p>"))
        labelLayout.addWidget(label)
        vlayout.addLayout(labelLayout)

        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.createGroupBox(vlayout)
        self.createDesktopOption(vlayout)

        self.desktopCount = 2
        self.desktopType = "org.kde.desktopcontainment"
        self.iconSet = None
        self.showDesktop = False
        self.widgetStyle = "qtcurve"
        self.windowStyle = None
        self.colorScheme = None
        self.desktopTheme = None


    def createGroupBox(self, layout):
        group1 = QGroupBox(self)
        group1.setMinimumHeight(200)
        layout.addWidget(group1)

        grLayout = QVBoxLayout(group1)
        tabWidget = ThemeTabWidget(group1)
        grLayout.addWidget(tabWidget)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))

        tabWidget.listWidgetIconSet.itemClicked.connect(self.iconSetSelect)
        tabWidget.listWidgetWindowStyle.itemClicked.connect(self.windowStyleSelect)
        tabWidget.comboBoxWidgetStyle.currentIndexChanged[str].connect(self.widgetStyleSelect)
        tabWidget.listWidgetDesktopTheme.itemClicked.connect(self.desktopThemeSelect)
        tabWidget.listWidgetColorScheme.itemClicked.connect(self.colorSchemeSelect)


    def createDesktopOption(self, layout):
        hlayout = QHBoxLayout()
        layout.addLayout(hlayout)

        vlayout1 = QVBoxLayout()
        vlayout2 = QVBoxLayout()
        hlayout.addLayout(vlayout1)
        hlayout.addLayout(vlayout2)

        label1 = QLabel()
        label1.setText(self.tr("Desktop Type"))
        vlayout1.addWidget(label1)
        label2 = QLabel()
        label2.setText(self.tr("Number of Desktops"))
        vlayout2.addWidget(label2)

        comboBox = QComboBox()
        comboBox.addItem(self.tr("Desktop View"))
        comboBox.addItem(self.tr("Folder View"))
        comboBox.currentIndexChanged.connect(self.desktopTypeCreate)
        vlayout1.addWidget(comboBox)
        spinBox = QSpinBox()
        spinBox.setMinimum(2)
        spinBox.setMaximum(20)
        spinBox.valueChanged.connect(self.desktopCreate)
        vlayout2.addWidget(spinBox)
        self.checkBox = QCheckBox()
        self.checkBox.setText(self.tr("Add Show Desktop Plasmoid"))
        self.checkBox.clicked.connect(self.showDesktopF)
        hlayout.addWidget(self.checkBox)

    def windowStyleSelect(self, item):
        self.windowStyle = item.setStyleText

    def widgetStyleSelect(self, text):
        self.widgetStyle = text.lower()

    def desktopThemeSelect(self, item):
        self.desktopTheme = item.panelText

    def colorSchemeSelect(self, item):
        self.colorScheme = item.colorSchemeName

    def showDesktopF(self):
        self.showDesktop = self.checkBox.isChecked()

    def iconSetSelect(self, item):
        self.iconSet = str(item.text()).lower()

    def desktopCreate(self, value):
        self.desktopCount = value

    def desktopTypeCreate(self, value):
        if value == 0:
            self.desktopType = "org.kde.desktopcontainment"
        else:
            self.desktopType = "org.kde.plasma.folder"

    def execute(self):
        settings = QSettings(join(QDir.homePath(), ".config", "kwinrc"), QSettings.IniFormat)
        settings.setValue("Desktops/Number", self.desktopCount)
        settings.setValue("Desktops/Rows", 2)
        settings.sync()

        if self.iconSet != None:
            settings = QSettings(join(QDir.homePath(), ".config", "kdeglobals"), QSettings.IniFormat)
            settings.setValue("Icons/Theme", self.iconSet)
            settings.sync()

            os.system("rm -rf {}".format(join(QDir.homePath(), ".cache", "icon-cache.kcache")))

        if self.widgetStyle != None:
            settings = QSettings(join(QDir.homePath(), ".config", "kdeglobals"), QSettings.IniFormat)
            settings.setValue("KDE/widgetStyle", self.widgetStyle.lower())
            settings.sync()

        if self.windowStyle != None:
            settings = QSettings(join(QDir.homePath(), ".config", "kwinrc"), QSettings.IniFormat)
            settings.setValue("org.kde.kdecoration2/library", self.windowStyle)
            settings.sync()
        if self.windowStyle == "org.kde.kwin.aurorae":
            settings = QSettings(join(QDir.homePath(), ".config", "kwinrc"), QSettings.IniFormat)
            settings.setValue("org.kde.kdecoration2/theme", self.windowTheme)
            settings.sync()

            prc = QProcess()
            prc.startDetached("kwin_x11 --replace") 

        if self.desktopTheme != None:
            settings = QSettings(join(QDir.homePath(), ".config", "plasmarc"), QSettings.IniFormat)
            settings.setValue("Theme/name", self.desktopTheme)
            settings.sync()

        if self.colorScheme != None:
            colorSettings = QSettings(join("/usr/share/color-schemes", self.colorScheme), QSettings.IniFormat)
            colorParameter = colorSettings.allKeys()
            print(join("/usr/share/color-schemes", self.colorScheme))
            settings = QSettings(join(QDir.homePath(), ".config", "kdeglobals"), QSettings.IniFormat)
            for parameter in colorParameter:
                print(parameter, colorSettings.value(parameter))
                settings.setValue(parameter, colorSettings.value(parameter))

            settings.sync()

            with open(join(QDir.homePath(), ".config", "kdeglobals"), "r+") as rep:
                cache = rep.read().replace("%3A", ":")
                rep.seek(0)
                rep.truncate()
                rep.write(cache)

        configFilePath = join(QDir.homePath(), ".config", "plasma-org.kde.plasma.desktop-appletsrc")

        parser = Parser(configFilePath)
        desktopView = parser.getDesktopType()

        if self.desktopType != desktopView[1]:
            parser.setDesktopType(self.desktopType)

        if self.showDesktop:
            parser.setShowDesktopApplet()
