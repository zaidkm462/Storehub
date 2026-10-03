from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QLineEdit, QComboBox,
    QRadioButton, QButtonGroup, QPushButton, QFileDialog, QApplication,
    QSpacerItem, QSizePolicy, QCompleter
)
from PyQt6.QtCore import Qt
import traceback
import Style
import report
from HideDlg import HideDlg


class ReportDlg(QDialog):
    styl = """
    QFrame{
        border: 0px solid black;    
    }
    QLabel{
        font-family: Noto Sans Arabic;
        font-size: 22px;    
    }
    QLineEdit{
        font-family: Noto Sans Arabic;
        font-size: 18px;
        border: 5px solid #a17da4;
        background-color: #f0f0f0;
		
	}
    QPushButton{
		background-color: #a17daf;
		border: none; 
		color: #f0f0f0;
		font-size: 22px;
		font-family: Noto Sans Arabic;
    }
    
    """
    def __init__(self, parent, db):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.db = db
        self.parent = parent
        self.cols = {0: [[], []], 1: [[], []], 2: [[], []], 3: [[], []]}
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        frame_0 = QFrame(parent=self)
        vLayout_0 = QVBoxLayout(frame_0)
        vLayout_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        frame_1 = QFrame(parent=frame_0)
        frame_1.setStyleSheet(self.styl)
        frame_1.setFixedWidth(520)
        hLayout_0 = QHBoxLayout(frame_1)        
        mat_l = QLabel("ادخل أسم المادة: ")
        mat_l.adjustSize()
        self.mat_ln = QLineEdit("الكل")
        self.mat_ln.setFixedWidth(300)
        hLayout_0.addWidget(self.mat_ln)
        hLayout_0.addWidget(mat_l)
        hLayout_0.setSpacing(30)
        completer = QCompleter(db.mat.keys())
        completer.popup().setStyleSheet(Style.cmpltr_style)
        self.mat_ln.setCompleter(completer)
        completer.popup().setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        completer.popup().setWordWrap(True)
        
        frame_2 = QFrame(parent=frame_0)
        frame_2.setStyleSheet(self.styl)
        frame_2.setFixedWidth(520)
        hLayout_1 = QHBoxLayout(frame_2)        
        repo_l = QLabel("ادخل أسم المخزن: ")
        repo_l.adjustSize()
        self.repo_ln = QLineEdit("الكل")
        self.repo_ln.setFixedWidth(300)
        hLayout_1.addWidget(self.repo_ln)
        hLayout_1.addWidget(repo_l)
        hLayout_1.setSpacing(30)
        completer = QCompleter(db.repo.keys())
        completer.popup().setStyleSheet(Style.cmpltr_style)
        self.repo_ln.setCompleter(completer)
        completer.popup().setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        completer.popup().setWordWrap(True)
        
        frame_3 = QFrame(parent=frame_0)
        frame_3.setStyleSheet(self.styl)
        frame_3.setFixedWidth(520)
        hLayout_2 = QHBoxLayout(frame_3)        
        clas_l = QLabel("ادخل أسم التصنيف: ")
        clas_l.adjustSize()
        self.clas_ln = QLineEdit("الكل")
        self.clas_ln.setFixedWidth(300)
        hLayout_2.addWidget(self.clas_ln)
        hLayout_2.addWidget(clas_l)
        hLayout_2.setSpacing(30)
        completer = QCompleter(db.clas.keys())
        completer.popup().setStyleSheet(Style.cmpltr_style)
        self.clas_ln.setCompleter(completer)
        completer.popup().setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        completer.popup().setWordWrap(True)
        
        cols_frame = QFrame(parent=frame_0)
        cols_frame.setStyleSheet(self.styl)
        cols_frame.setFixedWidth(520)
        cols_layout_h = QHBoxLayout(cols_frame)        
        cols_l = QLabel("اختر اعمدة التقرير: ")
        cols_l.adjustSize()
        
        cols_btns_lframe = QFrame()
        cols_btns_rframe = QFrame()
        cols_btn_llayout = QVBoxLayout(cols_btns_lframe)
        cols_btn_rlayout = QVBoxLayout(cols_btns_rframe)
        cols_btn_llayout.setContentsMargins(0, 0, 0, 0)        
        cols_btn_rlayout.setContentsMargins(10, 0, 0, 0)
        
        ex_btn = QPushButton("الموجودات")
        cons_btn = QPushButton("المستهلكات")
        corr_btn = QPushButton("المتلفات")
        sold_btn = QPushButton("المبيعات")
        
        ex_btn.setFixedWidth(120)
        cons_btn.setFixedWidth(120)
        corr_btn.setFixedWidth(120)
        sold_btn.setFixedWidth(120)
        
        ex_btn.clicked.connect(lambda: self.slct_cols(0))
        cons_btn.clicked.connect(lambda: self.slct_cols(1))
        corr_btn.clicked.connect(lambda: self.slct_cols(2))
        sold_btn.clicked.connect(lambda: self.slct_cols(3))
        
        
        ex_btn.setCursor(Qt.CursorShape.PointingHandCursor)        
        cons_btn.setCursor(Qt.CursorShape.PointingHandCursor)      
        corr_btn.setCursor(Qt.CursorShape.PointingHandCursor)      
        sold_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        
        cols_btn_llayout.addWidget(cons_btn)
        cols_btn_llayout.addWidget(sold_btn)
        cols_btn_rlayout.addWidget(ex_btn)
        cols_btn_rlayout.addWidget(corr_btn)
		
        cols_layout_h.addWidget(cols_btns_lframe)
        cols_layout_h.addWidget(cols_btns_rframe)
        cols_layout_h.addWidget(cols_l)
        cols_layout_h.setSpacing(20)
        
        
        frame_4 = QFrame(parent=frame_0)
        frame_4.setStyleSheet(Style.radio2)
        hLayout_3 = QHBoxLayout(frame_4)
        hLayout_3.setSpacing(70)
        
        frame_6 = QFrame(parent=frame_0)
        frame_6.setStyleSheet(Style.radio2)
        vLayout_1 = QVBoxLayout(frame_6)
        
        frame_7 = QFrame(parent=frame_6)
        frame_7.setStyleSheet(Style.radio2)
        hLayout_5 = QHBoxLayout(frame_7)
        hLayout_5.setSpacing(40)
        hLayout_5.setContentsMargins(0,0,0,0)
        
        frame_8 = QFrame(parent=frame_6)
        frame_8.setStyleSheet(Style.radio2)
        hLayout_6 = QHBoxLayout(frame_8)
        hLayout_6.setSpacing(50)
        hLayout_6.setContentsMargins(0,0,0,0)
        
        type_l = QLabel("اختر نوع التقرير: ")
        type_l.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        type_l.adjustSize()
        #hLayout_3.setContentsMargins(5, 5, 5, 15)
        self.rgroup = QButtonGroup(parent=frame_4)
        self.rgroup.buttonClicked.connect(self.on_radio)
        self.r1 = QRadioButton("    يومي")
        self.r2 = QRadioButton("  شهري")
        self.r3 = QRadioButton("  سنوي")
        self.r4 = QRadioButton("     الكل")
        self.r4.setChecked(True)
        self.rgroup.addButton(self.r1, 1)
        self.rgroup.addButton(self.r2, 2)
        self.rgroup.addButton(self.r3, 3)
        self.rgroup.addButton(self.r4, 4)
        hLayout_5.addWidget(self.r2)
        hLayout_5.addWidget(self.r1)
        hLayout_6.addWidget(self.r3)
        hLayout_6.addWidget(self.r4)
        
        
        
        vLayout_1.addWidget(frame_8)
        vLayout_1.addWidget(frame_7)
        hLayout_3.addWidget(frame_6)
        hLayout_3.addWidget(type_l)
        
        frame_5 = QFrame(parent=frame_0)
        frame_5.setStyleSheet(self.styl)
        frame_5.setFixedWidth(520)
        hLayout_4 = QHBoxLayout(frame_5)        
        dur_l = QLabel("ادخل تاريخ التقرير: ")
        dur_l.adjustSize()
        
        self.day = QComboBox()
        self.day.addItem("اليوم")
        self.day.addItems([str(i) for i in range(1, 32)])
        self.day.setStyleSheet(Style.combo)
        self.day.setCursor(Qt.CursorShape.PointingHandCursor)
        line_day = QLineEdit()
        self.day.setLineEdit(line_day)
        self.day.setEditable(True)
        self.day.setEnabled(False)
        line_day.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        self.month = QComboBox()
        self.month.addItem("الشهر")
        self.month.addItems([str(i) for i in range(1, 13)])
        self.month.setStyleSheet(Style.combo)
        self.month.setCursor(Qt.CursorShape.PointingHandCursor)
        line_month = QLineEdit()
        self.month.setLineEdit(line_month)
        self.month.setEditable(True)
        self.month.setEnabled(False)
        line_month.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        self.year = QComboBox()
        self.year.addItem("السنة")
        yrs = list(db.al.keys()) + list(db.cons.keys()) + list(db.sold.keys()) + list(db.corr.keys())
        self.year.addItems(list(set(yrs)))
        self.year.setStyleSheet(Style.combo)
        self.year.setCursor(Qt.CursorShape.PointingHandCursor)
        line_year = QLineEdit()
        self.year.setLineEdit(line_year)
        self.year.setEditable(True)
        self.year.setEnabled(False)
        line_year.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        hLayout_4.addWidget(self.day)
        hLayout_4.addWidget(self.month)        
        hLayout_4.addWidget(self.year)
        hLayout_4.addWidget(dur_l)
        hLayout_4.setSpacing(30)
        
        frame_9 = QFrame(frame_0)
        frame_9.setFixedWidth(505)
        frame_9.setStyleSheet(self.styl)
        l4 = QHBoxLayout(frame_9)
        l4.setContentsMargins(0,20,0,0)
        l4.setSpacing(30)
        
        self.btn1 = QPushButton("الغاء")
        self.btn1.clicked.connect(self.dispoze)  # just for close the message box.
        self.btn1.setFixedHeight(55)
        self.btn1.setFixedWidth(140)


        self.btn2 = QPushButton("تم")
        self.btn2.clicked.connect(self.done_press)  # just for close the message box.
        self.btn2.setFixedHeight(55)
        self.btn2.setFixedWidth(140)
        
        
        spacerItem = QSpacerItem(20, 30, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.btn1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn2.setCursor(Qt.CursorShape.PointingHandCursor)

        l4.addWidget(self.btn1)
        l4.addWidget(self.btn2)
        l4.addItem(spacerItem)
        
        
        
        
        vLayout_0.addWidget(frame_1, alignment=Qt.AlignmentFlag.AlignCenter)        
        vLayout_0.addWidget(frame_2, alignment=Qt.AlignmentFlag.AlignCenter)
        vLayout_0.addWidget(frame_3, alignment=Qt.AlignmentFlag.AlignCenter)
        vLayout_0.addWidget(cols_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        vLayout_0.addWidget(frame_4, alignment=Qt.AlignmentFlag.AlignCenter)
        vLayout_0.addWidget(frame_5, alignment=Qt.AlignmentFlag.AlignCenter)
        vLayout_0.addWidget(frame_9, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(frame_0, alignment=Qt.AlignmentFlag.AlignCenter)
           
   
        self.resize(0, 0)
        self.setStyleSheet(Style.dlg_Style)
        
        self.slct_cols(0, True)
        self.slct_cols(1, True)
        self.slct_cols(2, True)
        self.slct_cols(3, True)

    def showEvent(self, event):
        super().showEvent(event)
        screen = QApplication.primaryScreen().availableGeometry()
        dialog_rect = self.frameGeometry()
        dialog_rect.moveCenter(screen.center())
        self.move(dialog_rect.topLeft())     


    def on_radio(self, button):
        if button == self.r1:     	
        	self.day.setEnabled(True)
        	self.month.setEnabled(True)
        	self.year.setEnabled(True)
        	self.day.setStyleSheet(Style.get_combo("#a17da4"))
        	self.month.setStyleSheet(Style.get_combo("#a17da4"))
        	self.year.setStyleSheet(Style.get_combo("#a17da4"))        	
        elif button == self.r2:
        	self.day.setEnabled(False)
        	self.month.setEnabled(True)
        	self.year.setEnabled(True)
        	self.day.setStyleSheet(Style.get_combo("darkgrey"))
        	self.month.setStyleSheet(Style.get_combo("#a17da4"))
        	self.year.setStyleSheet(Style.get_combo("#a17da4"))       
        elif button == self.r3:
        	self.day.setEnabled(False)
        	self.month.setEnabled(False)
        	self.year.setEnabled(True)
        	self.day.setStyleSheet(Style.get_combo("darkgrey"))
        	self.month.setStyleSheet(Style.get_combo("darkgrey"))
        	self.year.setStyleSheet(Style.get_combo("#a17da4"))            
        elif button == self.r4:
        	self.day.setEnabled(False)
        	self.month.setEnabled(False)
        	self.year.setEnabled(False)
        	self.day.setStyleSheet(Style.get_combo("darkgrey"))
        	self.month.setStyleSheet(Style.get_combo("darkgrey"))
        	self.year.setStyleSheet(Style.get_combo("darkgrey"))
    def done_press(self):
        rtype = 0
        dt = ""
        clean = False
        if self.mat_ln.text() != 'الكل' and not self.mat_ln.text() in self.db.mat:            
            self.hide()
            self.parent.delegate.show_popup(1, "المادة المدخلة غير موجودة")
            self.show()
        elif self.repo_ln.text() != 'الكل' and not self.repo_ln.text() in self.db.repo:           
            self.hide()
            self.parent.delegate.show_popup(1, "المخزن المدخل غير موجود")
            self.show()
        elif self.clas_ln.text() != 'الكل' and not self.clas_ln.text() in self.db.clas:           
            self.hide()
            self.parent.delegate.show_popup(1, "التصنيف المدخل غير موجود")
            self.show()
        else:
            if self.r4.isChecked():
                clean = True         
            elif self.r3.isChecked() and self.check_combo(self.year):
                rtype = 1
                dt= self.year.currentText()
                clean = True
            elif self.r2.isChecked() and self.check_combo(self.year) and self.check_combo(self.month):
                rtype = 2
                mnth = self.month.currentText() if len(self.month.currentText()) > 1 else "0"+self.month.currentText()
                dt= self.year.currentText() + '-' + mnth
                clean = True
            elif self.r1.isChecked() and self.check_combo(self.year) and self.check_combo(self.month)  and self.check_combo(self.day):
                rtype = 3
                mnth = self.month.currentText() if len(self.month.currentText()) > 1 else "0"+self.month.currentText()
                di = self.day.currentText() if len(self.day.currentText()) > 1 else "0"+self.day.currentText()
                dt= self.year.currentText() + '-' + mnth + '-' + di
                clean = True
            
            hdr = [self.cols[0][1], self.cols[1][1], self.cols[2][1], self.cols[3][1]]
            cols = [self.cols[0][0], self.cols[1][0], self.cols[2][0], self.cols[3][0]]
            for i in hdr:
                if len(i) == 0:
                    self.hide()
                    self.parent.delegate.show_popup(1, "يرجى اختيار أعمدة!")
                    self.show()
                    return
                elif len(i) > 9:
                    self.hide()
                    self.parent.delegate.show_popup(1, "عدد الأعمدة يجب أن يكون أقل من 10 !")
                    self.show()
                    return
        
            if clean:
                path = QFileDialog.getExistingDirectory(self, "اختر مكان حفظ التقرير")
                if not path:
                    return
                QApplication.processEvents()
                self.hide()
                try:
                    report.generate(path, self.db, self.mat_ln.text(), self.repo_ln.text(), self.clas_ln.text(), rtype, dt, cols, hdr)
                    self.parent.delegate.show_popup(1, "تم حفظ التقرير")
                    self.parent.log("report generated > "+path)
                except Exception as e:
                    traceback.print_exc()
                    self.parent.log(e, True)
                    self.parent.delegate.show_popup(1, "حدث خطأ اثناء توليد التقرير!")
                self.show()
    def dispoze(self):
        self.setParent(None)
        self.close()
        self.parent.show_wait(False)
        
    def check_combo(self, combo):
        if combo.currentText() in ("اليوم", "الشهر", "السنة") or combo.findText(combo.currentText()) == -1:
            self.hide()
            self.parent.delegate.show_popup(1, "ادخل التاريخ بشكل صحيح")
            self.show()
            return False
        else:
            return True
            
	
    def slct_cols(self, t, d=False):
        if t==0: names, checked = self.parent.tb_header, [2, 3, 4, 5, 6, 7]
        elif t==1: names, checked = self.parent.cons_head, [2, 3, 5, 17, 18, 19]
        elif t==2: names, checked = self.parent.corr_head, [2, 3, 4, 5, 17]
        else: names, checked = self.parent.sold_head, [2, 3, 5, 22, 23, 24]
	    
        if not d:
            dlg = HideDlg(self.parent, True, names, checked)
            self.hide()
            dlg.exec()
            cols = dlg.x
        else:
            cols = checked
        self.cols[t][0] = list(reversed(cols))
        self.cols[t][1] = list(reversed([names[i] for i in cols]))    
	    
        if not d: self.show()
	    
