from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QCheckBox, QRadioButton, QSlider, QProgressBar,
    QSpinBox, QDateEdit, QTextEdit, QWidget, QHBoxLayout
)
from PySide6.QtCore import Qt
from collapsible_pane import CollapsiblePane


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Flex Zone 🧩")

        section = CollapsiblePane("🔥 Ultimate Pane of Power", 250, self)

        # 🎨 Customize title bar
        section.set_title_bar_style(background_color="#222831", foreground_color="#FFD369")
        section.set_content_style(
            background_color="#393E46",
            border_color="#FFD369",
            border_width=2,
            border_style="solid"
        )

        # 💎 Add a bunch of widgets to show off
        contentLayout = QVBoxLayout()

        contentLayout.addWidget(QLabel("📝 Enter your details:"))
        contentLayout.addWidget(QLineEdit("Name here..."))
        contentLayout.addWidget(QLineEdit("Email address..."))

        contentLayout.addWidget(QLabel("🔽 Choose a category:"))
        combo = QComboBox()
        combo.addItems(["Developer", "Designer", "Hacker", "Wizard"])
        contentLayout.addWidget(combo)

        contentLayout.addWidget(QCheckBox("Subscribe to newsletter 📬"))
        contentLayout.addWidget(QRadioButton("Light Mode ☀️"))
        contentLayout.addWidget(QRadioButton("Dark Mode 🌙"))

        contentLayout.addWidget(QLabel("🔊 Volume:"))
        slider = QSlider(Qt.Horizontal)
        slider.setValue(40)
        contentLayout.addWidget(slider)

        progress = QProgressBar()
        progress.setValue(70)
        contentLayout.addWidget(progress)

        contentLayout.addWidget(QSpinBox())
        contentLayout.addWidget(QDateEdit())

        contentLayout.addWidget(QLabel("🧾 Bio:"))
        textEdit = QTextEdit()
        textEdit.setPlaceholderText("Tell us something cool...")
        contentLayout.addWidget(textEdit)

        contentLayout.addWidget(QPushButton("🚀 Launch!"))

        # Set layout
        section.set_content_layout(contentLayout)

        # 🌟 Main layout
        container = QWidget()
        mainLayout = QHBoxLayout(container)
        mainLayout.addWidget(section)
        self.setCentralWidget(container)
