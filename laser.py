import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QLinearGradient, QColor
import ctypes
from ctypes import wintypes
from pynput import keyboard, mouse

def update_gradient_position():
    global gradient_position, timer
    gradient_position -= 0.5
    if gradient_position < 0:
        timer.stop()
        gradient_position = 0
    window.update()

def paint_event(event):
    painter = QPainter(window)
    gradient = QLinearGradient(0, gradient_position, 0, window.height())
    gradient.setColorAt(0, QColor(255, 0, 0, 0))
    gradient.setColorAt(1, QColor(255, 0, 0, 100))
    painter.fillRect(window.rect(), gradient)

def exit_app(event=None):
    QApplication.quit()
    
    

app = QApplication.instance()
if not app:  # Create a new instance if no instance exists
    app = QApplication(sys.argv)

window = QWidget()
window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput | Qt.Tool | Qt.WindowSystemMenuHint)
window.setAttribute(Qt.WA_TranslucentBackground)

screen = QApplication.primaryScreen().size()
taskbar_handle = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
rect = wintypes.RECT()
ctypes.windll.user32.GetWindowRect(taskbar_handle, ctypes.byref(rect))
taskbar_height = (rect.bottom - rect.top) * 2

window.setGeometry(0, screen.height() - taskbar_height, screen.width(), taskbar_height)

gradient_position = window.height()
timer = QTimer(window)
timer.timeout.connect(update_gradient_position)
timer.start(100)

window.paintEvent = paint_event

keyboard_listener = keyboard.Listener(on_press=exit_app)
mouse_listener = mouse.Listener(on_move=lambda x, y: exit_app())

keyboard_listener.start()
mouse_listener.start()

window.show()
app.exec_()

    