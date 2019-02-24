# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 15:08:05 2018

@author: ZhiD
"""


def hello_world():
    from PyQt5.QtWidgets import QApplication, QLabel
    
    app = QApplication([])
    label = QLabel('Hello World!')
    label.show()
    app.exec_()


def demo_layouts():
    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
    
    app = QApplication([])  
    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QPushButton('Top'))
    layout.addWidget(QPushButton('Bottom'))
    window.setLayout(layout)
    window.show()
    app.exec_


def demo_colors():
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPalette
    from PyQt5.QtWidgets import QApplication, QPushButton
    
    app = QApplication([])
    
    # to apply a style
    style_win = ['Fusion', 'Windows', 'WindowsVista']
    style_mac = ['Macintosh']
    my_style = style_win[0]
    app.setStyle(my_style)
    
    # to pick a color
    palette = QPalette()
    palette.setColor(QPalette.ButtonText, Qt.red)
    app.setPalette(palette)
    
    button = QPushButton('Hello World!')
    button.show()
    app.exec_()

def demo_style_sheet():
    '''
    style sheet is Qt's analogue of CSS
    '''
    from PyQt5.QtWidgets import QApplication, QPushButton
    
    app = QApplication([])
    
    # to use style sheet
    app.setStyleSheet('QPushButton {margin: 10ex;}')
    
    button= QPushButton('Hello World!')
    button.show()
    app.exec_()
    
def demo_signal_slot():
    '''
    Qt uses a mechanism called signals to let you react to events
    such as the user clicks a button.
    '''
    from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox
    
    def on_button_clicked():
        alert = QMessageBox()
        alert.setText('You clicked the button!')
        alert.exec()
    
    app = QApplication([])
    button = QPushButton('Click')
    
    # button.clicked is a signal
    # .connect() lets us install a slot on it
    # the slot is a function that gets called when the signal occurs
    button.clicked.connect(on_button_clicked)
    button.show()
    app.exec_()
    
if __name__ == '__main__':
    # hello_world()
    # demo_layouts()
    # demo_colors()
    # demo_style_sheet()
    demo_signal_slot()
