from PyQt5.QtWidgets import QWizardPage, QLabel, QGroupBox, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import webbrowser


class OtherWidget(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSubTitle(self.tr("<h2>Congratulations!</h2>"))

        self.homepage_url = "https://kaosx.us/"
        self.forum_url = "http://kaosx.us/about/contact/"
        self.wiki_url = "http://kaosx.us/docs/"

        vlayout = QVBoxLayout(self)

        label = QLabel(self)
        label.setWordWrap(True)
        label.setText(self.tr("<p><strong>Your settings have been applied.</strong> Now you can start enjoying KaOS. \
        Don't forget to <strong>join our community!</strong></p>"))
        vlayout.addWidget(label)

        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))

        groupBox1 = QGroupBox()
        groupBox1.setTitle(self.tr("System Settings"))
        groupBox1.setMinimumHeight(150)

        groupHLayout1 = QHBoxLayout(groupBox1)
        groupLabelImage = QLabel()
        groupLabelImage.setPixmap(QIcon.fromTheme("preferences-system").pixmap(64, 64))
        groupLabelImage.setMaximumSize(64,64)
        groupHLayout1.addWidget(groupLabelImage)
        groupLabel1 = QLabel()
        groupLabel1.setWordWrap(True)
        groupLabel1.setText(self.tr("<p>Configuration tools for KaOS such as the display, network, keyboard, user manager...</p>"))
        groupButton1 = QPushButton()
        groupButton1.setMaximumWidth(200)
        groupButton1.setText(self.tr("System Settings"))

        groupHLayout1.addWidget(groupLabel1)
        groupHLayout1.addItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Preferred))
        groupHLayout1.addWidget(groupButton1)

        vlayout.addWidget(groupBox1)

        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))

        groupBox2 = QGroupBox()
        groupBox2.setTitle(self.tr("Help and Support"))
        groupBox2.setMinimumHeight(150)

        groupHLayout2 = QHBoxLayout(groupBox2)
        groupLabelImage2 = QLabel()
        groupLabelImage2.setPixmap(QIcon.fromTheme("system-help").pixmap(64, 64))
        groupHLayout2.addWidget(groupLabelImage2)
        groupLabelImage2.setMaximumSize(64,64)
        groupLabel2 = QLabel()
        groupLabel2.setWordWrap(True)
        groupLabel2.setText(self.tr("<p>KaOS community, mailing lists, chat rooms, documents, help and support pages...</p>"))
        groupButton2 = QPushButton()
        groupButton2.setMaximumWidth(200)
        groupButton2.setText(self.tr("Help and Support"))

        groupHLayout2.addWidget(groupLabel2)
        groupHLayout2.addItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Preferred))
        groupHLayout2.addWidget(groupButton2)

        vlayout.addWidget(groupBox2)

        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))

        groupButton2.clicked.connect(self.helpPagesOpen)
        groupButton1.clicked.connect(self.systemSettingsOpen)

    def helpPagesOpen(self):
        webbrowser.open_new_tab(self.homepage_url)
        webbrowser.open_new_tab(self.forum_url)
        webbrowser.open_new_tab(self.wiki_url)
        """QDesktopServices.openUrl(QUrl(self.homepage_url))
        QDesktopServices.openUrl(QUrl(self.forum_url))
        QDesktopServices.openUrl(QUrl(self.wiki_url))"""

    def systemSettingsOpen(self):
        procSettings = QProcess()
        procSettings.startDetached("systemsettings5")
