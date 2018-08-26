from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

def menuTab(menu, itemName):
    return menu.addMenu(itemName)

def exitButton(tab, widget):
    exitButton = QAction('Exit', widget)
    exitButton.setStatusTip('Exit application')
    exitButton.triggered.connect(qApp.quit)
    tab.addAction(exitButton)
