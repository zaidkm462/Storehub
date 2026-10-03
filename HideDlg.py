from PyQt6.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QCheckBox, QApplication, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
import Style



class HideDlg(QDialog):
    def __init__(self, parent, rprt=False, names=None, checked = None):
        super().__init__()
        self.parent = parent
        self.overlay = None
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.names = []
        self.cols = []
        self.ds = None
        self.rprt = rprt
        self.x = []
        self.checked = checked
        
        if self.rprt:
            self.names = names
        elif parent.x == 0:
            self.names = parent.tb_header
            self.ds = "exist_cols"
        elif parent.x == 1:
            self.names = parent.cons_head
            self.ds = "cons_cols"
        elif parent.x == 2:
            self.names = parent.corr_head
            self.ds = "corr_cols"
        else:
            self.names = parent.sold_head
            self.ds = "sold_cols"
        
        self.btn_style = """
        QPushButton{
			background-color: #a17daf;
			border: none; 
			color: white;
			font-size: 22px;
			font-family: Noto Sans Arabic;
		}       
        """
        self.frame_style = "QFrame{border: 0px solid black;}"
        self.label_style = "QLabel{ font-family: Noto Sans Arabic; font-size: 20px;}"
        self.check_style = """
        QFrame{border: 0px solid black;}
        QCheckBox{        
			font-size: 16px;
			font-family: Noto Sans Arabic;
        }
        QCheckBox::indicator{
        width: 20px;
        height: 20px;
        }
        
        """        
		
		# main frame vertical.
        self.frame = QFrame(parent=self)
        #self.frame.setStyleSheet(self.frame_style)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(8)

        # label layout & frame horizontal.
        self.label_frame = QFrame(parent=self.frame)
        self.label_frame.setStyleSheet(self.frame_style)
        self.label_layout_h = QHBoxLayout(self.label_frame)
        
        # checks layout & frame horizontal.
        self.checks_frame = QFrame(parent=self.frame)
        self.checks_frame.setStyleSheet(self.frame_style)  
        self.checks_layout_h = QHBoxLayout(self.checks_frame)
        self.checks_layout_h.setSpacing(20)
        
        # btns layout & frame horizontal.
        self.btns_frame = QFrame(parent=self.frame)
        self.btns_frame.setStyleSheet(self.frame_style)  
        self.btns_layout_h = QHBoxLayout(self.btns_frame)
        self.btns_layout_h.setSpacing(15)
      
        # left checks layout & frame vertiacl.
        self.lchecks_frame = QFrame(parent=self.checks_frame)
        self.lchecks_frame.setStyleSheet(self.check_style)  
        self.lchecks_layout_v = QVBoxLayout(self.lchecks_frame)
        self.lchecks_layout_v.setSpacing(5)        
        self.lchecks_frame.hide()
        
        # middle checks layout & frame vertiacl.
        self.mchecks_frame = QFrame(parent=self.checks_frame)
        self.mchecks_frame.setStyleSheet(self.check_style)  
        self.mchecks_layout_v = QVBoxLayout(self.mchecks_frame)
        self.mchecks_layout_v.setSpacing(5)
        
        # right checks layout & frame vertiacl.
        self.rchecks_frame = QFrame(parent=self.checks_frame)
        self.rchecks_frame.setStyleSheet(self.check_style)  
        self.rchecks_layout_v = QVBoxLayout(self.rchecks_frame)
        self.rchecks_layout_v.setSpacing(5)
        
        self.verticalLayout.addWidget(self.label_frame)
        self.verticalLayout.addWidget(self.checks_frame)
        self.verticalLayout.addWidget(self.btns_frame)
        
        label = QLabel("حدد الاعمدة التي تريد اظهارها")
        label.setStyleSheet(self.label_style)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_layout_h.addWidget(label)
        
        self.add_checks(self.names[0: 10], self.names[10: 20],  self.names[20: 30])
        
        mspacerItem = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.mchecks_layout_v.addItem(mspacerItem)
        
        lspacerItem = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.lchecks_layout_v.addItem(lspacerItem)

        self.checks_layout_h.addWidget(self.lchecks_frame)
        self.checks_layout_h.addWidget(self.mchecks_frame)
        self.checks_layout_h.addWidget(self.rchecks_frame)
        
        self.btn1 = QPushButton("الغاء")
        self.btn1.setStyleSheet(self.btn_style)
        self.btn1.clicked.connect(self.accept)
        self.btn1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn1.setFixedHeight(53)

        self.btn2 = QPushButton("حفظ")
        self.btn2.setStyleSheet(self.btn_style)
        self.btn2.clicked.connect(self.done_pressed)
        self.btn2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn2.setFixedHeight(53)
        
        
        self.btns_layout_h.addWidget(self.btn1)
        self.btns_layout_h.addWidget(self.btn2)


        self.setLayout(self.verticalLayout)
        self.setStyleSheet(Style.dlg_Style)
        self.resize(0, 0)
        
    def done_pressed(self):
        cols = []
        for i in range(len(self.cols)):
        	if self.cols[i].isChecked():
        	   cols.append(i)
        if self.rprt: self.x = cols
        else: self.parent.pref[self.ds] = cols
        self.accept()
        


    def add_checks(self, l1, l2, l3):
        if l3:
            self.lchecks_frame.show() 

        for i in range(0, len(l1)):
            c = QCheckBox(l1[i]+"  ")
            c.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self.rchecks_layout_v.addWidget(c)
            self.cols.append(c)
        
        for i in range(0, len(l2)):
            c = QCheckBox(l2[i]+"  ")
            c.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self.mchecks_layout_v.addWidget(c)
            self.cols.append(c)
    
        for i in range(0, len(l3)):
            c = QCheckBox(l3[i]+"  ")
            c.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self.lchecks_layout_v.addWidget(c)
            self.cols.append(c)
        
        for i in range(len(self.cols)):
            if self.rprt:
                if i in self.checked: self.cols[i].setChecked(True)
            elif i in self.parent.pref[self.ds]:
                self.cols[i].setChecked(True)
            
    def showEvent(self, event):
        super().showEvent(event)
        screen = QApplication.primaryScreen().availableGeometry()
        dialog_rect = self.frameGeometry()
        dialog_rect.moveCenter(screen.center())
        self.move(dialog_rect.topLeft())
            
  
