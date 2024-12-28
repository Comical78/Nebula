"""
has debugging features, use with caution
"""

import sys
import random
import string
import subprocess
from datetime import datetime
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QApplication, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon, QPalette, QBrush
from PyQt6.QtCore import Qt, QSize, QRect, QEvent
import base64
import json

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("LoginOverlay")

        # Set window size and make it non-resizable and non-maximizable
        self.setFixedSize(1000, 650)
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.MSWindowsFixedSizeDialogHint)

        # Set background image
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(QPixmap("Images/bg_main.png")))
        self.setPalette(palette)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create login widget
        self.login_widget = QWidget(central_widget)
        self.login_widget.setGeometry(
            QRect((1000 - 400) // 2, (650 - 300) // 2, 400, 300)
        )  # Center the login rectangle
        self.login_widget.setStyleSheet("background-color: transparent; border: 0px;")

        # Add background image (without resizing or cropping)
        background_image = QLabel(self.login_widget)
        background_image.move(0, 0)
        original_pixmap = QPixmap("Images/rect_logindialog.png")
        background_image.setPixmap(original_pixmap)
        background_image.resize(original_pixmap.size())

        # Add input fields
        self.account_id_input = QLineEdit(self.login_widget)
        self.account_id_input.setGeometry(50, 50, 300, 30)
        self.account_id_input.setPlaceholderText("   Account/ID")
        self.account_id_input.setStyleSheet("""
            QLineEdit {
                background-color: #e6e6e6;
                color: black;
                padding-left: 3px;
            }
            QLineEdit::placeholder {
                color: #b5b5b5;
            }
        """)

        self.password_input = QLineEdit(self.login_widget)
        self.password_input.setGeometry(50, 100, 300, 30)
        self.password_input.setPlaceholderText("   Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #e6e6e6;
                color: black;
                padding-left: 3px;
            }
            QLineEdit::placeholder {
                color: #b5b5b5;
            }
        """)

        # Add login button
        login_button = QPushButton(self.login_widget)
        login_button.setGeometry(50, 150, 300, 40)
        login_button.setText("Login")
        login_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: grey;
                color: white;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #007bff, stop: 1 #66b1ff); 
            }
        """)

        # Add "Can't Login?" and "Create Account" buttons
        cant_login_label = QLabel(self.login_widget)
        cant_login_label.setGeometry(50, 200, 150, 20)
        cant_login_label.setText("<a href='#'>Can't login?</a>")
        cant_login_label.setOpenExternalLinks(True)
        cant_login_label.setStyleSheet("background: transparent;")

        create_account_button = QPushButton(self.login_widget)
        create_account_button.setGeometry(270, 200, 150, 20)  # Moved further to the right
        create_account_button.setText("Create account")
        create_account_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: blue;
                text-decoration: underline;
                border: none;
            }
            QPushButton:hover {
                color: darkblue;
            }
        """)
        create_account_button.clicked.connect(self.show_create_account)

        # Add cancel button with hover effect (darkness change)
        self.cancel_button = QPushButton(self.login_widget)
        self.cancel_button.setGeometry(370, 10, 20, 20)
        self.cancel_button.setIcon(QIcon("Images/ic_cancel.png"))
        self.cancel_button.setIconSize(QSize(20, 20))
        self.cancel_button.setStyleSheet("border: none;")
        self.cancel_button.installEventFilter(self)

        # Create account widget
        self.create_account_widget = QWidget(central_widget)
        self.create_account_widget.setGeometry(
            QRect((1000 - 400) // 2, (650 - 300) // 2, 400, 300)
        )  # Center the create account rectangle
        self.create_account_widget.setStyleSheet("background-color: transparent; border: 0px;")
        self.create_account_widget.hide()

        # Add background image (without resizing or cropping)
        create_account_background_image = QLabel(self.create_account_widget)
        create_account_background_image.move(0, 0)
        create_account_background_pixmap = QPixmap("Images/rect_logindialog.png")
        create_account_background_image.setPixmap(create_account_background_pixmap)
        create_account_background_image.resize(create_account_background_pixmap.size())

        # Add input fields for create account
        self.username_input = QLineEdit(self.create_account_widget)
        self.username_input.setGeometry(50, 50, 300, 30)
        self.username_input.setPlaceholderText("   Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #e6e6e6;
                color: black;
                padding-left: 3px;
            }
            QLineEdit::placeholder {
                color: #b5b5b5;
            }
        """)

        self.create_password_input = QLineEdit(self.create_account_widget)
        self.create_password_input.setGeometry(50, 100, 300, 30)
        self.create_password_input.setPlaceholderText("   Password")
        self.create_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.create_password_input.setStyleSheet("""
            QLineEdit {
                background-color: #e6e6e6;
                color: black;
                padding-left: 3px;
            }
            QLineEdit::placeholder {
                color: #b5b5b5;
            }
        """)

        self.confirm_password_input = QLineEdit(self.create_account_widget)
        self.confirm_password_input.setGeometry(50, 150, 300, 30)
        self.confirm_password_input.setPlaceholderText("   Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setStyleSheet("""
            QLineEdit {
                background-color: #e6e6e6;
                color: black;
                padding-left: 3px;
            }
            QLineEdit::placeholder {
                color: #b5b5b5;
            }
        """)

        # Add create account button
        create_account_button = QPushButton(self.create_account_widget)
        create_account_button.setGeometry(50, 200, 300, 40)
        create_account_button.setText("Create Account")
        create_account_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: grey;
                color: white;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #007bff, stop: 1 #66b1ff); 
            }
        """)
        create_account_button.clicked.connect(self.register_account)

        # Add return button
        return_button = QPushButton(self.create_account_widget)
        return_button.setGeometry(50, 250, 300, 40)
        return_button.setText("Return to Login")
        return_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: grey;
                color: white;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #007bff, stop: 1 #66b1ff); 
            }
        """)
        return_button.clicked.connect(self.show_login)

        # Add cancel button with hover effect (darkness change) to create account widget
        self.create_account_cancel_button = QPushButton(self.create_account_widget)
        self.create_account_cancel_button.setGeometry(370, 10, 20, 20)
        self.create_account_cancel_button.setIcon(QIcon("Images/ic_cancel.png"))
        self.create_account_cancel_button.setIconSize(QSize(20, 20))
        self.create_account_cancel_button.setStyleSheet("border: none;")
        self.create_account_cancel_button.installEventFilter(self)

        # Connect signals and slots
        self.cancel_button.clicked.connect(self.close)
        self.create_account_cancel_button.clicked.connect(self.close)

    def show_create_account(self):
        self.login_widget.hide()
        self.create_account_widget.show()

    def show_login(self):
        self.create_account_widget.hide()
        self.login_widget.show()

    def eventFilter(self, source, event):
        if source in [self.cancel_button, self.create_account_cancel_button]:
            if event.type() == QEvent.Type.Enter:
                source.setIcon(QIcon("Images/ic_cancel_dark.png"))
            elif event.type() == QEvent.Type.Leave:
                source.setIcon(QIcon("Images/ic_cancel.png"))
        return super().eventFilter(source, event)

    def register_account(self):
        username = self.username_input.text().strip()
        password = self.create_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Warning", "All fields are required!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Warning", "Passwords do not match!")
            return

        # Generate userId, creationTime, and accessToken
        user_id = 1  # Assuming this is the first user
        creation_time = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
        access_token = ''.join(random.choices(string.ascii_letters + string.digits, k=24))

        # Construct the SQL command to create the table if it doesn't exist
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS account (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT NOT NULL,
            creationTime TEXT NOT NULL,
            accessToken TEXT NOT NULL
        );
        """

        # Construct the SQL command to insert the new account
        insert_account_sql = f"""
        INSERT INTO account (userId, password, creationTime, accessToken)
        VALUES ({user_id}, '{password}', '{creation_time}', '{access_token}');
        """

        # Encode the SQL commands in base64
        create_table_sql_base64 = base64.b64encode(create_table_sql.encode('utf-8')).decode('utf-8')
        insert_account_sql_base64 = base64.b64encode(insert_account_sql.encode('utf-8')).decode('utf-8')

        # Construct the curl command to create the table
        curl_create_table_command = [
            "curl", "-F", f"apikey={apikey-dbhub}",
            "-F", "dbowner={dbowner}", "-F", "dbname={dbname}",
            "-F", f"sql={create_table_sql_base64}",
            "https://api.dbhub.io/v1/execute"
        ]

        # Construct the curl command to insert the new account
        curl_insert_account_command = [
            "curl", "-F", f"apikey={apikey-dbhub}",
            "-F", "dbowner={dbowner}", "-F", "dbname={dbname}",
            "-F", f"sql={insert_account_sql_base64}",
            "https://api.dbhub.io/v1/execute"
        ]

        print("Executing curl command to create table:")
        print(" ".join(curl_create_table_command))

        try:
            result = subprocess.run(curl_create_table_command, capture_output=True, text=True)
            print("Curl command output for creating table:")
            print(result.stdout)
            print(result.stderr)
            if result.returncode != 0:
                QMessageBox.critical(self, "Error", f"Failed to create table: {result.stderr}")
                return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while creating table: {e}")
            return

        print("Executing curl command to insert account:")
        print(" ".join(curl_insert_account_command))

        try:
            result = subprocess.run(curl_insert_account_command, capture_output=True, text=True)
            print("Curl command output for inserting account:")
            print(result.stdout)
            print(result.stderr)
            if result.returncode == 0:
                response = result.stdout
                try:
                    response_json = json.loads(response)
                    if response_json.get("status") == "OK":
                        rows_changed = response_json.get("rows_changed", 0)
                        QMessageBox.information(self, "Success", f"Account created successfully! Rows changed: {rows_changed}")
                        self.show_login()
                    else:
                        QMessageBox.critical(self, "Error", f"Failed to create account: {response_json}")
                except json.JSONDecodeError:
                    QMessageBox.critical(self, "Error", f"Failed to parse response: {response}")
            else:
                QMessageBox.critical(self, "Error", f"Failed to create account: {result.stderr}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()