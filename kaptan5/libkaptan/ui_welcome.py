import sys, os
from PyQt5.QtWidgets import QWizardPage, QLabel, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class WelcomeWidget(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSubTitle(self.tr("<h2>Welcome to KaOS</h2>"))

        vlayout = QVBoxLayout(self)
        vlayout.addItem(QSpacerItem(20, 30, QSizePolicy.Preferred, QSizePolicy.Minimum))

        hlayout = QHBoxLayout(self)
        label = QLabel(self)
        label.setText(self.tr("""<h1>What is KaOS?</h1>
        <p>The idea behind KaOS is to create a tightly integrated rolling and<br />
        transparent distribution for the modern desktop, build from scratch with<br />
        a very specific focus. Focus on one DE (KDE), one toolkit (Qt) & one architecture (x86_64).<br />
        Plus a focus on evaluating and selecting the most suitable tools and applications.</p>
        <p>This wizard will help you personalize your KaOS workspace easily and quickly.</p>
        <p>Please click <code style=color:#3498DB>Next</code> in order to begin. Click <code style=color:#3498DB>Cancel</code> anytime and changes won't be saved.</p>"""))
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft)
        hlayout.addWidget(label)

        kaptan_logo = QLabel(self)
        kaptan_logo.setPixmap(QPixmap(":/data/images/welcome.png"))
        kaptan_logo.setAlignment(Qt.AlignRight)
        kaptan_logo.setMaximumSize(157, 181)
        hlayout.addWidget(kaptan_logo)
        vlayout.addLayout(hlayout)

        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))
        
        desktop_file = os.path.join(os.environ["HOME"], ".config", "autostart", "kaptan.desktop")
        if os.path.exists(desktop_file):
            self.checkBox = QCheckBox()
            self.checkBox.setText(self.tr("Run on system startup"))
            self.checkBox.setChecked(True)
            self.checkBox.clicked.connect(self.autoRemove)
            vlayout.addWidget(self.checkBox)
        
    def autoRemove(self):
        self.autoRemove != self.checkBox.isChecked()
    
    def autoRemove(self):
        desktop_file = os.path.join(os.environ["HOME"], ".config", "autostart", "kaptan.desktop")
        if os.path.exists(desktop_file):
            os.remove(desktop_file)
        
