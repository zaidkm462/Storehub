mode = 1

theme1 = ["#333333", "#a17da4", "#f0f0f0", "#e0dede"]
theme2 = []
colors = theme1

lstStyle = """
QListWidget {
    background-color: #f0f0f0; 
    border: 6px solid #a17da4;
    /*border-top: none;*/
}
QListWidget::item {   
    font-family: Noto Sans Arabic;
    padding: 10px;
    color: black;
    border-bottom: 5px solid #a17da4;
}
QListWidget::item:hover {
    background-color: #e0dede;
}
QListWidget::item:selected {
    color: #a17da4;
    font size: 25px;
    font-weight: bold;
    /*background-color: #a17da4;*/
}"""
tableStyle = """
QTableView {
    background-color: #f0f0f0;
    font-family: Noto Sans Arabic;
    font-size: 14px;
    color: #333333;
    border: 6px solid #a17da4;   
    border-bottom: none;
    gridline-color: #a17da4;
}

QHeaderView::section {
    font-family: Noto Sans Arabic;
    font-size: 16px;
    color: black; 
    border-right: 1px solid #a17da4;
    border-left: 4px solid #a17da4;
    border-top: none;    
    border-bottom: 4px solid #a17da4;
}
QTableView::item:alternate {
    background-color: #e0dede;
}
QTableView::item {
    font-family: Noto Sans Arabic;
    background-color: #f0f0f0;
    border-left: 4px solid #a17da4;
    border-bottom: 4px solid #a17da4;
}
QTableView::item:selected {    
    background-color: #696969;
    color: white;
}

QScrollBar:horizontal {
    background: transparent;
    height: 15px;    
    padding: 3px;
}


QScrollBar::handle:horizontal {
    background: #333;
    min-width: 10px;
    width: 10px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background: #555;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
    background: none;
    border: none;

}

/*
QScrollBar:vertical {
    background: transparent;
    width: 15px;
    padding: 3px;
}

QScrollBar::handle:vertical {
    background: #333;
    min-width: 10px;
    width: 10px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #555;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    width: 0px;
    height: 0px;
    background: none;
    border: none;

}
*/

"""
add_btn_Style = """
QPushButton{
    background: #a17da4;
    color: #f0f0f0;
    border: none;
}
QPushButton:pressed{
    border: 1px solid #e0dede;
}"""
export_btn_style = """
QPushButton{
    background: #a17da4;
    color: white;
    border: none;
}
QPushButton:pressed{
    border: 1px solid #e0dede;
}
"""
editor_style = "QLineEdit {color: black; font-family: Noto Sans Arabic; font-size: 13px;  background: transparent; border: none;}"
date_editor_style = "QLineEdit {color: gray; font-size: 14px; background: transparent; border: none;}"
date_editor2_style = """
QLineEdit {
    color: #333333;
    padding-left: 100px;
}
}"""


cmpltr_style = """
QListView {
    wrap: true;  /* Enable text wrapping */
    word-wrap: break-word;  /* Enable word wrapping */
    text-align: center;  /* Center-align text */
    border: 2px solid #a17da4;  /* Border color and thickness */
    background-color: #a17da4;  /* Background color */
    padding: 2px;  /* Internal padding */
    outline: none;  /* Remove outline */
}

QListView::item {
    font-family: Nont Sans Arabic;
    text-align: center;  /* Center-align text in items */
    padding: 8px 16px;  /* Padding inside items */
    background-color: #ffffff;  /* Background color of items */
    border-bottom: 1px solid #9ca5ab;  /* Line between items */
    white-space: normal;  /* Allow text wrapping */
    text-overflow: unset;  /* Disable ellipsis */
    overflow: visible;  /* Ensure text is not clipped */
}

QListView::item:hover {
    background-color: #a17da4;  /* Background color on hover */
    color: white;  /* Text color on hover */
}

QListView::item:selected {
    background-color: #a17da4;  /* Background color of selected item */
    color: white;  /* Text color of selected item */
}
"""

calender_style = """
QCalendarWidget QAbstractItemView {
    gridline-color: transparent;
    background-color: #f0f0f0;
    selection-background-color: lightgray;
    font-size: 13px;
}

QCalendarWidget QAbstractItemView::item:hover {
    gridline-color: transparent;
    background-color: #f0f0f0;
    background-color: lightgray;
    font-size: 13px;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    height: 50px;
    background-color: #a17da4;
    color: white;
    font-size: 13px;
}

QCalendarWidget QToolButton {
    height: 30px;
    padding-right: 5px;
    font-weight: normal;
}

QCalendarWidget QToolButton::menu-indicator {
    image: none;
    width: 0px;
    height: 0px;
    margin: 0px;
}

QSpinBox {
    background-color: #a17da4;
    padding: 5px;
    font-size: 14px;
    color: darkred;
}

QSpinBox::up-button, QSpinBox::down-button {
    width: 0px;
    height: 0px;
    border: none;
    background: transparent;
    margin: 0;
}

QCalendarWidget QMenu {
    background-color: #f0f0f0;
    border: 3px solid #a17da4;
}

QCalendarWidget QMenu::item:selected {
    background-color: #a17da4;
    color: white;
}
"""

ok_btn_style = """
QPushButton {
    background-color: #a17da4;
    font-weight: bold;
    color: white;
    font-size: 20px;
    border: none;
}
/*QPushButton:hover {
    background-color: #9ca5ab;
}
QPushButton:pressed {
    background-color: #9ca5ab;
}*/

"""

no_result = "QLabel {color: #9ca5ab; font-family: Noto Sans Arabic; font-size: 22px;}"


dlg_Style = """
QDialog {
    border: 6px solid #a17da4; 
    background-color: #f0f0f0; 
}
"""

menue = """
QFrame{
background-color: #f0f0f0;
border: 6px solid #a17da4;
border-left: none;
}

"""

radio = """
QFrame{
border: none;
margin-top: 30px;
}
QRadioButton{
font-size: 22px;
margin-left: 20px;
font-family: Noto Sans Arabic;
}
QPushButton{
background-color: #a17daf;
border: none; 
color: #f0f0f0;
font-size: 22px;
font-family: Noto Sans Arabic;
}
QRadioButton::indicator {
width: 23px;
height: 23px;
border: 4px solid #a17da4; 
border-radius: 17px;		
padding-top: 4px;		
padding-right: 4px;
}
QRadioButton::indicator:checked {
background-image: url(':/img/radio.png');
background-position: center; 
background-repeat: no-repeat;
}
"""

wait_label = "QLabel {color: #333; font-family: Noto Sans Arabic; font-size: 22px; border: 4px solid #a17da4; background-color: #f0f0f0; padding: 20; padding-top: 10; padding-bottom: 10;}"




contact = """
QFrame QFrame{
border: none;
}
QFrame :hover{
}

QToolButton{
background-color: transparent;
border: none;
}
QLabel{
    background-color: transparent;
    padding-right: 10px;

    font-family: Noto Sans Arabic;
    font-size: 15px;
    border: 1px solid black;
}

"""

menue_item = """


QFrame QFrame{
border: none;
}

QFrame :hover{
background-color: #E0DEDE;
}

QToolButton{
background-color: transparent;
border: none;
}
QLabel{
    background-color: transparent;
    padding-right: 10px;
    font-family: Noto Sans Arabic;
    font-size: 22px;
    border: 1px solid black;}

"""

menue_item_slctd= """


QFrame QFrame{
border: none;
}

QFrame :hover{
background-color: #E0DEDE;
}

QToolButton{
background-color: transparent;
border: none;
}
QLabel{
	color: #a17da4; 
    background-color: transparent;
    padding-right: 10px;
    font-family: Noto Sans Arabic;
    font-size: 22px;
    border: 1px solid black;}

"""

    
combo = """
QComboBox QAbstractItemView::item:hover {
    background-color:  #a17da4;
    border: transparent;
}
QComboBox QAbstractItemView::item:selected {
    background-color:  #a17da4;
    border: none;
}
QComboBox QAbstractItemView {
    background-color: #f0f0f0;
    border: 3px solid #a17da4;
}
QComboBox {
	font-family: Noto Sans Arabic;
	padding: -3px 0px -3px 5px;
	font-size: 18px;
	color: #333333;
    border: 3px solid darkgrey;
    background-color: #f0f0f0;
    text-align: center;
}
QComboBox::drop-down:button{
image: url(:/img/dd2.png);
padding-top: 10px;
padding-left: 5px;
padding-right: 5px;
width: 13px;
height: 13px

}
"""


balance_combo = """
QComboBox QAbstractItemView::item:hover {
    background-color:  #a17da4;
    border: transparent;
}
QComboBox QAbstractItemView::item:selected {
    background-color:  #a17da4;
    border: none;

}
QComboBox QAbstractItemView {
    background-color: #f0f0f0;
    border: 3px solid #a17da4;

}
QComboBox {
	font-family: Noto Sans Arabic;
	padding: -2px 0px -2px 0px;
	font-size: 18px;
	color: #333333;
    border: 5px solid #a17da4;
    background-color: #f0f0f0;

    text-align: center;
}
QComboBox::drop-down:button{
image: url(:/img/dd2.png);
padding-top: 12px;
padding-left: 10px;
width: 13px;

height: 13px

}
"""

radio2 = """
QLabel{
        font-family: Noto Sans Arabic;
        font-size: 22px;
        margin-top: 5px;
    }
QFrame{
border: 0px solid black;  
}
QRadioButton{
font-size: 22px;
font-family: Noto Sans Arabic;
}
QPushButton{
background-color: #a17daf;
border: none; 
color: #f0f0f0;
font-size: 22px;
font-family: Noto Sans Arabic;
}
QRadioButton::indicator {
width: 22px;
height: 22px;
border: 4px solid #a17da4; 
border-radius: 16px;		
padding-top: 3px;		
padding-right: 3px;
}
QRadioButton::indicator:checked {
background-image: url(':/img/radio.png');
background-position: center; 
background-repeat: no-repeat;
}
"""

right_click = """
QMenu {
    border: 2px solid #a17da4;  /* Border color and thickness */
    background-color: #a17da4;  /* Background color */
    padding: 2px;  /* Internal padding */
    outline: none;  /* Remove outline */
    font-family: Noto Sans Arabic;
}

QMenu::item {
    padding: 8px 10px 8px 40px;  /* Padding inside items */
    background-color: #ffffff;  /* Background color of items */
    border-bottom: 1px solid #9ca5ab;  /* Line between items */
}

QMenu::item:hover {
    background-color: #a17da4;  /* Background color on hover */
    color: white;  /* Text color on hover */
}

QMenu::item:selected {
    background-color: #a17da4;  /* Background color of selected item */
    color: white;  /* Text color of selected item */
}


"""


def get_combo(border):
    return f"""
QComboBox QAbstractItemView::item:hover {{
    background-color:  #a17da4;
    border: transparent;
}}
QComboBox QAbstractItemView::item:selected {{
    background-color:  #a17da4;
    border: none;
}}
QComboBox QAbstractItemView {{
    background-color: #f0f0f0;
    border: 3px solid #a17da4;
}}
QComboBox {{
	font-family: Noto Sans Arabic;
	padding: -3px 0px -3px 5px;
	font-size: 18px;
	color: #333333;
    border: 3px solid {border};
    background-color: #f0f0f0;
    text-align: center;
}}

QComboBox::drop-down:button{{
image: url(:/img/dd2.png);
padding-top: 10px;
padding-left: 5px;
padding-right: 5px;
width: 13px;
height: 13px

}}

"""

srch_combo = """
QComboBox QAbstractItemView::item:hover {
    background-color:  #a17da4;    
    border: 3px solid #a17da4;
}
QComboBox QAbstractItemView::item:selected {
    background-color:  #a17da4;
    border: none;
}
QComboBox QAbstractItemView {
    background-color: #f0f0f0;
    border: 3px solid #a17da4;
}
QComboBox {
	font-family: Noto Sans Arabic;
	padding: -3px 0px -3px 5px;
	font-size: 18px;
	color: #333333;
    border: 3px solid #a17da4;
    background-color: #f0f0f0;
    text-align: center;
}

QListView {
	font-family: Noto Sans Arabic;
	padding: -3px 0px -3px 0px;
	font-size: 18px;
	color: #333333;
    border: 3px solid #a17da4;
    background-color: #f0f0f0;
    text-align: center;

}

QComboBox::drop-down:button{
image: url(:/img/dd2.png);
padding-top: 10px;
padding-left: 5px;
padding-right: 5px;
width: 13px;
height: 13px
}


QScrollBar:vertical {
    background: #a17da4;
    width: 13px;    
    padding: 3px;
    padding-right: 0px;
}


QScrollBar::handle:vertical {
    background: #333;
    min-width: 10px;
    width: 10px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #555;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    width: 0px;
    background: none;
    border: none;

}

"""



