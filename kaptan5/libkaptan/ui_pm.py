from PyQt5.QtWidgets import QWizardPage, QLabel


class PMWidget(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        label = QLabel(self)
        label.setText("Merhaba!")