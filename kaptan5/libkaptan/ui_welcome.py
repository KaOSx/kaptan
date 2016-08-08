from PyQt5.QtWidgets import QWizardPage, QLabel, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class WelcomeWidget(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSubTitle(self.tr("<h2>Welcome to KaOS</h2>"))

        vlayout = QVBoxLayout(self)
        vlayout.addItem(QSpacerItem(20, 150, QSizePolicy.Preferred, QSizePolicy.Minimum))

        hlayout = QHBoxLayout(self)
        label = QLabel(self)
        label.setText(self.tr("""<h1>What is KaOS?</h1>
        The idea behind KaOS is to create a tightly integrated rolling and<p>
        transparent distribution for the modern desktop, build from scratch with<p>
        a very specific focus. Focus on one DE (KDE), one toolkit (Qt) & one architecture (x86_64).<p>
        Plus a focus on evaluating and selecting the most suitable tools and applications.</p>
        This wizard will help you personalize your KaOS workspace easily and quickly.<p>
        Please click <i>Next</i> in order to begin. Click <i>Cancel</i> anytime and changes won't be saved,</p>
        click <i>close window</i> or <i>Close</i> and the wizard won't autostart any longer.</p>"""))
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
