import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_main import Ui_MainWindow
from username_generator import load_names, generate_usernames

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Auto-load name files
        try:
            self.first_names = load_names('FName.txt')
            self.last_names = load_names('LName.txt')
        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))
            self.first_names, self.last_names = [], []

        # Connect signals
        self.ui.generateButton.clicked.connect(self.handle_generate)

    def handle_generate(self):
        try:
            count = int(self.ui.countSpinBox.value())
            symbols = self.ui.symbolsEdit.text().split() or ['_', '-']
            style = self.ui.styleCombo.currentText()
            use_numbers = self.ui.numbersCheck.isChecked()
            lowercase = self.ui.lowercaseCheck.isChecked()
            uppercase = self.ui.uppercaseCheck.isChecked()

            usernames = generate_usernames(
                self.first_names,
                self.last_names,
                symbols,
                count,
                style,
                use_numbers,
                lowercase,
                uppercase
            )

            self.ui.previewList.clear()
            self.ui.previewList.addItems(usernames)

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())