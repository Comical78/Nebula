import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QGraphicsOpacityEffect,
    QDialog,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QFrame,
)
from PyQt6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QTimer,
    QPoint,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
)
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QLinearGradient,
    QPainterPath,
    QPixmap,
    QFontDatabase,
    QFont,
)
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

class ScrollableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setStyleSheet("border: none; font-size: 11px; color: black;")
        self.setFixedWidth(370)  # Fix the width for proper alignment

class AnnouncementOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Terms of Services")
        self.setFixedSize(parent.size())
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")  # Darken the background

        # Create the central widget that fills the whole window
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background-color: rgba(79, 79, 79, 0.9); border-radius: 10px;")
        central_widget.setGeometry(0, 0, self.width(), self.height())
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
        ok_button.clicked.connect(self.close_overlay)
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

    def close_overlay(self):
        self.setParent(None)
        self.deleteLater()

def show_announcement(parent):
    overlay = AnnouncementOverlay(parent)
    overlay.show()

class ClickableLabel(QLabel):
    def __init__(self, parent=None, window=None):
        super().__init__(parent)
        self.window = window

    def mousePressEvent(self, event):
        if self.window:
            self.window.showNoticeDialog()

class RoundedProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(950, 30)
        self._progress = 0
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)

    def setProgress(self, value):
        self._progress = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        corner_radius = 15

        background_path = QPainterPath()
        background_path.addRoundedRect(0, 0, self.width(), self.height(), corner_radius, corner_radius)
        painter.fillPath(background_path, QColor(50, 50, 50))

        if self._progress > 0:
            progress_width = (self.width() * self._progress) / 100

            progress_path = QPainterPath()
            progress_path.addRoundedRect(0, 0, progress_width, self.height(), corner_radius, corner_radius)

            # Create a QLinearGradient object
            gradient = QLinearGradient(0, 0, progress_width, 0)

            # Set the gradient colors with a smooth transition
            gradient.setColorAt(0.0, QColor("#04d0ff"))  # Light blue
            gradient.setColorAt(0.5, QColor("#04d0ff"))  # Light blue
            gradient.setColorAt(0.5, QColor("#e702ff"))  # Pink
            gradient.setColorAt(1.0, QColor("#e702ff"))  # Pink

            painter.fillPath(progress_path, gradient)


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        image_path = "Images/bg_main.png"
        self.background = QPixmap(image_path)
        if self.background.isNull():
            print(f"Error: Failed to load background image from {image_path}.")

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_bg = self.background.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        painter.drawPixmap(self.rect(), scaled_bg)


class ProgressWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 650)
        self.setWindowTitle("Progress")

        # Load the font
        font_path = "Font/droidsans/DroidSans.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id < 0:
            print(f"Error loading font from {font_path}")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family)

        main_widget = BackgroundWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Bottom overlay with semi-transparent black background
        self.overlay = QWidget()
        self.overlay.setFixedHeight(150)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.45);")
        layout.addStretch()
        layout.addWidget(self.overlay)

        # Center container for progress bar and text
        self.center_container = QWidget(self.overlay)
        self.center_container.setGeometry(0, 0, 1000, 150)

        self.center_layout = QVBoxLayout(self.center_container)
        self.center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.center_layout.setSpacing(20)
        self.center_layout.setContentsMargins(25, 0, 25, 0)

        self.progress_bar = RoundedProgressBar()
        self.center_layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Horizontal layout for progress text
        self.progress_text_layout = QHBoxLayout()
        self.progress_text_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_text_layout.setSpacing(10)

        self.progress_message_label = QLabel("Resources are downloading, please wait...")
        self.progress_message_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            background: transparent;
        """)
        self.progress_message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.progress_text_layout.addWidget(self.progress_message_label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.progress_label = QLabel("0%")
        self.progress_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            background: transparent;
        """)
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.progress_text_layout.addWidget(self.progress_label, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.center_layout.addLayout(self.progress_text_layout)

        # Initialize start game logo (hidden initially)
        start_game_logo_path = "Images/bg_start_game_logo.png"
        self.start_game_logo = QLabel(main_widget)
        self.start_game_logo.setPixmap(QPixmap(start_game_logo_path))
        if self.start_game_logo.pixmap().isNull():
            print(f"Error: Failed to load start_game_logo image from {start_game_logo_path}.")
        self.start_game_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_game_logo.setVisible(False)

        self.start_game_opacity = QGraphicsOpacityEffect()
        self.start_game_logo.setGraphicsEffect(self.start_game_opacity)
        self.start_game_opacity.setOpacity(0)

        # Initialize enter game image and text
        enter_game_image_path = "Images/bg_enter_game_text.png"
        self.enter_game_image = QLabel(main_widget)
        self.enter_game_image.setPixmap(QPixmap(enter_game_image_path))
        if self.enter_game_image.pixmap().isNull():
            print(f"Error: Failed to load enter_game_image from {enter_game_image_path}.")
        self.enter_game_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.enter_game_image.setVisible(False)

        self.join_text = QLabel("Join the game", self.enter_game_image)
        self.join_text.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            background: transparent;
        """)
        self.join_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.join_text.setVisible(False)

        # Initialize notice and login images
        notice_image_path = "Images/bg_start_game_notice.png"
        self.notice_image = ClickableLabel(main_widget, window=self)
        self.notice_image.setPixmap(QPixmap(notice_image_path))
        if self.notice_image.pixmap().isNull():
            print(f"Error: Failed to load bg_start_game_notice.png from {notice_image_path}")
        self.notice_image.setVisible(False)
        self.notice_image.setCursor(Qt.CursorShape.PointingHandCursor)

        login_image_path = "Images/bg_start_game_login.png"
        self.login_image = QLabel(main_widget)
        self.login_image.setPixmap(QPixmap(login_image_path))
        if self.login_image.pixmap().isNull():
            print(f"Error: Failed to load bg_start_game_login.png from {login_image_path}")
        self.login_image.setVisible(False)

    def setProgress(self, value):
        self.progress_bar.setProgress(value)
        self.progress_label.setText(f"{int(value)}%")
        if value == 100:
            self.overlay.hide()
            self.startLogoAnimation()

    def startLogoAnimation(self):
        self.start_game_logo.setVisible(True)

        # Opacity animation for start game logo
        self.fade_animation = QPropertyAnimation(self.start_game_opacity, b"opacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Position animation for start game logo
        self.start_game_logo.setGeometry(
            (self.width() - self.start_game_logo.pixmap().width()) // 2,
            -self.start_game_logo.pixmap().height(),
            self.start_game_logo.pixmap().width(),
            self.start_game_logo.pixmap().height()
        )

        self.move_logo = QPropertyAnimation(self.start_game_logo, b"pos")
        self.move_logo.setDuration(1000)
        self.move_logo.setStartValue(self.start_game_logo.pos())
        end_pos_logo = QPoint(
            (self.width() - self.start_game_logo.pixmap().width()) // 2,
            (self.height() - self.start_game_logo.pixmap().height()) // 2 - 50
        )
        self.move_logo.setEndValue(end_pos_logo)
        self.move_logo.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Group animations
        self.logo_animation_group = QParallelAnimationGroup()
        self.logo_animation_group.addAnimation(self.fade_animation)
        self.logo_animation_group.addAnimation(self.move_logo)

        self.logo_animation_group.finished.connect(self.showEnterGame)

        self.logo_animation_group.start()

    def showEnterGame(self):
        self.enter_game_image.setVisible(True)
        self.join_text.setVisible(True)

        # Position image below logo
        self.enter_game_image.setGeometry(
            (self.width() - self.enter_game_image.pixmap().width()) // 2,
            self.start_game_logo.y() + self.start_game_logo.pixmap().height() + 20,
            self.enter_game_image.pixmap().width(),
            self.enter_game_image.pixmap().height()
        )

        # Center text in image
        self.join_text.setGeometry(
            0, 0,
            self.enter_game_image.pixmap().width(),
            self.enter_game_image.pixmap().height()
        )

        # Create flashing effect
        self.createFlashingEffect()

        # Start notice and login animations
        self.animateNoticeAndLogin()

    def createFlashingEffect(self):
        # Opacity effect for enter game image
        self.enter_game_opacity = QGraphicsOpacityEffect()
        self.enter_game_image.setGraphicsEffect(self.enter_game_opacity)
        self.enter_game_opacity.setOpacity(1)

        # Opacity effect for join text
        self.join_text_opacity = QGraphicsOpacityEffect()
        self.join_text.setGraphicsEffect(self.join_text_opacity)
        self.join_text_opacity.setOpacity(1)

        # Set durations for 2-second flashing effect
        fade_in_duration = 1000  # 1 second
        fade_out_duration = 1000  # 1 second

        # Fade in animation for enter game image
        fade_in_image = QPropertyAnimation(self.enter_game_opacity, b"opacity")
        fade_in_image.setDuration(fade_in_duration)
        fade_in_image.setStartValue(0)
        fade_in_image.setEndValue(1)

        # Fade out animation for enter game image
        fade_out_image = QPropertyAnimation(self.enter_game_opacity, b"opacity")
        fade_out_image.setDuration(fade_out_duration)
        fade_out_image.setStartValue(1)
        fade_out_image.setEndValue(0)

        # Fade in animation for join text
        fade_in_text = QPropertyAnimation(self.join_text_opacity, b"opacity")
        fade_in_text.setDuration(fade_in_duration)
        fade_in_text.setStartValue(0)
        fade_in_text.setEndValue(1)

        # Fade out animation for join text
        fade_out_text = QPropertyAnimation(self.join_text_opacity, b"opacity")
        fade_out_text.setDuration(fade_out_duration)
        fade_out_text.setStartValue(1)
        fade_out_text.setEndValue(0)

        # Sequential animation group for enter game image
        self.image_animation_group = QSequentialAnimationGroup()
        self.image_animation_group.addAnimation(fade_in_image)
        self.image_animation_group.addAnimation(fade_out_image)
        self.image_animation_group.setLoopCount(-1)  # Loop indefinitely

        # Sequential animation group for join text
        self.text_animation_group = QSequentialAnimationGroup()
        self.text_animation_group.addAnimation(fade_in_text)
        self.text_animation_group.addAnimation(fade_out_text)
        self.text_animation_group.setLoopCount(-1)  # Loop indefinitely

        # Start animations
        self.image_animation_group.start()
        self.text_animation_group.start()

    def animateNoticeAndLogin(self):
        # Position notice image off-screen to the left
        self.notice_image.setVisible(True)
        self.notice_image.setGeometry(
            -self.notice_image.pixmap().width(),
            20,  # Margin from top
            self.notice_image.pixmap().width(),
            self.notice_image.pixmap().height()
        )

        # Fly-in animation for notice image
        self.notice_anim = QPropertyAnimation(self.notice_image, b"pos")
        self.notice_anim.setDuration(1000)
        self.notice_anim.setStartValue(self.notice_image.pos())
        self.notice_anim.setEndValue(QPoint(20, 20))  # Margin from left and top
        self.notice_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        # After notice animation finishes, start login animation
        self.notice_anim.finished.connect(self.startLoginAnimation)

        self.notice_anim.start()

    def startLoginAnimation(self):
        # Position login image off-screen to the left, below notice
        self.login_image.setVisible(True)
        self.login_image.setGeometry(
            -self.login_image.pixmap().width(),
            self.notice_image.y() + self.notice_image.height() + 10,  # Below notice_image with some margin
            self.login_image.pixmap().width(),
            self.login_image.pixmap().height()
        )

        # Fly-in animation for login image
        self.login_anim = QPropertyAnimation(self.login_image, b"pos")
        self.login_anim.setDuration(1000)
        self.login_anim.setStartValue(self.login_image.pos())
        self.login_anim.setEndValue(QPoint(20, self.notice_image.y() + self.notice_image.height() + 10))
        self.login_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.login_anim.start()

    def showNoticeDialog(self):
        show_announcement(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressWindow()
    window.show()

    global progress
    progress = 0

    def updateProgress():
        global progress
        if progress <= 100:
            window.setProgress(progress)
            progress += 1
        else:
            timer.stop()

    timer = QTimer()
    timer.timeout.connect(updateProgress)
    timer.start(16)

    sys.exit(app.exec())