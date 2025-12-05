from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Qt
from notifications import warn_invalid_file  # التأكد من وجود دالة التحذير في notifications.py

class InsertFilesActions:
    """
    دوال لإدراج الملفات (صور وPDF) في الخلايا.
    تقوم بالتحقق من نوع الملف قبل الإدراج وتعرض تحذيرًا إذا كان غير صالح.
    """

    def insert_image(self):
        # اختيار ملف صورة
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "اختر صورة",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_path:
            return

        # التحقق من امتداد الملف
        if not file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            warn_invalid_file(None, "العمود", "Image")
            return

        # الحصول على الخلية الحالية
        idx = self.table_view.currentIndex()
        if not idx.isValid():
            return

        # إدراج مسار الصورة في DataFrame وتحديث الجدول
        self.model._df.iat[idx.row(), idx.column()] = file_path
        self.model.dataChanged.emit(idx, idx, [Qt.DisplayRole])

    def insert_pdf(self):
        # اختيار ملف PDF
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "اختر ملف PDF",
            "",
            "PDF (*.pdf)"
        )
        if not file_path:
            return

        # التحقق من امتداد الملف
        if not file_path.lower().endswith(".pdf"):
            warn_invalid_file(None, "العمود", "PDF")
            return

        # الحصول على الخلية الحالية
        idx = self.table_view.currentIndex()
        if not idx.isValid():
            return

        # إدراج مسار PDF في DataFrame وتحديث الجدول
        self.model._df.iat[idx.row(), idx.column()] = file_path
        self.model.dataChanged.emit(idx, idx, [Qt.DisplayRole])
