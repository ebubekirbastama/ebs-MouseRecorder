import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QLabel, QHeaderView, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QClipboard
from pynput import mouse
import pyautogui
import time

# ---------------------------
# Thread: Mouse listener
# ---------------------------
class MouseListenerThread(QThread):
    new_click = pyqtSignal(tuple)  # x, y koordinatlarını gönderir

    def run(self):
        def on_click(x, y, button, pressed):
            if pressed:
                self.new_click.emit((x, y))
        with mouse.Listener(on_click=on_click) as listener:
            self.listener = listener
            listener.join()

    def stop(self):
        if hasattr(self, 'listener'):
            self.listener.stop()

# ---------------------------
# Ana GUI
# ---------------------------
class MouseRecorderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EBS Mouse Koordinat Kaydedici ")
        self.setGeometry(200, 200, 600, 500)

        self.layout = QVBoxLayout()

        # Info label
        self.info_label = QLabel("Başlat'a basın ve mouse ile tıklayın. Koordinatlar tabloya eklenecek.")
        self.info_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.layout.addWidget(self.info_label)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Sıra", "X", "Y"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                gridline-color: #555555;
            }
            QHeaderView::section {
                background-color: #444444;
                color: white;
            }
        """)
        self.layout.addWidget(self.table)

        # Buttons
        self.start_btn = QPushButton("Başlat")
        self.start_btn.clicked.connect(self.start_listener)
        self.stop_btn = QPushButton("Bitir")
        self.stop_btn.clicked.connect(self.stop_listener)
        self.export_btn = QPushButton("Dışa Aktar (.txt)")
        self.export_btn.clicked.connect(self.export_txt)
        self.copy_btn = QPushButton("Clipboard'a Kopyala")
        self.copy_btn.clicked.connect(self.copy_clipboard)
        self.play_btn = QPushButton("Koordinatları Oynat")
        self.play_btn.clicked.connect(self.play_coordinates)
        self.delete_btn = QPushButton("Seçili Satırı Sil")
        self.delete_btn.clicked.connect(self.delete_selected)

        for btn in [self.start_btn, self.stop_btn, self.export_btn, self.copy_btn, self.play_btn, self.delete_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
            """)
            self.layout.addWidget(btn)

        self.setLayout(self.layout)
        self.counter = 0
        self.listener_thread = None
        self.coordinates = []

    # Başlat
    def start_listener(self):
        self.info_label.setText("Mouse listener başladı. Şimdi tıklayın...")
        self.start_btn.setEnabled(False)
        self.listener_thread = MouseListenerThread()
        self.listener_thread.new_click.connect(self.add_coordinate)
        self.listener_thread.start()

    # Durdur
    def stop_listener(self):
        if self.listener_thread:
            self.listener_thread.stop()
            self.listener_thread.quit()
            self.listener_thread.wait()
            self.info_label.setText("Mouse listener durduruldu.")
            self.start_btn.setEnabled(True)

    # Koordinat ekle
    def add_coordinate(self, pos):
        x, y = pos
        self.counter += 1
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(str(self.counter)))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(x)))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(y)))
        self.coordinates.append((x, y))
        self.info_label.setText(f"Koordinat {self.counter} eklendi: ({x}, {y})")

    # Dışa aktar (.txt)
    def export_txt(self):
        if not self.coordinates:
            QMessageBox.warning(self, "Uyarı", "Henüz koordinat yok!")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Dosya kaydet", "", "Text Files (*.txt)")
        if path:
            with open(path, "w") as f:
                for i, (x, y) in enumerate(self.coordinates, start=1):
                    f.write(f"{i}: ({x}, {y})\n")
            QMessageBox.information(self, "Başarılı", f"Koordinatlar kaydedildi:\n{path}")

    # Clipboard'a kopyala
    def copy_clipboard(self):
        if not self.coordinates:
            QMessageBox.warning(self, "Uyarı", "Henüz koordinat yok!")
            return
        clipboard = QApplication.clipboard()
        text = "\n".join([f"{i}: ({x}, {y})" for i, (x, y) in enumerate(self.coordinates, start=1)])
        clipboard.setText(text)
        QMessageBox.information(self, "Kopyalandı", "Tüm koordinatlar clipboard'a kopyalandı!")

    # Koordinatları oynat
    def play_coordinates(self):
        if not self.coordinates:
            QMessageBox.warning(self, "Uyarı", "Henüz koordinat yok!")
            return
        self.info_label.setText("Koordinatlar oynatılıyor...")
        for x, y in self.coordinates:
            pyautogui.moveTo(x, y, duration=0.5)  # Mouse'u hareket ettirir
            pyautogui.click()
            time.sleep(0.2)
        self.info_label.setText("Koordinatlar oynatma tamamlandı.")

    # Seçili satırı sil
    def delete_selected(self):
        selected_rows = set([idx.row() for idx in self.table.selectedIndexes()])
        if not selected_rows:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir satır seçin!")
            return
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)
            del self.coordinates[row]
        # Sıra numaralarını güncelle
        for i in range(self.table.rowCount()):
            self.table.setItem(i, 0, QTableWidgetItem(str(i+1)))
        self.counter = self.table.rowCount()
        self.info_label.setText("Seçili satırlar silindi.")

# ---------------------------
# Uygulama çalıştır
# ---------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    # Dark theme
    dark_palette = app.palette()
    dark_palette.setColor(dark_palette.Window, Qt.black)
    dark_palette.setColor(dark_palette.WindowText, Qt.white)
    dark_palette.setColor(dark_palette.Base, Qt.black)
    dark_palette.setColor(dark_palette.AlternateBase, Qt.gray)
    dark_palette.setColor(dark_palette.ToolTipBase, Qt.white)
    dark_palette.setColor(dark_palette.ToolTipText, Qt.white)
    dark_palette.setColor(dark_palette.Text, Qt.white)
    dark_palette.setColor(dark_palette.Button, Qt.black)
    dark_palette.setColor(dark_palette.ButtonText, Qt.white)
    dark_palette.setColor(dark_palette.Highlight, Qt.blue)
    dark_palette.setColor(dark_palette.HighlightedText, Qt.white)
    app.setPalette(dark_palette)

    window = MouseRecorderGUI()
    window.show()
    sys.exit(app.exec_())
