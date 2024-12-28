"""
old version, not working
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QRadioButton, QButtonGroup, QGraphicsOpacityEffect, QGraphicsColorizeEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QPoint
from PyQt6.QtGui import QPixmap, QColor

class LoginOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(parent.size())
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")  # Black 50% transparency

        # Central widget for the rounded rectangle
        central_widget = QWidget(self)
        central_widget.setFixedSize(800, 400)
        central_widget.setStyleSheet("background-color: white; border-radius: 20px;")
        central_widget.move((self.width() - central_widget.width()) // 2, (self.height() - central_widget.height()) // 2)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Left side with image
        left_widget = QLabel(central_widget)
        left_widget.setPixmap(QPixmap("Images/banhaobg-edit.png"))
        left_widget.setScaledContents(True)
        left_widget.setFixedSize(400, 400)
        layout.addWidget(left_widget)

        # Right side with login/register selection
        right_widget = QWidget(central_widget)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)

        # Selection buttons
        self.stacked_widget = QStackedWidget(right_widget)
        self.stacked_widget.addWidget(self.create_login_widget())
        self.stacked_widget.addWidget(self.create_register_widget())

        button_group = QButtonGroup(right_widget)
        login_button = QRadioButton("Login")
        register_button = QRadioButton("Register")
        login_button.setChecked(True)
        button_group.addButton(login_button, 0)
        button_group.addButton(register_button, 1)
        button_group.buttonClicked.connect(self.switch_page)

        button_layout = QHBoxLayout()
        button_layout.addWidget(login_button)
        button_layout.addWidget(register_button)
        right_layout.addLayout(button_layout)
        right_layout.addWidget(self.stacked_widget)

        layout.addWidget(right_widget)

        # Close button
        close_button = QLabel(self)
        close_button.setPixmap(QPixmap("Images/ic_cancel.png"))
        close_button.setScaledContents(True)
        close_button.setFixedSize(30, 30)
        close_button.move(self.width() - close_button.width() - 20, 20)
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.mousePressEvent = self.close_overlay

        # Saturation effect on hover
        self.saturation_effect = QGraphicsColorizeEffect()
        self.saturation_effect.setColor(QColor(255, 255, 255, 0))
        close_button.setGraphicsEffect(self.saturation_effect)
        close_button.installEventFilter(self)

    def create_login_widget(self):
        login_widget = QWidget()
        layout = QVBoxLayout(login_widget)
        layout.addWidget(QLabel("Login Form"))
        # Add more login form elements here
        return login_widget

    def create_register_widget(self):
        register_widget = QWidget()
        layout = QVBoxLayout(register_widget)
        layout.addWidget(QLabel("Register Form"))
        # Add more register form elements here
        return register_widget

    def switch_page(self, button):
        index = button.group().id(button)
        self.stacked_widget.setCurrentIndex(index)

    def close_overlay(self, event):
        self.hide()

    def eventFilter(self, source, event):
        if event.type() == event.Type.Enter:
            self.saturation_effect.setColor(QColor(255, 255, 255, 255))
        elif event.type() == event.Type.Leave:
            self.saturation_effect.setColor(QColor(255, 255, 255, 0))
        return super().eventFilter(source, event)

def show_login_overlay(parent):
    overlay = LoginOverlay(parent)
    overlay.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setFixedSize(1000, 650)
    main_window.setWindowTitle("Main Window")
    main_window.show()

    # Show the login overlay
    show_login_overlay(main_window)

    sys.exit(app.exec())