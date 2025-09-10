from PySide6.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation, Signal, QEasingCurve
from PySide6.QtWidgets import (
    QWidget, QToolButton, QScrollArea, QGridLayout, QSizePolicy
)


class CollapsiblePane(QWidget):
    toggled = Signal(bool)

    def __init__(self, title="", animation_duration=100, parent=None):
        super().__init__(parent)
        if title is not str:
            return
        if animation_duration is not int:
            return

        self.animation_duration = animation_duration

        self.toggle_button = QToolButton(self)
        self.toggle_animation = QParallelAnimationGroup(self)
        self.content_area = QScrollArea(self)
        self.main_layout = QGridLayout(self)

        # Toggle button setup
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.setText(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toggle_button.setStyleSheet(self._generate_button_style("#444", "#eee"))

        # Content area setup
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)
        self.content_area.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.content_area.setWidgetResizable(True)

        # Animations
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.content_area, b"maximumHeight"))

        # Layout setup
        self.main_layout.setVerticalSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.toggle_button, 0, 0)
        self.main_layout.addWidget(self.content_area, 1, 0)
        self.setLayout(self.main_layout)

        self.toggle_button.toggled.connect(self.toggle)

    def _generate_button_style(self, bg_color: str="#0066ff", fg_color: str="#ffffff") -> str:
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

    def clear_widget(self):
        if self.content_area.widget():
            old = self.content_area.widget()
            self.content_area.takeWidget()
            old.deleteLater()

        # Reset animation values so the pane collapses properly
        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()

        for i in range(self.toggle_animation.animationCount() - 1):
            animation = self.toggle_animation.animationAt(i)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height)
            animation.setEasingCurve(QEasingCurve.OutCubic)

        content_anim = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_anim.setStartValue(0)
        content_anim.setEndValue(0)

        # Also collapse the pane visually
        self.content_area.setMaximumHeight(0)

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

    @property
    def content_widget(self) -> QWidget:
        return self.content_area.widget()

    @content_widget.setter
    def content_widget(self, widget: QWidget):
        # Remove old widget if any
        if self.content_area.widget() is widget:
            return  # No need to do anything

        if self.content_area.widget():
            old_widget = self.content_area.widget()
            old_widget.setParent(None)

        self.content_area.setWidget(widget)

        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        content_height = widget.sizeHint().height()

        for i in range(self.toggle_animation.animationCount() - 1):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(self.animation_duration)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)
            animation.setEasingCurve(QEasingCurve.OutCubic)

        content_anim = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_anim.setDuration(self.animation_duration)
        content_anim.setStartValue(0)
        content_anim.setEndValue(content_height)

    @property
    def is_expanded(self):
        return self.toggle_button.isChecked()

    def toggle(self, collapsed: bool):
        self.toggled.emit(collapsed)

        if collapsed:
            self.toggle_button.setArrowType(Qt.DownArrow)
        else:
            self.toggle_button.setArrowType(Qt.RightArrow)

        # If there's no content widget, skip animation
        content = self.content_area.widget()
        if content is None:
            self.content_area.setMaximumHeight(0)
            return

        # Compute heights for animation
        collapsed_height = self.toggle_button.sizeHint().height()
        content_height = content.sizeHint().height()

        for i in range(self.toggle_animation.animationCount() - 1):
            anim = self.toggle_animation.animationAt(i)
            anim.setStartValue(collapsed_height)
            anim.setEndValue(collapsed_height + content_height)
            anim.setEasingCurve(QEasingCurve.OutCubic)

        content_anim = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_anim.setStartValue(0)
        content_anim.setEndValue(content_height)

        # Animate
        if self.toggle_animation.state() == QAbstractAnimation.Running:
            self.toggle_animation.setDirection(
                QAbstractAnimation.Backward if self.toggle_animation.direction() == QAbstractAnimation.Forward else QAbstractAnimation.Forward
            )
        else:
            self.toggle_animation.setDirection(
                QAbstractAnimation.Forward if collapsed else QAbstractAnimation.Backward
            )

        self.toggle_animation.start()

