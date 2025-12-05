from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QMessageBox
import pandas as pd
import datetime
from notifications import warn_invalid_input

class DataFrameModel(QAbstractTableModel):
    """
    نموذج بيانات لدعم QTableView مع:
    - DataFrame من pandas
    - تنسيقات لكل خلية
    - التحقق من نوع البيانات لكل عمود
    """

    def __init__(self, df=pd.DataFrame(), column_types=None):
        """
        column_types: dict { "ColumnName": "type" }
        type يمكن أن يكون: "str", "int", "float", "percent", "date", "image", "pdf"
        """
        super().__init__()
        self._df = df.copy()
        self._formats = {}
        self.column_types = column_types or {col: "str" for col in df.columns}

    # -------------------------- أساسيات النموذج --------------------------
    def rowCount(self, parent=None):
        return len(self._df.index)

    def columnCount(self, parent=None):
        return len(self._df.columns)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return str(self._df.columns[section]) if section < len(self._df.columns) else ""
        else:
            return str(section + 1)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    # -------------------------- عرض البيانات --------------------------
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        r, c = index.row(), index.column()
        col_name = self._df.columns[c]
        val = self._df.iat[r, c]

        if role in (Qt.DisplayRole, Qt.EditRole):
            if pd.isna(val) or val is None:
                return ""
            return str(val)

        fmt = self._formats.get((r, c), {})
        if role == Qt.FontRole:
            return fmt.get("font", None)
        if role == Qt.BackgroundRole:
            return fmt.get("bg", None)
        if role == Qt.ForegroundRole:
            return fmt.get("fg", None)
        if role == Qt.TextAlignmentRole:
            return fmt.get("align", None)
        return None

    # -------------------------- تعيين البيانات مع التحقق --------------------------
    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False

        row, col = index.row(), index.column()
        col_name = self._df.columns[col]
        col_type = self.column_types.get(col_name, "str")

        # التحقق من نوع البيانات
        if not self._validate_value(value, col_type):
            warn_invalid_input(None, col_name, col_type)
            return False

        # تحويل للقيم الصحيحة إذا لزم الأمر
        value = self._convert_value(value, col_type)

        self._df.iat[row, col] = value
        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        return True

    # -------------------------- تحديث كامل DataFrame --------------------------
    def update_dataframe(self, df, column_types=None):
        self.beginResetModel()
        df.columns = [str(c) if c else f"Column {i+1}" for i, c in enumerate(df.columns)]
        self._df = df.copy()
        self._formats.clear()
        if column_types:
            self.column_types = column_types
        else:
            for col in df.columns:
                if col not in self.column_types:
                    self.column_types[col] = "str"
        self.endResetModel()

    # -------------------------- تنسيقات الخلايا --------------------------
    def set_format_for_indexes(self, indexes, font=None, bg=None, fg=None, align=None):
        changed = []
        for idx in indexes:
            if not idx.isValid():
                continue
            key = (idx.row(), idx.column())
            fmt = self._formats.get(key, {})
            if font is not None: fmt["font"] = font
            if bg is not None: fmt["bg"] = bg
            if fg is not None: fmt["fg"] = fg
            if align is not None: fmt["align"] = align
            self._formats[key] = fmt
            changed.append(idx)
        if changed:
            self.dataChanged.emit(
                changed[0], changed[-1],
                [Qt.FontRole, Qt.BackgroundRole, Qt.ForegroundRole, Qt.TextAlignmentRole]
            )

    # -------------------------- وظائف مساعدة للتحقق --------------------------
    def _validate_value(self, value, col_type):
        """التحقق من صحة البيانات حسب نوع العمود."""
        if col_type in ("str",):
            return True
        elif col_type in ("int", "float"):
            try:
                float(value)
                return True
            except:
                return False
        elif col_type == "percent":
            try:
                val = float(value)
                return 0 <= val <= 100
            except:
                return False
        elif col_type == "date":
            try:
                if isinstance(value, datetime.date):
                    return True
                pd.to_datetime(value)
                return True
            except:
                return False
        elif col_type in ("image", "pdf"):
            import os
            if not isinstance(value, str):
                return False
            if col_type == "image":
                return os.path.splitext(value)[1].lower() in (".png", ".jpg", ".jpeg", ".bmp")
            elif col_type == "pdf":
                return os.path.splitext(value)[1].lower() == ".pdf"
        return False

    def _convert_value(self, value, col_type):
        """تحويل القيمة إلى النوع الصحيح عند الحاجة."""
        if col_type == "int":
            return int(float(value))
        if col_type in ("float", "percent"):
            return float(value)
        if col_type == "date":
            if isinstance(value, datetime.date):
                return value
            return pd.to_datetime(value).date()
        return value
