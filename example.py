import sys

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QCheckBox, QRadioButton, QSlider, QProgressBar,
    QSpinBox, QDateEdit, QTextEdit, QWidget, QHBoxLayout, QApplication
)
from PySide6.QtCore import Qt
from collapsible_pane import CollapsiblePane


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Flex Zone 🧩")

        # Create the collapsible pane
        section = CollapsiblePane("🔥 Ultimate Pane of Power", 150, self)

        # 🎨 Customize title bar
        section.set_title_bar_style(background_color="#0066ff", foreground_color="#FFFFFF")
        section.set_content_style(
            background_color="#FFFFFF",
            border_color="#0066FF",
            border_width=2,
            border_style="solid"
        )

        # 💎 Create a widget to hold the layout
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        content_layout.addWidget(QLabel("📝 Enter your details:"))
        content_layout.addWidget(QLineEdit("Name here..."))
        content_layout.addWidget(QLineEdit("Email address..."))

        content_layout.addWidget(QLabel("🔽 Choose a category:"))
        combo = QComboBox()
        combo.addItems(["Developer", "Designer", "Hacker", "Wizard"])
        content_layout.addWidget(combo)

        content_layout.addWidget(QCheckBox("Subscribe to newsletter 📬"))
        content_layout.addWidget(QRadioButton("Light Mode ☀️"))
        content_layout.addWidget(QRadioButton("Dark Mode 🌙"))

        content_layout.addWidget(QLabel("🔊 Volume:"))
        slider = QSlider(Qt.Horizontal)
        slider.setValue(40)
        content_layout.addWidget(slider)

        progress = QProgressBar()
        progress.setValue(70)
        content_layout.addWidget(progress)

        content_layout.addWidget(QSpinBox())
        content_layout.addWidget(QDateEdit())

        content_layout.addWidget(QLabel("🧾 Bio:"))
        text_edit = QTextEdit()
        text_edit.setPlaceholderText("Tell us something cool...")
        content_layout.addWidget(text_edit)

        content_layout.addWidget(QPushButton("🚀 Launch!"))

        # Set the content widget using the property
        section.widget = content_widget

        # 🌟 Main layout
        # 🌟 Main layout
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.addWidget(section)
        main_layout.setAlignment(section, Qt.AlignTop)  # <--- THIS does the magic
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())