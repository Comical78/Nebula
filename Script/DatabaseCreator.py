import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QTabWidget, QPushButton, QFileDialog, QTextEdit, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

class DatabaseCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Creator")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.create_db_tab = QWidget()
        self.convert_sql_tab = QWidget()

        self.tab_widget.addTab(self.create_db_tab, "Create DB")
        self.tab_widget.addTab(self.convert_sql_tab, "Convert SQL")

        self.setup_create_db_tab()
        self.setup_convert_sql_tab()

    def setup_create_db_tab(self):
        layout = QVBoxLayout()
        self.create_db_tab.setLayout(layout)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        load_button = QPushButton("Load Database")
        load_button.clicked.connect(self.load_database)
        layout.addWidget(load_button)

    def setup_convert_sql_tab(self):
        layout = QVBoxLayout()
        self.convert_sql_tab.setLayout(layout)

        self.sql_text_edit = QTextEdit()
        layout.addWidget(self.sql_text_edit)

        button_layout = QHBoxLayout()
        load_sql_button = QPushButton("Load SQL File")
        load_sql_button.clicked.connect(self.load_sql_file)
        button_layout.addWidget(load_sql_button)

        preview_button = QPushButton("Preview SQL")
        preview_button.clicked.connect(self.preview_sql)
        button_layout.addWidget(preview_button)

        convert_button = QPushButton("Convert to DB")
        convert_button.clicked.connect(self.convert_to_db)
        button_layout.addWidget(convert_button)

        layout.addLayout(button_layout)

    def load_database(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Database File", "", "SQLite Files (*.db);;All Files (*)", options=options)
        if file_name:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            if tables:
                table_name = tables[0][0]
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                self.table_widget.setRowCount(len(rows))
                self.table_widget.setColumnCount(len(rows[0]) if rows else 0)

                for row_idx, row in enumerate(rows):
                    for col_idx, value in enumerate(row):
                        self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            conn.close()

    def load_sql_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open SQL File", "", "SQL Files (*.sql);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                sql_content = file.read()
                self.sql_text_edit.setPlainText(sql_content)

    def preview_sql(self):
        sql_content = self.sql_text_edit.toPlainText()
        if not sql_content.strip():
            QMessageBox.warning(self, "Warning", "SQL content is empty!")
            return

        preview_dialog = QMessageBox(self)
        preview_dialog.setWindowTitle("SQL Preview")
        preview_dialog.setText("SQL Content Preview:")
        preview_dialog.setInformativeText(sql_content)
        preview_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        preview_dialog.exec()

    def convert_to_db(self):
        sql_content = self.sql_text_edit.toPlainText()
        if not sql_content.strip():
            QMessageBox.warning(self, "Warning", "SQL content is empty!")
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Database File", "", "SQLite Files (*.db);;All Files (*)", options=options)
        if file_name:
            try:
                conn = sqlite3.connect(file_name)
                cursor = conn.cursor()
                cursor.executescript(sql_content)
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Success", "Database created successfully!")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to create database: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseCreator()
    window.show()
    sys.exit(app.exec())