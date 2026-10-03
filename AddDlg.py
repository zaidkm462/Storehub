from PyQt6.QtWidgets import (
	QDialog, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
	QPushButton, QSpacerItem, QSizePolicy, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
import Style
import traceback



class AddDlg(QDialog):
	def __init__(self, parent, r=0, vals=[]):
		super().__init__()
		self.parent = parent
		self.overlay = None
		self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
		self.edtrs = []
		self.row = r
		self.vals = vals
		
		self.style = """
	   QLineEdit{
		   padding: 10px;
		   font-size: 22px;
	   }
	   QPushButton{
			background-color: #a17daf;
			border: none;رقر
			color: white;
			font-size: 22px;
			font-family: Noto Sans Arabic;
			margin-left: 50px;
			margin-right: 50px;
		}"""
		
		# main frame horizontal.
		self.frame = QFrame(parent=self)
		self.horizontalLayout = QHBoxLayout(self.frame)
		self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
		self.horizontalLayout.setSpacing(15)

		# left frame vertical.
		self.frame_1 = QFrame(parent=self.frame)
		self.frame_1.setStyleSheet(self.style)
		self.verticalLayout_1 = QVBoxLayout(self.frame_1)
		self.verticalLayout_1.setContentsMargins(5, 5, 5, 5)
		self.verticalLayout_1.setSpacing(15)
		
		# right frame vertical.
		self.frame_2 = QFrame(parent=self.frame)
		self.frame_2.setStyleSheet(self.style)
		self.verticalLayout_2 = QVBoxLayout(self.frame_2)
		self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
		self.verticalLayout_2.setSpacing(15)
		
		emp_edtr = self.other_editors(parent, 1)
		mat_edtr = self.other_editors(parent, 2)
		
		serial_edtr = self.other_editors(parent, 3)
		origin_edtr = self.other_editors(parent, 4)
		
		price_edtr = self.other_editors(parent, 5)
		quant_edtr = self.other_editors(parent, 6)
		
		hprice_edtr = self.other_editors(parent, 7)
		bdate_edtr = self.date_editor(parent)
		bdate_edtr.setText("اختر تاريخ الشراء")
		
		indoc_edtr = self.other_editors(parent, 9)
		indate_edtr = self.date_editor(parent)
		indate_edtr.setText("اختر تاريخ مستند الادخال")
		
		clas_edtr = self.other_editors(parent, 13)
		corp_edtr = self.other_editors(parent, 14)
		
		prodate_edtr = self.date_editor(parent)
		expdate_edtr = self.date_editor(parent)
		prodate_edtr.setText("اختر تاريخ الانتاج (اختياري)")
		expdate_edtr.setText("اختر تاريخ الانتهاء (اختياري)")
		
		prevrepo_edtr = self.other_editors(parent, 17)
		#for i in range(len(vals)): print(i, vals[i])
		self.edtrs = [emp_edtr, mat_edtr, serial_edtr, origin_edtr, price_edtr,quant_edtr, hprice_edtr, bdate_edtr, indoc_edtr, indate_edtr, clas_edtr, corp_edtr, prodate_edtr, expdate_edtr, prevrepo_edtr]
		
		if vals:
			vind = list(range(len(vals)))
			del vind[18]
			del vind[12]
			del vind[11]
			del vind[0]
			for i, j in enumerate(vind):
				if vals[j] or vals[j] == 0: self.edtrs[i].setText(str(vals[j]))
		
		self.verticalLayout_2.addWidget(emp_edtr)
		self.verticalLayout_1.addWidget(mat_edtr)
		
		self.verticalLayout_2.addWidget(serial_edtr)
		self.verticalLayout_1.addWidget(origin_edtr)
		
		self.verticalLayout_2.addWidget(price_edtr)
		self.verticalLayout_1.addWidget(quant_edtr)
		
		self.verticalLayout_2.addWidget(bdate_edtr)
		self.verticalLayout_1.addWidget(hprice_edtr)
		
		self.verticalLayout_2.addWidget(indoc_edtr)
		self.verticalLayout_1.addWidget(indate_edtr)
			   
		self.verticalLayout_2.addWidget(clas_edtr)
		self.verticalLayout_1.addWidget(corp_edtr)
			 
		self.verticalLayout_2.addWidget(prodate_edtr)
		self.verticalLayout_1.addWidget(expdate_edtr)
		
		self.verticalLayout_2.addWidget(prevrepo_edtr)

		self.btn1 = QPushButton("الغاء")
		self.btn1.clicked.connect(self.dispoze)  # just for close the message box.
		self.btn1.setFixedHeight(53)
		#self.btn1.setFixedWidth(220)

		self.btn2 = QPushButton("تم")
		self.btn2.clicked.connect(self.done_press)  # just for close the message box.
		self.btn2.setFixedHeight(53)
		
		self.btn1.setCursor(Qt.CursorShape.PointingHandCursor)
		self.btn2.setCursor(Qt.CursorShape.PointingHandCursor)
		self.horizontalLayout.addWidget(self.frame_1)
		self.horizontalLayout.addWidget(self.frame_2)

		spacerItem = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		self.verticalLayout_1.addItem(spacerItem)
		
		
		self.verticalLayout_1.addWidget(self.btn1)
		self.verticalLayout_2.addWidget(self.btn2)


		self.setLayout(self.horizontalLayout)
		self.setStyleSheet(Style.dlg_Style)
		self.resize(650, 0)


	def auto(self):
		p = self.edtrs[4].text()
		q = self.edtrs[5].text()
		p = int(p) if p.isdigit() else 0
		q = int(q) if q.isdigit() else 0
		self.edtrs[6].setText(str(p*q))

	def dispoze(self):
		self.setParent(None)
		self.close()
		self.parent.overlay.close()

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
		elif c == indx['prepo']:
			self.parent.delegate.create_completer(editor, self.parent.db.repo.keys())
		return editor


	def date_editor(self, parent):
		editor = QLineEdit(parent)
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
		r = [self.vals[0] if self.vals else 0]
		for i in self.edtrs: r.append(i.text())
		r.insert(11, self.vals[11] if self.vals else "")
		r.insert(12, self.vals[12] if self.vals else "")
		r.append(self.vals[18] if self.vals else "المخزن الرئيسي")
		
		
		# Check for accurate input.
		for i in range(1, 18):
			# opt dates.
			if i in (indx['pdate'], indx['edate']) and not r[i][0].isdigit(): r[i] = ""
			
			# opt others.
			elif i in (indx['serial'], indx['corp'], indx['prepo'], indx['outdoc'], indx['outdate']): continue
			
			# dates.
			elif i in (indx['bdate'], indx['indate']) and not r[i][0].isdigit():
				self.hide()
				self.parent.delegate.show_popup(0, "يرجى ادخال تاريخ الشراء والادخال.")
				self.show()
			
			# digits.
			elif i in (indx['price'], indx['quant'], indx['hprice'], indx['indoc']):
				if not r[i].isdigit():
					self.hide()
					self.parent.delegate.show_popup(0, "يرجى ادخال رقم للسعر والكمية والمستند.")
					self.show()
					return False
				else: r[i] = int(r[i])			
			
			# non-empty.
			elif r[i] == "": 
				self.hide()
				self.parent.delegate.show_popup(0)
				self.show()
				return False


		if not self.vals: self.parent.delegate.add(r, self)
		else:
			if self.vals[10][:4] != r[10][:4]: move = 2
			elif self.vals[13] != r[13]: move = 1
			else: move = 0
			try:
				if self.parent.db.check_integrity(0, str(r[9]), str(r[10])):
					self.parent.delegate.edit(self.row, r, self.vals, move)
					self.hide()
					self.parent.delegate.show_popup(0, "تم تعديل العنصر")
					self.dispoze()
				else:
					self.hide()		
					self.parent.delegate.show_popup(0, "رقم مستند الادخال وتاريخ المستند يجب أن يكون فريدا!")
					self.dispoze()
			except Exception as e:				
				self.hide()
				self.parent.delegate.show_popup(0, "حدث خطأ لايمكن تعديل العنصر!")
				self.show()
				self.parent.log(traceback.format_exc(), True)
