from PySide6.QtGui import QGuiApplication, QFont
from PySide6.QtCore import Qt

class ClipboardActions:
    def get_selected_indexes(self):
        """إرجاع قائمة المؤشرات المختارة في الجدول"""
        if hasattr(self, "table_view") and self.table_view:
            return self.table_view.selectionModel().selectedIndexes()
        return []

    def copy_selection(self):
        """نسخ البيانات المختارة مع التنسيقات إلى الحافظة"""
        idxs = sorted(self.get_selected_indexes(), key=lambda x: (x.row(), x.column()))
        if not idxs or not hasattr(self, "model") or not hasattr(self.model, "_df"):
            return

        rows = {}
        formats = {}
        for idx in idxs:
            r, c = idx.row(), idx.column()
            rows.setdefault(r, {})[c] = self.model._df.iat[r, c]
            formats[(r, c)] = self.model._formats.get((r, c), {})

        rmin, rmax = idxs[0].row(), idxs[-1].row()
        cmin, cmax = idxs[0].column(), idxs[-1].column()
        lines = []
        for r in range(rmin, rmax + 1):
            parts = [str(rows.get(r, {}).get(c, "")) for c in range(cmin, cmax + 1)]
            lines.append('\t'.join(parts))

        # حفظ البيانات في الحافظة
        QGuiApplication.clipboard().setText('\n'.join(lines))

        # حفظ التنسيقات مؤقتًا (يمكن استخدام dict خارجي إذا أردنا الاحتفاظ بها بعد اللصق)
        self._clipboard_formats = formats

    def paste_from_clipboard(self):
        """لصق البيانات مع التنسيقات من الحافظة"""
        if not hasattr(self, "model") or not hasattr(self.model, "_df"):
            return

        text = QGuiApplication.clipboard().text()
        if not text:
            return

        start_idx = getattr(self.table_view, "currentIndex", lambda: None)()
        if not start_idx or not start_idx.isValid():
            start_idx = self.model.index(0, 0)

        r0, c0 = start_idx.row(), start_idx.column()
        rows = text.split('\n')

        for i, line in enumerate(rows):
            cols = line.split('\t')
            for j, val in enumerate(cols):
                r, c = r0 + i, c0 + j

                # إضافة صفوف إذا لزم
                while r >= self.model.rowCount():
                    if hasattr(self, "add_row"):
                        self.add_row()
                    else:
                        import pandas as pd
                        new_row = pd.DataFrame([[""] * self.model.columnCount()], columns=self.model._df.columns)
                        self.model._df = pd.concat([self.model._df, new_row], ignore_index=True)

                # إضافة أعمدة إذا لزم
                while c >= self.model.columnCount():
                    new_col_name = f"Column {self.model.columnCount() + 1}"
                    self.model._df[new_col_name] = ""

                # لصق القيمة
                self.model._df.iat[r, c] = val

                # لصق التنسيقات إذا وجدت
                if hasattr(self, "_clipboard_formats"):
                    fmt = self._clipboard_formats.get((r - r0, c - c0), {})
                    if fmt:
                        self.model._formats[(r, c)] = fmt.copy()

        # إشعار الجدول بتغيير البيانات
        self.model.dataChanged.emit(
            self.model.index(0, 0),
            self.model.index(self.model.rowCount() - 1, max(0, self.model.columnCount() - 1))
        )

