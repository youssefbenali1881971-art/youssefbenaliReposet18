import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QMovie
from undo_redo import UndoRedoActions

# وحدات العمليات المقسمة
from db_actions import DatabaseActions
from sheet_actions import SheetActions
from row_col_actions import RowColumnActions
from formatting import FormattingActions
from clipboard import ClipboardActions
from insert_files import InsertFilesActions
from signals import connect_signals

# -------------------------- مسارات ثابتة --------------------------
UI_PATH = r"C:\Users\nizar\Desktop\New folder\tab.ui"
LOGO_PATH = r"C:\Users\nizar\Desktop\New folder\logo.gif"

def load_main_ui():
    loader = QUiLoader()
    ui = loader.load(UI_PATH)

    # إعداد الشعار
    logo_label = ui.findChild(QLabel, "logo")
    if logo_label:
        logo_label.setFixedSize(50, 50)
        movie = QMovie(LOGO_PATH)
        logo_label.setMovie(movie)
        movie.start()
    return ui

# -------------------------- MainWindow --------------------------
class MainWindow(
    QMainWindow,
    DatabaseActions,
    SheetActions,
    RowColumnActions,
    FormattingActions,
    ClipboardActions,
    InsertFilesActions,
    UndoRedoActions
):

    def __init__(self):
        super().__init__()

        # -------------------------- تحميل واجهة المستخدم --------------------------
        self.ui = load_main_ui()
        self.setCentralWidget(self.ui)

        # -------------------------- العناصر الرئيسية من الواجهة --------------------------
        self.table_view = self.ui.tableView
        self.formula_bar = self.ui.formulaBar
        self.sheet_selector = self.ui.sheetSelector
        self.dirCombo = self.ui.dirCombo   # مهم لاتجاه الورقة

        # -------------------------- أزرار Database Actions --------------------------
        self.btnCreateDatabase = self.ui.btnCreateDatabase
        self.btnOpenDatabase = self.ui.btnOpenDatabase
        self.btnCloseDatabase = self.ui.btnCloseDatabase
        self.btnDeleteDatabase = self.ui.btnDeleteDatabase
        self.btnRenameDatabase = self.ui.btnRenameDatabase

        # -------------------------- Row / Column Operations --------------------------
        self.btnAddRow = self.ui.btnAddRow
        self.btnDeleteRow = self.ui.btnDeleteRow
        self.btnAddColumn = self.ui.btnAddColumn
        self.btnDeleteColumn = self.ui.btnDeleteColumn

        # -------------------------- Undo / Redo --------------------------
        self.btnUndo = self.ui.btnUndo
        self.btnRedo = self.ui.btnRedo

        # -------------------------- Saving / Exporting --------------------------
        self.btnSaveDatabase = self.ui.btnSaveDatabase
        self.btnExportDatabase = self.ui.btnExportDatabase
        self.btnSaveSheet = self.ui.btnSaveSheet
        self.btnClearSheet = self.ui.btnClearSheet

        # -------------------------- Sheet Management --------------------------
        self.btnAddSheet = self.ui.btnAddSheet
        self.btnDeleteSheet = self.ui.btnDeleteSheet
        self.btnRenameSheet = self.ui.btnRenameSheet
        self.btnImportSheet = self.ui.btnImportSheet

        # -------------------------- Clipboard & Formatting --------------------------
        self.btnCopy = self.ui.btnCopy
        self.btnPaste = self.ui.btnPaste
        self.btnMerge = self.ui.btnMerge
        self.btnBold = self.ui.btnBold
        self.btnBGColor = self.ui.btnBGColor
        self.btnTextColor = self.ui.btnTextColor

        # -------------------------- Insert Files --------------------------
        self.btnInsertImage = self.ui.btnInsertImage
        self.btnInsertPdf = self.ui.btnInsertPdf

        # -------------------------- Adjust Table Size --------------------------
        self.btnColumnWidth = self.ui.btnColumnWidth
        self.btnRowHeight = self.ui.btnRowHeight

        # -------------------------- Research / Additional Tools --------------------------
        self.btnResarch = self.ui.btnResarch  # لفتح واجهة البحث (Research)

        self.btnUndo.clicked.connect(self.undo)
        self.btnRedo.clicked.connect(self.redo)
        # -------------------------- ComboBoxes إضافية --------------------------
        self.fontCombo = self.ui.fontCombo
        self.fontSizeCombo = self.ui.fontSizeCombo
        self.alignCombo = self.ui.alignCombo
        self.colTypeCombo = self.ui.colTypeCombo



        # -------------------------- ربط جميع الإشارات --------------------------
        connect_signals(self)

        # -------------------------- تحميل أول ورقة إذا موجودة --------------------------
        if hasattr(self, "db_manager") and self.db_manager.current_sheet:
            self.load_sheet(self.db_manager.current_sheet)


# -------------------------- تشغيل التطبيق --------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
