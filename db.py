import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox, QDialog, QScrollArea, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import mysql.connector

class TableWindow(QDialog):
    def __init__(self, table_name):
        super().__init__()
        self.setWindowTitle(f"Таблица {table_name}")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        table = self.create_table(table_name)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(table)

        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def create_table(self, table_name):
        conn = mysql.connector.connect(
                host="ВАШ_IP_АДРЕС",
                port="3306",
                database="ИМЯ_БАЗЫ_ДАННЫХ",
                user="ИМЯ_ПОЛЬЗОВАТЕЛЯ",
                password="ПАРОЛЬ"
        )
        cursor = conn.cursor()

        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            result = cursor.fetchall()

            table = QTableWidget()
            table.setColumnCount(len(result[0]))
            table.setRowCount(len(result))

            column_names = [str(header[0]) for header in cursor.description]
            column_types = [self.get_column_type(header[1]) for header in cursor.description]

            table.setHorizontalHeaderLabels(column_names)

            table.setStyleSheet("""
                QTableWidget {
                    border: 1px solid #d0d0d0;
                    background-color: #f0f0f0;
                    alternate-background-color: #e0e0e0;
                }
                QTableWidget::item {
                    padding: 5px;
                }
                QTableWidget::item:selected {
                    background-color: #3498db;
                    color: white;
                }
                QHeaderView::section {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                }
            """)

            for row in range(len(result)):
                for col in range(len(result[row])):
                    item = QTableWidgetItem(str(result[row][col]))
                    table.setItem(row, col, item)

            for col, column_type in enumerate(column_types):
                header_item = table.horizontalHeaderItem(col)
                header_text = header_item.text()
                header_item.setText(f"{header_text} ({column_type})")

            table.resizeColumnsToContents()
            table.resizeRowsToContents()

            return table

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть таблицу {table_name}:\n{str(e)}")
            self.reject()

        cursor.close()
        conn.close()

    def get_column_type(self, column_type_code):
        if column_type_code == mysql.connector.constants.FieldType.INT24:
            return "INT"
        elif column_type_code == mysql.connector.constants.FieldType.LONG:
            return "BIGINT"
        elif column_type_code == mysql.connector.constants.FieldType.FLOAT:
            return "FLOAT"
        elif column_type_code == mysql.connector.constants.FieldType.DOUBLE:
            return "DOUBLE"
        elif column_type_code == mysql.connector.constants.FieldType.DECIMAL:
            return "DECIMAL"
        elif column_type_code == mysql.connector.constants.FieldType.DATE:
            return "DATE"
        elif column_type_code == mysql.connector.constants.FieldType.DATETIME:
            return "DATETIME"
        elif column_type_code == mysql.connector.constants.FieldType.TIMESTAMP:
            return "TIMESTAMP"
        elif column_type_code == mysql.connector.constants.FieldType.TIME:
            return "TIME"
        elif column_type_code == mysql.connector.constants.FieldType.YEAR:
            return "YEAR"
        elif column_type_code == mysql.connector.constants.FieldType.TINY:
            return "TINYINT"
        elif column_type_code == mysql.connector.constants.FieldType.SHORT:
            return "SMALLINT"
        elif column_type_code == mysql.connector.constants.FieldType.STRING:
            return "VARCHAR"
        elif column_type_code == mysql.connector.constants.FieldType.BLOB:
            return "BLOB"
        elif column_type_code == mysql.connector.constants.FieldType.SET:
            return "SET"
        elif column_type_code == mysql.connector.constants.FieldType.LONGLONG:
            return "BIGINT"
        elif column_type_code == mysql.connector.constants.FieldType.VAR_STRING:
            return "VARCHAR"
        elif column_type_code == mysql.connector.constants.FieldType.TINY_BLOB:
            return "TINYBLOB"
        elif column_type_code == mysql.connector.constants.FieldType.MEDIUM_BLOB:
            return "MEDIUMBLOB"
        elif column_type_code == mysql.connector.constants.FieldType.LONG_BLOB:
            return "LONGBLOB"
        elif column_type_code == mysql.connector.constants.FieldType.VARCHAR:
            return "VARCHAR"
        elif column_type_code == mysql.connector.constants.FieldType.VAR_CHAR:
            return "VARCHAR"
        elif column_type_code == mysql.connector.constants.FieldType.ENUM:
            return "ENUM"
        elif column_type_code == mysql.connector.constants.FieldType.JSON:
            return "JSON"
        else:
            return "UNKNOWN"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список таблиц в базе данных")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        tables = self.get_tables_from_database()

        for table_name in tables:
            button = QPushButton(table_name)
            button.setObjectName("tableButton")
            button.clicked.connect(lambda checked, name=table_name: self.table_clicked(name))
            layout.addWidget(button)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)

        self.setCentralWidget(scroll_area)

        self.setStyleSheet("""
            #tableButton {
                border: none;
                padding: 10px;
                font-size: 16px;
                background-color: #3498db;
                color: white;
            }
            #tableButton:hover {
                background-color: #2980b9;
            }
        """)

    def get_tables_from_database(self):
        host = "ВАШ_IP_АДРЕС"
        port = "3306"
        database = "ИМЯ_БАЗЫ_ДАННЫХ"
        user = "ИМЯ_ПОЛЬЗОВАТЕЛЯ"
        password = "ПАРОЛЬ"

        conn = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]

        cursor.close()
        conn.close()

        return tables

    def table_clicked(self, table_name):
        table_window = TableWindow(table_name)
        table_window.exec_()

app = QApplication(sys.argv)

app.setStyleSheet("""
    QDialog {
        background-color: #f0f0f0;
    }
    QLabel {
        color: #555555;
        font-size: 16px;
    }
""")

app_icon = QIcon("icon.png")
app.setWindowIcon(app_icon)

window = MainWindow()
window.show()
sys.exit(app.exec_())
