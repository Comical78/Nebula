import sys
import json
import math
import random
import sqlite3
import requests
from io import BytesIO
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit, QDialog, QMessageBox
)
from PyQt6.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor, QPixmap, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QTimer, QPoint, QRectF, QPropertyAnimation, pyqtProperty

class SpinnerWheel(QWidget):
    def __init__(self, rewards, parent=None):
        super().__init__(parent)
        self.rewards = rewards
        self.num_segments = len(self.rewards)
        self.angle_per_segment = 360 / self.num_segments
        self.current_angle = 0
        self.target_angle = 0
        self.is_spinning = False

        self.setMinimumSize(400, 400)
        self.preload_images()

    def preload_images(self):
        """Preload images from URLs to avoid loading them during paint event."""
        self.loaded_images = {}
        for reward in self.rewards:
            image_url = reward.get("image", "")
            if image_url and image_url not in self.loaded_images:
                try:
                    response = requests.get(image_url)
                    response.raise_for_status()
                    image_data = BytesIO(response.content)
                    pixmap = QPixmap()
                    if pixmap.loadFromData(image_data.read()):
                        self.loaded_images[image_url] = pixmap
                    else:
                        print(f"Error: Failed to load image data from {image_url}")
                        self.loaded_images[image_url] = None
                except Exception as e:
                    print(f"Error fetching image from {image_url}: {e}")
                    self.loaded_images[image_url] = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        size = min(rect.width(), rect.height()) - 20
        painter.translate(rect.width() / 2, rect.height() / 2)
        painter.rotate(self.current_angle)

        radius = size / 2
        for i, reward in enumerate(self.rewards):
            start_angle = i * self.angle_per_segment
            path = QPainterPath()
            path.moveTo(0, 0)
            path.arcTo(QRectF(-radius, -radius, 2*radius, 2*radius), start_angle, self.angle_per_segment)
            path.closeSubpath()

            # Set color
            color = QColor(50, 50, 50) if i % 2 == 0 else QColor(80, 80, 80)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            painter.drawPath(path)

            # Draw reward image
            image_url = reward.get("image", "")
            pixmap = self.loaded_images.get(image_url)
            if pixmap:
                # Calculate position for the image
                painter.save()
                painter.rotate(start_angle + self.angle_per_segment / 2)
                painter.translate(radius * 0.6, 0)
                painter.rotate(- (start_angle + self.angle_per_segment / 2))
                # Scale pixmap if necessary
                scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                painter.drawPixmap(-scaled_pixmap.width() / 2, -scaled_pixmap.height() / 2, scaled_pixmap)
                painter.restore()

        # Draw center circle
        painter.setBrush(QBrush(QColor(30, 30, 30)))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawEllipse(-20, -20, 40, 40)

    def spin(self):
        if self.is_spinning:
            return
        self.is_spinning = True
        # Select a reward based on weights
        reward_ids = [reward["rewardId"] for reward in self.rewards]
        weights = [reward.get("weight", 1) for reward in self.rewards]
        selected_reward_id = random.choices(reward_ids, weights=weights, k=1)[0]
        selected_reward_index = next(i for i, reward in enumerate(self.rewards) if reward["rewardId"] == selected_reward_id)
        # Calculate target angle
        extra_spins = 5  # Total spins
        total_spin = 360 * extra_spins
        # Ensure the selected segment aligns at the top after spinning
        target_angle = total_spin + (360 - selected_reward_index * self.angle_per_segment - self.angle_per_segment / 2)
        self.animation = QPropertyAnimation(self, b"rotation")
        self.animation.setDuration(5000)  # 5 seconds
        self.animation.setStartValue(self.current_angle)
        self.animation.setEndValue(target_angle)
        self.animation.finished.connect(lambda: self.on_spin_finish(selected_reward_id))
        self.animation.start()

    def on_spin_finish(self, reward_id):
        self.is_spinning = False
        # Find the reward details
        reward = next((r for r in self.rewards if r["rewardId"] == reward_id), None)
        if reward:
            QMessageBox.information(self, "Congratulations!", f"You won: {reward.get('rewardName', 'Unknown Reward')}")
        else:
            QMessageBox.information(self, "Congratulations!", f"You won Reward ID: {reward_id}")

    def get_rotation(self):
        return self.current_angle

    def set_rotation(self, angle):
        self.current_angle = angle % 360
        self.update()

    rotation = pyqtProperty(float, fget=get_rotation, fset=set_rotation)

class SpinnerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reward Spinner")
        self.setFixedSize(600, 700)

        # Initialize Database
        self.init_db()

        # Load Rewards
        self.rewards = self.load_rewards("Script/rewards.json")

        # Load Custom Font
        self.load_custom_font()

        # Set up UI
        self.setup_ui()

    def init_db(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                email_provided BOOLEAN
            )
        """)
        self.conn.commit()

    def load_rewards(self, filepath):
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
            # Combine all reward lists
            rewards = []
            for category in data.values():
                for reward_list in category.values():
                    rewards.extend(reward_list)
            # Remove duplicates based on rewardId
            unique_rewards = {reward["rewardId"]: reward for reward in rewards}
            return list(unique_rewards.values())
        except Exception as e:
            print(f"Error loading rewards: {e}")
            return []

    def load_custom_font(self):
        font_path = "Script/Font/droidsans/DroidSans.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Failed to load DroidSans font from {font_path}.")
            self.font = QFont("Arial", 10)  # Fallback font
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family, 10)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(20)

        # Email Input with Label
        email_layout = QHBoxLayout()
        email_label = QLabel("Email (optional):")
        email_label.setFont(QFont(self.font.family(), 12))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setFont(QFont(self.font.family(), 12))
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        main_layout.addLayout(email_layout)

        # Spinner Wheel
        self.spinner = SpinnerWheel(self.rewards)
        main_layout.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)

        # Spin Button
        self.spin_button = QPushButton("Spin")
        self.spin_button.setFont(QFont(self.font.family(), 14))
        self.spin_button.setFixedSize(100, 50)
        self.spin_button.clicked.connect(self.handle_spin)
        main_layout.addWidget(self.spin_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def handle_spin(self):
        email = self.email_input.text().strip()
        email_provided = bool(email)
        if email_provided:
            if "@" not in email or "." not in email:
                QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
                return
        # Insert into database
        try:
            self.cursor.execute("""
                INSERT INTO users (email, email_provided) VALUES (?, ?)
            """, (email if email_provided else None, email_provided))
            self.conn.commit()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to record your attempt: {e}")
            return
        # Spin the wheel
        self.spinner.spin()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply the custom font globally
    font_path = "Font/droidsans/DroidSans.ttf"
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family, 10))
    else:
        print(f"Failed to load DroidSans font from {font_path}.")

    window = SpinnerWindow()
    window.show()
    sys.exit(app.exec())