from PySide6.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation
from PySide6.QtWidgets import (
    QWidget, QToolButton, QScrollArea, QGridLayout, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy, QApplication, QMainWindow
)
import sys


class CollapsiblePane(QWidget):
    def __init__(self, title="", animation_duration=100, parent=None):
        super().__init__(parent)
        self.animation_duration = animation_duration

        self.toggle_button = QToolButton(self)
        self.toggle_animation = QParallelAnimationGroup(self)
        self.content_area = QScrollArea(self)
        self.main_layout = QGridLayout(self)

        # Toggle button style and behavior
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.setText(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toggle_button.setStyleSheet(self._generate_button_style("#444", "#eee"))  # default colors

        # Content area settings
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)
        self.content_area.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")

        # Add animations
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.content_area, b"maximumHeight"))

        # Layout
        self.main_layout.setVerticalSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.toggle_button, 0, 0)
        self.main_layout.addWidget(self.content_area, 1, 0)
        self.setLayout(self.main_layout)

        self.toggle_button.toggled.connect(self.toggle)

    def _generate_button_style(self, bg_color: str, fg_color: str) -> str:
        return f"""
        QToolButton {{
            background-color: {bg_color};
            color: {fg_color};
            border: none;
            padding: 6px;
            font-weight: bold;
        }}
        QToolButton::menu-indicator {{ image: none; }}
        """

    def set_content_style(self, background_color="#ffffff", border_color="#cccccc", border_width=1, border_style="solid"):
        self.content_area.setStyleSheet(f"""
        QScrollArea {{
            background-color: {background_color};
            border: {border_width}px {border_style} {border_color};
            border-radius: 4px;
        }}
        """)


    def set_title_bar_style(self, background_color: str, foreground_color: str):
        self.toggle_button.setStyleSheet(
            self._generate_button_style(background_color, foreground_color)
        )

    def set_content_layout(self, content_layout):
        oldLayout = self.content_area.layout()
        if oldLayout is not None:
            QWidget().setLayout(oldLayout)

        self.content_area.setLayout(content_layout)

        collapsedHeight = self.sizeHint().height() - self.content_area.maximumHeight()
        contentHeight = content_layout.sizeHint().height()

        for i in range(self.toggle_animation.animationCount() - 1):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(self.animation_duration)
            animation.setStartValue(collapsedHeight)
            animation.setEndValue(collapsedHeight + contentHeight)

        contentAnimation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        contentAnimation.setDuration(self.animation_duration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

    def toggle(self, collapsed):
        if collapsed:
            self.toggle_button.setArrowType(Qt.DownArrow)
            self.toggle_animation.setDirection(QAbstractAnimation.Forward)
        else:
            self.toggle_button.setArrowType(Qt.RightArrow)
            self.toggle_animation.setDirection(QAbstractAnimation.Backward)
        self.toggle_animation.start()
