"""
old version, not working
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QStackedWidget, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve, Qt, QPoint, QSize
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPainterPath

class RoundedImage(QLabel):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(image_path)
        self.setFixedSize(400, 400)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        rect = self.rect()
        radius = 20
        
        # Top-left and bottom-left corners rounded
        path.moveTo(QPoint(rect.topRight()))
        path.lineTo(QPoint(rect.topLeft()) + QPoint(radius, 0))
        path.arcTo(QRect(QPoint(rect.topLeft()), QSize(radius * 2, radius * 2)), 90, 90)
        path.lineTo(QPoint(rect.bottomLeft()) - QPoint(0, radius))
        path.arcTo(QRect(QPoint(rect.bottomLeft()) - QPoint(0, radius * 2), QSize(radius * 2, radius * 2)), 180, 90)
        path.lineTo(QPoint(rect.bottomRight()))
        path.lineTo(QPoint(rect.topRight()))
        
        painter.setClipPath(path)
        painter.drawPixmap(self.rect(), self.pixmap)

class LoginOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(parent.size())
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")

        central_widget = QWidget(self)
        central_widget.setFixedSize(800, 400)
        central_widget.setStyleSheet("background-color: white; border-radius: 20px;")
        central_widget.move((self.width() - central_widget.width()) // 2, (self.height() - central_widget.height()) // 2)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Left side with rounded image
        left_widget = RoundedImage("Images/banhaobg-edit.png", central_widget)
        layout.addWidget(left_widget)

        # Right side with login/register selection
        right_widget = QWidget(central_widget)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)

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
        close_button.move(central_widget.x() + central_widget.width() - 15, central_widget.y() - 15)
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.mousePressEvent = self.close_overlay

    def create_login_widget(self):
        login_widget = QWidget()
        layout = QVBoxLayout(login_widget)
        layout.addWidget(QLabel("Login Form"))
        return login_widget

    def create_register_widget(self):
        register_widget = QWidget()
        layout = QVBoxLayout(register_widget)
        layout.addWidget(QLabel("Register Form"))
        return register_widget

    def switch_page(self, button):
        index = button.group().id(button)
        self.stacked_widget.setCurrentIndex(index)

    def close_overlay(self, event):
        self.hide()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 650)
        self.setWindowTitle("Main Window")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.login_overlay = LoginOverlay(self)
        self.login_overlay.hide()

        test_button = QPushButton("Show Login", self)
        test_button.clicked.connect(self.show_login_overlay)
        layout.addWidget(test_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def show_login_overlay(self):
        self.login_overlay.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())