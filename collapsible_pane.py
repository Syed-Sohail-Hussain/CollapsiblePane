from PySide6.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QToolButton, QFrame, QScrollArea,
    QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
)
import sys


class Section(QWidget):
    def __init__(self, title="", animationDuration=100, parent=None):
        super().__init__(parent)
        self.animationDuration = animationDuration
        self.toggleButton = QToolButton(self)
        self.headerLine = QFrame(self)
        self.toggleAnimation = QParallelAnimationGroup(self)
        self.contentArea = QScrollArea(self)
        self.mainLayout = QGridLayout(self)

        self.toggleButton.setStyleSheet("QToolButton {border: none;}")
        self.toggleButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggleButton.setArrowType(Qt.RightArrow)
        self.toggleButton.setText(title)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)

        self.headerLine.setFrameShape(QFrame.HLine)
        self.headerLine.setFrameShadow(QFrame.Sunken)
        self.headerLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.contentArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)

        self.toggleAnimation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggleAnimation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggleAnimation.addAnimation(QPropertyAnimation(self.contentArea, b"maximumHeight"))

        self.mainLayout.setVerticalSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        row = 0
        self.mainLayout.addWidget(self.toggleButton, row, 0, 1, 1, Qt.AlignLeft)
        self.mainLayout.addWidget(self.headerLine, row, 2, 1, 1)
        self.mainLayout.addWidget(self.contentArea, row + 1, 0, 1, 3)
        self.setLayout(self.mainLayout)

        self.toggleButton.toggled.connect(self.toggle)

    def setContentLayout(self, contentLayout):
        oldLayout = self.contentArea.layout()
        if oldLayout is not None:
            QWidget().setLayout(oldLayout)  # Clear previous layout safely

        self.contentArea.setLayout(contentLayout)

        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()

        for i in range(self.toggleAnimation.animationCount() - 1):
            animation = self.toggleAnimation.animationAt(i)
            animation.setDuration(self.animationDuration)
            animation.setStartValue(collapsedHeight)
            animation.setEndValue(collapsedHeight + contentHeight)

        contentAnimation = self.toggleAnimation.animationAt(self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

    def toggle(self, collapsed):
        if collapsed:
            self.toggleButton.setArrowType(Qt.DownArrow)
            self.toggleAnimation.setDirection(QAbstractAnimation.Forward)
        else:
            self.toggleButton.setArrowType(Qt.RightArrow)
            self.toggleAnimation.setDirection(QAbstractAnimation.Backward)
        self.toggleAnimation.start()


if __name__ == '__main__':
    class Window(QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            section = Section("Section", 100, self)

            anyLayout = QVBoxLayout()
            anyLayout.addWidget(QLabel("Some Text in Section", section))
            anyLayout.addWidget(QPushButton("Button in Section", section))
            anyLayout.addWidget(QPushButton("Button in Section", section))
            anyLayout.addWidget(QPushButton("Button in Section", section))
            anyLayout.addWidget(QPushButton("Button in Section", section))
            anyLayout.addWidget(QPushButton("Button in Section", section))
            anyLayout.addWidget(QPushButton("Button in Section", section))


            section.setContentLayout(anyLayout)

            self.place_holder = QWidget()
            mainLayout = QHBoxLayout(self.place_holder)
            mainLayout.addWidget(section)
            mainLayout.addStretch(1)
            self.setCentralWidget(self.place_holder)

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
