import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
import subprocess

class WiFiPasswordApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıtlı Wi-Fi Parolaları")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Kayıtlı Wi-Fi Ağlarının Parolaları:", self)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.label)

        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.layout.addWidget(self.text_area)

        self.button = QPushButton("Parolaları Göster", self)
        self.button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px;")
        self.button.clicked.connect(self.show_passwords)
        self.layout.addWidget(self.button)

    def get_wifi_passwords(self):
        data = (
            subprocess.check_output(["netsh", "wlan", "show", "profiles"])
            .decode("utf-8")
            .split("\n")
        )
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        passwords = []
        for i in profiles:
            results = (
                subprocess
                .check_output(["netsh", "wlan", "show", "profile", i, "key=clear"])
                .decode("utf-8")
                .split("\n")
            )
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            password = results[0] if results else "Parola bulunamadı"
            passwords.append((i, password))
        return passwords

    def show_passwords(self):
        passwords = self.get_wifi_passwords()
        self.text_area.clear()
        for wifi, password in passwords:
            self.text_area.insertPlainText(f"Wi-Fi Adı: {wifi}\nParola: {password}\n\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WiFiPasswordApp()
    window.show()
    sys.exit(app.exec_())
