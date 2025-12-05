from PySide6.QtWidgets import QInputDialog, QMessageBox
import pandas as pd
import datetime
from notifications import (
    warn_invalid_date, warn_invalid_number,
    warn_invalid_percentage, warn_invalid_text, warn_invalid_file
)

class RowColumnActions:

    # -------------------------- إضافة / حذف الصفوف --------------------------
    def add_row(self):
        sheet = self.db_manager.current_sheet
        if not sheet:
            return
        df = self.db_manager.sheets[sheet]
        new_row = pd.DataFrame([[""] * df.shape[1]], columns=df.columns)
        self.db_manager.sheets[sheet] = pd.concat([df, new_row], ignore_index=True)
        self.load_sheet(sheet)

    def delete_row(self):
        sheet = self.db_manager.current_sheet
        if not sheet:
            return
        idx = self.table_view.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(None, "خطأ", "الرجاء اختيار صف للحذف.")
            return
        df = self.db_manager.sheets[sheet]
        df = df.drop(idx.row()).reset_index(drop=True)
        self.db_manager.sheets[sheet] = df
        self.load_sheet(sheet)

    # -------------------------- إضافة / حذف الأعمدة --------------------------
    def add_column(self):
        sheet = self.db_manager.current_sheet
        if not sheet:
            return
        col_name, ok = QInputDialog.getText(None, "إضافة عمود", "اسم العمود:")
        if not ok or not col_name:
            return
        df = self.db_manager.sheets[sheet]
        df[col_name] = ""
        self.db_manager.sheets[sheet] = df
        self.load_sheet(sheet)

    def delete_column(self):
        sheet = self.db_manager.current_sheet
        if not sheet:
            return
        df = self.db_manager.sheets[sheet]
        if df.empty or df.shape[1] == 0:
            QMessageBox.warning(None, "خطأ", "لا توجد أعمدة للحذف.")
            return
        col_name, ok = QInputDialog.getItem(
            None, "حذف عمود", "اختر العمود المراد حذفه:", df.columns.tolist(), 0, False
        )
        if not ok or not col_name:
            return
        df = df.drop(columns=[col_name])
        self.db_manager.sheets[sheet] = df
        self.load_sheet(sheet)

    # -------------------------- تغيير أبعاد الصفوف / الأعمدة --------------------------
    def set_row_height(self):
        sheet = self.db_manager.current_sheet
        if not sheet:
            return
        idx = self.table_view.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(None, "خطأ", "الرجاء اختيار صف لتغيير ارتفاعه.")
            return
        height, ok = QInputDialog.getInt(None, "تغيير ارتفاع الصف", "أدخل ارتفاع الصف (px):", 25, 10, 1000)
        if ok:
            self.table_view.setRowHeight(idx.row(), height)

    def set_column_widths(self):
        sheet = self.db_manager.current_sheet
        if not sheet:
            return
        idx = self.table_view.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(None, "خطأ", "الرجاء اختيار عمود لتغيير عرضه.")
            return
        width, ok = QInputDialog.getInt(None, "تغيير عرض العمود", "أدخل عرض العمود (px):", 100, 10, 1000)
        if ok:
            self.table_view.setColumnWidth(idx.column(), width)

    # -------------------------- التحقق من صحة البيانات --------------------------
    def validate_cell_input(self, row, col, value, col_type):
        """
        التحقق من صحة البيانات حسب نوع العمود
        """
        col_type_lower = str(col_type).lower()
        if col_type_lower in ["number", "رقم"]:
            try:
                float(value)
                return True
            except ValueError:
                warn_invalid_number(None, col)
                return False
        elif col_type_lower in ["percentage", "نسبة مئوية"]:
            try:
                v = float(value)
                if 0 <= v <= 100:
                    return True
                else:
                    warn_invalid_percentage(None, col)
                    return False
            except ValueError:
                warn_invalid_percentage(None, col)
                return False
        elif col_type_lower in ["date", "تاريخ"]:
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d")
                return True
            except ValueError:
                warn_invalid_date(None, col)
                return False
        elif col_type_lower in ["text", "نص"]:
            if isinstance(value, str):
                return True
            else:
                warn_invalid_text(None, col)
                return False
        elif col_type_lower in ["image", "صورة", "pdf"]:
            # قبول أي مسار ملف كصورة أو PDF
            return True
        else:
            # نوع غير معروف، نعتبره إدخال غير صالح
            warn_invalid_file(None, col)
            return False
    def merge_cells(self):
            idxs = self.table_view.selectionModel().selectedIndexes()
            if not idxs:
                QMessageBox.warning(None, "خطأ", "اختر الخلايا لدمجها.")
                return
            # تبسيط: دمج المحتوى في الخلية الأولى
            first = idxs[0]
            merged_value = " ".join(str(self.model._df.iat[i.row(), i.column()]) for i in idxs)
            self.model._df.iat[first.row(), first.column()] = merged_value
            for idx in idxs[1:]:
                self.model._df.iat[idx.row(), idx.column()] = ""
            self.model.dataChanged.emit(first, idxs[-1], [Qt.DisplayRole])

    def apply_formula(self):
        idx = self.table_view.currentIndex()
        if not idx.isValid():
            return
        formula = self.formula_bar.text()
        # تبسيط: فقط ضع النص في الخلية
        self.model._df.iat[idx.row(), idx.column()] = formula
        self.model.dataChanged.emit(idx, idx, [Qt.DisplayRole, Qt.EditRole])
        # مسح شريط الصيغة بعد التطبيق (اختياري)
        self.formula_bar.clear()
