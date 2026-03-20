import sys
import os
import json
import keyboard
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPixmap, QFont

COUNTER_FILE = "C:/Users/max.valentin/Documents/TIATIL00S/bongoclone/counter.json"

class BongoOverlay(QLabel):
    def __init__(self):
        super().__init__()
        # Transparent och alltid ovanpå
        self.setWindowFlags(Qt.FramelessWindowHint | 
                            Qt.WindowStaysOnTopHint |
                            Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Ladda sprite sheet
        self.sheet = QPixmap("C:/Users/max.valentin/Documents/TIATIL00S/bongoclone/assets/bongoclone_sheet.png")
        if self.sheet.isNull():
            print("Fel: kunde inte ladda bongoclone_sheet.png")
            sys.exit(1)

        self.frame_width = 64
        self.frame_height = 64

        # Frames: 0=idle, 1=vänster, 2=höger
        self.current_frame = 0
        self.setFixedSize(self.frame_width, self.frame_height)
        self.update_frame()

        # Load taps
        self.taps = self.load_counter()

        # Skapa label för taps
        self.counter_label = QLabel(str(self.taps), self)
        self.counter_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.counter_label.setStyleSheet("color: white; background-color: rgba(0,0,0,150); border-radius: 5px; padding: 2px;")
        self.counter_label.move(-20, 0)  # ovanför katten
        self.counter_label.adjustSize()

        # Setup keyboard hooks
        self.setup_keyboard_hooks()

    # ---------------- Tap-räknare -----------------
    def increment_counter(self):
        self.taps += 1
        self.counter_label.setText(str(self.taps))
        self.counter_label.adjustSize()
        self.save_counter()

    def load_counter(self):
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("taps", 0)
            except:
                return 0
        return 0

    def save_counter(self):
        with open(COUNTER_FILE, "w") as f:
            json.dump({"taps": self.taps}, f)

    # ---------------- Keyboard & animation -----------------
    def setup_keyboard_hooks(self):
        left_keys = set("123456yhqwertasdfgzxcvb")
        right_keys = set("7890uiopjklbnm")

        def on_key(event):
            if event.event_type != "down":
                return
            key = event.name.lower()
            if len(key) != 1:
                return
            if key in left_keys:
                QTimer.singleShot(0, self.play_left)
            elif key in right_keys:
                QTimer.singleShot(0, self.play_right)

        keyboard.hook(on_key)

    def play_left(self):
        self.current_frame = 1
        self.update_frame()
        self.increment_counter()
        QTimer.singleShot(100, self.reset_to_idle)

    def play_right(self):
        self.current_frame = 2
        self.update_frame()
        self.increment_counter()
        QTimer.singleShot(100, self.reset_to_idle)

    def reset_to_idle(self):
        self.current_frame = 0
        self.update_frame()

    # ---------------- Sprite sheet -----------------
    def get_frame(self, frame_index):
        rect = QRect(frame_index * self.frame_width, 0, self.frame_width, self.frame_height)
        return self.sheet.copy(rect)

    def update_frame(self):
        self.setPixmap(self.get_frame(self.current_frame))

# ---------------- Main -----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = BongoOverlay()
    overlay.show()

    # Placering nära taskbar (1080p)
    overlay.move(960, 940)

    sys.exit(app.exec_())
