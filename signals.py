from PySide6.QtCore import Qt
from PySide6.QtWidgets import QInputDialog, QColorDialog, QMessageBox

def connect_signals(main_window):
    """
    ربط جميع الإشارات (Signals) للأزرار والـ ComboBoxes والشريط الصيغي (formula bar).
    """

    # -------------------------- Database Actions --------------------------
    main_window.btnCreateDatabase.clicked.connect(main_window.create_database)
    main_window.btnOpenDatabase.clicked.connect(main_window.open_database)
    main_window.btnCloseDatabase.clicked.connect(main_window.close_database)
    main_window.btnDeleteDatabase.clicked.connect(main_window.delete_database)
    main_window.btnRenameDatabase.clicked.connect(main_window.rename_database)

    # -------------------------- Sheet Selection --------------------------
    if main_window.sheet_selector:
        main_window.sheet_selector.currentTextChanged.connect(main_window.change_sheet)

    # -------------------------- Row / Column Operations --------------------------
    main_window.btnAddRow.clicked.connect(main_window.add_row)
    main_window.btnDeleteRow.clicked.connect(main_window.delete_row)
    main_window.btnAddColumn.clicked.connect(main_window.add_column)
    main_window.btnDeleteColumn.clicked.connect(main_window.delete_column)

    # -------------------------- Undo / Redo --------------------------
    main_window.btnUndo.clicked.connect(main_window.undo)
    main_window.btnRedo.clicked.connect(main_window.redo)

    # -------------------------- Saving & Export --------------------------
    main_window.btnSaveDatabase.clicked.connect(main_window.save_database)
    main_window.btnExportDatabase.clicked.connect(main_window.export_database)
    main_window.btnSaveSheet.clicked.connect(main_window.save_sheet)
    main_window.btnClearSheet.clicked.connect(main_window.clear_sheet)

    # -------------------------- Sheet Management --------------------------
    main_window.btnAddSheet.clicked.connect(main_window.add_sheet)
    main_window.btnDeleteSheet.clicked.connect(main_window.delete_sheet)
    main_window.btnRenameSheet.clicked.connect(main_window.rename_sheet)
    main_window.btnImportSheet.clicked.connect(main_window.import_sheet)

    # -------------------------- Clipboard & Formatting --------------------------
    main_window.btnCopy.clicked.connect(main_window.copy_selection)
    main_window.btnPaste.clicked.connect(main_window.paste_from_clipboard)
    main_window.btnMerge.clicked.connect(main_window.merge_cells)
    main_window.btnBold.clicked.connect(main_window.toggle_bold)
    main_window.btnBGColor.clicked.connect(main_window.set_bg_color)
    main_window.btnTextColor.clicked.connect(main_window.set_text_color)

    # -------------------------- Font & Alignment ComboBoxes --------------------------
    if main_window.fontCombo:
        main_window.fontCombo.currentTextChanged.connect(main_window.apply_font)
    if main_window.fontSizeCombo:
        main_window.fontSizeCombo.currentTextChanged.connect(main_window.apply_font)
    if main_window.alignCombo:
        main_window.alignCombo.currentTextChanged.connect(main_window.apply_alignment)

    # -------------------------- Formula Bar --------------------------
    if main_window.formula_bar:
        main_window.formula_bar.returnPressed.connect(main_window.apply_formula)

    # -------------------------- Insert Files --------------------------
    main_window.btnInsertImage.clicked.connect(main_window.insert_image)
    main_window.btnInsertPdf.clicked.connect(main_window.insert_pdf)

    # -------------------------- Table Dimensions --------------------------
    main_window.btnColumnWidth.clicked.connect(main_window.set_column_widths)
    main_window.btnRowHeight.clicked.connect(main_window.set_row_height)

    # -------------------------- Sheet Direction --------------------------
    if hasattr(main_window, "dirCombo") and main_window.dirCombo:
        main_window.dirCombo.addItems(["من الشمال الى اليمين", "من اليمين الى الشمال"])
        main_window.dirCombo.currentTextChanged.connect(main_window.change_table_direction)

    # -------------------------- Research / Additional Tools --------------------------
    if hasattr(main_window, "btnResarch") and main_window.btnResarch:
        main_window.btnResarch.clicked.connect(main_window.open_research_window)  # تأكد من وجود الدالة
