import re
from PyQt5.QtCore import QSettings


class Parser(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        with open(self.file_name) as config_file:
            return config_file.read()

    def sync(self, data):
        with open(self.file_name, "w") as self.config_file:
            self.config_file.write(data)
            self.config_file.flush()

    def getApplets(self):
        regex = "(\n\[Containments\]\[([1-9]+)\]\[Applets\]\[([1-9]+)\]\nimmutability=1\nplugin=(.*)\n)"

        all_applets = re.findall(regex, self.read())

        if all_applets:
            return all_applets
    # Example [('[Containments][1][Applets][2]\nimmutability=1\nplugin=org.kde.plasma.kickoff\n', '1', '2', 'org.kde.plasma.kickoff')]

    def setMenuStyleOrCreate(self, menu_style):
        is_there = False
        menu_applet = None
        applets = self.getApplets()

        for applet in applets:
            if ("org.kde.plasma.kicker"  in applet) or ("org.kde.plasma.kickoff"  in applet) or ("org.kde.plasma.kickerdash" in applet):
                is_there = True
                menu_applet = applet
                break

        if is_there:
            regex = r"\n\[Containments\]\[%s\]\[Applets\]\[%s\]\nimmutability=.\nplugin=.*\n"%(menu_applet[1], menu_applet[2])

            com = re.compile(regex)

            new_data = com.sub(menu_applet[0].replace(menu_applet[3], menu_style), self.read())
            self.sync(new_data)
            # '[Containments][1][Applets][2]\nimmutability=1\nplugin=org.kde.plasma.kicker\n'
        else:
            last_nums = []
            first_applet = applets[0]
            for applet in applets:
                last_nums.append(int(applet[2]))

            applet_index = str(max(last_nums)+1)
            applet = "\n[Containments][{}][Applets][{}]\nimmutability=1\nplugin={}\n".format(first_applet[1], applet_index, menu_style)

            com = re.compile("\n\[Containments\]\[%s\]\[Applets\]\[%s\]\nimmutability=.\nplugin=.*\n"%(first_applet[1], first_applet[2]))

            new_data = com.sub(first_applet[0] + applet, self.read())
            self.sync(new_data)
            self.setAppletOrder(0, applet_index)

    # Sadece wallpaper kısmı var mı diye aramayacak sayısını da hesap edecek.
    # Ayrıca 1-9+ kısmındaki rakam da değer olarak döndürülecek.
    # Masaüstünü temsil eden id li ayar kısmı baz alınarak işlenecek.
    def getWallpaper(self):
        regex = "(\[Containments\]\[[1-9]+\]\[Wallpaper\]\[org.kde.image\]\[General\]\n(.*)=(.*)\n)"

        read = re.search(regex, self.read())

        if read:
            if read.group(2) != "Image":
                regex = "(\[Containments\]\[[1-9]+\]\[Wallpaper\]\[org.kde.image\]\[General\]\n)((.*)=.*\n.*\n)"

                read = re.search(regex, self.read())

                if read:
                    return read.group(1), read.group(2), read.group(3)

            return read.group(1), read.group(2), read.group(3)

        else:
            return False


    #
    def setWallpaper(self, path):
        if self.getWallpaper()[1] != "Image":
            regex = "\[Containments\]\[[1-9]+\]\[Wallpaper\]\[org.kde.image\]\[General\]\n.*\n.*\n"
            com = re.compile(regex)

            new_data =  com.sub((self.getWallpaper()[0]+"Image=%s\n"+self.getWallpaper()[1])%path, self.read())
            self.sync(new_data)
            
        elif self.getWallpaper()[1] == "Image":
            regex = r"\[Containments\]\[[1-9]+\]\[Wallpaper\]\[org.kde.image\]\[General\]\n%s=.*\n"%(self.getWallpaper()[1])

            com = re.compile(regex)

            new_data = com.sub(self.getWallpaper()[0].replace(self.getWallpaper()[2], path), self.read())
            self.sync(new_data)
            
        else:
            pass # Buraya wallpaper ile ilgili bir ayar yoksa sıfırdan oluşturulacak

    def getDesktopType(self):
        regex = "(\[Containments\]\[[1-9]*\]\nactivityId=.+\n.*\n.*\nlastScreen=.*\n.*\nplugin=(.*)\n)"

        read = re.search(regex, self.read())

        if read:
            return read.group(1), read.group(2)

    def setDesktopType(self, view):
        regex = "\[Containments\]\[[1-9]*\]\nactivityId=.+\n.*\n.*\nlastScreen=.*\n.*\nplugin=(.*)\n"

        com = re.compile(regex)

        if view != self.getDesktopType()[1]:
            new_data = com.sub(self.getDesktopType()[0].replace(self.getDesktopType()[1], view), self.read())
            self.sync(new_data)

    def getAppletOrder(self):
        regex = "(\n\[Containments\]\[([1-9]+)\]\[General\]\nAppletOrder=(.*)\n)"

        applet_order = re.findall(regex, self.read())

        if applet_order:
            return applet_order[0]

    def setAppletOrder(self, index = int, value = str):
        applet_order = self.getAppletOrder()

        order = applet_order[-1].split(";")
        order.insert(index, value)

        values = ";".join(order)

        regex = r"\n\[Containments\]\[%s\]\[General\]\nAppletOrder=.+\n"%applet_order[1]

        com = re.compile(regex)

        new_data = com.sub(applet_order[0].replace(applet_order[2], values), self.read())
        self.sync(new_data)

    def setShowDesktopApplet(self):
        is_there = False
        applets = self.getApplets()

        for applet in applets:
            if "org.kde.plasma.showdesktop"  in applet:
                is_there = True
                break

        if not is_there:
            last_nums = []
            first_applet = applets[0]
            for applet in applets:
                last_nums.append(int(applet[2]))

            applet_index = str(max(last_nums)+1)
            applet = "\n[Containments][{}][Applets][{}]\nimmutability=1\nplugin={}\n".format(first_applet[1],
                                                                                             applet_index, "org.kde.plasma.showdesktop")

            com = re.compile(r"\n\[Containments\]\[%s\]\[Applets\]\[%s\]\nimmutability=.\nplugin=.*\n"%(first_applet[1], first_applet[2]))

            new_data = com.sub(first_applet[0] + applet, self.read())
            self.sync(new_data)
            self.setAppletOrder(1, applet_index)


#parser = Parser("/home/metehan/.config/plasma-org.kde.plasma.desktop-appletsrc2")

#print(parser.getApplets())
#print(parser.getAppletOrder())
#parser.setMenuStyleOrCreate("org.kde.plasma.kickerdash")
#print(parser.setAppletOrder(0, "2"))
#parser.setShowDesktopApplet()
#print(parser.getWallpaper())
#parser.setWallpaper("/home/metehan/Dropbox/metehan.png")
#print(parser.getDesktopType())
#parser.setDesktopType("org.kde.plasma.folder")

def listToStr(list):
    str = ""
    for l in list:
        str += l + ","
    return str[:-1]

def iniToCss(file):
    """
    label text color
    button background-border-text
    groupbox background-bordor
    textbrowser background-text-linktext-alinktext
    """

    iniFile = QSettings(file, QSettings.IniFormat)

    cssText = """QLabel#previewLabel {
    color : rgb(%s);
    }

    QPushButton#previewPushButton {
    color : rgb(%s);
    background-color : rgb(%s);
    }

    QGroupBox#previewGroupBox {
    background-color : rgb(%s);
    }

    QTextBrowser#previewTextBrowser {
    background-color : rgb(%s);
    color : rgb(%s);
    }"""%(listToStr(iniFile.value("Colors:Window/ForegroundNormal")),
          listToStr(iniFile.value("Colors:Button/ForegroundNormal")),
          listToStr(iniFile.value("Colors:Button/BackgroundNormal")),
          listToStr(iniFile.value("Colors:Window/BackgroundNormal")),
          listToStr(iniFile.value("Colors:View/BackgroundNormal")),
          listToStr(iniFile.value("Colors:View/ForegroundNormal")))

    textbrowser = listToStr(iniFile.value("Colors:View/ForegroundLink")), listToStr(iniFile.value("Colors:View/ForegroundVisited"))

    return cssText, textbrowser


#print(iniToCss("/usr/share/color-schemes/Breeze.colors"))
