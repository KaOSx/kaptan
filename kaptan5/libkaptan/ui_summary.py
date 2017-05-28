from PyQt5.QtWidgets import QWizardPage, QLabel, QGroupBox, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout
from PyQt5.QtCore import *

class SummaryWidget(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSubTitle(self.tr("<h2>Save Your Settings</h2>"))

        vlayout = QVBoxLayout(self)

        label = QLabel(self)
        label.setWordWrap(True)
        label.setText(self.tr("<p>You have successfully finished all steps. Here's a summary of the settings you want to apply. \
        Click <strong>Apply Settings</strong> to save them now. You are now ready to enjoy KaOS!</p>"))
        vlayout.addWidget(label)
        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))

        groupBox = QGroupBox()
        groupBox.setTitle(self.tr("The following settings will be applied"))
        groupBox.setMinimumHeight(350)

        groupLayout = QHBoxLayout(groupBox)
        self.labelSummary = QLabel()
        self.labelSummary.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        groupLayout.addWidget(    self.labelSummary)
        self.labelSummary2 = QLabel()
        self.labelSummary2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        groupLayout.addWidget(    self.labelSummary2)
        vlayout.addWidget(groupBox)

        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Preferred, QSizePolicy.Preferred))

        self.summary = {}
        self.parent().summaryVisible.connect(self.summaryWrite)


    def summaryWrite(self):
        # -----------QFrame ---QWidget---Kaptan :S
        parent = self.parent().parent().parent()
        #MouseWidget
        mouseWidget = parent.page(1)
        #ThemeWidget
        themeWidget = parent.page(2)
        #MenuWidget
        menuWidget = parent.page(3)
        #WallpaperWidget
        wallpaperWidget = parent.page(4)
        #AvatarWidget
        avatarWidget = parent.page(5)

        selectWallpaper = ""
        userAvatar = ""
        windowStyle = None

        if mouseWidget.mouseButtonMap == "RightHanded":
            mouseButtonMap = self.tr("Right Handed")
        else:
            mouseButtonMap = self.tr("Left Handed")

        if mouseWidget.folderSingleClick:
            folderSingleClick = self.tr("Single Click")
        else:
            folderSingleClick = self.tr("Double Click")

        if themeWidget.desktopType == "org.kde.desktopcontainment":
            desktopType = self.tr("Desktop View")
        else:
            desktopType = self.tr("Folder View")

        if menuWidget.menuSelected == 0:
            menuSelected = self.tr("Application Launcher")
        elif menuWidget.menuSelected == 1:
            menuSelected = self.tr("Application Menu")
        else:
            menuSelected = self.tr("Application Panel")

        if wallpaperWidget.selectWallpaper:
            selectWallpaper = "<img src='{}' width='128' height='96'/>".format(wallpaperWidget.selectWallpaper)

        if avatarWidget.userAvatar:
            userAvatar = "<img src='{}' width='128' height='128'/>".format(avatarWidget.userAvatar)

        if themeWidget.windowStyle:
            windowStyle = themeWidget.windowStyle.split(".")[-1].capitalize()


        html = self.tr("""
        <ul>
            <li><strong>Mouse Options</strong>
            </li>
                <ul>
                    <li>Selected Hand: <strong>{}</strong></li>
                    <li>Selected Clicking Behavior: <strong>{}</strong></li>
                </ul>
            <li><strong>Theme Options</strong>
                <ul>
                    <li>Desktop Count: <strong>{}</strong></li>
                    <li>Desktop Type: <strong>{}</strong></li>
                    <li>Widget Style: <strong>{}</strong></li>
                    <li>Window Style: <strong>{}</strong></li>
                    <li>Color Scheme: <strong>{}</strong></li>
                    <li>Desktop Theme: <strong>{}</strong></li>
                    <li>Icon Set: <strong>{}</strong></li>
                </ul>
            </li>
            <li><strong>Menu Option</strong>
                <ul>
                    <li>Selected Menu: <strong>{}</strong></li>
                </ul>
            </li>
        </ul>""")

        self.labelSummary.setText(html.format(mouseButtonMap, folderSingleClick, themeWidget.desktopCount, desktopType,
                          (themeWidget.widgetStyle or self.tr("Unspecified.")).capitalize(), windowStyle or self.tr("Unspecified."),
                          themeWidget.colorScheme or self.tr("Unspecified."),
                          (themeWidget.desktopTheme or self.tr("Unspecified.")).replace("-", " ").title(),
                          (themeWidget.iconSet or self.tr("Unspecified.")).capitalize(), menuSelected))

        html = self.tr("""
        <ul>
            <li><strong>Selected Wallpaper</strong>
                <ul>
                    <li><strong>{}</strong></li>
                </ul>
            </li>
            <li><strong>Selected Avatar</strong>
                <ul>
                    <li><strong>{}</strong></li>
                </ul>
            </li>
        </ul>""")

        self.labelSummary2.setText(html.format(selectWallpaper or self.tr("Unspecified."), userAvatar or self.tr("Unspecified.")))
