from PyQt6.QtCore import Qt, QRect, QSize, QStringListModel
from PyQt6.QtGui import QCursor, QIcon, QPen, QBrush, QPainter, QColor, QAction, QTextCharFormat
from PyQt6.QtWidgets import QApplication, QStyledItemDelegate, QWidget, QHBoxLayout, QPushButton, QLineEdit, QCompleter, QSizePolicy, \
	QCalendarWidget, QToolButton, QMessageBox, QVBoxLayout, QLabel, QDialog, QFrame, QSpacerItem, QButtonGroup, \
	QRadioButton, QComboBox, QFileDialog
import Style
from report import generate
import traceback
from ExportDlg import ExportDlg
from SellDlg import SellDlg
from MissingDlg import MissingDlg

class CustomDelegate(QStyledItemDelegate):
	def __init__(self, date, parent):
		super().__init__(parent)
		self.parent = parent
		self.date = date
		self.overlay = None
		self.calendar_widget = None
		self.placeholders = [
			"",
			"ادخل اسم الموظف",
			"ادخل اسم المادة",
			"الرقم التسلسلي (اختياري)",
			"ادخل المنشأ الصناعي",
			"ادخل سعر المفرد",
			"ادخل الكمية",
			"ادخل السعر الكلي",
			"ادخل تاريخ الشراء",
			"ادخل رقم مستند الادخال",
			"ادخل تاريخ مستند الادخال",
			" رقم مستند الاخراج",
			"ادخل ناريخ مستند الاخراج",
			"ادخل التصنيف",
			"ادخل الشركة المصنعة (اختياري)",
			"ادخل تاريخ الانتاح (اختياري)",
			"ادخل تاريخ الانتهاء (اختياري)",
			"ادخل  المخزن السابق (اختياري)",
			
		]
		self.cons = False
		self.btn = False
		self.ref_model = True


	def paint(self, painter, option, index):
		if index.column() == 18 and not self.parent.x and (self.btn or index.model().data(index, Qt.ItemDataRole.EditRole) == "المخزن الرئيسي"):
			background_color = QColor("#a17da4")
			text_color = QColor("#f0f0f0")
			# draw a rectangle
			painter.save()
			painter.setRenderHint(QPainter.RenderHint.Antialiasing)
			rect = option.rect.adjusted(12, 12, -12, -12)  # margins
			painter.setBrush(QBrush(background_color))  # background
			painter.setPen(QPen(QColor("#e0dede"), 2)) # borders #if self.pressed_index else QPen(Qt.PenStyle.NoPen)
			painter.drawRect(rect)
			# draw text
			painter.setPen(QPen(text_color))
			painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "اخراج")
			painter.restore()
			# redrawing the cell -since paint will override it-
			#painter.setPen(QPen(QColor("#a17da4"), 0))
			#painter.drawRect(option.rect)'''
		elif index.column() == 24 and self.cons:
			background_color = QColor("#a17da4")
			text_color = QColor("#f0f0f0")
			# draw a rectangle
			painter.save()
			painter.setRenderHint(QPainter.RenderHint.Antialiasing)
			rect = option.rect.adjusted(12, 12, -12, -12)  # margins
			painter.setBrush(QBrush(background_color))  # background
			painter.setPen(QPen(QColor("#e0dede"), 2))  # borders
			painter.drawRect(rect)
			# draw text
			painter.setPen(QPen(text_color))
			painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "بيع")
			painter.restore()
		else:
			super().paint(painter, option, index)

	def editorEvent(self, event, model, option, index):
		"""called whenever cell is clicked"""
		if event.type() == event.Type.HoverEnter:
			print("Hover started")
		elif event.type() == event.Type.HoverLeave:
			print("Hover left")
		elif index.column() == self.parent.db.indcs[0]['repo'] and (self.btn or index.model().data(index, Qt.ItemDataRole.EditRole) == "المخزن الرئيسي"):
			if event.type() == event.Type.MouseButtonPress and option.rect.contains(event.pos()):
			   self.export(index.row())
			   return True
			'''elif event.type() == event.Type.MouseButtonRelease:
				if self.pressed_index == index and option.rect.contains(event.pos()):
					self.pressed_index = None
					return True'''
		elif index.column() == self.parent.db.indcs[1]['sell'] and self.cons:
			if event.type() == event.Type.MouseButtonPress and option.rect.contains(event.pos()):
				self.sell(index.row())
				return True
		return False

	'''def createEditor(self, parent, option, index):
		return super().createEditor(parent, option, index)
		print('hi')
		value = index.model().data(index, Qt.ItemDataRole.EditRole)
		if index.column() == 12:
			#if value == "" or value == "اخراج":
				#return Editors.export_btn(parent)
			return None
		if index.row() == 0 and not value:
			if index.column() == 0:
				return self.add_row_btn(parent)
			if index.column() == 8 or index.column() == 10:
				return self.date_editor(parent)
			else:
				return self.other_editors(parent, index)
		return super().createEditor(parent, option, index)'''

	def setEditorData(self, editor, index):
		pass
		'''if index.row() == 0 and isinstance(editor, QLineEdit):
			value = index.model().data(index, Qt.ItemDataRole.EditRole)
			#editor.setText(value)
		else:
			pass #super().setEditorData(editor, index)'''

	def setModelData(self, editor, model, index):
		pass
		'''if index.row() == 0 and isinstance(editor, QLineEdit) :
			model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)
		else:
			super().setModelData(editor, model, index)'''

	# show completer without typing.
	'''def on_editor_click(self, editor):
		def show_completer(event):
			editor.completer().complete()  #show suggestions.
			QLineEdit.mousePressEvent(editor, event)
		return show_completer'''

	def add_row_btn(self, parent):
		editor = QWidget(parent)
		editor.setStyleSheet("background-color: #f0f0f0;")
		layout = QHBoxLayout(editor)
		layout.setContentsMargins(10, 10, 10, 10)
		button = QPushButton("اضافة صف")
		button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		button.setStyleSheet(Style.add_btn_Style)
		button.clicked.connect(self.add)
		layout.addWidget(button)
		return editor

	def date_editor(self, parent):
		editor = QLineEdit(parent)
		editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
		icon = QIcon(":/img/dd.png")
		action = QAction(editor)
		action.setIcon(QIcon(icon))
		editor.addAction(action, QLineEdit.ActionPosition.LeadingPosition)
		action.triggered.connect(lambda: self.show_calendar(editor))
		editor.mousePressEvent = lambda event: self.show_calendar(editor)
		editor.setStyleSheet(Style.date_editor_style)
		editor.setReadOnly(True)
		#editor.setText(f"{current_time.tm_year}-{current_time.tm_mon:02d}-{current_time.tm_mday:02d}")
		editor.setText(self.date)
		return editor

	def other_editors(self, parent, index):
		indx = self.parent.db.indcs[0]
		editor = QLineEdit(parent)
		#editor.setText('000')
		editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
		editor.setStyleSheet(Style.editor_style)
		editor.setPlaceholderText(self.placeholders[index.column()])

		if index.column() == indx['price']:
			editor.textChanged.connect(self.auto)
		elif index.column() == indx['quant']:
			editor.textChanged.connect(self.auto)

		if index.column() == indx['emp']:
			self.create_completer(editor, self.parent.db.emp.keys())
		elif index.column() == indx['mat']:
			self.create_completer(editor, self.parent.db.mat.keys())
		elif index.column() == indx['origin']:
			self.create_completer(editor, self.parent.db.origin.keys())
		elif index.column() == indx['clas']:
			self.create_completer(editor, self.parent.db.clas.keys())
		elif index.column() == indx['corp']:
			self.create_completer(editor, self.parent.db.corp.keys())
		elif index.column() == indx['prepo']:
			self.create_completer(editor, self.parent.db.repo.keys())
		return editor

	def show_calendar(self, editor, o=True):
		editor.deselect()
		if self.calendar_widget:
			self.calendar_widget.close()
		self.calendar_widget = QCalendarWidget()
		self.calendar_widget.setWindowFlags(Qt.WindowType.Popup)
		self.calendar_widget.setGridVisible(True)
		pos = QCursor.pos() # calender position.
		self.calendar_widget.setGeometry(QRect(pos.x(), pos.y(), 350, 220))
		self.calendar_widget.show()
		self.calendar_widget.clicked.connect(lambda date: self.update_date(editor, date, o))
		self.calendar_widget.setStyleSheet(Style.calender_style)
		self.calendar_widget.findChild(QToolButton, "qt_calendar_prevmonth").setIcon(QIcon(":/img/lar.png"))
		self.calendar_widget.findChild(QToolButton, "qt_calendar_nextmonth").setIcon(QIcon(":/img/rar.png"))
		day_format = QTextCharFormat()
		day_format.setBackground(QColor("#f0f0f0"))  # background.
		day_format.setForeground(QColor("black"))  # text-color.
		self.calendar_widget.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
		[self.calendar_widget.setWeekdayTextFormat(Qt.DayOfWeek(day), day_format) for day in range(1, 8)]

	def update_date(self, editor, date, o=True):
		editor.setText(date.toString("yyyy-MM-dd"))
		if editor.parent().objectName():
			editor.setStyleSheet(Style.editor_style if o else """
		QLineEdit{
			border: 3px solid #a17da4;
			font-family: Noto Sans Ararbic;
			font-size: 16px;
		}	   
		""")
		else:
			editor.setStyleSheet(Style.date_editor2_style if o else """
		QLineEdit{
			border: 3px solid #a17da4;
			font-family: Noto Sans Ararbic;
			font-size: 16px;
			color: #333;
		}	   
		""")
		self.calendar_widget.close()

	def create_completer(self, editor, l):		
		completer = QCompleter(l) 
		#completer = QCompleter(list(self.parent.db.emp.keys())+list(self.parent.db.mat.keys())+list(self.parent.db.origin.keys())+list(self.parent.db.clas.keys()))
		completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
		#editor.mousePressEvent = self.on_editor_click(editor) # show completer without typing.
		completer.popup().setStyleSheet(Style.cmpltr_style)
		editor.setCompleter(completer)
		completer.popup().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		completer.popup().setLayoutDirection(Qt.LayoutDirection.RightToLeft)
		completer.popup().setMinimumWidth(150)
		completer.popup().setWordWrap(True)
	
	def show_popup(self, n, t=None):
		# default popup show and hide the overlay.
		if n == 0:
			self.show_wait()
			dialog = CustomDialog(self.parent, t)
			dialog.exec()
			self.overlay.close()
		# called by another dialog.
		elif n == 1:
			dialog = CustomDialog(self.parent, t)
			dialog.exec()
		# sell dialog.
		elif n == 3:
			self.show_wait()
			dialog = SellDlg(self)
			dialog.exec()
			self.overlay.close()
		# 2 for export dialog.
		else:
			self.show_wait()
			dialog = ExportDlg(self)
			dialog.exec()
			self.overlay.close()
		#dialog_rect = dialog.geometry()
		#dialog_rect.moveCenter(self.parent.geometry().center())
		#dialog.move(dialog_rect.topLeft())

	def show_wait(self):
		if not self.overlay:
			self.overlay = QWidget(self.parent)
			self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 200);")
		self.overlay.setGeometry(self.parent.rect())
		self.overlay.show()


	def check_row0(self):
		indx = self.parent.db.indcs[0]
		r = [None] * 18
		r.append("المخزن الرئيسي")
		r.append(1)
		
		a = [i for i in self.parent.pref['exist_cols'] if i not in (0, 11, 12, 18)]
		b = [i for i in range(1, 18) if i not in a and i not in (11, 12)]
		
		# Check for accurate input.
		for i in a:
			r[i] = self.parent.table_view.indexWidget(self.parent.model.index(0, i)).text()
			if i in (indx['serial'], indx['outdate'], indx['corp'], indx['pdate'], indx['edate'], indx['prepo']):
				continue		   
			elif r[i] == '':
				self.show_popup(0)
				return False
			if i in (indx['price'], indx['quant'], indx['hprice'], indx['indoc']):
				if not r[i].isdigit():
					self.show_popup(0, "يرجى ادخال رقم للسعر والكمية والمستند.")
					return False
				r[i] = int(r[i])
		if not b: return r
		
		self.show_wait()
		dlg = MissingDlg(self.parent, b, r)
		dlg.exec()
		self.overlay.close()
		if not dlg.clean: return False
		else:			
			r = dlg.r
			return r

	def up_clas_repo(self, clas, repo):	#View.
		# if there is new clas, repo > it will be added to view.
		if not clas in self.parent.db.clas.keys():
			self.parent.clasfLstVu.addItem(clas)
			self.parent.clasfLstVu.item(self.parent.clasfLstVu.count()-1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
		if not repo in self.parent.db.repo.keys():
			self.parent.departsLstVu.addItem(repo)
			self.parent.departsLstVu.item(self.parent.departsLstVu.count()-1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

	def clas_eq_repo(self, clas, repo):
		if clas == repo:
			return True
		if clas in self.parent.db.repo.keys():
			return True
		if repo in self.parent.db.clas.keys():
			return True
		return False

	def new_year(self, year, o):
		if o == 0:
			d = self.parent.db.al
		elif o == 1:
			d = self.parent.db.cons
		elif o == 2:
			d = self.parent.db.corr
		else:
			d = self.parent.db.sold
		if not year in list(d.keys()):
			self.parent.slctYr.addItem(year)
			e = [] if o else [('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'المخزن الرئيسي', '')] 
			d[year] = {"e": e, "srch":[]}
			#self.parent.db.al[r[10][:4]]["الكل"].append()
			for j in self.parent.db.repo.keys():
				d[year][j] = [] if o else [0]
			for j in self.parent.db.clas.keys():
				d[year][j] = [] if o else [0]

	def sim_lst_click(self):
		# simulation a click to update the view.
		if self.parent.departsLstVu.currentRow() > -1:
			self.parent.departsLstVu.itemClicked.emit(self.parent.departsLstVu.item(self.parent.departsLstVu.currentRow()))
		elif self.parent.clasfLstVu.currentRow() > -1:
			self.parent.clasfLstVu.itemClicked.emit(self.parent.clasfLstVu.item(self.parent.clasfLstVu.currentRow()))


	def add(self, r=None, o=None):
		indx  = self.parent.db.indcs[0]
		
		# check if the adding through add or export button.
		if not r:
			r  = self.check_row0()
			if not r:
				return

		# insert into db.
		r[0] = self.parent.db.last + 1
		if self.clas_eq_repo(r[indx['clas']], r[indx['repo']]) or self.clas_eq_repo(r[indx['clas']], r[indx['prepo']]):
			if o: o.hide()
			self.show_popup(1 if o else 0, "لايمكنك أعطاء أسم للتصنيف نفس أسم احد المخازن!")
			if o: o.show()
			return
		
		
		self.up_clas_repo(r[indx['clas']], r[indx['repo']])
		
		try:
			if self.parent.db.check_integrity(0, r[indx['indoc']], r[indx['indate']]):	
				self.parent.db.db_insert(r)
			else:
				if o: o.hide()
				self.show_popup(1 if o else 0, "رقم مستند الادخال وتاريخ المستند يجب أن يكون فريدا!")
				if o: o.show()
				return			
		except Exception as e:
			if o: o.hide()
			self.show_popup(1 if o else 0, "حدث خطأ أعد تشغيل التطبيق أو الجهاز!")
			if o: o.show()
			error_msg = traceback.format_exc()
			self.parent.log(error_msg, True)
			print(error_msg.replace("||", "\n"))
			return

		# Insert into view.
		self.new_year(r[indx['indate']][:4], 0)

		# Insert into ds.
		self.parent.db.last += 1
		self.parent.db.al[r[indx['indate']][:4]]['e'].append(r)
		self.parent.db.al[r[indx['indate']][:4]]['الكل'].append(len(self.parent.db.al[r[indx['indate']][:4]]['e'])-1)
		self.parent.db.al[r[indx['indate']][:4]][r[indx['clas']]].append(len(self.parent.db.al[r[indx['indate']][:4]]['e'])-1)
		self.parent.db.al[r[indx['indate']][:4]][r[indx['repo']]].append(len(self.parent.db.al[r[indx['indate']][:4]]['e'])-1)

		self.sim_lst_click()
				
		if o: o.hide()
		self.show_popup(1 if o else 0, "تمت أضافة العنصر بنجاح")
		if o: o.show()
		#self.create_completer(self.parent.lineEdit, 0)
		self.parent.log("add row: "+str(r))

	def export(self, row):
		indx = self.parent.db.indcs[0]
		# check if row is zero, get r from editors.
		# else get r from table and pass it to cd2.
		if row == 0:
			r = self.check_row0()
			if not r:
				return
		else:
			r = [self.parent.model.data(self.parent.model.index(row, col), Qt.ItemDataRole.DisplayRole) for col in range(19)]
			 #f = [print(type(i)) for i in r]
		if self.clas_eq_repo(r[indx['clas']], r[indx['repo']]) or self.clas_eq_repo(r[indx['clas']], r[indx['prepo']]):
			self.show_popup(0, "لايمكنك أعطاء أسم للتصنيف نفس أسم احد المخازن!")
			return

		self.show_wait()
		dialog = ExportDlg(self, r, row)
		dialog.exec()
		self.overlay.close()
		if self.ref_model:
			lst =  self.parent.departsLstVu if self.parent.departsLstVu.currentRow() > -1 else self.parent.clasfLstVu
			lst.itemClicked.emit(lst.item(lst.currentRow()))
		else:
			self.ref_model = True

	def get_indexes(self, r, repo, clas):
		a = {'a': 0, 'r':0, 'c':0, 'e': 0}
		if self.parent.model.k == "srch":
			a['e'] = self.parent.model._data["srch"][r]
			for i in range(0, len(self.parent.model._data[repo])):
				if self.parent.model._data[repo][i] == a['e']:
					a['r'] = i
			for i in range(0, len(self.parent.model._data[clas])):
				if self.parent.model._data[clas][i] == a['e']:
					a['c'] = i
			for i in range(0, len(self.parent.model._data['الكل'])):
				if self.parent.model._data['الكل'][i] == a['e']:
					a['a'] = i
		elif self.parent.departsLstVu.currentRow() > -1:
			# print(">-1: ", self.parent.departsLstVu.currentRow())
			a['r'] = r
			a['e'] = self.parent.model._data[repo][r]
			for i in range(0, len(self.parent.model._data[clas])):
				if self.parent.model._data[clas][i] == a['e']:
					a['c'] = i
			for i in range(0, len(self.parent.model._data['الكل'])):
				if self.parent.model._data['الكل'][i] == a['e']:
					a['a'] = i
		elif self.parent.clasfLstVu.currentRow() > 0:
			#print(">0: ", self.parent.clasfLstVu.currentRow())
			a['c'] = r
			a['e'] = self.parent.model._data[clas][r]
			for i in range(0, len(self.parent.model._data[repo])):
				if self.parent.model._data[repo][i] == a['e']:
					a['r'] = i
			for i in range(0, len(self.parent.model._data['الكل'])):
				if self.parent.model._data['الكل'][i] == a['e']:
					a['a'] = i
		else:
			# print("=0: ", self.parent.clasfLstVu.currentRow())
			a['a'] = r
			a['e'] = self.parent.model._data['الكل'][r]
			for i in range(0, len(self.parent.model._data[clas])):
				if self.parent.model._data[clas][i] == a['e']:
					a['c'] = i
			for i in range(0, len(self.parent.model._data[repo])):
				if self.parent.model._data[repo][i] == a['e']:
					a['r'] = i
		return a

	def edit(self, r, d, old_d, move):
		indx = self.parent.db.indcs[0]		
		year = d[indx['indate']][:4]
		a = self.get_indexes(r, d[indx['repo']], old_d[indx['clas']])
	
		if move == 0:
			self.parent.db.al[year]['e'][a['e']] = tuple(d)		
			#self.parent.model.dataChanged.emit(self.parent.model.index(r, 0), self.parent.model.index(r, self.parent.model.cc-1))
		
		elif move == 1:
			self.up_clas_repo(d[indx['clas']], d[indx['repo']]) #view.		
			self.parent.db.new_clas(d[indx['clas']])	
			try:
				del self.parent.db.al[old_d[indx['indate']][:4]][old_d[indx['clas']]][a['c']]
			except:
				pass			
			self.parent.db.al[d[indx['indate']][:4]][d[indx['clas']]].append(a['e'])
			self.parent.db.al[year]['e'][a['e']] = tuple(d)	   
		
		else:
			self.up_clas_repo(d[indx['clas']], d[indx['repo']]) #view.
			self.parent.db.new_clas(d[indx['clas']])
			self.new_year(d[indx['indate']][:4], 0) 
	
			# delete from ds.
			try:
				del self.parent.db.al[old_d[indx['indate']][:4]][old_d[indx['repo']]][a['r']]
			except:
				pass
			try:
				del self.parent.db.al[old_d[indx['indate']][:4]][old_d[indx['clas']]][a['c']]
			except:
				pass		
			del self.parent.db.al[old_d[indx['indate']][:4]]['الكل'][a['a']]
		
			
			# Insert into ds.
			self.parent.db.al[d[indx['indate']][:4]]['e'].append(d)
			e_i = len(self.parent.db.al[d[indx['indate']][:4]]['e'])-1
			self.parent.db.al[d[indx['indate']][:4]]['الكل'].append(e_i)
			self.parent.db.al[d[indx['indate']][:4]][d[indx['clas']]].append(e_i)
			self.parent.db.al[d[indx['indate']][:4]][d[indx['repo']]].append(e_i)		   	
		
		#for i in range(len(old_d)): print(d[i], "\t\t", old_d[i])		
		self.parent.db.edit(d, old_d)
		self.sim_lst_click()
		
	def change_repo_ds(self, r, d, new_repo, old_qty, new_qty, out_doc, out_date):
		indx = self.parent.db.indcs[0]
		# get al, repo, clas indexes.
		year = d[indx['indate']][:4]
		a = self.get_indexes(r, d[indx['repo']], d[indx['clas']])
		old_repo = d[indx['repo']]
		
		if old_qty != new_qty:  # partial export.
			# only change the quantity for the original row.
			d[indx['quant']] = old_qty - new_qty
			#d[indx['hprice']] = d[indx['price']] * d[indx['quant']]
			self.parent.db.al[year]['e'][a['e']] = tuple(d) # update e tuple.
			
			try:
				self.parent.db.partial_export(d[indx['quant']], d[indx['hprice']], d[0])
			except Exception as e:
				self.show_popup(0, "حدث خطأ أعد تشغيل التطبيق أو الجهاز!")
				print(traceback.format_exc())
				self.parent.log(traceback.format_exc())
				return
			
			# redunt the original row with new data.
			d[indx['seq']] = self.parent.db.last + 1
			d[indx['quant']] = new_qty
			#d[indx['hprice']] = d[indx['price']] * d[indx['quant']]
			d[indx['prepo']] = d[indx['repo']]
			d[indx['repo']] = new_repo
			d[indx['outdoc']] = out_doc
			d[indx['outdoc']] = out_date
			
			try:
				self.parent.db.db_insert(d)
			except Exception as e:
				self.show_popup(0, "حدث خطأ أعد تشغيل التطبيق أو الجهاز!")
				print(e)
				self.parent.log(e)
				return

			# Insert into view.
			self.new_year(d[indx['indate']][:4], 0)

			# Insert into ds.
			self.parent.db.last += 1
			self.parent.db.al[d[indx['indate']][:4]]['e'].append(d)
			self.parent.db.al[d[indx['indate']][:4]]['الكل'].append(len(self.parent.db.al[d[indx['indate']][:4]]['e'])-1)
			self.parent.db.al[d[indx['indate']][:4]][d[indx['clas']]].append(len(self.parent.db.al[d[indx['indate']][:4]]['e'])-1)
			self.parent.db.al[d[indx['indate']][:4]][d[indx['repo']]].append(len(self.parent.db.al[d[indx['indate']][:4]]['e'])-1)
						
		else:
			d[indx['prepo']] = d[indx['repo']]
			d[indx['repo']] = new_repo
			d[indx['outdoc']] = out_doc
			d[indx['outdate']] = out_date
			try:
				self.parent.db.full_export(old_repo, d[indx['repo']], d[indx['seq']])
			except Exception as e:
				self.show_popup(0, "حدث خطأ أعد تشغيل التطبيق أو الجهاز!")
				print(traceback.format_exc())
				self.parent.log(traceback.format_exc())
				return
			self.parent.db.al[year]['e'][a['e']] = tuple(d) # update e tuple.
			del self.parent.db.al[year][old_repo][a['r']]   # delete the index from old repo.
			self.parent.db.al[year][d[indx['repo']]].append(a['e'])   # append the index to the new repo.
		
		self.show_popup(1, "تم أخراج العنصر إلى " + d[indx['repo']] + " بنجاح!")
		self.parent.log("change repo: "+old_repo+" > "+str(d))

			
	def cons_ds(self, r, d, nd):
		indx = self.parent.db.indcs[0]
		indx1 = self.parent.db.indcs[1]
		v = self.parent.db.cons
		
		# get al, repo, clas indexes.
		a = self.get_indexes(r, d[indx['repo']], d[indx['clas']])
		
		nd = d[:17] + nd + d[17: ] + [1] + [d[0]]  # cons full tuple. (17 is prepo)
		nd[0] =  self.parent.db.last_cons+1

		try:
			tmp = [nd[indx1['seq']], nd[indx1['alseq']], nd[indx1['cquant']], nd[indx1['cprice']],
				   nd[indx1['c_hprice']], nd[indx1['cdoc']], nd[indx1['cdate']], self.parent.db.repo[nd[indx1['repo']]], 1]
			
			if self.parent.db.check_integrity(1, nd[indx1['cdoc']], nd[indx1['cdate']]):
				self.parent.db.cons_corr(True, tmp, d[indx['quant']], d[indx['seq']])
			else:
				self.show_popup(0, "رقم مستند الاستهلاك وتاريخ المستند يجب أن يكون فريدا!")
				return			
		except Exception as e:
			self.show_popup(0, "حدث خطأ أعد تشغيل التطبيق أو الجهاز!")
			print(traceback.format_exc())
			self.parent.log(traceback.format_exc())
			return
		
		self.parent.db.last_cons += 1
		
		
		self.new_year(nd[indx1['cdate']][:4], 1)
		v[nd[indx1['cdate']][:4]]['e'].append(nd)
		v[nd[indx1['cdate']][:4]]['الكل'].append(len(v[nd[indx1['cdate']][:4]]['e']) - 1)
		v[nd[indx1['cdate']][:4]][nd[indx1['clas']]].append(len(v[nd[indx1['cdate']][:4]]['e']) - 1)
		v[nd[indx1['cdate']][:4]][nd[indx1['repo']]].append(len(v[nd[indx1['cdate']][:4]]['e']) - 1)
		
		if not d[6]:
			del self.parent.db.al[d[indx['indate']][:4]]['الكل'][a['a']]
			del self.parent.db.al[d[indx['indate']][:4]][d[indx['repo']]][a['r']]
			del self.parent.db.al[d[indx['indate']][:4]][d[indx['clas']]][a['c']]
		else:
			#print(a['e'], len(self.parent.db.al[d[10][:4]]['e']))
			self.parent.db.al[d[indx['indate']][:4]]['e'][a['e']] = tuple(d)
		
		self.show_popup(0, "تمت اضافة العنصر الى المستهلكات!")
		self.parent.log("consume: " + str(nd))


	def corr_ds(self, r, d, nd):
		indx = self.parent.db.indcs[0]
		indx1 = self.parent.db.indcs[2]
		v = self.parent.db.corr
		
		# get al, repo, clas indexes.
		a = self.get_indexes(r, d[indx['repo']], d[indx['clas']])
		
		nd = d[:17] + nd + d[17: ] + [d[0]]  # cons full tuple. (17 is prepo)
		nd[0] =  self.parent.db.last_corr+1

		try:
			tmp = [nd[indx1['seq']], nd[indx1['alseq']], nd[indx1['cquant']], nd[indx1['cdoc']], nd[indx1['cdate']], self.parent.db.repo[nd[indx1['repo']]]]
			
			if self.parent.db.check_integrity(2, nd[indx1['cdoc']], nd[indx1['cdate']]):
				self.parent.db.cons_corr(False, tmp, d[indx['quant']], d[indx['seq']])
			else:
				self.show_popup(0, "رقم مستند الاتلاف وتاريخ المستند يجب أن يكون فريدا!")
				return		
		except Exception as e:
			self.show_popup(0, "حدث خطأ أعد تشغيل التطبيق أو الجهاز!")
			print(traceback.format_exc())
			self.parent.log(traceback.format_exc())
			return
		
		self.parent.db.last_corr += 1
		
		self.new_year(nd[indx1['cdate']][:4], 2)
		v[nd[indx1['cdate']][:4]]['e'].append(nd)
		v[nd[indx1['cdate']][:4]]['الكل'].append(len(v[nd[indx1['cdate']][:4]]['e']) - 1)
		v[nd[indx1['cdate']][:4]][nd[indx1['clas']]].append(len(v[nd[indx1['cdate']][:4]]['e']) - 1)
		v[nd[indx1['cdate']][:4]][nd[indx1['repo']]].append(len(v[nd[indx1['cdate']][:4]]['e']) - 1)
		
		if not d[6]:
			del self.parent.db.al[d[indx['indate']][:4]]['الكل'][a['a']]
			del self.parent.db.al[d[indx['indate']][:4]][d[indx['repo']]][a['r']]
			del self.parent.db.al[d[indx['indate']][:4]][d[indx['clas']]][a['c']]
		else:
			#print(a['e'], len(self.parent.db.al[d[10][:4]]['e']))
			self.parent.db.al[d[indx['indate']][:4]]['e'][a['e']] = tuple(d)
		
		self.show_popup(0, "تمت اضافة العنصر الى المتلفات!")
		self.parent.log("corrupt: "+str(nd))
  
	def sell(self, r):
		d = [self.parent.model.data(self.parent.model.index(r, col), Qt.ItemDataRole.DisplayRole) for col in range(26)]
		self.show_wait()
		dialog = SellDlg(self, d, r)
		dialog.exec()
		self.overlay.close()
		lst = self.parent.departsLstVu if self.parent.departsLstVu.currentRow() > -1 else self.parent.clasfLstVu
		lst.itemClicked.emit(lst.item(lst.currentRow()))

	def sell_ds(self, r, d, nd):
		indx1 = self.parent.db.indcs[1]
		indx2 = self.parent.db.indcs[3]
		a = self.get_indexes(r, d[indx1['repo']], d[indx1['clas']])
		v = self.parent.db.sold
		nd = d[:indx1['prepo']] + nd + [d[indx1['prepo']]] + [d[indx1['repo']]] + [d[indx1['alseq']]] + [d[0]]
		nd[0] = self.parent.db.last_sold+1
		
		
		try:
			if self.parent.db.check_integrity(3, nd[indx2['sdoc']], nd[indx2['sdate']]):
				self.parent.db.sell(nd, d[indx1['seq']])
			else:
				self.show_popup(1, "رقم مستند البيع وتاريخ المستند يجب أن يكون فريدا!")
				return		
		except Exception as e:
			self.show_popup(1, "حدث خطأ أعد تشغيل التطبيق أو الجهاز!")
			print(traceback.format_exc())
			self.parent.log(traceback.format_exc())
			return
		
		self.parent.db.last_sold += 1
		
		self.new_year(nd[indx2['sdate']][:4], 3)
		v[nd[indx2['sdate']][:4]]['e'].append(nd)
		v[nd[indx2['sdate']][:4]]['الكل'].append(len(v[nd[indx2['sdate']][:4]]['e']) - 1)
		v[nd[indx2['sdate']][:4]][nd[indx2['clas']]].append(len(v[nd[indx2['sdate']][:4]]['e']) - 1)
		v[nd[indx2['sdate']][:4]][nd[indx2['repo']]].append(len(v[nd[indx2['sdate']][:4]]['e']) - 1)
		
		if d[indx1['cquant']] == 0:
			del self.parent.db.cons[nd[indx2['cdate']][:4]]['الكل'][a['a']]
			del self.parent.db.cons[nd[indx2['cdate']][:4]][nd[indx2['repo']]][a['r']]
			del self.parent.db.cons[nd[indx2['cdate']][:4]][nd[indx2['clas']]][a['c']]
		else:
			self.parent.db.cons[d[indx1['cdate']][:4]]['e'][a['e']] = tuple(d)
		self.show_popup(1, "تمت أضافة العنصر الى المبيعات!")
		self.parent.log("sell: "+str(nd))

	def delete(self, r, d):
		indx = self.parent.db.indcs[0]
		a = self.get_indexes(r, d[indx['repo']], d[indx['clas']])
		if not self.parent.db.delete(d[indx['seq']], d[indx['emp']], d[indx['mat']], d[indx['origin']], d[indx['clas']], d[indx['repo']], d[indx['prepo']], d[indx['corp']]):
			self.show_popup(0, "لايمكنك حذف هذا الصف لأن مرتبط بالمستهلكات أو بالمتلفات!")
			return

		# this code was in try block because the repo or clas could be deleted by db.delete.
		try:
			del self.parent.db.al[d[indx['indate']][:4]][d[indx['repo']]][a['r']]
		except:
			pass
		try:
			del self.parent.db.al[d[indx['indate']][:4]][d[indx['clas']]][a['c']]
		except:
			pass
		
		del self.parent.db.al[d[indx['indate']][:4]]['الكل'][a['a']]
		
		#self.parent.model.beginResetModel()
		self.parent.model.rc -= 1
		#self.parent.model.endResetModel()
		self.show_popup(0, "تم حذف الصف بنجاح")
		self.parent.log("delete: "+str(d))

	def auto(self):
		indx = self.parent.db.indcs[0]
		p = self.parent.table_view.indexWidget(self.parent.model.index(0, 5)).text()
		q = self.parent.table_view.indexWidget(self.parent.model.index(0, 6)).text()
		p = int(p) if p.isdigit() else 0
		q = int(q) if q.isdigit() else 0
		self.parent.table_view.indexWidget(self.parent.model.index(0, 7)).setText(str(p*q))



class ClickableLineEdit(QLineEdit):
	def __init__(self, parent=None):
		super(ClickableLineEdit, self).__init__(parent)
		self.o = False

	def mousePressEvent(self, event):
		pass
		#self.parent().showPopup()
		'''if not self.o:
			self.parent().showPopup()
			self.o = True
		else:
			self.parent().hidePopup()
			self.o = False'''

class CenteredItemDelegate(QStyledItemDelegate):
	def __init__(self, parent=None):
		super(CenteredItemDelegate, self).__init__(parent)
	def paint(self, painter, option, index):
		option.displayAlignment = Qt.AlignmentFlag.AlignCenter
		super().paint(painter, option, index)

class CustomDialog(QDialog):
	def __init__(self, parent, t=None):
		super().__init__()
		self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
		label = QLabel("اكمل ملئ المعلومات اولاً رجاءاً" if t is None else t)
		label.setStyleSheet("font-size: 20px; color: #333333; font-family: Noto Sans Arabi; font-weight: bold;")
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		ok_button = QPushButton("حسناً")
		ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
		ok_button.setFixedSize(200, 60)
		ok_button.clicked.connect(self.accept)  # just for close the message box.
		ok_button.setStyleSheet(Style.ok_btn_style)
		layout = QVBoxLayout()
		layout.addWidget(label)
		layout.addWidget(ok_button)
		layout.setAlignment(ok_button, Qt.AlignmentFlag.AlignCenter)
		self.setLayout(layout)
		#parent_width = parent.width() #
		#parent_height = parent.height()
		self.resize(750, 380)
		self.setStyleSheet(Style.dlg_Style)

class CustomDialog4(QDialog):
	def __init__(self, parent):
		super().__init__()
		self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
		label = QLabel("يرجى الأنتظار...")
		label.setStyleSheet("font-size: 20px; color: #333333; font-weight: bold;")
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		ok_button = QPushButton("حسناً")
		ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
		ok_button.setFixedSize(200, 60)
		ok_button.clicked.connect(self.accept)  # just for close the message box.
		ok_button.setStyleSheet(Style.ok_btn_style)
		layout = QVBoxLayout()
		layout.addWidget(label)
		#layout.addWidget(ok_button)
		layout.setAlignment(ok_button, Qt.AlignmentFlag.AlignCenter)
		self.setLayout(layout)
		#parent_width = parent.width() #
		#parent_height = parent.height()
		self.resize(750, 380)
		self.setStyleSheet(Style.dlg_Style)
		
		

			
		

