from PyQt6.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpacerItem, QSizePolicy, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
import Style



class MissingDlg(QDialog):
    def __init__(self, parent, m, r):
        super().__init__(parent)
        self.parent = parent
        self.overlay = None
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.m = m
        self.r = r
        self.clean = False
        self.edtrs = {}
        self.style = """
       QLineEdit{
           padding: 10px;
           font-size: 22px;
       }
       QPushButton{
			background-color: #a17daf;
			border: none; 
			color: white;
			font-size: 22px;
			font-family: Noto Sans Arabic;
		}"""
        self.self_vlayout = QVBoxLayout(self)		
        self.self_vlayout.setContentsMargins(0, 0, 0, 0)
        self.self_vlayout.setSpacing(0)
        
		# main frame horizontal.
        self.frame = QFrame(parent=self)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(15, 15, 15, 15)
        self.horizontalLayout.setSpacing(15)

        # left frame vertical.
        self.frame_1 = QFrame(parent=self.frame)
        self.frame_1.setStyleSheet(self.style)
        self.verticalLayout_1 = QVBoxLayout(self.frame_1)
        #self.verticalLayout_1.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_1.setSpacing(15)
        
        # right frame vertical.
        self.frame_2 = QFrame(parent=self.frame)
        self.frame_2.setStyleSheet(self.style)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        #self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setSpacing(15)
        
        indx = self.parent.db.indcs[0]
        for i in range(len(self.m)):
            if self.m[i] in (indx['bdate'], indx['indate'], indx['pdate'], indx['edate']): edtr = self.date_editors(parent, self.m[i])
            else: edtr = self.other_editors(parent, self.m[i])
            self.edtrs[i] = edtr
            if i < int(len(m)/2 + 0.5): self.verticalLayout_2.addWidget(edtr)
            else: self.verticalLayout_1.addWidget(edtr)
            
        if len(self.m) == 1: self.frame_1.hide()
            
        


        self.btn1 = QPushButton("الغاء")
        self.btn1.clicked.connect(self.dispoze)  # just for close the message box.
        self.btn1.setFixedHeight(53)
        #self.btn1.setFixedWidth(220)

        self.btn2 = QPushButton("اضافة")
        self.btn2.clicked.connect(self.done_press)  # just for close the message box.
        self.btn2.setFixedHeight(53)
        
        self.btn1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn2.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btns_frame = QFrame(self.frame)
        self.btns_hlayout = QHBoxLayout(self.btns_frame)
        self.btns_hlayout.setContentsMargins(25, 0, 25, 25)
        self.btns_hlayout.setSpacing(20)
        self.btns_frame.setStyleSheet(self.style)
        
        self.btns_hlayout.addWidget(self.btn1)
        self.btns_hlayout.addWidget(self.btn2)
                
        
        self.horizontalLayout.addWidget(self.frame_1)
        self.horizontalLayout.addWidget(self.frame_2)

        spacerItem = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout_1.addItem(spacerItem)
        
        self.self_vlayout.addWidget(self.frame)
        self.self_vlayout.addWidget(self.btns_frame)

        

        self.setLayout(self.self_vlayout)
        self.setStyleSheet(Style.dlg_Style)
        self.resize(650, 0)


    def dispoze(self):
        self.setParent(None)
        self.close()
        self.parent.delegate.overlay.close()

    def showEvent(self, event):
        super().showEvent(event)
        screen = QApplication.primaryScreen().availableGeometry()
        dialog_rect = self.frameGeometry()
        dialog_rect.moveCenter(screen.center())
        self.move(dialog_rect.topLeft())


    def other_editors(self, parent, c):
        indx = self.parent.db.indcs[0]
        editor = QLineEdit()
        #editor.setText('000')
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        editor.setStyleSheet("""
        QLineEdit{
        	border: 3px solid #a17da4;
        	font-family: Noto Sans Ararbic;
        	font-size: 16px;
        	background-color: white;
        }
        
        
        """)
        editor.setPlaceholderText(self.parent.delegate.placeholders[c])
        editor.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        if c == indx['price']:
            editor.textChanged.connect(self.auto)
        elif c == indx['quant']:
            editor.textChanged.connect(self.auto)

        if c == indx['emp']:
            self.parent.delegate.create_completer(editor, self.parent.db.emp.keys())
        elif c == indx['mat']:
            self.parent.delegate.create_completer(editor, self.parent.db.mat.keys())
        elif c == indx['origin']:
            self.parent.delegate.create_completer(editor, self.parent.db.origin.keys())
        elif c == indx['clas']:
            self.parent.delegate.create_completer(editor, self.parent.db.clas.keys())
        elif c == indx['corp']:
            self.parent.delegate.create_completer(editor, self.parent.db.corp.keys())
        elif c == ['prepo']:
            self.parent.delegate.create_completer(editor, self.parent.db.repo.keys())
        return editor


    def date_editors(self, parent, c):
        editor = QLineEdit()
        editor.setText(self.parent.delegate.placeholders[c])
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = QIcon(":/img/dd.png")
        action = QAction(editor)
        action.setIcon(QIcon(icon))
        editor.addAction(action, QLineEdit.ActionPosition.LeadingPosition)
        action.triggered.connect(lambda: self.parent.delegate.show_calendar(editor, False))
        editor.mousePressEvent = lambda event: self.parent.delegate.show_calendar(editor, False)
        editor.setStyleSheet("""
        QLineEdit{
        	border: 3px solid #a17da4;
        	font-family: Noto Sans Ararbic;
        	font-size: 16px;
        	color: gray;
        }     
        
        """)
        editor.setReadOnly(True)
        return editor



    def done_press(self):
        indx = self.parent.db.indcs[0]
        self.clean = True
        
        for i in range(len(self.m)):
            # opt dates.
            if self.m[i] in (indx['pdate'], indx['edate']):
                if self.edtrs[i].text()[0].isdigit(): self.r[self.m[i]] = self.edtrs[i].text()
                else: self.r[self.m[i]] = ""
            
            # dates.
            elif self.m[i] in (indx['bdate'], indx['indate']):
                if self.edtrs[i].text()[0].isdigit(): self.r[self.m[i]] = self.edtrs[i].text()
                else:
                    self.clean = False
                    self.setWindowOpacity(0)
                    self.parent.delegate.show_popup(1, "يرجى ادخال تاريخ الشراء والادخال.")
                    self.setWindowOpacity(1)
                    break
            
            # opt others.
            elif self.m[i] in (indx['serial'], indx['corp'], indx['prepo']):
                self.r[self.m[i]] = self.edtrs[i].text()
                continue
            
            # digits.
            elif self.m[i] in (indx['price'], indx['quant'], indx['hprice'], indx['indoc']):
                if not self.edtrs[i].text().isdigit():
                    self.clean = False
                    self.setWindowOpacity(0)
                    self.parent.delegate.show_popup(1, "يرجى ادخال رقم للسعر والكمية والمستند.")
                    self.setWindowOpacity(1)
                    break
                else: self.r[self.m[i]] = int(self.edtrs[i].text())
                        
            # non-empty.
            elif self.edtrs[i].text() == "": 
                self.clean = False
                self.setWindowOpacity(0)
                self.parent.delegate.show_popup(1)
                self.setWindowOpacity(1)
                break
            
            else:
                self.r[self.m[i]] = self.edtrs[i].text()
        if self.clean : self.dispoze()
            
            
            
            
            
