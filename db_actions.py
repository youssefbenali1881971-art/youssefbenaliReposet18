import os
import pandas as pd
from PySide6.QtWidgets import QMessageBox, QInputDialog, QFileDialog

class DatabaseManager:
    def __init__(self):
        self.sheets = {}
        self.current_sheet = None
        self.current_database_path = None

    def reset_database(self):
        """إعادة ضبط قاعدة البيانات"""
        self.sheets = {}
        self.current_sheet = None
        self.current_database_path = None

    def create_database(self, path):
        self.reset_database()
        self.current_database_path = path

    def open_database(self, path):
        self.reset_database()
        self.current_database_path = path
        if os.path.exists(path):
            xls = pd.ExcelFile(path)
            for sheet_name in xls.sheet_names:
                self.sheets[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
            if self.sheets:
                self.current_sheet = list(self.sheets.keys())[0]

    def save_database(self):
        if not self.current_database_path:
            return
        with pd.ExcelWriter(self.current_database_path) as writer:
            for sheet_name, df in self.sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def export_database(self, path):
        with pd.ExcelWriter(path) as writer:
            for sheet_name, df in self.sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def clear_sheet(self, sheet_name):
        if sheet_name in self.sheets:
            self.sheets[sheet_name] = pd.DataFrame()

    def import_sheet(self, sheet_name, df):
        self.sheets[sheet_name] = df.copy()
        self.current_sheet = sheet_name

    def rename_database_file(self, new_name):
        if self.current_database_path and os.path.exists(self.current_database_path):
            new_path = os.path.join(os.path.dirname(self.current_database_path), new_name)
            os.rename(self.current_database_path, new_path)
            self.current_database_path = new_path


class DatabaseActions:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def create_database(self):
        path, _ = QFileDialog.getSaveFileName(None, "Create Database", "", "Excel (*.xlsx)")
        if path:
            self.db_manager.create_database(path)
            if self.db_manager.current_sheet and hasattr(self, "load_sheet"):
                self.load_sheet(self.db_manager.current_sheet)
            QMessageBox.information(None, "تم", "تم إنشاء قاعدة البيانات")

    def open_database(self):
        path, _ = QFileDialog.getOpenFileName(None, "Open Database", "", "Excel (*.xlsx)")
        if path:
            self.db_manager.open_database(path)
            if self.db_manager.current_sheet and hasattr(self, "load_sheet"):
                self.load_sheet(self.db_manager.current_sheet)
            QMessageBox.information(None, "تم", "تم فتح قاعدة البيانات")

    def save_database(self):
        self.db_manager.save_database()
        QMessageBox.information(None, "تم", "تم حفظ قاعدة البيانات")

    def export_database(self):
        path, _ = QFileDialog.getSaveFileName(None, "Export Database", "", "Excel (*.xlsx)")
        if path:
            self.db_manager.export_database(path)
            QMessageBox.information(None, "تم", f"تم تصدير قاعدة البيانات إلى {path}")

    def close_database(self):
        self.db_manager.reset_database()
        QMessageBox.information(None, "تم", "تم إغلاق قاعدة البيانات")

    def delete_database(self):
        self.db_manager.reset_database()
        QMessageBox.information(None, "تم", "تم حذف قاعدة البيانات")

    def rename_database(self):
        new_name, ok = QInputDialog.getText(None, "إعادة تسمية قاعدة البيانات", "الاسم الجديد:")
        if ok and new_name:
            self.db_manager.rename_database_file(new_name)
            QMessageBox.information(None, "تم", f"تم إعادة تسمية قاعدة البيانات إلى {new_name}")
