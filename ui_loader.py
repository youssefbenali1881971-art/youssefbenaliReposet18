from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

def load_main_ui():
    """
    يقوم بتحميل ملف tab.ui وإرجاع الواجهة الجاهزة للاستخدام.
    """
    loader = QUiLoader()
    ui_file = QFile("tab.ui")
    ui_file.open(QFile.ReadOnly)
    ui = loader.load(ui_file)
    ui_file.close()
    return ui
