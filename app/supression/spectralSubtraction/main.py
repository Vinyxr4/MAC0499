from PyQT4.QtGui import *

def spectralSubtractionWidget():
    specSubGroup = QBoxGroup('Spectral Subtraction')
    contentGrid = QGridLayout()

    specSubGroup.setLayout(contentGrid)

    return specSubGroup
