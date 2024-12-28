import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QScrollArea
)
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt, QPoint

class ScrollableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setStyleSheet("border: none; font-size: 11px; color: black;")
        self.setFixedWidth(370)  # Fix the width for proper alignment

class AnnouncementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terms of Services")
        self.setFixedSize(1000, 650)
        self.setStyleSheet("background-color: rgb(79, 79, 79);")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load the custom font
        font_id = QFontDatabase.addApplicationFont("Font/DIN/DIN-Medium.ttf")
        if font_id == -1:
            print("Failed to load font.")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.custom_font = QFont(font_family, 11, QFont.Weight.Light)

        # Load the font for the OK button
        ok_font_id = QFontDatabase.addApplicationFont("Font/DIN/DIN-Regular.ttf")
        if ok_font_id == -1:
            print("Failed to load OK button font.")
        else:
            ok_font_family = QFontDatabase.applicationFontFamilies(ok_font_id)[0]
            self.ok_button_font = QFont(ok_font_family, 12, QFont.Weight.Bold)

        # Create the announcement box
        announcement_box = QWidget(self)
        announcement_box.setFixedSize(400, 450)
        announcement_box.setStyleSheet("background-color: white; border-radius: 10px;")

        box_layout = QVBoxLayout(announcement_box)
        box_layout.setContentsMargins(10, 10, 10, 10)

        # Create the announcement title
        title_label = QLabel("Terms of Services", self)
        title_label.setFont(QFont(self.custom_font.family(), 16, QFont.Weight.Light))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box_layout.addWidget(title_label)

        # Create the scrollable text area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedSize(370, 350)
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = ScrollableLabel(
            "Welcome to Blockman Forge!\n\n"
            "Copyright © [2024] Drej aka AxtonDonovan. All rights reserved.\n\n"
            "These terms of service (\"Terms\") govern your access to and use of Blockman Forge (\"the Game\"), provided by [Drej] aka [AxtonDonovan] (\"we\", \"us\", or \"our\"). By accessing or using the Game, you agree to be bound by these Terms. If you do not agree to these Terms, do not access or use the Game.\n\n"
            "1. License and Use: [Drej] aka [AxtonDonovan] grants you a limited, non-exclusive, non-transferable license to download and play the Game for personal use only. You may not modify, distribute, transmit, display, perform, reproduce, publish, license, create derivative works from, transfer, or sell any information, software, products, or services obtained from the Game. Modifying or editing the Blockman Forge application may result in violations of copyright law.\n\n"
            "2. User Content: By using the Game, you may submit content, including but not limited to text, images, and other materials (\"User Content\"). You retain ownership of any intellectual property rights that you hold in the User Content. By submitting User Content, you grant [Drej] aka [AxtonDonovan] a worldwide, non-exclusive, royalty-free, sublicensable, and transferable license to use, reproduce, distribute, prepare derivative works of, display, and perform the User Content in connection with the Game.\n\n"
            "3. Prohibited Conduct: You agree not to engage in any of the following prohibited activities: (a) use the Game for any illegal purpose or in violation of any local, state, national, or international law; (b) violate or infringe upon the rights of others, including privacy, publicity, intellectual property, or contractual rights; (c) engage in any conduct that restricts or inhibits anyone's use or enjoyment of the Game; (d) attempt to gain unauthorized access to the Game or its related systems or networks.\n\n"
            "4. Original Content Disclaimer: Blockman Forge is a fanmade game inspired by [BlockMan Go], and is not affiliated with or endorsed by [SandBox / GVERSE]. All original content and intellectual property rights related to [SandBox / GVERSE] belong to their respective owners.\n\n"
            "5. Modification and Fanmade Games: If you wish to modify or create your own fanmade game based on Blockman Forge, we recommend using the original Blockman Go APK and giving proper credits to [SandBox / GVERSE]. Unauthorized modification of Blockman Forge may result in copyright infringement.\n\n"
            "6. Termination: We may terminate or suspend your access to the Game without prior notice or liability for any reason, including if you violate these Terms.\n\n"
            "7. Disclaimer of Warranties: The Game is provided \"as is\" without warranties of any kind, either express or implied, including, but not limited to, implied warranties of merchantability, fitness for a particular purpose, or non-infringement.\n\n"
            "8. Limitation of Liability: [Drej] aka [AxtonDonovan] shall not be liable for any indirect, incidental, special, consequential, or punitive damages, or any loss of profits or revenues, whether incurred directly or indirectly, or any loss of data, use, goodwill, or other intangible losses, resulting from (a) your access to or use of or inability to access or use the Game; (b) any conduct or content of any third party on the Game.\n\n"
            "9. Changes to Terms: We reserve the right to modify or replace these Terms at any time. If a revision is material, we will provide at least 30 days' notice prior to any new terms taking effect. What constitutes a material change will be determined at our sole discretion.\n\n"
            "10. Governing Law: These Terms shall be governed by and construed in accordance with the laws of [World Wide], without regard to its conflict of law provisions.\n\n"
            "11. Contact Us: If you have any questions about these Terms, please contact us at [Our Community Discord Server].\n\n"
            "By using Blockman Forge, you agree to these Terms. Enjoy the game!",
            self,
        )
        scroll_content.setFont(self.custom_font)
        scroll_area.setWidget(scroll_content)
        box_layout.addWidget(scroll_area)

        # Create the separator line
        separator_line = QFrame(self)
        separator_line.setFrameShape(QFrame.Shape.HLine)
        separator_line.setFrameShadow(QFrame.Shadow.Plain)
        separator_line.setStyleSheet("background-color: black;")
        separator_line.setFixedHeight(1)
        separator_line.setFixedWidth(380)  # Match the width of the parent layout
        separator_line.raise_()  # Bring the separator line to the front
        box_layout.addWidget(separator_line, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create the OK button
        ok_button = QPushButton("OK", self)
        ok_button.setFixedWidth(380)  # Match button width to parent layout
        ok_button.setStyleSheet(
            "background-color: transparent; color: #0051ff; border: none; height: 30px; font-size: 14px; border-radius: 5px;"
        )
        ok_button.setFont(self.ok_button_font)  # Use the bold font for the OK button
        ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_button.clicked.connect(self.close)
        box_layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(announcement_box)

        # Enable mouse dragging for scrolling
        self.scroll_area = scroll_area
        self.scroll_area.viewport().installEventFilter(self)
        self.dragging = False
        self.last_pos = QPoint()

    def eventFilter(self, source, event):
        if source == self.scroll_area.viewport():
            if event.type() == event.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.dragging = True
                    self.last_pos = event.pos()
                    return True
            elif event.type() == event.Type.MouseMove:
                if self.dragging:
                    delta = event.pos() - self.last_pos
                    self.scroll_area.verticalScrollBar().setValue(
                        self.scroll_area.verticalScrollBar().value() - delta.y()
                    )
                    self.last_pos = event.pos()
                    return True
            elif event.type() == event.Type.MouseButtonRelease:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.dragging = False
                    return True
        return super().eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnnouncementWindow()
    window.show()
    sys.exit(app.exec())