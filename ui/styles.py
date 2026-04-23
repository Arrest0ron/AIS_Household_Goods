PURPLE_STYLESHEET = """
/* === Global === */
QMainWindow, QDialog {
    background-color: #F8F4FF;
    color: #2D1B69;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 10pt;
}

/* === QTabWidget === */
QTabWidget::pane {
    border: 1px solid #D8CCF0;
    border-top: none;
    background: #FFFFFF;
    border-radius: 0 0 8px 8px;
}
QTabBar::tab {
    background: #EDE4FF;
    color: #4A2D8A;
    padding: 10px 20px;
    margin-right: 2px;
    border: 1px solid #D8CCF0;
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    font-weight: 600;
    min-width: 100px;
}
QTabBar::tab:selected {
    background: #FFFFFF;
    color: #6D28D9;
    border-bottom: 2px solid #7C3AED;
}
QTabBar::tab:hover:!selected {
    background: #E0D4F7;
}

/* === QPushButton === */
QPushButton {
    background-color: #7C3AED;
    color: #FFFFFF;
    border: none;
    padding: 8px 18px;
    border-radius: 6px;
    font-weight: 600;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #6D28D9;
}
QPushButton:pressed {
    background-color: #5B21B6;
}
QPushButton:disabled {
    background-color: #D8CCF0;
    color: #9A84C7;
}

/* Danger buttons (delete) */
QPushButton[danger="true"] {
    background-color: #F43F5E;
}
QPushButton[danger="true"]:hover {
    background-color: #E11D48;
}

/* Success buttons (add) */
QPushButton[success="true"] {
    background-color: #10B981;
}
QPushButton[success="true"]:hover {
    background-color: #059669;
}

/* === QLineEdit === */
QLineEdit {
    border: 2px solid #D8CCF0;
    border-radius: 6px;
    padding: 8px 12px;
    background: #FFFFFF;
    color: #2D1B69;
    selection-background-color: #C4B5FD;
}
QLineEdit:focus {
    border-color: #7C3AED;
}

/* === QTableWidget === */
QTableWidget {
    background: #FFFFFF;
    border: 1px solid #D8CCF0;
    border-radius: 8px;
    gridline-color: #EDE4FF;
    selection-background-color: #C4B5FD;
    selection-color: #2D1B69;
    outline: none;
}
QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #F3EEFF;
}
QTableWidget::item:selected {
    background: #C4B5FD;
    color: #2D1B69;
}
QHeaderView::section {
    background: #EDE4FF;
    color: #4A2D8A;
    padding: 8px 10px;
    border: none;
    border-bottom: 2px solid #D8CCF0;
    font-weight: 700;
}

/* === QComboBox === */
QComboBox {
    border: 2px solid #D8CCF0;
    border-radius: 6px;
    padding: 8px 12px;
    background: #FFFFFF;
    color: #2D1B69;
    min-height: 16px;
}
QComboBox:focus {
    border-color: #7C3AED;
}
QComboBox::drop-down {
    border: none;
    width: 30px;
}
QComboBox QAbstractItemView {
    background: #FFFFFF;
    border: 1px solid #D8CCF0;
    selection-background-color: #C4B5FD;
    selection-color: #2D1B69;
}

/* === QSpinBox === */
QSpinBox {
    border: 2px solid #D8CCF0;
    border-radius: 6px;
    padding: 8px 12px;
    background: #FFFFFF;
    color: #2D1B69;
    min-height: 16px;
}
QSpinBox:focus {
    border-color: #7C3AED;
}

/* === QGroupBox === */
QGroupBox {
    background: #F3EEFF;
    border: 1px solid #D8CCF0;
    border-radius: 10px;
    margin-top: 14px;
    padding: 16px 12px 12px 12px;
    font-weight: 700;
    color: #4A2D8A;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 12px;
    color: #6D28D9;
}

/* === QTextEdit === */
QTextEdit {
    border: 1px solid #D8CCF0;
    border-radius: 8px;
    background: #FFFFFF;
    color: #2D1B69;
    padding: 8px;
}

/* === QLabel === */
QLabel {
    color: #2D1B69;
}

/* === QSplitter === */
QSplitter::handle {
    background: #D8CCF0;
    height: 3px;
}

/* === Dialog === */
QDialog {
    background: #F8F4FF;
}
"""

BUTTON_STYLES = {
    "add": 'QPushButton { background-color: #10B981; color: #fff; border: none; padding: 8px 18px; border-radius: 6px; font-weight: 600; } QPushButton:hover { background-color: #059669; }',
    "edit": 'QPushButton { background-color: #7C3AED; color: #fff; border: none; padding: 8px 18px; border-radius: 6px; font-weight: 600; } QPushButton:hover { background-color: #6D28D9; }',
    "delete": 'QPushButton { background-color: #F43F5E; color: #fff; border: none; padding: 8px 18px; border-radius: 6px; font-weight: 600; } QPushButton:hover { background-color: #E11D48; }',
    "search": 'QPushButton { background-color: #6D28D9; color: #fff; border: none; padding: 8px 18px; border-radius: 6px; font-weight: 600; } QPushButton:hover { background-color: #5B21B6; }',
    "pdf": 'QPushButton { background-color: #D946EF; color: #fff; border: none; padding: 8px 18px; border-radius: 6px; font-weight: 600; } QPushButton:hover { background-color: #C026D3; }',
}
