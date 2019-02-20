import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout,QDesktopWidget, QMessageBox, QLabel, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import requests
import act
urls = act.get_douyu_roomlist()


class MyLabel(QLabel):

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)

    def mouseDoubleClickEvent(self, e):
        print('mouse double clicked')
    # def mousePressEvent(self,e):
    #     print('mousePressEvent')
    def leaveEvent(self, e): #鼠标离开label
        print('leaveEvent')
    def enterEvent(self, e): #鼠标移入label
        print('enterEvent')


class MainWindow(QWidget):
    def __init__(self, url=urls):
        self.url = url
        super(MainWindow, self).__init__()
        self.screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(0.8*self.screen.width(), 0.8*self.screen.height())
        self._loadStart = False
        self.center()
        self.setWindowTitle("直播")
        self.show()
        self.initUI()

    def center(self):
        window = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        window.moveCenter(center_point)
        self.move(window.topLeft())

    def initUI(self):
        wlayout = self.left_list()
        vbox = self.right_list()
        hbox1 = QHBoxLayout()
        hbox1.addLayout(wlayout)
        hbox1.addLayout(vbox)
        self.setLayout(hbox1)

    def left_list(self):
        Live_platform_category = {'哔哩哔哩': ['映评馆', '音乐台'],
                                  '斗鱼': ['主题点播影院', '懒人轮播影院', '妹纸陪看', '电视剧', '动漫', '综艺', '自然科学记录', '美食记录', '小姐姐女团',
                                         '千奇百怪'],
                                  'YY': ['音乐']}
        self.treeWidget = QTreeWidget()
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(['直播平台'])
        for Live_platform in Live_platform_category.keys():
            child1 = QTreeWidgetItem(self.treeWidget)
            child1.setText(0, Live_platform)
            for category in Live_platform_category[Live_platform]:
                child2 = QTreeWidgetItem(child1)
                child2.setText(0, category)
        self.treeWidget.expandAll()
        self.treeWidget.itemDoubleClicked.connect(self.showSelected)
        wlayout = QHBoxLayout()
        wlayout.addWidget(self.treeWidget)
        wlayout.addStretch()
        return wlayout

    def right_list(self, *cover_url):
        bt1 = QPushButton('首页', self)
        bt1.setObjectName("fpage")
        bt2 = QPushButton('上一页', self)
        bt3 = QPushButton('下一页', self)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(bt1)
        hbox.addWidget(bt2)
        hbox.addWidget(bt3)
        hbox.addStretch()
        positions = [(j, i) for i in range(4) for j in range(6)]
        grid = QGridLayout()
        grid.setSpacing(5)
        for position, link in zip(positions, a):
            lb = MyLabel()
            if 'http' in link:
                req = requests.get(link)
                photo = QPixmap()
                photo.loadFromData(req.content)
                lb.setPixmap(photo)
                lb.setFixedSize(0.16*self.screen.width(), 0.16*self.screen.height())
            else:
                lb.setWordWrap(True)
                lb.setText(link)
            grid.addWidget(lb, *position)
        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addLayout(hbox)
        QtCore.QMetaObject.connectSlotsByName(self)
        return vbox

    @QtCore.pyqtSlot()
    def on_fpage_clicked(self):
        print("单击了OK按钮")


    def showSelected(self):
        item = self.treeWidget.currentItem()
        print(item.text(0))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exit(app.exec_())
