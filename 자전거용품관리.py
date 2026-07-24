import sys
import sqlite3
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QGridLayout,
    QHeaderView,
)
from PyQt6.QtGui import QFont


DB_PATH = Path(__file__).with_name("bicycle_products.db")


class BicycleProductManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("자전거용품 관리 프로그램")
        self.resize(820, 580)
        self.setStyleSheet(
            """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #fff7e6, stop:1 #e4f1ff);
            }
            QWidget {
                color: #1f2937;
                font-family: 'Malgun Gothic';
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit {
                background: #ffffff;
                border: 2px solid #9ec5fe;
                border-radius: 10px;
                padding: 8px;
                min-height: 30px;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
                background: #f8fbff;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4f46e5, stop:1 #06b6d4);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4338ca, stop:1 #0891b2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3730a3, stop:1 #0e7490);
            }
            QTableWidget {
                background: #ffffff;
                border: 2px solid #93c5fd;
                border-radius: 12px;
                gridline-color: #dbeafe;
            }
            QHeaderView::section {
                background: #1d4ed8;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e5e7eb;
            }
            QTableWidget::item:selected {
                background: #bfdbfe;
                color: #111827;
            }
            """
        )

        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
        self.create_table()

        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.form_layout = QGridLayout()
        self.form_layout.setContentsMargins(10, 10, 10, 10)
        self.form_layout.setHorizontalSpacing(12)
        self.form_layout.setVerticalSpacing(12)
        self.main_layout.addLayout(self.form_layout)

        self.id_label = QLabel("ID")
        self.id_edit = QLineEdit()
        self.id_edit.setPlaceholderText("자동 생성")
        self.id_edit.setReadOnly(True)

        self.name_label = QLabel("제품명")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("예: 자전거 안장")

        self.price_label = QLabel("가격")
        self.price_edit = QLineEdit()
        self.price_edit.setPlaceholderText("예: 25000")

        self.form_layout.addWidget(self.id_label, 0, 0)
        self.form_layout.addWidget(self.id_edit, 0, 1)
        self.form_layout.addWidget(self.name_label, 1, 0)
        self.form_layout.addWidget(self.name_edit, 1, 1)
        self.form_layout.addWidget(self.price_label, 2, 0)
        self.form_layout.addWidget(self.price_edit, 2, 1)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        self.button_layout.setContentsMargins(0, 5, 0, 5)
        self.main_layout.addLayout(self.button_layout)

        self.insert_btn = QPushButton("입력")
        self.update_btn = QPushButton("수정")
        self.delete_btn = QPushButton("삭제")
        self.search_btn = QPushButton("검색")

        self.insert_btn.clicked.connect(self.insert_product)
        self.update_btn.clicked.connect(self.update_product)
        self.delete_btn.clicked.connect(self.delete_product)
        self.search_btn.clicked.connect(self.search_product)

        self.button_layout.addWidget(self.insert_btn)
        self.button_layout.addWidget(self.update_btn)
        self.button_layout.addWidget(self.delete_btn)
        self.button_layout.addWidget(self.search_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "제품명", "가격"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(
            """
            QTableWidget {
                background: #fdfefe;
            }
            """
        )
        self.table.cellClicked.connect(self.load_selected_row)
        self.main_layout.addWidget(self.table)

        self.load_products()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS MyProduct (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def insert_product(self):
        name = self.name_edit.text().strip()
        price_text = self.price_edit.text().strip()

        if not name or not price_text:
            QMessageBox.warning(self, "입력 오류", "제품명과 가격을 모두 입력해주세요.")
            return

        try:
            price = int(price_text)
        except ValueError:
            QMessageBox.warning(self, "입력 오류", "가격은 숫자로 입력해주세요.")
            return

        self.cur.execute(
            "INSERT INTO MyProduct(name, price) VALUES (?, ?)",
            (name, price),
        )
        self.conn.commit()
        self.clear_inputs()
        self.load_products()
        QMessageBox.information(self, "입력 완료", "제품이 등록되었습니다.")

    def update_product(self):
        product_id = self.id_edit.text().strip()
        name = self.name_edit.text().strip()
        price_text = self.price_edit.text().strip()

        if not product_id or not name or not price_text:
            QMessageBox.warning(self, "수정 오류", "수정할 ID, 제품명, 가격을 모두 입력해주세요.")
            return

        try:
            product_id = int(product_id)
            price = int(price_text)
        except ValueError:
            QMessageBox.warning(self, "수정 오류", "ID와 가격은 숫자로 입력해주세요.")
            return

        self.cur.execute(
            "UPDATE MyProduct SET name = ?, price = ? WHERE id = ?",
            (name, price, product_id),
        )
        self.conn.commit()
        self.clear_inputs()
        self.load_products()
        QMessageBox.information(self, "수정 완료", "제품 정보가 수정되었습니다.")

    def delete_product(self):
        product_id = self.id_edit.text().strip()
        if not product_id:
            QMessageBox.warning(self, "삭제 오류", "삭제할 ID를 선택해주세요.")
            return

        try:
            product_id = int(product_id)
        except ValueError:
            QMessageBox.warning(self, "삭제 오류", "ID는 숫자로 입력해주세요.")
            return

        self.cur.execute("DELETE FROM MyProduct WHERE id = ?", (product_id,))
        self.conn.commit()
        self.clear_inputs()
        self.load_products()
        QMessageBox.information(self, "삭제 완료", "제품이 삭제되었습니다.")

    def search_product(self):
        keyword = self.name_edit.text().strip()
        if not keyword:
            self.load_products()
            return

        self.cur.execute(
            "SELECT id, name, price FROM MyProduct WHERE name LIKE ? ORDER BY id",
            (f"%{keyword}%",),
        )
        rows = self.cur.fetchall()
        self.show_rows(rows)

    def load_products(self):
        self.cur.execute("SELECT id, name, price FROM MyProduct ORDER BY id")
        rows = self.cur.fetchall()
        self.show_rows(rows)

    def show_rows(self, rows):
        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_index, col_index, item)

    def load_selected_row(self, row, col):
        product_id = self.table.item(row, 0).text()
        product_name = self.table.item(row, 1).text()
        product_price = self.table.item(row, 2).text()

        self.id_edit.setText(product_id)
        self.name_edit.setText(product_name)
        self.price_edit.setText(product_price)

    def clear_inputs(self):
        self.id_edit.clear()
        self.name_edit.clear()
        self.price_edit.clear()

    def closeEvent(self, event):
        self.conn.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BicycleProductManager()
    window.show()
    sys.exit(app.exec())
