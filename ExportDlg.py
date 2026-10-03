from PyQt6.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QVBoxLayout,
    QButtonGroup, QRadioButton, QPushButton,
    QLabel, QLineEdit, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

import Style

class ExportDlg(QDialog):
    def __init__(self, parent, d, r):
        super().__init__()
        self.parent = parent
        self.d = d
        self.r = r
        self.t = self.d[18]
        self.overlay = None
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        self.frame = QFrame(parent=self)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)

        # left frame.
        self.frame_3 = QFrame(parent=self.frame)
        self.frame_3.setStyleSheet(Style.radio)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 15)

        self.rgroup = QButtonGroup(parent=self.frame_3)
        self.rgroup.buttonClicked.connect(self.on_radio)
        self.r1 = QRadioButton("  اخراج")
        self.r2 = QRadioButton("  استهلاك")
        self.r3 = QRadioButton("  اتلاف")
        self.r4 = QRadioButton("  حذف")
        self.r1.setChecked(True)
        self.rgroup.addButton(self.r1, 1)
        self.rgroup.addButton(self.r2, 2)
        self.rgroup.addButton(self.r3, 3)
        self.rgroup.addButton(self.r4, 3)
        self.verticalLayout_2.addWidget(self.r1)
        self.verticalLayout_2.addWidget(self.r2)
        self.verticalLayout_2.addWidget(self.r3)
        self.verticalLayout_2.addWidget(self.r4)
        if r == 0:
            self.r2.setDisabled(True)
            self.r3.setDisabled(True)
            self.r4.setDisabled(True)

        '''self.label = QLabel("لأخراج العنصر الى مؤسسة اخرى الرجاء ملئ البيانات" ,parent=self.frame_3)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.verticalLayout_2.addWidget(self.label)'''

        spacerItem = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.frame_4 = QFrame(self.frame_3)
        self.l4 = QHBoxLayout(self.frame_4)
        self.l4.setContentsMargins(0,0,0,0)
        self.l4.setSpacing(20)
        self.verticalLayout_2.addWidget(self.frame_4)

        self.btn1 = QPushButton("الغاء")
        self.btn1.clicked.connect(self.cancel)  # just for close the message box.
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
        self.lineEdit.setPlaceholderText("رقم قيد الاخراج:")
        self.lineEdit.setStyleSheet("border: 6px solid #a17da4; ")
        self.verticalLayout.addWidget(self.lineEdit)

        self.container = QFrame()
        self.container.setFixedHeight(65)
        self.container.setStyleSheet("QFrame{border: 6px solid #a17da4;} QLabel{border:none;} QLineEdit{border:none;}")
        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        icon_widget = QLabel()
        icon_widget.setPixmap(QIcon(":/img/dd.png").pixmap(26, 26))
        icon_widget.setContentsMargins(7, 7, 0, 0)
        self.editor = QLineEdit()
        self.editor.mousePressEvent = lambda event: self.parent.show_calendar(self.editor)
        icon_widget.mouseReleaseEvent = lambda event: self.parent.show_calendar(self.editor)
        self.editor.setReadOnly(True)
        self.editor.setPlaceholderText("تاريخ قيد الاخراج")
        layout.addWidget(icon_widget)
        layout.addWidget(self.editor)
        self.verticalLayout.addWidget(self.container)

        self.lineEdit_3 = QLineEdit(parent=self.frame_2)
        self.lineEdit_3.setPlaceholderText("الى المؤسسة:")
        self.lineEdit_3.setStyleSheet("border: 6px solid #a17da4; ")
        self.parent.create_completer(self.lineEdit_3, self.parent.parent.db.repo)
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

        #self.editor.setText("2025-13-2")
        #self.lineEdit.setText("19")
        #self.lineEdit_3.setText("29")
        #self.lineEdit_4.setText("39")

    def done_press(self):
        # check whether export, cons, corr.
        if self.r1.isChecked():
            self.export()            
        elif self.r2.isChecked():
            self.cons()
        elif self.r3.isChecked():
            self.corr()
        else:
            self.parent.delete(self.r, self.d)
            self.accept()

    def on_radio(self, button):
        self.lineEdit.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.editor.setText("")
        if button != self.r4:
            self.lineEdit.setDisabled(False)
            self.container.setDisabled(False)
            self.lineEdit_3.setDisabled(False)
            self.lineEdit_4.setDisabled(False)
            self.lineEdit_4.show()
            self.lineEdit.setStyleSheet("border: 6px solid #a17da4; ")
            self.container.setStyleSheet("QFrame{border: 6px solid #a17da4;} QLabel{border:none;} QLineEdit{border:none;}")
            self.lineEdit_3.setStyleSheet("border: 6px solid #a17da4; ")
            self.lineEdit_4.setStyleSheet("border: 6px solid #a17da4; ")
            if button == self.r1:
                self.lineEdit_4.show()                
                self.parent.create_completer(self.lineEdit_3, self.parent.parent.db.repo)
                self.lineEdit.setPlaceholderText("رقم قيد الاخراج:")
                self.editor.setPlaceholderText("تاريخ قيد الاخراج")
                self.lineEdit_3.setPlaceholderText("الى المؤسسة:")
            elif button == self.r2:
                self.lineEdit_4.show()
                self.lineEdit_3.setCompleter(None)
                self.lineEdit.setPlaceholderText("رقم قيد الاستهلاك:")
                self.editor.setPlaceholderText("تاريخ قيد الاستهلاك")
                self.lineEdit_3.setPlaceholderText("تسعير المفرد:")
            else:
                self.lineEdit_4.hide()
                self.lineEdit_3.setCompleter(None)
                self.lineEdit.setPlaceholderText("رقم قيد الأتلاف:")
                self.editor.setPlaceholderText("تاريخ قيد الأتلاف")
                self.lineEdit_3.setPlaceholderText("العدد:")
        else:
            self.lineEdit.setStyleSheet("border: 6px solid darkgrey; ")
            self.container.setStyleSheet("QFrame{border: 6px solid darkgrey;} QLabel{border:none;} QLineEdit{border:none;}")
            self.lineEdit_3.setStyleSheet("border: 6px solid darkgrey; ")
            self.lineEdit_4.setStyleSheet("border: 6px solid darkgrey; ")
            self.lineEdit.setDisabled(True)
            self.container.setDisabled(True)
            self.lineEdit_3.setDisabled(True)
            self.lineEdit_4.setDisabled(True)

    def cancel(self):
        self.parent.ref_model = False
        self.accept()
    
    def export(self):
        print(self.r)
        indx = self.parent.parent.db.indcs[0]
        if self.lineEdit.text().isdigit() and self.editor.text() and self.lineEdit_3.text() and self.lineEdit_4.text().isdigit():
            new_repo = self.lineEdit_3.text()
            out_date = self.editor.text()
            out_doc = int(self.lineEdit.text())
            if int(self.lineEdit_4.text()) > self.d[indx['quant']]:
                self.parent.show_popup(1, "لا يمكنك اخراج عدد أكبر من الكمية الموجودة!")
                return
            if self.lineEdit_3.text() == self.d[indx['repo']]:
                self.parent.show_popup(1, "لا يمكنك أخراج العنصر من مخزن الى نفس المخزن!")
                return
            if self.parent.clas_eq_repo(self.d[indx['clas']], self.lineEdit_3.text()):
                self.parent.show_popup(1, "لايمكنك أعطاء أسم للمخزن نفس أسم احد التصنيفات!")
                return
            if self.r == 0:
                self.parent.add(self.d)
            else:
                self.parent.up_clas_repo(self.d[indx['clas']], new_repo)
                self.parent.change_repo_ds(self.r, self.d, new_repo, self.d[indx['quant']], int(self.lineEdit_4.text()), out_doc, out_date)
            self.accept()
        else:
            self.parent.show_popup(1)
    
    def cons(self):
        # lineEdit = doc, editor = date, lineEdit_3 = price, lineEdit_4=quant.
        if self.lineEdit.text().isdigit() and self.editor.text() and self.lineEdit_3.text().isdigit() and self.lineEdit_4.text().isdigit():
            if int(self.lineEdit_4.text()) > self.d[6]:
                self.parent.show_popup(1, "لا يمكنك أستهلاك عدد أكبر من الكمية الموجودة!")
                return
            self.d[6] -= int(self.lineEdit_4.text())
            tmp = [int(self.lineEdit_4.text()), int(self.lineEdit_3.text()), int(self.lineEdit_4.text()) * int(self.lineEdit_3.text()), int(self.lineEdit.text()), self.editor.text()]
            self.parent.cons_ds(self.r, self.d, tmp)
            self.accept()
        else:
            self.parent.show_popup(1)
            
    def corr(self):
        if self.lineEdit.text().isdigit() and self.editor.text() and self.lineEdit_3.text().isdigit():
            if int(self.lineEdit_3.text()) > self.d[6]:
                self.parent.show_popup(1, "لا يمكنك أتلاف عدد أكبر من الكمية الموجودة!")
                return
            self.d[6] -= int(self.lineEdit_3.text())
            tmp = [int(self.lineEdit_3.text()), int(self.lineEdit.text()), self.editor.text()]
            self.parent.corr_ds(self.r, self.d, tmp)
            self.accept()
        else:
            self.parent.show_popup(1)

