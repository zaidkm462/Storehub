from openpyxl import load_workbook

def check_sheet(sheet, header, dlt):
	header = header.copy()
	for i in dlt: del header[i]
	cols = len(header)
	col_count = sum(1 for cell in sheet[1] if cell.value is not None)
	row_count = sum(1 for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row) if row[0].value is not None)
	
	if col_count != cols or row_count < 1:
		return f"عدد الحقول يجب أن يساوي {str(cols)}"
	
	for i in range(0, cols):
		if sheet[1][i].value != header[i]:
			return f"اسم الحقل ({sheet[1][i].value}) يجب أن يكون ({header[i]})"

	return row_count


def new_repo(db, repo):
	if not repo in db.repo:
		self.cursor.execute("INSERT INTO repo(name) VALUES(?)", (repo,))
		self.repo[repo] = self.cursor.lastrowid
	return db.repo[repo]
	

def check_date(txt):
	lst = str(txt).split(" ")[0].split("-")
	if len(lst) != 3 : return False
	if len(lst[0]) != 4 or not lst[0].isdigit() or int(lst[0]) < 1000: return False
	if len(lst[1]) != 2 or not lst[1].isdigit() or int(lst[1]) > 12: return False
	if len(lst[2]) != 2 or not lst[2].isdigit() or int(lst[2]) > 31: return False
	return True
	
	
def check_cons_part(row, i, header):
	e = [0] * 5
	for j in range(19, 24):
		# doc_date.
		if j == 20:			
			if row[j] and check_date(str(row[j])):
				e[j-19] = str(row[j]).split()[0]
			else:
				return f"التاريخ في حقل {header[j]} في الصف {i} يجب أن يكتب بالتنسيق الصحيح"
		# integers (doc, price, quant, h_price).
		else:
			if not isinstance(row[j], (int, float)):
				return f"الخلية في عمود {header[j]} في الصف {i} يجب أن تكون رقما"
			e[j-19] = int(row[j])
	return e

			
def check_ex_part(row, i, header):
	e = [0] * 19	 
	for j in range(1, 19):
		# serial (opt-str).
		if j in (3, 14, 17) : e[j] = None if row[j] is None else str(row[j]) 
	
		# outdoc (opt-num).
		elif j == 11:
			if not row[j]: e[j] = None
			elif isinstance(row[j], (int, float)): e[j] = int(row[j])
			else: return f"الخلية في عمود مستند الاخراج في الصف {i} يجب أما ان تترك فارغة أو تكون رقما"

		# outdate & prod & exp date (opt-date).
		elif j in (12, 15, 16):
			if not e[j]: e[j] = None
			elif check_date(row[j]): e[j] = str(row[j]).split()[0]
			else: return f"التاريخ في حقل {header[j]} في الصف {i} يجب أن يكتب بالتنسيق الصحيح أو يترك فارغ"
		
		# b_date & in_date (man-date).
		elif j in (8, 10):
			if check_date(row[j]): e[j] = str(row[j]).split()[0]
			else: return f"التاريخ في حقل {header[j]} في الصف {i} يجب أن يكتب بالتنسيق الصحيح"
		
		# price & quant & h_price & in_doc (man-num).
		elif j in (5, 6, 7, 9):
			if not isinstance(row[j], (int, float)):
				print(j, row[j])
				return f"الخلية في عمود {header[j]} في الصف {i} يجب أن تكون رقما"
			e[j] = int(row[j])
		
		# everything else required.
		elif not row[j]: return f"الخلية في عمود {header[j]} في الصف {i} يجب أن لا تكون فارغة"
		else: e[j] = str(row[j])								

	return e
	

def read_ex(db, path):
	header1 = ["التسلسل", "أسم الموظف", "أسم المادة", "الرقم التسلسلي", "المنشأ", "سعر المفرد", "الكمية", "السعر الكلي", "تاريخ الشراء", "رقم مستند الأدخال", "تاريخ مستند الأدخال", "رقم مستند الأخراج", "تاريخ مستند الأخراج", "التصنيف", "الشركة المصنعة", "تاريخ الانتاج", "تاريخ الانتهاء", "المخزن السابق", "الى المؤسسة"]
	
	wb = load_workbook(path, data_only=True)
	sheet = wb.active	
	row_count = check_sheet(sheet, header1, (0, ))
	if isinstance(row_count, str) : return row_count  
	
	for i in range(2, row_count+1):		
		row = [c.value for c in sheet[i]]
		row.insert(0, 0)
		e = check_ex_part(row, i, header1)
		if isinstance(e, str):
			db.conn.rollback()
			return e
		else:
			e[0] = db.last+1
			e += [1]
			
			if db.check_integrity(0, str(e[9]), str(e[10])):
				db.db_insert(e, False)
			else:
				db.conn.rollback()
				return f"مستند وتاريخ الادخال في الصف {i} مكررة سابقا"
			
			db.last += 1
	   
	db.conn.commit()
	return "تم الأستيراد بنجاح"


def read_cons(db, path):	
	header1 = ["التسلسل", "أسم الموظف", "أسم المادة", "الرقم التسلسلي", "المنشأ", "سعر المفرد","الكمية", "السعر الكلي", "تاريخ الشراء", "رقم مستند الأدخال", "تاريخ مستند الأدخال", "رقم مستند الأخراج", "تاريخ مستند الأخراج", "التصنيف", "الشركة المصنعة", "تاريخ الانتاج", "تاريخ الانتهاء", "المخزن السابق", "الى المؤسسة", "رقم مستند الأستهلاك", "تاريخ مستند الأستهلاك", "سعر الأستهلاك المفرد", "الكمية", "السعر الكلي للأستهلاك"]
	wb = load_workbook(path, data_only=True)
	sheet = wb.active
	
	row_count = check_sheet(sheet, header1, (6, 0))
	if isinstance(row_count, str) : return row_count		  
	
	for i in range(2, row_count+1):
		row = [c.value for c in sheet[i]]
		row.insert(0, 0)	
		row.insert(6, 0)
		e1 = check_ex_part(row, i, header1)
		if isinstance(e1, str): return e1
		e2 = check_cons_part(row, i, header1)
		if isinstance(e2, str): return e2


		db.cursor.execute("SELECT id FROM al WHERE indoc = ? AND indoc_date = ?", (e1[9], e1[10]))
		results = db.cursor.fetchone()
		#print(e1[9], e1[10], results)

		if results:
			e2.insert(0, results[0])
			e2.insert(0, db.last_cons+1)
			e2.append(new_repo(db, e1[18]))
			e2.append(1)
			if db.check_integrity(1, str(e2[2]), str(e2[3])):
				db.cursor.execute("INSERT INTO cons(prime, id, doc, doc_date, nprice, quant, hprice, repo, sell) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", e2)
			else:
				db.conn.rollback()
				return f"مستند وتاريخ الاستهلاك في الصف {i} مكررة سابقا"

			db.last_cons += 1
		
		else:
			e1[0] = db.last+1
			e1.append(0)
			db.db_insert(e1, False)
			db.last += 1
			
			e2.insert(0, db.last)
			e2.insert(0, db.last_cons+1)
			e2.append(new_repo(db, e1[18]))
			e2.append(0)
			
			if db.check_integrity(1, str(e2[2]), str(e2[3])):			
				db.cursor.execute("INSERT INTO cons(prime, id, doc, doc_date, nprice, quant, hprice, repo, sell) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", e2)	
			else:
				db.conn.rollback()
				return f"مستند وتاريخ الاستهلاك في الصف {i} مكررة سابقا"
			
			db.last_cons += 1
	
	db.conn.commit()
	return "تم الأستيراد بنجاح"


def read_corr(db, path):
	
	header1 = ["التسلسل", "أسم الموظف", "أسم المادة", "الرقم التسلسلي", "المنشأ", "سعر المفرد","الكمية", "السعر الكلي", "تاريخ الشراء", "رقم مستند الأدخال", "تاريخ مستند الأدخال", "رقم مستند الأخراج", "تاريخ مستند الأخراج", "التصنيف", "الشركة المصنعة", "تاريخ الانتاج", "تاريخ الانتهاء", "المخزن السابق", "الى المؤسسة", "رقم مستند الاتلاف", "تاريخ مستند الاتلاف", "الكمية"]
	
	wb = load_workbook(path, data_only=True)
	sheet = wb.active
	
		
	row_count = check_sheet(sheet, header1, (6, 0))
	if isinstance(row_count, str) : return row_count		  
	
	for i in range(2, row_count+1):
		row = [c.value for c in sheet[i]]
		row.insert(0, 0)	
		row.insert(6, 0)
		e1 = check_ex_part(row, i, header1)
		e2 = [0] * 4
		if isinstance(e1, str):			
			db.conn.rollback()
			return e1
		
		for j in range(19, 22):
			# dates.
			if j == 20:
				if row[j] and check_date(str(row[j])): e2[j-19+1] = str(row[j]).split()[0]
				else:
					db.conn.rollback()
					return  f"تاريخ مستند الاتلاف في الصف {i} يجب أن يكتب بالتنسيق الصحيح"

			# integers.
			else:
				if not isinstance(row[j], (int, float)):
					db.conn.rollback()
					return f"الخلية في عمود {header[j]} في الصف {i} يجب أن تكون رقما"
				e2[j-19+1] = int(row[j])
		
		
		db.cursor.execute("SELECT id FROM al WHERE indoc = ? AND indoc_date = ?", (e1[9], e1[10]))
		results = db.cursor.fetchone()

		if results:
			e2[0] = results[0]
			e2.append(new_repo(db, e1[18]))
			
			if db.check_integrity(2, str(e2[1]), str(e2[2])):
				db.cursor.execute("INSERT INTO corr(id, doc, doc_date, quant, repo) VALUES(?, ?, ?, ?, ?);", e2)
			else:
				db.conn.rollback()
				return f"مستند وتاريخ الاتلاف في الصف {i} مكررة سابقا"
				
		else:
			e1[0] = db.last+1
			e1.append(0)		
			db.db_insert(e1, False)			
			db.last+=1
			e2[0] = db.last
			e2.append(new_repo(db, e1[18]))
			
			if db.check_integrity(2, str(e2[1]), str(e2[2])):
				db.cursor.execute("INSERT INTO corr(id, doc, doc_date, quant, repo) VALUES(?, ?, ?, ?, ?);", e2)
			else:
				db.conn.rollback()
				return f"مستند وتاريخ الاتلاف في الصف {i} مكررة سابقا"

				
	db.conn.commit()
	return "تم الأستيراد بنجاح"


def read_sold(db, path):
	
	header1 = ["التسلسل", "أسم الموظف", "أسم المادة", "الرقم التسلسلي", "المنشأ", "سعر المفرد", "الكمية", "السعر الكلي", "تاريخ الشراء", "رقم مستند الأدخال", "تاريخ مستند الأدخال", "رقم مستند الأخراج", "تاريخ مستند الأخراج", "التصنيف", "الشركة المصنعة", "تاريخ الانتاج", "تاريخ الانتهاء", "المخزن السابق", "الى المؤسسة", "رقم مستند الأستهلاك", "تاريخ مستند الأستهلاك", "سعر الأستهلاك المفرد", "الكمية", "السعر الكلي للأستهلاك","رقم مستند البيع", "تاريخ مستند البيع", "سعر البيع", "الكمية المباعة", "سعر البيع الكلي"]

	wb = load_workbook(path, data_only=True)
	sheet = wb.active	
	  
	row_count = check_sheet(sheet, header1, (22, 6, 0))
	if isinstance(row_count, str) : return row_count   
		
	for i in range(2, row_count + 1):
		e3 = [0] * 7
		row = [c.value for c in sheet[i]]
		row.insert(0, 0)	
		row.insert(6, 0)
		row.insert(22, 0)
		
		e1 = check_ex_part(row, i, header1)
		if isinstance(e1, str):
			db.conn.rollback()
			return e1
		
		e2 = check_cons_part(row, i, header1)
		if isinstance(e2, str):
			db.conn.rollback()
			return e2

		for j in range(24, 29):
			# dates.
			if j == 25:
				if row[j] and check_date(str(row[j])): e3[j-24+2] = str(row[j]).split()[0]
				else:
					db.conn.rollback()
					return  f"تاريخ مستند البيع في الصف {i} يجب أن يكتب بالتنسيق الصحيح"

			# integers.
			else:
				if not isinstance(row[j], (int, float)):
					db.conn.rollback()
					return f"الخلية في عمود {header[j]} في الصف {i} يجب أن تكون رقما"
				e3[j-24+2] = int(row[j])
		
		db.cursor.execute("SELECT prime, id FROM cons WHERE doc = ? AND doc_date = ?", (e2[0], e2[1]))
		results = db.cursor.fetchone()

		if results:
			e3[0] = results[1]
			e3[1] = results[0]
			
			if db.check_integrity(3, str(e3[2]), str(e3[3])):
				db.cursor.execute("INSERT INTO sold(id, id2, doc, doc_date, price, quant, hprice) VALUES(?, ?, ?, ?, ?, ?, ?);", e3)
			else:
				db.conn.rollback()
				return f"مستند وتاريخ البيع في الصف {i} مكررة سابقا"

		else:
			db.cursor.execute("SELECT id FROM al WHERE indoc = ? AND indoc_date = ?", (e1[9], e1[10]))
			results2 = db.cursor.fetchone()

			if results2:
				e2.insert(0, results2[0])
				e2.insert(0, db.last_cons+1)
				e2.append(0)
				e2[5] = 0
				db.cursor.execute("INSERT INTO cons(prime, id, doc, doc_date, nprice, quant, hprice, sell) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", e2)
				db.last_cons += 1
				
				e3[1] = db.last_cons
				e3[0] = results2[0]
				
				
				if db.check_integrity(3, str(e3[2]), str(e3[3])):
					db.cursor.execute("INSERT INTO sold(id, id2, doc, doc_date, price, quant, hprice) VALUES(?, ?, ?, ?, ?, ?, ?);", e3)
				else:
					db.conn.rollback()
					return f"مستند وتاريخ البيع في الصف {i} مكررة سابقا"

			else:
				e1[0] = db.last+1
				e1.append(0)
				db.db_insert(e1, False)
				db.last += 1
				
				e2.insert(0, db.last)
				e2.insert(0, db.last_cons+1)
				e2.append(new_repo(db, e1[18]))
				e2.append(0)
				db.cursor.execute("INSERT INTO cons(prime, id, doc, doc_date, nprice, quant, hprice, repo, sell) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", e2)
				db.last_cons += 1
				
				e3[0] = db.last_cons
				e3[1] = db.last_cons
				
				if db.check_integrity(3, str(e3[2]), str(e3[3])):
					db.cursor.execute("INSERT INTO sold(id, id2, doc, doc_date, price, quant, hprice) VALUES(?, ?, ?, ?, ?, ?, ? );", e3)
				else: 
					db.conn.rollback()
					return f"مستند وتاريخ البيع في الصف {i} مكررة سابقا"

	db.conn.commit()
	return "تم الأستيراد بنجاح"
