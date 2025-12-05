from PySide6.QtWidgets import QInputDialog, QMessageBox, QFileDialog
import pandas as pd
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget
import os
class SheetActions:
    # -------------------------- إضافة ورقة جديدة --------------------------
    def add_sheet(self):
        name, ok = QInputDialog.getText(self, "إضافة ورقة", "اسم الورقة:")
        if ok and name:
            self.db_manager.sheets[name] = pd.DataFrame()
            self.db_manager.current_sheet = name
            if hasattr(self, "sheet_selector") and self.sheet_selector:
                self.sheet_selector.addItem(name)
            self.load_sheet(name)

    # -------------------------- حذف ورقة --------------------------
    def delete_sheet(self):
        sheet = self.db_manager.current_sheet
        if not sheet:
            return
        reply = QMessageBox.question(
            self, "تأكيد الحذف", f"هل تريد حذف الورقة {sheet}؟",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            del self.db_manager.sheets[sheet]
            if hasattr(self, "sheet_selector") and self.sheet_selector:
                self.sheet_selector.removeItem(self.sheet_selector.currentIndex())
            if self.db_manager.sheets:
                self.db_manager.current_sheet = list(self.db_manager.sheets.keys())[0]
                self.load_sheet(self.db_manager.current_sheet)
            else:
                self.db_manager.current_sheet = None

    # -------------------------- إعادة تسمية ورقة --------------------------
    def rename_sheet(self):
        old_name = self.db_manager.current_sheet
        if not old_name:
            return
        new_name, ok = QInputDialog.getText(
            self, "إعادة تسمية الورقة",
            f"الاسم القديم: {old_name}\nالاسم الجديد:"
        )
        if ok and new_name:
            self.db_manager.sheets[new_name] = self.db_manager.sheets.pop(old_name)
            self.db_manager.current_sheet = new_name
            if hasattr(self, "sheet_selector") and self.sheet_selector:
                idx = self.sheet_selector.currentIndex()
                self.sheet_selector.setItemText(idx, new_name)

    # -------------------------- تحميل ورقة --------------------------
    def load_sheet(self, sheet_name):
        if sheet_name not in self.db_manager.sheets:
            return
        df = self.db_manager.sheets[sheet_name].copy()
        df.columns = [str(c) if c else f"Column {i+1}" for i, c in enumerate(df.columns)]
        if hasattr(self, "model"):
            self.model.update_dataframe(df)

    # -------------------------- مسح محتوى الورقة --------------------------
    def clear_sheet(self):
        sheet = self.db_manager.current_sheet
        if not sheet:
            return
        reply = QMessageBox.question(
            self, "تأكيد المسح",
            f"هل تريد مسح محتوى الورقة '{sheet}'؟",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db_manager.clear_sheet(sheet)
            self.load_sheet(sheet)

    # -------------------------- استيراد ورقة من ملف Excel --------------------------
    def import_sheet(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "استيراد ورقة", "", "Excel (*.xlsx *.xls *.xlsm)"
        )
        if not file_path:
            return
        df = pd.read_excel(file_path)
        sheet_name, ok = QInputDialog.getText(
            self, "اسم الورقة الجديدة", "اختر اسمًا للورقة:"
        )
        if not ok or not sheet_name:
            return
        self.db_manager.import_sheet(sheet_name, df)
        if hasattr(self, "sheet_selector") and self.sheet_selector:
            self.sheet_selector.addItem(sheet_name)
        self.load_sheet(sheet_name)

    # -------------------------- تغيير الورقة الحالية --------------------------
    def change_sheet(self, sheet_name):
        """تغيير الورقة المعروضة عند اختيار ورقة من ComboBox"""
        if sheet_name in self.db_manager.sheets:
            self.db_manager.current_sheet = sheet_name
            self.load_sheet(sheet_name)

    # -------------------------- حفظ الورقة الحالية --------------------------
    def save_sheet(self):
        sheet = self.db_manager.current_sheet
        if sheet:
            self.db_manager.save_sheet(sheet)
            QMessageBox.information(self, "تم", f"تم حفظ الورقة {sheet}")
            self.load_sheet(sheet)

    def change_table_direction(self, text):
            """
            تغيير اتجاه الجدول حسب النص المحدد في dirCombo
            """
            if text.lower() in ["يمين لليسار", "rtl", "right to left"]:
                self.table_view.setLayoutDirection(Qt.RightToLeft)
            else:  # افتراضي: يسار لليمين
                self.table_view.setLayoutDirection(Qt.LeftToRight)   


    def open_research_window(self):
        """
        فتح واجهة البحث research.ui
        """
        ui_path = r"C:\Users\nizar\Desktop\New folder\research.ui"
        if not os.path.exists(ui_path):
            from notifications import critical_open_error
            critical_open_error(self, f"ملف البحث غير موجود:\n{ui_path}")
            return

        loader = QUiLoader()
        self.research_window = loader.load(ui_path)
        if self.research_window is None:
            from notifications import critical_open_error
            critical_open_error(self, f"فشل تحميل واجهة البحث:\n{ui_path}")
            return

        self.research_window.show()

