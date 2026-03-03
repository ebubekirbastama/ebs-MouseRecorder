import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QLabel, QHeaderView, QFileDialog, QMessageBox, QComboBox, QInputDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pynput import mouse
import pyautogui
import time

# ---------------------------
# Mouse Listener Thread
# ---------------------------
class MouseListenerThread(QThread):
    new_click = pyqtSignal(tuple, str)  # x, y, click_type

    def run(self):
        self.last_click_time = 0
        self.double_click_threshold = 0.4  # saniye

        def on_click(x, y, button, pressed):
            if pressed:
                current_time = time.time()
        
                if current_time - self.last_click_time <= self.double_click_threshold:
                    click_type = "Double Click"
                else:
                    click_type = "Single Click"
        
                self.last_click_time = current_time
        
                # ✅ HANGİ TUŞ
                if button == mouse.Button.left:
                    btn = "Left"
                elif button == mouse.Button.right:
                    btn = "Right"
                elif button == mouse.Button.middle:
                    btn = "Middle"
                else:
                    btn = "Left"
        
                self.new_click.emit((x, y), f"{btn} - {click_type}")

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
        self.setWindowTitle("Mouse Recorder + Typing")
        self.setGeometry(200, 200, 700, 600)

        self.layout = QVBoxLayout()
        self.info_label = QLabel("Başlat'a basın ve tıklayın. Yazı eklemek için 'Yazı Satırı Ekle' kullanın.")
        self.info_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.layout.addWidget(self.info_label)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Sıra", "X", "Y", "Eylem Türü", "Detay"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #2b2b2b; color: white; gridline-color: #555555; }
            QHeaderView::section { background-color: #444444; color: white; }
        """)
        self.layout.addWidget(self.table)

        # Buttons
        self.start_btn = QPushButton("Başlat")
        self.start_btn.clicked.connect(self.start_listener)
        self.stop_btn = QPushButton("Bitir")
        self.stop_btn.clicked.connect(self.stop_listener)
        self.add_text_btn = QPushButton("Yazı Satırı Ekle")
        self.add_text_btn.clicked.connect(self.add_text_row)
        self.export_btn = QPushButton("Dışa Aktar (.txt)")
        self.export_btn.clicked.connect(self.export_txt)
        self.copy_btn = QPushButton("Clipboard'a Kopyala")
        self.import_btn = QPushButton("İçeri Aktar (.txt)")
        self.import_btn.clicked.connect(self.import_txt)
        self.copy_btn.clicked.connect(self.copy_clipboard)
        self.play_btn = QPushButton("Koordinatları Oynat")
        self.play_btn.clicked.connect(self.play_coordinates)
        self.delete_btn = QPushButton("Seçili Satırı Sil")
        self.delete_btn.clicked.connect(self.delete_selected)
        for btn in [self.start_btn, self.stop_btn, self.add_text_btn, self.export_btn, self.import_btn, self.copy_btn, self.play_btn, self.delete_btn]:
            btn.setStyleSheet("""
                QPushButton { background-color: #0078d7; color: white; font-weight: bold; padding: 8px; border-radius: 5px; }
                QPushButton:hover { background-color: #005a9e; }
            """)
            self.layout.addWidget(btn)

        self.setLayout(self.layout)
        self.counter = 0
        self.listener_thread = None

    # Başlat
    def start_listener(self):
        self.info_label.setText("Mouse listener başladı. Tıklayın...")
        self.start_btn.setEnabled(False)
        self.listener_thread = MouseListenerThread()
        self.listener_thread.new_click.connect(self.add_click_row)
        self.listener_thread.start()

    # Bitir
    def stop_listener(self):
        if self.listener_thread:
            self.listener_thread.stop()
            self.listener_thread.quit()
            self.listener_thread.wait()
            self.start_btn.setEnabled(True)
    
            # ✅ SON EKLENENİ SİL (Bitir butonuna tıklamayı kaldır)
            if self.table.rowCount() > 0:
                last_row = self.table.rowCount() - 1
                self.table.removeRow(last_row)
    
                self.counter -= 1
    
                self.info_label.setText("Listener durduruldu. Son tıklama (Bitir) silindi.")
            else:
                self.info_label.setText("Listener durduruldu.")

    # Tıklama ekle
    def add_click_row(self, pos, click_info):
        x, y = pos
        self.counter += 1
        row = self.table.rowCount()
        self.table.insertRow(row)
    
        # click_info = "Left - Single Click"
        btn, click_type = click_info.split(" - ")
    
        self.table.setItem(row, 0, QTableWidgetItem(str(self.counter)))
        self.table.setItem(row, 1, QTableWidgetItem(str(x)))
        self.table.setItem(row, 2, QTableWidgetItem(str(y)))
    
        # Action
        action_combo = QComboBox()
        action_combo.addItems(["Click", "Type"])
        action_combo.setCurrentText("Click")
        self.table.setCellWidget(row, 3, action_combo)
    
        # Detail: Button + Click türü
        detail_combo = QComboBox()
        detail_combo.addItems([
            "Left - Single Click",
            "Left - Double Click",
            "Right - Single Click",
            "Right - Double Click",
            "Middle - Single Click"
        ])
        detail_combo.setCurrentText(f"{btn} - {click_type}")
        self.table.setCellWidget(row, 4, detail_combo)
    
        self.info_label.setText(f"{self.counter}. ({x},{y}) - {btn} - {click_type}")

    # Yazı satırı ekle
    def add_text_row(self):
        text, ok = QInputDialog.getText(self, "Yazı Satırı Ekle", "Yazılacak metni girin:")
        if ok and text.strip():
            self.counter += 1
            row = self.table.rowCount()
            self.table.insertRow(row)

            # X, Y boş olabilir
            self.table.setItem(row, 0, QTableWidgetItem(str(self.counter)))
            self.table.setItem(row, 1, QTableWidgetItem(""))
            self.table.setItem(row, 2, QTableWidgetItem(""))

            # Eylem Türü ComboBox
            action_combo = QComboBox()
            action_combo.addItems(["Click", "Type"])
            action_combo.setCurrentText("Type")
            self.table.setCellWidget(row, 3, action_combo)

            # Detay: yazı metni
            detail_item = QTableWidgetItem(text)
            self.table.setItem(row, 4, detail_item)

            self.info_label.setText(f"{self.counter}. Yazı satırı eklendi: '{text}'")

    # Dışa aktar
    def export_txt(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Uyarı", "Henüz veri yok!")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Dosya kaydet", "", "Text Files (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                for i in range(self.table.rowCount()):
                    x = self.table.item(i,1).text()
                    y = self.table.item(i,2).text()
                    action = self.table.cellWidget(i,3).currentText()
                    if action == "Click":
                        detail = self.table.cellWidget(i,4).currentText()
                    else:
                        detail = self.table.item(i,4).text()
                    f.write(f"{i+1}: ({x},{y}) - {action} - {detail}\n")
            QMessageBox.information(self, "Başarılı", f"Tablo kaydedildi: {path}")
    
    #İçeri Aktar
    def import_txt(self):
        path, _ = QFileDialog.getOpenFileName(self, "Dosya seç", "", "Text Files (*.txt)")
        if not path:
            return
    
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
    
            self.table.setRowCount(0)
            self.counter = 0
    
            for line in lines:
                try:
                    # Format:
                    # 1: (x,y) - Click - Left - Double Click
                    # 2: (x,y) - Click - Single Click   (eski)
                    # 3: (,) - Type - merhaba
    
                    parts = line.strip().split(" - ")
    
                    coords_part = parts[0].split(": ")[1]
                    action = parts[1]
    
                    # ✅ detail artık dinamik (önemli fix)
                    detail = " - ".join(parts[2:])
    
                    x, y = coords_part.strip("()").split(",")
    
                    self.counter += 1
                    row = self.table.rowCount()
                    self.table.insertRow(row)
    
                    self.table.setItem(row, 0, QTableWidgetItem(str(self.counter)))
                    self.table.setItem(row, 1, QTableWidgetItem(x))
                    self.table.setItem(row, 2, QTableWidgetItem(y))
    
                    # Action Combo
                    action_combo = QComboBox()
                    action_combo.addItems(["Click", "Type"])
                    action_combo.setCurrentText(action)
                    self.table.setCellWidget(row, 3, action_combo)
    
                    if action == "Click":
                        detail_combo = QComboBox()
                        detail_combo.addItems([
                            "Left - Single Click",
                            "Left - Double Click",
                            "Right - Single Click",
                            "Right - Double Click",
                            "Middle - Single Click"
                        ])
    
                        # ✅ Eski kayıt fix
                        if " - " in detail:
                            detail_combo.setCurrentText(detail)
                        else:
                            detail_combo.setCurrentText(f"Left - {detail}")
    
                        self.table.setCellWidget(row, 4, detail_combo)
    
                    else:  # Type
                        self.table.setItem(row, 4, QTableWidgetItem(detail))
    
                except Exception as e:
                    print("Satır okunamadı:", line, e)
    
            self.info_label.setText(f"{len(lines)} satır içeri aktarıldı.")
    
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya okunamadı:\n{e}")
            
    # Clipboard
    def copy_clipboard(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Uyarı", "Henüz veri yok!")
            return
        text = ""
        for i in range(self.table.rowCount()):
            x = self.table.item(i,1).text()
            y = self.table.item(i,2).text()
            action = self.table.cellWidget(i,3).currentText()
            if action == "Click":
                detail = self.table.cellWidget(i,4).currentText()
            else:
                detail = self.table.item(i,4).text()
            text += f"{i+1}: ({x},{y}) - {action} - {detail}\n"
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Kopyalandı", "Tablo clipboard'a kopyalandı!")

    # Oynat
    def play_coordinates(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Uyarı", "Henüz veri yok!")
            return
        self.info_label.setText("Oynatma başladı...")
        for i in range(self.table.rowCount()):
            action = self.table.cellWidget(i,3).currentText()
            if action == "Click":
                x = int(self.table.item(i,1).text())
                y = int(self.table.item(i,2).text())
                detail = self.table.cellWidget(i,4).currentText()
                
                if " - " in detail:
                    btn, click_type = detail.split(" - ")
                else:
                    btn = "Left"
                    click_type = detail
                
                button_map = {
                    "Left": "left",
                    "Right": "right",
                    "Middle": "middle"
                }
                
                pyautogui.moveTo(x, y, duration=0.5)
                
                if click_type.lower() == "double click":
                    pyautogui.click(button=button_map[btn], clicks=2, interval=0.1)
                else:
                    pyautogui.click(button=button_map[btn])
                pyautogui.moveTo(x, y, duration=0.5)
                if click_type.lower() == "double click":
                    pyautogui.click(clicks=2, interval=0.1)
                else:
                    pyautogui.click()
            else:  # Type
                text = self.table.item(i,4).text()
                pyautogui.write(text)
            time.sleep(0.2)
        self.info_label.setText("Oynatma tamamlandı.")

    # Seçili satır sil
    def delete_selected(self):
        selected_rows = set(idx.row() for idx in self.table.selectedIndexes())
        if not selected_rows:
            QMessageBox.warning(self, "Uyarı", "Lütfen satır seçin!")
            return
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)
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
    palette = app.palette()
    palette.setColor(palette.Window, Qt.black)
    palette.setColor(palette.WindowText, Qt.white)
    palette.setColor(palette.Base, Qt.black)
    palette.setColor(palette.AlternateBase, Qt.gray)
    palette.setColor(palette.ToolTipBase, Qt.white)
    palette.setColor(palette.ToolTipText, Qt.white)
    palette.setColor(palette.Text, Qt.white)
    palette.setColor(palette.Button, Qt.black)
    palette.setColor(palette.ButtonText, Qt.white)
    palette.setColor(palette.Highlight, Qt.blue)
    palette.setColor(palette.HighlightedText, Qt.white)
    app.setPalette(palette)

    window = MouseRecorderGUI()
    window.show()
    sys.exit(app.exec_())
