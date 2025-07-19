# CollapsiblePane (PySide6)

The `CollapsiblePane` is a reusable and customizable PySide6 widget that allows users to toggle the visibility of a content area with smooth animations—perfect for organizing UI sections. It mimics JavaFX’s `TitledPane` behavior and is designed to cleanly encapsulate widgets within collapsible sections.

Inspired by JavaFX's TitledPane.

---

## Features

- Expand/Collapse content with animation
- Fully customizable title bar and content styling
- Add or replace content widgets easily
- Clean, layout-friendly design
- Signal support for toggled state

---

## Installation

```bash
pip install collapsiblepane
```

Or if you're testing locally:

```bash
pip install dist/collapsiblepane-0.1.0-py3-none-any.whl
```

---

## Usage

```python
import sys

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QCheckBox, QRadioButton, QSlider, QProgressBar,
    QSpinBox, QDateEdit, QTextEdit, QWidget, QApplication
)
from PySide6.QtCore import Qt

from collapsiblepane import CollapsiblePane


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
        section.content_widget = content_widget


        # 🌟 Main layout
        # 🌟 Main layout
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.addWidget(section)
        button=QPushButton(self)
        main_layout.addWidget(button)
        button.clicked.connect(section.clear_widget)
        main_layout.setAlignment(section, Qt.AlignTop)  # <--- THIS does the magic
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
```

---

## Screenshot

| Collapsed | Expanded |
| --------- | -------- |
|![Collapsed View](https://raw.githubusercontent.com/mjk22071998/CollapsiblePane/refs/heads/main/screenshot/expanded.PNG)|![Expanded View](https://raw.githubusercontent.com/mjk22071998/CollapsiblePane/refs/heads/main/screenshot/expanded.PNG)|

> Ensure these URLs point to actual image files in your GitHub repo. Raw links must be used for PyPI to render them.

---

## API Overview

### Constructor

```python
CollapsiblePane(title="", animation_duration=100)
```

### Properties

- `content_widget`: `QWidget`
- `is_expanded`: `bool`

### Methods

- `clear_widget()`
- `set_content_style(background_color, border_color, ...)`
- `set_title_bar_style(background_color, foreground_color)`

### Signals

- `toggled(bool)` — emits when pane expands or collapses

---

## Contributions
For contributions olease visit [Github Repository](https://github.com/mjk22071998/CollapsiblePane)

