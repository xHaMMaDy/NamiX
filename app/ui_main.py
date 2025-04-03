from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QLineEdit, QCheckBox, QComboBox, QTabWidget, QSpinBox, QApplication, QFileDialog, QHBoxLayout, QGridLayout
import qtawesome as qta
from PySide6.QtCore import QSize, Qt, QMimeData, QPropertyAnimation
import json
import csv

class Ui_MainWindow(object):
    default_first_names = '''Maya
Bahaa
Fadel
Muslim
Mohammad
Naji
Yasmine
Adnan
Mohameed
Mansour
...'''.splitlines()
    default_last_names = '''Bahaa
Fadel
Muslim
Mohammad
Naji
Adnan
Mohameed
Mansour
...'''.splitlines()

    def choose_name_file(self, role):
        path, _ = QFileDialog.getOpenFileName(None, f"Choose {role} name file", "", "Text Files (*.txt)")
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]
                    if role == "First":
                        self.first_names = lines
                    else:
                        self.last_names = lines
            except Exception as e:
                print(f"Error reading {role} name file:", e)
    def copy_selected(self):
        items = self.previewList.selectedItems()
        if items:
            clipboard = QApplication.clipboard()
            clipboard.setText(items[0].text())

    def copy_all(self):
        items = [self.previewList.item(i).text() for i in range(self.previewList.count())]
        clipboard = QApplication.clipboard()
        clipboard.setText('\n'.join(items))

    def export_usernames(self, filetype):
        if filetype == 'txt':
            path, _ = QFileDialog.getSaveFileName(None, "Save as TXT", "usernames.txt", "Text Files (*.txt)")
            if path:
                with open(path, 'w', encoding='utf-8') as f:
                    for i in range(self.previewList.count()):
                        f.write(self.previewList.item(i).text() + '\n')
        elif filetype == 'csv':
            path, _ = QFileDialog.getSaveFileName(None, "Save as CSV", "usernames.csv", "CSV Files (*.csv)")
            if path:
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['username'])
                    for i in range(self.previewList.count()):
                        writer.writerow([self.previewList.item(i).text()])
        elif filetype == 'json':
            path, _ = QFileDialog.getSaveFileName(None, "Save as JSON", "usernames.json", "JSON Files (*.json)")
            if path:
                data = [self.previewList.item(i).text() for i in range(self.previewList.count())]
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

    def enable_dragging(self, MainWindow):
        def mousePressEvent(event):
            if event.button() == Qt.LeftButton:
                self._drag_pos = event.globalPosition().toPoint()

        def mouseMoveEvent(event):
            if event.buttons() == Qt.LeftButton:
                MainWindow.move(MainWindow.pos() + event.globalPosition().toPoint() - self._drag_pos)
                self._drag_pos = event.globalPosition().toPoint()

        self.title_bar.mousePressEvent = mousePressEvent
        self.title_bar.mouseMoveEvent = mouseMoveEvent

    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("NamiX")
        MainWindow.setWindowIcon(qta.icon('fa5s.microchip'))
        MainWindow.resize(600, 400)
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #2e3440;
                color: #d8dee9;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 1px solid #4c566a;
                background: #2e3440;
            }
            QTabBar::tab {
                background: #4c566a;
                color: #d8dee9;
                padding: 8px;
                margin: 1px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #5e81ac;
            }
            QPushButton {
                background-color: #5e81ac;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #81a1c1;
            }
            QLineEdit, QComboBox, QSpinBox, QListWidget {
                background-color: #434c5e;
                color: #eceff4;
                border: 1px solid #5e81ac;
                border-radius: 4px;
                padding: 4px;
            }
            QCheckBox {
                spacing: 6px;
            }
        """)

        MainWindow.setWindowFlags(MainWindow.windowFlags() | Qt.FramelessWindowHint)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)

        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(35)
        self.title_bar.setStyleSheet("background-color: #3b4252;")

        self.title_layout = QHBoxLayout(self.title_bar)
        from PySide6.QtCore import QPropertyAnimation
        self.logo_icon = QLabel()
        self.logo_icon.setPixmap(qta.icon('fa5s.microchip').pixmap(20, 20))
        self.title_layout.addWidget(self.logo_icon)

        self.title_label = QLabel("NamiX")
        self.title_label.setStyleSheet("font-weight: bold; margin-left: 10px;")
        self.title_layout.addWidget(self.title_label)

        self.title_anim = QPropertyAnimation(self.title_label, b"styleSheet")
        self.title_anim.setDuration(1000)
        self.title_anim.setStartValue("color: transparent;")
        self.title_anim.setEndValue("color: white; font-weight: bold; margin-left: 10px;")
        self.title_anim.start()

        self.minimizeButton = QPushButton("−")
        self.minimizeButton.setFixedSize(35, 25)
        self.minimizeButton.setStyleSheet("background-color: #4c566a; color: #d8dee9; border: none;")
        self.title_layout.addWidget(self.minimizeButton)

        self.closeButton = QPushButton("×")
        self.closeButton.setFixedSize(35, 25)
        self.closeButton.setStyleSheet("background-color: #bf616a; color: white; border: none;")
        self.title_layout.addWidget(self.closeButton)

        self.closeButton.clicked.connect(MainWindow.close)
        self.minimizeButton.clicked.connect(MainWindow.showMinimized)

        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.enable_dragging(MainWindow)

        self.layout = QVBoxLayout(self.centralwidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.title_bar)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Tab 1: Settings
        self.first_names = self.default_first_names
        self.last_names = self.default_last_names
        self.tab_settings = QWidget()
        self.tabs.addTab(self.tab_settings, "⚙️ Settings")
        from PySide6.QtWidgets import QFormLayout
        self.settings_layout = QFormLayout(self.tab_settings)
        self.settings_layout.setLabelAlignment(Qt.AlignLeft)

        self.countSpinBox = QSpinBox()
        self.countSpinBox.setMinimum(1)
        self.countSpinBox.setMaximum(10000)
        self.countSpinBox.setValue(10)
        self.settings_layout.addWidget(QLabel("🔢 Number of usernames:"))
        self.settings_layout.addWidget(self.countSpinBox)

        self.symbolsEdit = QLineEdit()
        self.symbolsEdit.setPlaceholderText("e.g. _ -")
        self.settings_layout.addWidget(QLabel("🔣 Symbols (space-separated):"))
        self.settings_layout.addWidget(self.symbolsEdit)

        self.styleCombo = QComboBox()
        self.styleCombo.addItems([
            'first_last', 'last.first', 'fLast', 'f.Last', 'f.last+num',
            'firstlast', 'lastfirst', 'first.last', 'firstL', 'firstLnum', 'random'
        ])
        self.settings_layout.addWidget(QLabel("🎨 Username style:"))
        self.settings_layout.addWidget(self.styleCombo)

        self.numbersCheck = QCheckBox("🔢 Include numbers")
        self.numbersCheck.setChecked(True)
        self.settings_layout.addWidget(self.numbersCheck)

        self.lowercaseCheck = QCheckBox("🔡 Convert to lowercase")
        self.settings_layout.addWidget(self.lowercaseCheck)

        self.uppercaseCheck = QCheckBox("🔠 Convert to uppercase")
        self.settings_layout.addWidget(self.uppercaseCheck)

        self.chooseFBtn = QPushButton(qta.icon('fa5s.file-import'), " Choose FName.txt")
        self.chooseFBtn.clicked.connect(lambda: self.choose_name_file("First"))
        self.settings_layout.addWidget(self.chooseFBtn)

        self.chooseLBtn = QPushButton(qta.icon('fa5s.file-import'), " Choose LName.txt")
        self.chooseLBtn.clicked.connect(lambda: self.choose_name_file("Last"))
        self.settings_layout.addWidget(self.chooseLBtn)

        # Tab 2: Preview
        self.tab_preview = QWidget()
        self.tabs.addTab(self.tab_preview, "👁️ Preview")
        self.preview_layout = QVBoxLayout(self.tab_preview)
        self.preview_controls = QHBoxLayout()

        self.generateButton = QPushButton(qta.icon('fa5s.cogs'), " Generate Usernames")
        self.preview_controls.addWidget(self.generateButton)

        self.previewList = QListWidget()
        self.preview_layout.addWidget(self.previewList)

        self.copyButton = QPushButton(qta.icon('fa5s.copy'), " Copy Selected")
        self.preview_controls.addWidget(self.copyButton)

        self.copyAllButton = QPushButton(qta.icon('fa5s.copy'), " Copy All")
        self.copyButton.clicked.connect(lambda: self.copy_selected())
        self.copyAllButton.clicked.connect(lambda: self.copy_all())
        self.preview_controls.addWidget(self.copyAllButton)
        self.preview_layout.addLayout(self.preview_controls)

        # Tab 3: Export
        self.tab_export = QWidget()
        self.tabs.addTab(self.tab_export, "💾 Export")
        self.export_layout = QGridLayout(self.tab_export)

        self.export_layout.addWidget(QLabel("🗃️ Choose export format:"))

        self.exportTxtBtn = QPushButton(qta.icon('fa5s.file-alt'), " Export to TXT")
        self.exportCsvBtn = QPushButton(qta.icon('fa5s.table'), " Export to CSV")
        self.exportJsonBtn = QPushButton(qta.icon('fa5s.code'), " Export to JSON")

        self.export_layout.addWidget(self.exportTxtBtn, 1, 0)
        self.export_layout.addWidget(self.exportCsvBtn, 1, 1)
        self.export_layout.addWidget(self.exportJsonBtn, 1, 2)

        self.fileDialog = QFileDialog()

        # About info in export tab
        self.about_layout = QVBoxLayout()
        self.about_label = QLabel("👤 Made by <b>Ibrahim Hammad</b> aka <b>HaMMaDy</b><br>🐙 GitHub: <a href='https://github.com/xHaMMaDy'>xHaMMaDy</a><br>📧 Email: <a href='mailto:xhammady@gmail.com'>xhammady@gmail.com</a>")
        self.about_label.setOpenExternalLinks(True)
        self.about_layout.addWidget(self.about_label)
        self.export_layout.addLayout(self.about_layout, 2, 0, 1, 3)
        self.exportTxtBtn.clicked.connect(lambda: self.export_usernames('txt'))
        self.exportCsvBtn.clicked.connect(lambda: self.export_usernames('csv'))
        self.exportJsonBtn.clicked.connect(lambda: self.export_usernames('json'))