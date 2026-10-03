import logging
import time
import sys
from PyQt6.QtGui import QIcon, QColor, QPainter, QFont, QFontDatabase, QPixmap, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView, QToolButton, QFrame, QWidget, \
     QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFileDialog, QMenu, QLineEdit, QComboBox, QListView, QScrollBar
from PyQt6.QtCore import Qt, QSize, QRect, QPropertyAnimation, QEasingCurve, QPoint
import traceback
from db2 import DB
from main import Ui_MainWindow
from CstmDlg import CustomDelegate, CenteredItemDelegate, ClickableLineEdit
from ReportDlg import ReportDlg
from AddDlg import AddDlg
from HideDlg import HideDlg
from BalanceDlg import BalanceDlg
import sys
from TableModel import TableModel

import Style
import r

import json
import os


logging.basicConfig(
    filename="app.log", 
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s",  
    datefmt="%Y-%m-%d %H:%M:%S", 
    encoding='utf-8'
)

def read_pref():
    default = {
        "exist_cols": list(range(19)),
        "cons_cols":  list(range(25)),
        "corr_cols":  list(range(22)),
        "sold_cols":  list(range(29)), 
    }

    if os.path.exists("prefrences.json"):
        with open("prefrences.json", "r") as file:
            pref = json.load(file)
            return pref
    else:
        with open("prefrences.json", "w") as file:
            json.dump(default, file, indent=4)
        return default


def log_exception(exc_type, exc_value, exc_traceback):
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)).replace("\n", "||")
    print(error_msg.replace("||", "\n"))
    logging.error(error_msg)

sys.excepthook = log_exception



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Store Hub")
        logging.info("app started")
        self.setupUi(self)
        self.x = 0
        self.pref = read_pref()
        self.srch = False
        self.srch_pos = None
        self.srch_fld = 2
        self.srch_frame = None
        
        self.tb_header = ['التسلسل', 'اسم الموظف', 'اسم المادة', 'الرقم التسلسلي', 'المنشأ', 'سعر المفرد', 'الكمية', 'السعر الكلي', 'تاريخ الشراء', 'رقم مستند الادخال', 'تاريخ مستند الادخال', 'رقم مستند الاخراج', 'تاريخ مستند الاخراج', 'التصنيف', 'الشركة المصنعة', 'تاريخ الانتاج', 'تاريخ الانتهاء', 'المخزن السابق', 'المؤسسة']
        self.corr_head = ['التسلسل', 'اسم الموظف', 'اسم المادة', 'الرقم التسلسلي', 'المنشأ', 'سعر المفرد', 'الكمية', 'السعر الكلي', 'تاريخ الشراء', 'رقم مستند الادخال', 'تاريخ مستند الادخال', 'رقم مستند الاخراج', 'تاريخ مستند الاخراج', 'التصنيف','الشركة المصنعة', 'تاريخ الانتاج', 'تاريخ الانتهاء', 'الكمية المتلفة', 'رقم مستند الاتلاف', 'تاريخ مستند الاتلاف', 'المخزن السابق', 'المؤسسة']
        self.sold_head = ['التسلسل', 'اسم الموظف', 'اسم المادة', 'الرقم التسلسلي', 'المنشأ', 'سعر المفرد', 'الكمية', 'السعر الكلي', 'تاريخ الشراء', 'رقم مستند الادخال', 'تاريخ مستند الادخال', 'رقم مستند الاخراج', 'تاريخ مستند الاخراج', 'التصنيف', 'الشركة المصنعة', 'تاريخ الانتاج', 'تاريخ الانتهاء', 'الكمية المستهلكة', 'سعر الأستهلاك المفرد', 'سعر الاستهلاك الكلي', 'رقم مستند الاستهلاك', 'تاريخ مستند الاستهلاك', 'الكمية المباعة', 'سعر البيع المفرد', 'سعر البيع الكلي', 'رقم مستند البيع', 'تاريخ مستند البيع', 'المخزن السابق', 'المؤسسة']
        self.cons_head = ['التسلسل', 'اسم الموظف', 'اسم المادة', 'الرقم التسلسلي', 'المنشأ', 'سعر المفرد', 'الكمية', 'السعر الكلي', 'تاريخ الشراء', 'رقم مستند الادخال', 'تاريخ مستند الادخال', 'رقم مستند الاخراج', 'تاريخ مستند الاخراج', 'التصنيف','الشركة المصنعة', 'تاريخ الانتاج', 'تاريخ الانتهاء', 'الكمية المستهلكة', 'سعر الأستهلاك المفرد', 'سعر الاستهلاك الكلي', 'رقم مستند الاستهلاك', 'تاريخ مستند الاستهلاك', 'المخزن السابق', 'المؤسسة', 'بيع']
        
        self.is_max = False
        self.db = DB(time.strftime("%Y-%m-%d"))

        self.pushButton.clicked.connect(self.show_menue)
        self.pushButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self.nr_label = QLabel( "لا يوجد نتائج", self)
        self.nr_label.setStyleSheet(Style.no_result)
        self.nr_label.adjustSize()


        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 175);")
        self.overlay.close()

        self.wait_label = QLabel("يرجى الانتظار...", self)
        self.wait_label.setStyleSheet(Style.wait_label)
        self.wait_label.adjustSize()
        self.wait_label.close()
        
        self.pixmap = QPixmap(":/img/klk.png")   
        self.logo_label = QLabel(self)
        self.scaled_pixmap = self.pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)  
        self.logo_label.resize(self.size())
        self.logo_label.setPixmap(self.scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)        
        self.logo_label.mousePressEvent = self.show_menue
        self.logo_label.close()  

        self.menue = QFrame(self)
        self.menue.setStyleSheet(Style.menue)

        layout = QVBoxLayout(self.menue)
        #layout.setSpacing(30)
        layout.setContentsMargins(0,10,0,0)
        #layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.con0 = QFrame(self.menue)
        self.con0.setStyleSheet(Style.menue_item)
        l0 = QHBoxLayout(self.con0)
        l0.setContentsMargins(0, 0, 0, 0)
        l0.setSpacing(0)
        b0 = QToolButton(self.con0)
        b0.setIcon(QIcon(":/img/m1.png"))
        b0.setIconSize(QSize(50, 50))
        lb0 = QLabel("الموجودات", self.con0)
        lb0.mousePressEvent = self.show_main
        b0.mousePressEvent = self.show_main
        self.con0.setFixedHeight(70)
        l0.addWidget(lb0)
        l0.addWidget(b0)
        layout.addWidget(self.con0)

        self.con1 = QFrame(self.menue)
        self.con1.setStyleSheet(Style.menue_item)
        l1 = QHBoxLayout(self.con1)
        l1.setContentsMargins(0,0,0,0)
        l1.setSpacing(0)
        b1 = QToolButton(self.con1)
        b1.setIcon(QIcon(":/img/cons.png"))
        b1.setIconSize(QSize(50, 50))
        lb1 = QLabel("المستهلكات", self.con1)
        lb1.mousePressEvent = self.show_cons
        b1.mousePressEvent = self.show_cons
        self.con1.setFixedHeight(70)
        l1.addWidget(lb1)
        l1.addWidget(b1)
        layout.addWidget(self.con1)

        self.con5 = QFrame(self.menue)        
        self.con5.setStyleSheet(Style.menue_item)
        l5 = QHBoxLayout(self.con5)
        l5.setContentsMargins(0, 0, 0, 0)
        l5.setSpacing(0)
        b5 = QToolButton(self.con5)
        b5.setIcon(QIcon(":/img/ruined.png"))
        b5.setIconSize(QSize(50, 50))
        lb5 = QLabel("المتلفات", self.con5)
        lb5.mousePressEvent = self.show_corr
        b5.mousePressEvent = self.show_corr
        self.con5.setFixedHeight(70)
        l5.addWidget(lb5)
        l5.addWidget(b5)
        layout.addWidget(self.con5)

        self.con2 = QFrame(self.menue)
        self.con2.setStyleSheet(Style.menue_item)
        l2 = QHBoxLayout(self.con2)
        l2.setContentsMargins(0,0,0,0)
        l2.setSpacing(0)
        b2 = QToolButton(self.con2)
        b2.setIcon(QIcon(":/img/buy.png"))
        b2.setIconSize(QSize(50, 50))
        lb2 = QLabel("المبيعات", self.con2)
        self.con2.setFixedHeight(70)
        lb2.mousePressEvent = self.show_sold
        b2.mousePressEvent = self.show_sold
        l2.addWidget(lb2)
        l2.addWidget(b2)
        layout.addWidget(self.con2)

        self.con3 = QFrame(self.menue)
        self.con3.setStyleSheet(Style.menue_item)
        l3 = QHBoxLayout(self.con3)
        l3.setContentsMargins(0,0,0,0)
        l3.setSpacing(0)
        b3 = QToolButton(self.con3)
        b3.setIcon(QIcon(":/img/report.png"))
        b3.setIconSize(QSize(50, 50))
        lb3 = QLabel("التقرير السنوي", self.con3)
        self.con3.setFixedHeight(70)
        lb3.mousePressEvent = self.report
        b3.mousePressEvent = self.report
        l3.addWidget(lb3)
        l3.addWidget(b3)
        layout.addWidget(self.con3)

        self.con4 = QFrame(self.menue)
        self.con4.setStyleSheet(Style.menue_item)
        l4 = QHBoxLayout(self.con4)
        l4.setContentsMargins(0,0,0,0)
        l4.setSpacing(0)
        b4 = QToolButton(self.con4)
        b4.setIcon(QIcon(":/img/excel.png"))
        b4.setIconSize(QSize(50, 50))
        lb4 = QLabel("استيراد اكسل", self.con4)
        self.con4.setFixedHeight(70)
        lb4.mousePressEvent = self.read
        b4.mousePressEvent = self.read
        l4.addWidget(lb4)
        l4.addWidget(b4)
        layout.addWidget(self.con4)
        
        self.con8 = QFrame(self.menue)
        self.con8.setStyleSheet(Style.menue_item)
        l8 = QHBoxLayout(self.con8)
        l8.setContentsMargins(0,0,0,0)
        l8.setSpacing(0)
        b8 = QToolButton(self.con8)
        b8.setIcon(QIcon(":/img/balance.png"))
        b8.setIconSize(QSize(50, 50))
        lb8 = QLabel("توليد رصيد", self.con8)
        self.con8.setFixedHeight(70)
        lb8.mousePressEvent = self.generate_balance
        b8.mousePressEvent = self.generate_balance
        l8.addWidget(lb8)
        l8.addWidget(b8)
        layout.addWidget(self.con8)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)
        
        self.con6 = QFrame(self.menue)
        self.con6.setStyleSheet(Style.contact)
        l6 = QHBoxLayout(self.con6)
        l6.setContentsMargins(10,0,0,0)
        l6.setSpacing(0)
        b6 = QToolButton(self.con6)
        b6.setIcon(QIcon(":/img/insta.png"))
        b6.setIconSize(QSize(50, 50))
        lb6 = QLabel("clic_kteam", self.con6)
        self.con6.setFixedHeight(30)
        l6.addWidget(b6)
        l6.addWidget(lb6)
        layout.addWidget(self.con6)
        
        self.con7 = QFrame(self.menue)
        self.con7.setStyleSheet(Style.contact)
        l7 = QHBoxLayout(self.con7)
        l7.setContentsMargins(10,0,0,20)
        l7.setSpacing(0)
        b7 = QToolButton(self.con7)
        b7.setIcon(QIcon(":/img/tele.png"))
        b7.setIconSize(QSize(50, 50))
        lb7 = QLabel("click_team_1", self.con7)
        self.con7.setFixedHeight(50)
        l7.addWidget(b7)
        l7.addWidget(lb7)
        layout.addWidget(self.con7)

        self.menue.setLayout(layout)

        self.menue.close()

        # close menue animation.
        self.animation2 = QPropertyAnimation(self.menue, b"maximumWidth")
        self.animation2.setDuration(370)
        self.animation2.setEndValue(0)
        self.animation2.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation2.finished.connect(self.menue.close)

        # show menue animation.
        self.animation = QPropertyAnimation(self.menue, b"minimumWidth")
        self.animation.setDuration(325)
        self.animation.setStartValue(0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # search button.
        button = QToolButton(self.lineEdit)
        button.setIcon(QIcon(":/img/search.png"))
        button.setIconSize(QSize(30, 30))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setStyleSheet("border: none; background: transparent;")
        self.lineEdit.setTextMargins(30, 0, 0, 0)
        self.lineEdit.returnPressed.connect(self.search)
        button.clicked.connect(self.search)
        self.lineEdit.focusInEvent = self.show_search

        # centering slctYr combo text.
        line_yr = ClickableLineEdit()
        self.slctYr.addItems(list(self.db.al.keys()))
        self.slctYr.setLineEdit(line_yr)
        self.slctYr.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.slctYr.setEditable(True)
        self.slctYr.currentIndexChanged.connect(self.change_year)
        self.slctYr.setCursor(Qt.CursorShape.PointingHandCursor)
        line_yr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line_yr.setReadOnly(True)
        self.slctYr.setItemDelegate(CenteredItemDelegate(self.slctYr))

        # adding items to departsLstVu.
        self.departsLstVu.addItems(self.db.repo)
        self.departsLstVu.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.departsLstVu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.departsLstVu.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        font = QFont("Noto Sans Arabic", 12)
        self.departsLstVu.setFont(font)
        self.departsLstVu.itemClicked.connect(self.departs)
        [self.departsLstVu.item(index).setTextAlignment(Qt.AlignmentFlag.AlignCenter) for index in range(self.departsLstVu.count())]

        # adding items to clasfLstVu.
        self.clasfLstVu.addItems(self.db.clas)
        self.clasfLstVu.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.clasfLstVu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.clasfLstVu.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.clasfLstVu.setFont(font)
        self.clasfLstVu.itemClicked.connect(self.classf)
        [self.clasfLstVu.item(index).setTextAlignment(Qt.AlignmentFlag.AlignCenter) for index in range(self.clasfLstVu.count())]
        self.clasfLstVu.setCurrentRow(0)

        self.departsLstVu.setStyleSheet(Style.lstStyle)
        self.clasfLstVu.setStyleSheet(Style.lstStyle)

        # set table model.
        #self.model = TableModel(data, self.tb_header)
        self.model = TableModel(self.db.al[self.slctYr.currentText()], self.tb_header, len(self.db.al[self.slctYr.currentText()]['الكل']), 19, self)
        self.table_view.setModel(self.model)


        # set table delegate.
        self.delegate = CustomDelegate(time.strftime("%Y-%m-%d"), self)
        self.table_view.setItemDelegate(self.delegate)
        # create completer for search box.
        #self.delegate.create_completer(self.lineEdit, 0)

        #self.open_editors()
        self.add_widgets()
        #self.table_view.edit(self.model.index(5, 12))


        # Right to Left Table Horizontal Scrolling.
        self.table_view.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.table_view.horizontalScrollBar().setInvertedAppearance(False)
        self.table_view.horizontalScrollBar().setInvertedControls(False)

        # scroll speed per pixle.
        self.table_view.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table_view.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)


        # disable vertical-horizontal bar.
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        #self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        #self.table_view.setShowGrid(False)
        #self.table_view.setVerticalScrollBar(QScrollBar(Qt.Orientation.Vertical))
        #self.table_view.verticalScrollBar().setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        #self.table_view.verticalScrollBar().setInvertedAppearance(False)

        # disable vertical header.
        self.table_view.verticalHeader().setVisible(False)

        # fix table header.
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # making rows-column resizable.
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table_view.setWordWrap(True)
        self.table_view.setStyleSheet(Style.tableStyle)
        self.table_view.setAlternatingRowColors(True)
        
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.right_click)


        self.no_result(False)
        self.hide_fields()
        self.table_view.setFocus()

    def generate_balance(self, a):
        self.show_menue(False)
        self.show_wait(True)
        dlg = BalanceDlg(self, self.db)
        dlg.show()
        
    
    def right_click(self, position: QPoint):
        index = self.table_view.indexAt(position)
        #print(index.row())
        menu = QMenu(self)
        menu.setStyleSheet(Style.right_click)
        
        minmaxtxt = "        تصغير الجدول" if self.is_max else "          تكبير الجدول"
        
        add_action    = QAction("            إضافة صف", self)
        delete_action = QAction("           حذف الصف", self)        
        edit_action   = QAction("          تعديل الصف", self)
        hide_action   = QAction("إضهار/إخفاء الأعمدة", self)
        export_action = QAction("                     اخراج", self)      
        max_action    = QAction(minmaxtxt, self)
              
        max_action.triggered.connect(self.maxi)
        delete_action.triggered.connect(lambda: self.delete_row(index))
        add_action.triggered.connect(self.add_row)
        edit_action.triggered.connect(lambda : self.edit_row(index))
        hide_action.triggered.connect(self.hide_fields_dlg)        
        export_action.triggered.connect(lambda: self.exprt(index))
        
        if self.x == 0 and index.isValid():
            add_action.setEnabled(True)
            edit_action.setEnabled(True)
            delete_action.setEnabled(True)
            export_action.setEnabled(True)
        else:    
            if self.x != 0:
                add_action.setEnabled(False)
                edit_action.setEnabled(False)
                delete_action.setEnabled(False)
                export_action.setEnabled(False)
        

        menu.addAction(add_action)
        menu.addAction(delete_action)
        menu.addAction(edit_action)
        menu.addAction(export_action)
        menu.addAction(max_action)
        menu.addAction(hide_action)
        
        menu.exec(self.table_view.viewport().mapToGlobal(position))

    def edit_row(self, index):
        if index.row() == 0 and self.departsLstVu.currentRow(): return
                    
        if not self.overlay:
            self.overlay = QWidget(self)
            self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 200);")
        self.overlay.setGeometry(self.rect())
        self.overlay.show()

        row = index.row() #selected[0].row()
        r = [self.model.data(self.model.index(row, col), Qt.ItemDataRole.DisplayRole) for col in range(0, 19)]
        dlg = AddDlg(self, row, r)
        dlg.show()

    def exprt(self, index):
        if index.row() == 0 and self.departsLstVu.currentRow(): return
    
        row = index.row() #selected[0].row()    
        self.delegate.export(row)
        self.table_view.clearSelection() 

    def hide_fields(self):
        ds = ""
        if self.x == 0: ds = "exist_cols"
        elif self.x == 1: ds = "cons_cols"
        elif self.x == 2: ds = "corr_cols"
        else: ds = "sold_cols"
        
        for i in range(self.model.cc):
            if i in self.pref[ds]:
                self.table_view.showColumn(i)
            else:
                self.table_view.hideColumn(i)
                   

    def hide_fields_dlg(self):
        if not self.overlay:
            self.overlay = QWidget(self)
            self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 200);")
        self.overlay.setGeometry(self.rect())
        self.overlay.show()       
        dlg = HideDlg(self)        
        dlg.exec()
        self.overlay.close()
        self.hide_fields()
        with open("prefrences.json", "w") as file:
            json.dump(self.pref, file, indent=4)

    def add_row(self):
        if not self.overlay:
            self.overlay = QWidget(self)
            self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 200);")
        self.overlay.setGeometry(self.rect())
        self.overlay.show()
        dlg = AddDlg(self)
        dlg.show()

    def maxi(self):
        if self.is_max:
            self.left_frame.show()
            self.head_frame.show()            
            self.horizontalLayout.insertItem(0, self.spacerItem)
            self.horizontalLayout.setStretch(0, 20)
        else:
            self.left_frame.hide()
            self.head_frame.hide()
            self.horizontalLayout.removeItem(self.spacerItem)            
        self.is_max = not self.is_max
        
    def delete_row(self, indx2):
        if indx2.row() == 0 and self.departsLstVu.currentRow(): return
   
        row = indx2.row() #selected[0].row()
        index = self.model.index(row, 0)
        cc = self.model.columnCount()
        d = [self.model.index(row, col).data() for col in range(cc)]
    
        self.delegate.delete(row, d)
        self.table_view.clearSelection()

    def paintEvent(self, event):
        painter = QPainter(self)
        window_height = self.height()
        r1_width = self.departsLstVu.width() * 0.55
        r2_width = self.width() - r1_width + 1
        pink_rect = QRect(0, 0, int(r1_width), window_height)
        painter.fillRect(pink_rect, QColor("#a17da4"))
        black_rect = QRect(int(r1_width), 0, int(r2_width), window_height)
        painter.fillRect(black_rect, QColor("#333333"))

    def open_editors(self):
        """Opening persistent editors so the user wouldn't have to click the cell to enable it delegate"""
        #pass
        for column in range(self.model.columnCount()):
            self.table_view.openPersistentEditor(self.model.index(0, column))
        #for row in range(self.model.rowCount()):
            #self.table_view.openPersistentEditor(self.model.index(row, 12))

    def add_widgets(self):
        indx = self.db.indcs[0]
        self.table_view.setIndexWidget(self.model.index(0, indx['seq']), self.delegate.add_row_btn(self))
        self.table_view.setIndexWidget(self.model.index(0, indx['bdate']), self.delegate.date_editor(self))
        self.table_view.setIndexWidget(self.model.index(0, indx['indate']),self.delegate.date_editor(self))
        self.table_view.setIndexWidget(self.model.index(0, indx['pdate']), self.delegate.date_editor(self))
        self.table_view.setIndexWidget(self.model.index(0, indx['edate']),self.delegate.date_editor(self))
        #self.table_view.setIndexWidget(self.model.index(0, 12), self.delegate.date_editor(self))

        for i in (1, 2, 3, 4, 5, 6, 7, 9, 13, 14, 17): # 11 was in the party.
            self.table_view.setIndexWidget(self.model.index(0, i), self.delegate.other_editors(self, self.model.index(0, i)))

    # called when everything is ready.
    def showEvent(self, event):
        self.resize_table()
        super().showEvent(event)

    # called when window is resized.
    def resizeEvent(self, event):
        self.resize_table()
        self.overlay.close()
        self.menue.close()
         
        self.scaled_pixmap = self.pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)  
        self.logo_label.resize(self.size())
        
        super().resizeEvent(event)

    def resize_table(self):
        total_width = self.table_view.viewport().width()
        total_height = self.table_view.viewport().height()
        self.table_view.horizontalHeader().setFixedHeight(max(int(total_height * 0.13), 55))
        self.table_view.horizontalHeader().setDefaultSectionSize(max(int(total_width * 0.2), 140))
        self.table_view.verticalHeader().setMinimumSectionSize(max(int(total_height * 0.13), 55))

        table_rect = self.table_view.viewport().geometry()
        center_x = table_rect.x() + total_width * 0.85
        center_y = table_rect.y() + total_height * 0.5
        self.nr_label.move(int(center_x), int(center_y))

        self.wait_label.move((self.width() - self.wait_label.width()) // 2, (self.height() - self.wait_label.height()) // 2)

    def no_result(self, t):
        if t:
            if self.model.rc > 0:
                self.nr_label.close()
            else:
                self.nr_label.show()
        else:
            if self.model.rc > 1:
                self.nr_label.close()
            else:
                self.nr_label.show()

    def departs(self, item):
        self.lineEdit.setText("")
        self.delegate.btn = True
        self.model.beginResetModel() 
        self.label.setText(item.text())
        self.model._data = self.db.data[self.slctYr.currentText()]
        self.model.k = item.text()
        self.model.rc = len(self.db.data[self.slctYr.currentText()][item.text()])
        #print(self.model.rc)
        self.table_view.showColumn(11)
        self.table_view.showColumn(12)
        self.model.endResetModel()
        # if the view is showing cons,corr, sold it will not hide r0.
        if self.x != 0:
            return
        if not self.departsLstVu.currentRow():
            self.table_view.showRow(0)
            self.table_view.hideColumn(11)
            self.table_view.hideColumn(12)
            self.add_widgets()
        else:
            self.table_view.hideRow(0)
        self.no_result(False)
        self.hide_fields()

    def classf(self, item):
        self.lineEdit.setText("")
        self.delegate.btn = False
        self.model.beginResetModel()
        self.model._data = self.db.data[self.slctYr.currentText()]
        self.model.k = item.text()
        self.model.rc = len(self.db.data[self.slctYr.currentText()][item.text()])
        self.table_view.showColumn(11)
        self.table_view.showColumn(12)
        self.model.endResetModel()
        if not self.clasfLstVu.currentRow():
            self.label.setText(item.text())
        if self.x == 0:
            self.table_view.showRow(0)
            self.add_widgets()
            if self.clasfLstVu.currentRow():
                self.table_view.indexWidget(self.model.index(0, 13)).setText(item.text())
        self.no_result(False)
        self.hide_fields()

    def change_year(self):
        if self.slctYr.currentIndex() == -1:
            return
        self.clasfLstVu.setCurrentRow(0)
        self.clasfLstVu.itemClicked.emit(self.clasfLstVu.item(0))

    def show_menue(self, a):
        if self.menue.isVisible():
            self.overlay.close()
            self.logo_label.close()
            self.menue.setMinimumWidth(0)
            self.animation2.setStartValue(self.width() * 0.27)
            self.animation2.start()
        else:
            self.overlay.setGeometry(QRect(0, 0, self.width(), self.height()))
            self.menue.setMinimumWidth(0)
            self.menue.setMaximumWidth(0)
            self.overlay.show()
            self.menue.show()
            self.logo_label.show()
            self.menue.setFixedHeight(self.height())
            self.animation.setEndValue(self.width() * 0.27)
            self.animation.start()

    def show_corr(self, f):
        self.mnu_slct_style(self.con5)
        self.show_menue(False)
        self.x = 2
        self.db.data = self.db.corr
        self.delegate.cons = False
        self.lineEdit.setText("")
        self.slctYr.clear()
        self.slctYr.addItems(list(self.db.corr.keys()))
        self.slctYr.setCurrentIndex(0)
        self.label.setText("المتلفات")
        
        self.model.beginResetModel()
        self.table_view.showRow(0)
        self.model.k = 'الكل'
        self.model._data = self.db.corr[self.slctYr.currentText()]
        self.model._headers = self.corr_head
        self.model.rc = len(self.db.corr[self.slctYr.currentText()]['الكل'])
        self.model.cc = 22
        self.model.endResetModel()
        self.hide_fields()
        self.no_result(True)
        self.table_view.setFocus()

    def show_sold(self, f):
        self.mnu_slct_style(self.con2)
        self.show_menue(False)
        self.x = 3
        self.db.data = self.db.sold
        self.delegate.cons = False
        self.lineEdit.setText("")
        self.slctYr.clear()
        self.slctYr.addItems(list(self.db.sold.keys()))
        self.slctYr.setCurrentIndex(0)
        self.label.setText('المبيعات')

        self.model.beginResetModel()
        self.table_view.showRow(0)
        self.model.k = 'الكل'
        self.model._data = self.db.sold[self.slctYr.currentText()]
        self.model._headers = self.sold_head
        self.model.rc = len(self.db.sold[self.slctYr.currentText()]['الكل'])
        self.model.cc = 29
        self.model.endResetModel()
        self.hide_fields()
        self.no_result(True)
        self.table_view.setFocus()

    def show_cons(self, f):
        self.mnu_slct_style(self.con1)
        self.show_menue(False)
        self.x = 1
        self.db.data = self.db.cons
        self.delegate.cons = True

        self.lineEdit.setText("")
        self.slctYr.clear()
        self.slctYr.addItems(list(self.db.cons.keys()))
        self.slctYr.setCurrentIndex(0)
        self.label.setText('المستهلكات')

        self.model.beginResetModel()
        self.table_view.showRow(0)
        self.model.k = 'الكل'
        self.model._data = self.db.cons[self.slctYr.currentText()]
        self.model._headers = self.cons_head
        self.model.rc = len(self.db.cons[self.slctYr.currentText()]['الكل'])
        self.model.cc = 25
        self.model.endResetModel()
        self.hide_fields()
        self.no_result(True)
        self.table_view.setFocus()

    def show_main(self, f):
        self.mnu_slct_style(self.con0)
        self.show_menue(False)
        self.x = 0
        self.db.data = self.db.al
        self.delegate.cons = False
        self.lineEdit.setText("")
        self.slctYr.clear()
        self.slctYr.addItems(list(self.db.al.keys()))
        self.slctYr.setCurrentIndex(0)
        self.label.setText('الكل')

        self.model.beginResetModel()
        self.model.k = 'الكل'
        self.model._data = self.db.al[self.slctYr.currentText()]
        self.model._headers = self.tb_header
        self.model.rc = len(self.db.al[self.slctYr.currentText()]['الكل'])
        self.model.cc = 19
        self.model.endResetModel()
        self.hide_fields()
        self.add_widgets()
        self.no_result(False)
        self.table_view.setFocus()

    def search_type(self, v):
        for i in self.db.emp.keys():
            if i == v:
                return 1
        for i in self.db.mat.keys():
            if i == v:
                return 2
        for i in self.db.origin.keys():
            if i == v:
                return 4
        return 3

    def show_search(self, e):
        if self.srch:
            QLineEdit.focusInEvent(self.lineEdit, e)
            return
        self.srch = True
        self.delegate.show_wait()
        geo = self.lineEdit.geometry()
        self.srch_pos = self.head_frame.mapToGlobal(self.lineEdit.pos())
        self.lineEdit.setParent(self)
        self.delegate.create_completer(self.lineEdit, self.db.mat)
        self.lineEdit.move(self.mapFromGlobal(self.srch_pos))
        self.lineEdit.show()
        self.lineEdit.raise_()
        self.lineEdit.setFocus()  
        self.delegate.overlay.mousePressEvent = self.hide_search
        QLineEdit.focusInEvent(self.lineEdit, e)
        if not self.srch_frame or not self.srch_frame.isVisible(): self.show_srch_frame()
        
       
    def show_srch_frame(self):
        c_style = """
            QFrame{
                border: 0px solid black;
            }
            QLabel{
                font-family: Noto Sans Arabic;
                font-size: 22px;
                color: white;
            }
        """
        self.srch_frame = QFrame(self)
        self.srch_frame.setStyleSheet(c_style)
        c_layout = QHBoxLayout(self.srch_frame)
        c_txt = QLabel("أختر الحقل الذي تريد البحث فيه: ")
        c_txt.adjustSize()
        
        
        c_combo = QComboBox()
        c_combo.setFixedHeight(40)
        c_combo.setStyleSheet(Style.srch_combo)
        
        c_line = ClickableLineEdit()
        c_combo.addItems(self.model._headers)
        c_combo.setLineEdit(c_line)
        c_combo.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        c_combo.setEditable(True)
        c_combo.setView(QListView())
        c_combo.setCurrentIndex(self.srch_fld if self.srch_fld else 2)
        c_combo.currentIndexChanged.connect(self.change_fld)
        c_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        c_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        c_line.setReadOnly(True)
        c_combo.setItemDelegate(CenteredItemDelegate(c_combo))
        
        
        c_layout.addWidget(c_combo)
        c_layout.addWidget(c_txt)
        self.srch_frame.show()
        geo = self.lineEdit.geometry()
        self.srch_frame.setGeometry(geo.x(), geo.y() + 100, geo.width(), geo.height()+10)
    
    
    def hide_search(self, e):
        self.srch = False
        self.delegate.overlay.mousePressEvent = None
        self.lineEdit.setParent(self.head_frame)
        self.lineEdit.move(self.head_frame.mapFromGlobal(self.srch_pos))
        self.lineEdit.show()
        self.delegate.overlay.close()
        self.srch_frame.hide()


    def change_fld(self, cid):
        indx = self.db.indcs[self.x]
        self.srch_fld = cid
        
        if indx['emp'] == cid : self.delegate.create_completer(self.lineEdit, self.db.emp)
        elif indx['mat'] == cid : self.delegate.create_completer(self.lineEdit, self.db.mat)
        elif indx['origin'] == cid : self.delegate.create_completer(self.lineEdit, self.db.origin)
        elif indx['clas'] == cid : self.delegate.create_completer(self.lineEdit, self.db.clas)
        elif indx['repo'] == cid : self.delegate.create_completer(self.lineEdit, self.db.repo)
        elif indx['prepo'] == cid : self.delegate.create_completer(self.lineEdit, self.db.repo)
        elif indx['corp'] == cid : self.delegate.create_completer(self.lineEdit, self.db.corp)
        else: self.lineEdit.setCompleter(None)       

    def search(self):
        if not self.srch: return
        
        value = self.lineEdit.text()
        if not value: return
        self.hide_search(None)
        t = self.srch_fld
        self.model._data['srch'] = []
        for i in range(0, len(self.model._data['e'])):
            if self.model._data['e'][i][t] == value:
                self.model._data['srch'].append(i)
        self.model.beginResetModel()
        self.model.k = 'srch'
        self.model.rc = len(self.model._data['srch'])
        self.model.endResetModel()
        self.no_result(True)

    def report(self, a):
        self.show_menue(False)
        self.show_wait(True)
        dlg = ReportDlg(self, self.db)
        dlg.show()
        

    def read(self, a):
        self.show_menue(a)
        import readxl
        try:
            if self.x == 0:
                file_path, _ = QFileDialog.getOpenFileName(self, "اختر ملف اكسل للموجودات", "", "Excel Files (*.xlsx)")
                self.show_wait(True)
                rt  = readxl.read_ex(self.db, file_path)
            elif self.x == 1:
                file_path, _ = QFileDialog.getOpenFileName(self, "اختر ملف اكسل للمستهلكات", "", "Excel Files (*.xlsx)")
                self.show_wait(True)
                rt  = readxl.read_cons(self.db, file_path)
            elif self.x == 2:
                file_path, _ = QFileDialog.getOpenFileName(self, "اختر ملف اكسل للمتلفات", "", "Excel Files (*.xlsx)")
                self.show_wait(True)
                rt  = readxl.read_corr(self.db, file_path)
            else:
                file_path, _ = QFileDialog.getOpenFileName(self, "اختر ملف اكسل للمبيعات", "", "Excel Files (*.xlsx)")
                self.show_wait(True)
                rt  = readxl.read_sold(self.db, file_path)
                #self.delegate.show_popup(0, readxl.read_sold(self.db, file_path))            
            
            nw = MainWindow()                
            self.delegate.show_popup(0, rt)
            if (rt == "تم الأستيراد بنجاح"):
                self.log("read "+str(self.x)+" > "+str(file_path))
                nw.showMaximized()
                self.close()
                self.__class__.current_window = nw
        except Exception as e:
            logging.error("import xls error -> " + traceback.format_exc())
            self.delegate.show_popup(0, "حدث خطأ أعد المحاولة!")

        self.show_wait(False)

    def log(self, m, t=False):
        if t:
        	logging.error(m)
        else:
    	    logging.warning(m)

    def mnu_slct_style(self, x):
        for i in (self.con0, self.con1, self.con2, self.con3, self.con4, self.con5):
            if i is x:
                i.setStyleSheet(Style.menue_item_slctd)
            else:
                i.setStyleSheet(Style.menue_item)

    def show_wait(self, c):
        if c:
            if not self.overlay:
                self.overlay = QWidget(self)
                self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 200);")
            self.overlay.setGeometry(self.rect())
            self.overlay.show()
            self.wait_label.show()
            self.wait_label.repaint()
            self.overlay.repaint()
        else:
            self.wait_label.close()
            self.overlay.close()

    def closeEvent(self, event):
        logging.info("app closed")
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/img/icon.png"))
		
    font_id = QFontDatabase.addApplicationFont("Noto.ttf")
    if font_id == -1:
        print("failed to load ")
        logging.error("failed to load font")
    else:
        1==1
        #families = QFontDatabase.applicationFontFamilies(font_id)


    window = MainWindow()
    window.showMaximized()
    app.exec()


if __name__ == '__main__':
    main()
