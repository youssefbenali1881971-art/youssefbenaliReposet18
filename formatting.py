from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QColorDialog

class FormattingActions:
    def get_selected_indexes(self):
        """إرجاع جميع الخلايا المحددة في الجدول"""
        return self.table_view.selectionModel().selectedIndexes()

    def apply_font(self):
        idxs = self.get_selected_indexes()
        if not idxs: 
            return
        font_family = self.fontCombo.currentText()
        font_size = int(self.fontSizeCombo.currentText())
        for idx in idxs:
            fmt = self.model._formats.get((idx.row(), idx.column()), {})
            font = fmt.get("font", QFont())
            font.setFamily(font_family)
            font.setPointSize(font_size)
            fmt["font"] = font
            self.model._formats[(idx.row(), idx.column())] = fmt
        self.model.dataChanged.emit(idxs[0], idxs[-1], [Qt.FontRole])

    def apply_alignment(self):
        idxs = self.get_selected_indexes()
        if not idxs:
            return
        alignment_map = {
            "Left": Qt.AlignLeft,
            "Center": Qt.AlignCenter,
            "Right": Qt.AlignRight
        }
        align = alignment_map.get(self.alignCombo.currentText(), Qt.AlignLeft)
        for idx in idxs:
            fmt = self.model._formats.get((idx.row(), idx.column()), {})
            fmt["align"] = align
            self.model._formats[(idx.row(), idx.column())] = fmt
        self.model.dataChanged.emit(idxs[0], idxs[-1], [Qt.TextAlignmentRole])

    def toggle_bold(self):
        idxs = self.get_selected_indexes()
        if not idxs:
            return
        current_bold = any(
            self.model._formats.get((idx.row(), idx.column()), {}).get("font", QFont()).bold() 
            for idx in idxs
        )
        for idx in idxs:
            fmt = self.model._formats.get((idx.row(), idx.column()), {})
            font = fmt.get("font", QFont())
            font.setBold(not current_bold)
            fmt["font"] = font
            self.model._formats[(idx.row(), idx.column())] = fmt
        self.model.dataChanged.emit(idxs[0], idxs[-1], [Qt.FontRole])

    def set_bg_color(self):
        idxs = self.get_selected_indexes()
        if not idxs:
            return
        color = QColorDialog.getColor()
        if color.isValid():
            for idx in idxs:
                fmt = self.model._formats.get((idx.row(), idx.column()), {})
                fmt["bg"] = color
                self.model._formats[(idx.row(), idx.column())] = fmt
            self.model.dataChanged.emit(idxs[0], idxs[-1], [Qt.BackgroundRole])

    def set_text_color(self):
        idxs = self.get_selected_indexes()
        if not idxs:
            return
        color = QColorDialog.getColor()
        if color.isValid():
            for idx in idxs:
                fmt = self.model._formats.get((idx.row(), idx.column()), {})
                fmt["fg"] = color
                self.model._formats[(idx.row(), idx.column())] = fmt
            self.model.dataChanged.emit(idxs[0], idxs[-1], [Qt.ForegroundRole])
