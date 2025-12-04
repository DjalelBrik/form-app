import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFrame, QPushButton, QLabel, QLineEdit,
    QComboBox, QTableWidget, QWidget, QVBoxLayout, QDesktopWidget,
    QHBoxLayout, QGridLayout, QTableWidgetItem, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
import sqlite3
from datetime import datetime
from PyQt5.QtGui import QIcon




APP_STYLES = """
/* Base */
QMainWindow {
    background-color: #0a0f2e;
}
QWidget {
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
    color: black;
}

/* Header bar */
#HeaderBar {
    background-color: #0f1a48;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

/* Header buttons */
QPushButton.HeaderBtn {
    background: transparent;
    color: #e9edf1;
    padding: 8px 14px;
    border-radius: 10px;
}
QPushButton.HeaderBtn:hover {
    background: rgba(255,255,255,0.08);
}
QPushButton.HeaderBtn:pressed {
    background: rgba(255,255,255,0.12);
}

/* Primary buttons */
QPushButton.Primary {
    background-color: #2463EB; /* indigo-500 */
    color: white;
    padding: 10px 18px;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}
QPushButton.Primary:hover {
    background-color: #1e4ed8; /* indigo-600 */
}
QPushButton.Primary:pressed {
    background-color: #1b46c4;
}

/* Danger & Success buttons (panel) */
QPushButton.Danger {
    background-color: #e11d48; /* rose-600 */
    color: white;
    padding: 8px 14px;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}
QPushButton.Danger:hover { background-color: #be123c; }

QPushButton.Success {
    background-color: #16a34a; /* green-600 */
    color: white;
    padding: 8px 14px;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}
QPushButton.Success:hover { background-color: #15803d; }

/* Inputs */
QLineEdit, QComboBox {
    background: #0f1a48;
    color: #e9edf1;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 10px 12px;
    selection-background-color: #2463EB;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #2463EB;
}

/* Section labels */
QLabel.SectionTitle {
    color: #c7d2fe; /* indigo-200 */
    font-weight: 700;
    letter-spacing: .5px;
}

/* Cards / panels */
QFrame.Card {
    background: #0d153f;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
}

/* Table */
QTableWidget {
    background: #0d153f;
    alternate-background-color: #0b1236;
    color: #e9edf1;
    gridline-color: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
}
QHeaderView::section {
    background: #0f1a48;
    color: #c7d2fe;
    padding: 10px;
    border: none;
    font-weight: 700;
}
QTableWidget::item {
    padding: 8px;
}

/* Subtle separators */
QFrame.Separator {
    background: rgba(255,255,255,0.08);
    max-height: 1px;
}
"""

def center_and_fix(window, w=1200, h=700):
    window.setFixedSize(w, h)
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form App")
        self.setWindowIcon(QIcon("icon.ico"))
        center_and_fix(self, 1200, 700)
        self.setStyleSheet(APP_STYLES)

        # Central layout
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(16)

        # Header
        self.header = QFrame()
        self.header.setObjectName("HeaderBar")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(16, 12, 16, 12)

        self.label1 = QLabel("Home")
        self.label1.setStyleSheet("font-size: 18px; font-weight: 700; color: #c7d2fe;")
        header_layout.addWidget(self.label1)

        header_layout.addStretch(1)

        self.btn_show = QPushButton("Show Content")
        self.btn_show.setProperty("class", "HeaderBtn")
        self.btn_show.setObjectName("HeaderBtn")
        self.btn_show.setStyleSheet("")  # use class styling
        self.btn_show.setCursor(Qt.PointingHandCursor)
        self.btn_show.setAccessibleName("Show Content")
        self.btn_show.setAccessibleDescription("Open the content listing")

        self.btn_add = QPushButton("Add New Content")
        self.btn_add.setProperty("class", "HeaderBtn")
        self.btn_add.setObjectName("HeaderBtn")
        self.btn_add.setStyleSheet("")
        self.btn_add.setCursor(Qt.PointingHandCursor)

        for b in (self.btn_show, self.btn_add):
            b.setMinimumHeight(36)
            b.setMinimumWidth(140)
            b.setStyleSheet("QPushButton {padding:8px 14px; border-radius:10px;}")

        header_layout.addWidget(self.btn_show)
        header_layout.addWidget(self.btn_add)
        root.addWidget(self.header)

        # Welcome Card
        hero = QFrame()
        hero.setObjectName("Hero")
        hero.setProperty("class", "Card")
        hero.setStyleSheet("")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 40, 24, 40)

        self.label2 = QLabel("Welcome")
        self.label2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label2.setStyleSheet("font-size: 56px; font-weight: 800; color: #e9edf1;")
        subtitle = QLabel("Manage users and booking preferences ")
        subtitle.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        subtitle.setStyleSheet("color:#94a3b8; font-size:16px;")
        hero_layout.addWidget(self.label2)
        hero_layout.addWidget(subtitle)

        root.addWidget(hero, 1)

        # Secondary actions
        actions = QHBoxLayout()
        actions.addStretch(1)
      
        
        actions.addSpacing(8)
    
        actions.addStretch(1)
        root.addLayout(actions)

        # Windows
        self.show_window = ShowWindow(self)
        self.add_window = AddWindow(self.show_window, self)

        # Connections (logic unchanged)
        self.btn_show.clicked.connect(self.open_show_window)
        self.btn_add.clicked.connect(self.open_add_window)
       

    def open_show_window(self):
        self.show_window.load_data()  # refresh table
        self.show_window.show()
        self.hide()

    def open_add_window(self):
        self.add_window.show()
        self.hide()



class ShowWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Form App")
        self.setWindowIcon(QIcon("icon.ico"))
        center_and_fix(self, 1200, 700)
        self.setStyleSheet(APP_STYLES)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        # Header
        self.header = QFrame()
        self.header.setObjectName("HeaderBar")
        self.header.setStyleSheet("")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(16, 12, 16, 12)

        self.label1 = QLabel("Home")
        self.label1.setStyleSheet("font-size: 18px; font-weight: 700; color: #c7d2fe;")
        header_layout.addWidget(self.label1)

        header_layout.addStretch(1)

        self.btn_show = QPushButton("Show Content")
        self.btn_show.setProperty("class", "HeaderBtn")
        self.btn_show.setStyleSheet("")
        self.btn_add = QPushButton("Add New Content")
        self.btn_add.setProperty("class", "HeaderBtn")
        self.btn_add.setStyleSheet("")
        for b in (self.btn_show, self.btn_add):
            b.setMinimumHeight(36)
            b.setMinimumWidth(140)
            b.setCursor(Qt.PointingHandCursor)

        header_layout.addWidget(self.btn_show)
        header_layout.addWidget(self.btn_add)
        layout.addWidget(self.header)

        self.btn_add.clicked.connect(self.open_add_window)

        # Table card
        table_card = QFrame()
        table_card.setProperty("class", "Card")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(16, 16, 16, 16)
        table_layout.setSpacing(12)

        table_title = QLabel("Users")
        table_title.setStyleSheet("font-size:18px; font-weight:700; color:#c7d2fe;")
        table_layout.addWidget(table_title)

        self.table = QTableWidget()
        self.table.setColumnCount(13)
        self.table.setRowCount(0)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("")  # uses global styles
        self.table.setHorizontalHeaderLabels([
            "Title", "Last Name", "First Name", "Birthday", "Phone N°",
            "Email", "Passport N°", "Date Mode",
            "First Date", "End Date", "Area", "isBooked", "BookedAt"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setDefaultSectionSize(140)
        self.table.verticalHeader().setDefaultSectionSize(38)
        table_layout.addWidget(self.table)

        layout.addWidget(table_card, 1)

        # Action panel
        self.Panel = QFrame()
        self.Panel.setLayout(QHBoxLayout())
        self.Panel.layout().setContentsMargins(0, 0, 0, 0)
        self.Panel.layout().setSpacing(10)

        self.Panel.setProperty("class", "Card")
        self.Panel.layout().addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.Editbutton = QPushButton("Edit")
        self.Editbutton.setProperty("class", "Success")
        self.Editbutton.setCursor(Qt.PointingHandCursor)
        self.Editbutton.clicked.connect(self.open_edit_window)
        self.Panel.layout().addWidget(self.Editbutton)

        self.Deletebutton = QPushButton("Delete")
        self.Deletebutton.setProperty("class", "Danger")
        self.Deletebutton.setCursor(Qt.PointingHandCursor)
        self.Deletebutton.clicked.connect(self.delete_selected)
        self.Panel.layout().addWidget(self.Deletebutton)

        layout.addWidget(self.Panel)

        # Ensure DB
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                title TEXT,
                last_name TEXT,
                first_name TEXT,
                birthday TEXT,
                phone TEXT,
                email TEXT,
                passport TEXT PRIMARY KEY ,
                date_mode TEXT,
                first_date TEXT,
                end_date TEXT,
                area TEXT,
                isbooked TEXT DEFAULT 'False',
                bookedAt TEXT
            )
        """)
        conn.commit()
        conn.close()

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT  title, last_name, first_name, birthday, phone, email, passport,
                 date_mode, first_date, end_date, area ,isbooked,bookedAt
            FROM users
        """)
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, item in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def open_add_window(self):
        self.main_window.add_window.show()
        self.hide()

    def delete_selected(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return  # nothing selected

        user_id = self.table.item(selected_row, 6).text()  # passport column

        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE passport = ?", (user_id,))
        conn.commit()
        conn.close()

        self.load_data()

    def open_edit_window(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return

        data = {}
        headers = ["title", "last_name", "first_name", "birthday", "phone", "email",
                   "passport", "date_mode", "first_date", "end_date", "area",
                   "isbooked", "bookedAt"]
        for i, header in enumerate(headers):
            self_item = self.table.item(selected_row, i)
            data[header] = self_item.text() if self_item else ""

        self.edit_window = EditWindow(self)
        self.edit_window.open_for_edit(data)


# ---------------------------------- Add Window ----------------------------------

class AddWindow(QMainWindow):
    def __init__(self, show_window, main_window):
        super().__init__()
        self.show_window = show_window
        self.main_window = main_window

        self.setWindowTitle("Form App")
        self.setWindowIcon(QIcon("icon.ico"))
        center_and_fix(self, 1200, 700)
        self.setStyleSheet(APP_STYLES)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.grid = QGridLayout()
        self.grid.setContentsMargins(18, 18, 18, 18)
        self.grid.setHorizontalSpacing(20)
        self.grid.setVerticalSpacing(10)
        central_widget.setLayout(self.grid)

        # Header
        self.header = QFrame()
        self.header.setObjectName("HeaderBar")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(16, 12, 16, 12)

        self.label1 = QLabel("Home")
        self.label1.setStyleSheet("font-size: 18px; font-weight: 700; color: #c7d2fe;")
        header_layout.addWidget(self.label1)
        header_layout.addStretch(1)

        self.btn_show = QPushButton("Show Content", self.header)
        self.btn_show.setProperty("class", "HeaderBtn")
        self.btn_show.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(self.btn_show)
        self.btn_show.clicked.connect(self.open_show_window)

        self.btn_add = QPushButton("Add New Content", self.header)
        self.btn_add.setProperty("class", "HeaderBtn")
        self.btn_add.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(self.btn_add)

        self.grid.addWidget(self.header, 0, 0, 1, 3)

        # Form (two-column layout on desktop scale)
        row = 1

        def add_labeled(widget_label, widget_field, col_left=True):
            nonlocal row
            self.grid.addWidget(widget_label, row, 0 if col_left else 1)
            self.grid.addWidget(widget_field, row + 1, 0 if col_left else 1)
            if not col_left:
                row += 2

        # Column containers (simulate two columns by spanning)
        left_col = 0
        right_col = 1

        # Title
        self.title = QLabel("Title:", self)
        self.title.setStyleSheet("color: #cbd5e1;")
        self.combo = QComboBox(self)
        self.combo.addItems(["Mr", "Ms"])
        self.combo.setMinimumHeight(40)
        self.grid.addWidget(self.title, row, left_col)
        self.grid.addWidget(self.combo, row + 1, left_col)

        # Last Name
        self.lname = QLabel("Last Name:", self)
        self.lname.setStyleSheet("color: #cbd5e1;")
        self.line = QLineEdit(self)
        self.line.setPlaceholderText("Last Name...")
        self.line.setMinimumHeight(40)
        self.grid.addWidget(self.lname, row, right_col)
        self.grid.addWidget(self.line, row + 1, right_col)
        row += 2

        # First Name
        self.fname = QLabel("First Name:", self)
        self.fname.setStyleSheet("color: #cbd5e1;")
        self.fline = QLineEdit(self)
        self.fline.setPlaceholderText("First Name...")
        self.fline.setMinimumHeight(40)
        self.grid.addWidget(self.fname, row, left_col)
        self.grid.addWidget(self.fline, row + 1, left_col)

        # Birthday
        self.Birthday = QLabel("Birthday (DD/MM/YYYY):", self)
        self.Birthday.setStyleSheet("color: #cbd5e1;")
        self.Birthdayline = QLineEdit(self)
        self.Birthdayline.setPlaceholderText("Birthday Date...")
        self.Birthdayline.setMinimumHeight(40)
        self.grid.addWidget(self.Birthday, row, right_col)
        self.grid.addWidget(self.Birthdayline, row + 1, right_col)
        row += 2

        # Phone
        self.phone = QLabel("Phone Number:", self)
        self.phone.setStyleSheet("color: #cbd5e1;")
        self.phoneline = QLineEdit(self)
        self.phoneline.setPlaceholderText("Phone Number...")
        self.phoneline.setMinimumHeight(40)
        self.grid.addWidget(self.phone, row, left_col)
        self.grid.addWidget(self.phoneline, row + 1, left_col)

        # Email
        self.email = QLabel("Email:", self)
        self.email.setStyleSheet("color: #cbd5e1;")
        self.emailline = QLineEdit(self)
        self.emailline.setPlaceholderText("Email...")
        self.emailline.setMinimumHeight(40)
        self.grid.addWidget(self.email, row, right_col)
        self.grid.addWidget(self.emailline, row + 1, right_col)
        row += 2

        # Passport
        self.passport = QLabel("Passport Number:", self)
        self.passport.setStyleSheet("color: #cbd5e1;")
        self.passline = QLineEdit(self)
        self.passline.setPlaceholderText("Passport Number...")
        self.passline.setMinimumHeight(40)
        self.grid.addWidget(self.passport, row, left_col)
        self.grid.addWidget(self.passline, row + 1, left_col)
        row += 2

        # Date section title
        self.Date = QLabel("📅 DATE SELECTION PREFERENCES", self)
        self.Date.setProperty("class", "SectionTitle")
        self.grid.addWidget(self.Date, row, 0, 1, 2)
        row += 1

        # Date mode
        self.date_label = QLabel("Selection Mode:", self)
        self.date_label.setStyleSheet("color:#cbd5e1;")
        self.datecombo = QComboBox(self)
        self.datecombo.addItems(["First Available Date", "Date Range"])
        self.datecombo.currentIndexChanged.connect(self.selection_changed)
        self.datecombo.setMinimumHeight(40)
        self.grid.addWidget(self.date_label, row, left_col)
        self.grid.addWidget(self.datecombo, row + 1, left_col)

        # First available date (or start date)
        self.fdate = QLabel("First Available Date:", self)
        self.fdate.setStyleSheet("color:#cbd5e1;")
        self.dateline = QLineEdit(self)
        self.dateline.setPlaceholderText("Date...")
        self.dateline.setMinimumHeight(40)
        self.grid.addWidget(self.fdate, row, right_col)
        self.grid.addWidget(self.dateline, row + 1, right_col)
        row += 2

        # Start/End for range
        self.start_label = QLabel("Start Date (DD/MM/YYYY):", self)
        self.start_label.setStyleSheet("color:#cbd5e1;")
        self.start_input = QLineEdit(self)
        self.start_input.setPlaceholderText("Start Date...")
        self.start_input.setMinimumHeight(40)

        self.end_label = QLabel("End Date (DD/MM/YYYY):", self)
        self.end_label.setStyleSheet("color:#cbd5e1;")
        self.end_input = QLineEdit(self)
        self.end_input.setPlaceholderText("End Date...")
        self.end_input.setMinimumHeight(40)

        self.grid.addWidget(self.start_label, row, left_col)
        self.grid.addWidget(self.start_input, row + 1, left_col)
        self.grid.addWidget(self.end_label, row, right_col)
        self.grid.addWidget(self.end_input, row + 1, right_col)
        row += 2

        self.start_label.hide()
        self.start_input.hide()
        self.end_label.hide()
        self.end_input.hide()

        # Area section
        self.Area = QLabel("🌍 AREA SELECTION", self)
        self.Area.setProperty("class", "SectionTitle")
        self.grid.addWidget(self.Area, row, 0, 1, 2)
        row += 1

        self.area = QLabel("Select Area:", self)
        self.area.setStyleSheet("color:#cbd5e1;")
        self.areacombo = QComboBox(self)
        self.areacombo.addItems(["Constantine", "Annaba"])
        self.areacombo.setMinimumHeight(40)
        self.grid.addWidget(self.area, row, left_col)
        self.grid.addWidget(self.areacombo, row + 1, left_col)
        row += 2

        # Save button (full width)
        self.savebutton = QPushButton("Save Information", self)
        self.savebutton.setProperty("class", "Primary")
        self.savebutton.setCursor(Qt.PointingHandCursor)
        self.savebutton.clicked.connect(self.AddForm)
        self.grid.addWidget(self.savebutton, row, 0, 1, 2, alignment=Qt.AlignCenter)

    def selection_changed(self):
        selected = self.datecombo.currentText()
        if selected == "First Available Date":
            self.fdate.show()
            self.dateline.show()
            self.start_label.hide()
            self.start_input.hide()
            self.end_label.hide()
            self.end_input.hide()
        else:
            self.fdate.hide()
            self.dateline.hide()
            self.start_label.show()
            self.start_input.show()
            self.end_label.show()
            self.end_input.show()

    def AddForm(self):
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        title = self.combo.currentText()
        last_name = self.line.text()
        first_name = self.fline.text()

        # ✅ Validate Birthday
        birthday = self.Birthdayline.text().strip()
        try:
            datetime.strptime(birthday, "%d/%m/%Y")
        except ValueError:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Invalid Date", "Please enter a valid Birthday in DD/MM/YYYY format.")
            conn.close()
            return

        phone = self.phoneline.text()
        email = self.emailline.text()
        passport = self.passline.text()

        # ✅ Handle First Date based on date_mode
        date_mode = self.datecombo.currentText()
        first_date = self.dateline.text().strip() if date_mode == "First Available Date" else self.start_input.text().strip()
        if first_date:
            try:
                datetime.strptime(first_date, "%d/%m/%Y")
            except ValueError:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Invalid Date", "Please enter a valid First Date in DD/MM/YYYY format.")
                conn.close()
                return

        # ✅ Handle End Date if provided
        end_date = self.end_input.text().strip() if date_mode != "First Available Date" else ""
        if end_date:
            try:
                datetime.strptime(end_date, "%d/%m/%Y")
                if first_date > end_date:
                    from PyQt5.QtWidgets import QMessageBox
                    QMessageBox.warning(self, "Invalid Dates", "Start Date cannot be after End Date.")
                    return
            except ValueError:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Invalid Date", "Please enter a valid End Date in DD/MM/YYYY format.")
                conn.close()
                return

        area = self.areacombo.currentText()
        isbooked = "False"
        bookedAt = None

        # ✅ Insert into database
        try:
            cursor.execute("""
                INSERT INTO users (
                    title, last_name, first_name, birthday, phone, email, passport,
                     date_mode, first_date, end_date, area, isbooked, bookedAt
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, last_name, first_name, birthday, phone, email, passport,
                  date_mode, first_date, end_date, area, isbooked, bookedAt))

            conn.commit()

            # ✅ Clear all input fields after saving
            self.line.clear()
            self.fline.clear()
            self.Birthdayline.clear()
            self.phoneline.clear()
            self.emailline.clear()
            self.passline.clear()
            self.dateline.clear()
            self.start_input.clear()
            self.end_input.clear()

            # ✅ Refresh data table
            self.show_window.load_data()

        except sqlite3.IntegrityError:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "This Passport Number Already Exists")
        finally:
            conn.close()

    def open_show_window(self):
        self.show_window.show()
        self.hide()




class EditWindow(QMainWindow):
    def __init__(self, show_window):
        super().__init__()
        self.show_window = show_window
        self.editing_passport = None

        self.setWindowTitle("Edit User")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setGeometry(100, 100, 500, 750)
        self.setStyleSheet("background-color: rgb(2,1,116); color: white;")

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Title Combo
        self.title_combo = QComboBox()
        self.title_combo.addItems(["Mr", "Ms"])

        # Text Fields
        self.lname_edit = QLineEdit()
        self.fname_edit = QLineEdit()
        self.birthday_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.pass_edit = QLineEdit()
        self.date_mode_combo = QComboBox()
        self.date_mode_combo.addItems(["First Available Date", "Date Range"])
        self.date_mode_combo.currentIndexChanged.connect(self.update_date_fields)
        self.first_date_edit = QLineEdit()
        self.end_date_edit = QLineEdit()
        self.area_combo = QComboBox()
        self.area_combo.addItems(["Constantine", "Annaba"])

        # ✅ New Fields
        self.is_booked_combo = QComboBox()
        self.is_booked_combo.addItems(["False", "True"])  # Default False

        self.booked_at_edit = QLineEdit()
        self.booked_at_edit.setPlaceholderText("Enter booked date or location...")

        # Add Widgets to Layout
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_combo)
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.lname_edit)
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.fname_edit)
        layout.addWidget(QLabel("Birthday (DD/MM/YYYY):"))
        layout.addWidget(self.birthday_edit)
        layout.addWidget(QLabel("Phone:"))
        layout.addWidget(self.phone_edit)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel("Passport Number:"))
        layout.addWidget(self.pass_edit)
        layout.addWidget(QLabel("Date Mode:"))
        layout.addWidget(self.date_mode_combo)
        layout.addWidget(QLabel("First Date:"))
        layout.addWidget(self.first_date_edit)
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(self.end_date_edit)
        layout.addWidget(QLabel("Area:"))
        layout.addWidget(self.area_combo)

        # ✅ Add New Fields to Layout
        layout.addWidget(QLabel("Is Booked:"))
        layout.addWidget(self.is_booked_combo)
        layout.addWidget(QLabel("Booked At:"))
        layout.addWidget(self.booked_at_edit)

        # Save Button
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setStyleSheet("background-color: green; color: white; padding: 8px; border-radius: 6px;")
        self.save_btn.clicked.connect(self.save_changes)
        layout.addWidget(self.save_btn)

        # Initialize date fields visibility
        self.update_date_fields()

    def open_for_edit(self, data):
        """Populate fields when opening edit window"""
        self.editing_passport = data['passport']

        self.title_combo.setCurrentText(data['title'])
        self.lname_edit.setText(data['last_name'])
        self.fname_edit.setText(data['first_name'])
        self.birthday_edit.setText(data['birthday'])
        self.phone_edit.setText(data['phone'])
        self.email_edit.setText(data['email'])
        self.pass_edit.setText(data['passport'])
        self.pass_edit.setDisabled(True)  # Cannot edit primary key
        self.date_mode_combo.setCurrentText(data['date_mode'])
        self.first_date_edit.setText(data['first_date'])
        self.end_date_edit.setText(data['end_date'])
        self.area_combo.setCurrentText(data['area'])

        # ✅ Load new fields
        self.is_booked_combo.setCurrentText(str(data['isbooked']))
        self.booked_at_edit.setText(str(data['bookedAt']))

        self.update_date_fields()
        self.show()

    def update_date_fields(self):
        """Show/Hide date inputs depending on selection"""
        mode = self.date_mode_combo.currentText()
        if mode == "First Available Date":
            self.first_date_edit.show()
            self.end_date_edit.hide()
        else:
            self.first_date_edit.show()
            self.end_date_edit.show()

    def save_changes(self):
        """Save edited user info to database"""
        title = self.title_combo.currentText()
        last_name = self.lname_edit.text().strip()
        first_name = self.fname_edit.text().strip()
        birthday = self.birthday_edit.text().strip()
        phone = self.phone_edit.text().strip()
        email = self.email_edit.text().strip()
        date_mode = self.date_mode_combo.currentText()
        first_date = self.first_date_edit.text().strip()
        end_date = self.end_date_edit.text().strip()
        area = self.area_combo.currentText()

        # ✅ Get new fields
        is_booked = self.is_booked_combo.currentText()
        booked_at = self.booked_at_edit.text().strip()

        # ✅ Validate birthday
        if birthday:
            try:
                bday_obj = datetime.strptime(birthday, "%d/%m/%Y")
                if bday_obj > datetime.today():
                    from PyQt5.QtWidgets import QMessageBox
                    QMessageBox.warning(self, "Invalid Date", "Birthday cannot be in the future!")
                    return
            except ValueError:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Invalid Date", "Please enter a valid Birthday in DD/MM/YYYY format.")
                return

        # ✅ Validate dates depending on date mode
        if date_mode == "First Available Date":
            if first_date:
                try:
                    datetime.strptime(first_date, "%d/%m/%Y")
                except ValueError:
                    from PyQt5.QtWidgets import QMessageBox
                    QMessageBox.warning(self, "Invalid Date", "Please enter a valid First Date in DD/MM/YYYY format.")
                    return
            end_date = ""  # Ignore end date in this mode
        else:
            try:
                start_obj = datetime.strptime(first_date, "%d/%m/%Y")
            except ValueError:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Invalid Date", "Please enter a valid Start Date in DD/MM/YYYY format.")
                return

            try:
                end_obj = datetime.strptime(end_date, "%d/%m/%Y")
            except ValueError:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Invalid Date", "Please enter a valid End Date in DD/MM/YYYY format.")
                return

            if start_obj > end_obj:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Invalid Dates", "Start Date cannot be after End Date.")
                return

        # ✅ Update database
        try:
            conn = sqlite3.connect("my_database.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET
                    title=?, last_name=?, first_name=?, birthday=?, phone=?, email=?,
                    date_mode=?, first_date=?, end_date=?, area=?, isbooked=?, bookedAt=?
                WHERE passport=?
            """, (
                title, last_name, first_name, birthday, phone, email,
                date_mode, first_date, end_date if date_mode == "Date Range" else "",
                area, is_booked, booked_at, self.editing_passport
            ))
            conn.commit()
            conn.close()

            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Success", "User information updated successfully!")
            self.show_window.load_data()
            self.close()

        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

