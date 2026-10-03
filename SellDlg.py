from PyQt6.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import Style



class SellDlg(QDialog):
    def __init__(self, parent, d, r):
        super().__init__()
        self.parent = parent
        self.overlay = None
        self.d = d
        self.r = r
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        self.frame = QFrame(parent=self)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)

        # left frame.
        self.frame_3 = QFrame(parent=self.frame)
        self.frame_3.setStyleSheet(Style.radio)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 15)

        self.label = QLabel("لأتمام عملية البيع الرجاء ملئ البيانات", parent=self.frame_3)
        self.label.setStyleSheet("""color: black; font-family: Noto Sans Arabic; font-size: 22px;""")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.label)

        spacerItem = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.frame_4 = QFrame(self.frame_3)
        self.l4 = QHBoxLayout(self.frame_4)
        self.l4.setContentsMargins(0,0,0,0)
        self.l4.setSpacing(20)
        self.verticalLayout_2.addWidget(self.frame_4)

        self.btn1 = QPushButton("الغاء")
        self.btn1.clicked.connect(self.accept)  # just for close the message box.
        self.btn1.setFixedHeight(55)

        self.btn2 = QPushButton("تم")
        self.btn2.clicked.connect(self.done_press)  # just for close the message box.
        self.btn2.setFixedHeight(55)
        
        self.btn1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn2.setCursor(Qt.CursorShape.PointingHandCursor)

        self.l4.addWidget(self.btn1)
        self.l4.addWidget(self.btn2)


        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 2)
        self.horizontalLayout.addWidget(self.frame_3)

        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        # right frame.
        self.frame_2 = QFrame(parent=self.frame)
        self.frame_2.setStyleSheet("QFrame{\n"
                                   "border: none;\n"
                                   "}\n"
                                   "QLineEdit{\n"
                                   "padding: 10px; background-color: #f0f0f0;\n"
                                   "font-size: 22px;\n"
                                   "}")
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setSpacing(10)

        self.lineEdit = QLineEdit(parent=self.frame_2)

        self.lineEdit.setPlaceholderText("رقم قرار البيع:")
        self.lineEdit.setStyleSheet("border: 6px solid #a17da4; ")
        self.verticalLayout.addWidget(self.lineEdit)

        container = QFrame()
        container.setFixedHeight(65)
        container.setStyleSheet("QFrame{border: 6px solid #a17da4;} QLabel{border:none;} QLineEdit{border:none;}")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        icon_widget = QLabel()
        icon_widget.setPixmap(QIcon(":/img/dd.png").pixmap(26, 26))
        icon_widget.setContentsMargins(7, 7, 0, 0)
        self.editor = QLineEdit()
        self.editor.mousePressEvent = lambda event: self.parent.show_calendar(self.editor)
        icon_widget.mouseReleaseEvent = lambda event: self.parent.show_calendar(self.editor)
        self.editor.setReadOnly(True)
        self.editor.setPlaceholderText("تاريخ قيد البيع")
        layout.addWidget(icon_widget)
        layout.addWidget(self.editor)
        self.verticalLayout.addWidget(container)

        self.lineEdit_3 = QLineEdit(parent=self.frame_2)
        self.lineEdit_3.setPlaceholderText("سعر البيع:")
        self.lineEdit_3.setStyleSheet("border: 6px solid #a17da4; ")
        self.verticalLayout.addWidget(self.lineEdit_3)
        
        self.lineEdit_4 = QLineEdit(parent=self.frame_2)
        self.lineEdit_4.setPlaceholderText("العدد:")
        self.lineEdit_4.setStyleSheet("border: 6px solid #a17da4; ")
        self.verticalLayout.addWidget(self.lineEdit_4)

        self.horizontalLayout.addWidget(self.frame_2)
        self.horizontalLayout.setStretch(0, 7)
        self.horizontalLayout.setStretch(1, 4)
        self.horizontalLayout.setStretch(2, 8)
        self.horizontalLayout.addWidget(self.frame)

        self.setLayout(self.horizontalLayout)
        self.setStyleSheet(Style.dlg_Style)
        self.resize(750, 300)

    def done_press(self):
        if self.lineEdit.text().isdigit() and self.editor.text() and self.lineEdit_3.text().isdigit() and self.lineEdit_4.text().isdigit():
            indx1 = self.parent.parent.db.indcs[1]
            
            tmp = [int(self.lineEdit_4.text()), int(self.lineEdit_3.text()), int(self.lineEdit_4.text()) * int(self.lineEdit_3.text()), int(self.lineEdit.text()), self.editor.text()]
            self.d[indx1['cquant']] -= int(self.lineEdit_4.text())
            self.parent.sell_ds(self.r, self.d, tmp)
            self.accept()
        else:
            self.parent.show_popup(1)

    def show_popup(self):
        if self.lineEdit.text() and self.editor.text() and self.lineEdit_3.text():
            self.accept()
        else:
            self.parent.show_popup(1)

