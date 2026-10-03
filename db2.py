import sqlite3
from PyQt6.QtCore import QThread
import time



class DB:
	def __init__(self, date):
		self.indcs = [
		{"seq": 0, "emp": 1, "mat": 2, "serial": 3, "origin": 4, "price": 5, "quant": 6, "hprice": 7, "bdate": 8, "indoc": 9, "indate": 10, "outdoc": 11, "outdate": 12, "clas": 13, "corp": 14, "pdate": 15, "edate": 16, "prepo": 17, "repo": 18},
		{"seq": 0, "emp": 1, "mat": 2, "serial": 3, "origin": 4, "price": 5, "quant": 6, "hprice": 7, "bdate": 8, "indoc": 9, "indate": 10, "outdoc": 11, "outdate": 12, "clas": 13, "corp": 14, "pdate": 15, "edate": 16, "cquant": 17, "cprice": 18, "c_hprice": 19, "cdoc": 20, "cdate": 21, "prepo": 22, "repo": 23, "sell": 24, "alseq": 25},
		{"seq": 0, "emp": 1, "mat": 2, "serial": 3, "origin": 4, "price": 5, "quant": 6, "hprice": 7, "bdate": 8, "indoc": 9, "indate": 10, "outdoc": 11, "outdate": 12, "clas": 13, "corp": 14, "pdate": 15, "edate": 16, "cquant": 17, "cdoc": 18, "cdate": 19, "prepo": 20, "repo": 21, "alseq": 22},
		{"seq": 0, "emp": 1, "mat": 2, "serial": 3, "origin": 4, "price": 5, "quant": 6, "hprice": 7, "bdate": 8, "indoc": 9, "indate": 10, "outdoc": 11, "outdate": 12, "clas": 13, "corp": 14, "pdate": 15, "edate": 16, "cquant": 17, "cprice": 18, "c_hprice": 19, "cdoc": 20, "cdate": 21, "squant": 22, "sprice": 23, "s_hprice": 24, "sdoc": 25, "sdate": 26, "prepo": 27, "repo": 28, "alseq": 29, 'cseq': 30}
		]
		self.thrd = None
		self.date = date
		self.last = 0
		self.last_cons = 0
		self.last_corr = 0
		self.last_sold = 0
		self.emp = {}
		self.mat = {}
		self.corp = {}
		self.origin = {}
		self.clas = {}
		self.repo = {}
		self.al = {}
		self.corr = {}
		self.sold = {}
		self.cons = {}
		self.data = {}
		self.conn = sqlite3.connect("db6.db")
		self.cursor = self.conn.cursor()
		self.cursor.execute("PRAGMA foreign_keys = ON;")
		self.create_tables()
		self.fetch1()
		self.fetch_al()
		self.fetch_corr()
		self.fetch_sold()
		self.fetch_cons()

	def create_tables(self):
		self.cursor.executescript("""
		CREATE TABLE IF NOT EXISTS emp(id INTEGER PRIMARY KEY, name TEXT);
		CREATE TABLE IF NOT EXISTS repo(id INTEGER PRIMARY KEY, name TEXT);
		CREATE TABLE IF NOT EXISTS mat(id INTEGER PRIMARY KEY, name TEXT);
		CREATE TABLE IF NOT EXISTS origin(id INTEGER PRIMARY KEY, name TEXT);
		CREATE TABLE IF NOT EXISTS clas(id INTEGER PRIMARY KEY, name TEXT);
		CREATE TABLE IF NOT EXISTS corp(id INTEGER PRIMARY KEY, name TEXT);
		CREATE TABLE IF NOT EXISTS al(
			id INTEGER PRIMARY KEY, emp INTEGER, mat INTEGER, sn TEXT, origin INTEGER,
			price INTEGER, quant INTEGER, h_price INTEGER, b_date TEXT, 
			indoc INTEGER, indoc_date TEXT, outdoc INTEGER, outdate TEXT, clas INTEGER,
			corp INTEGER, prod_date TEXT, exp_date TEXT, prev_repo INTEGER, repo INTEGER, booln INTEGER,
			FOREIGN KEY (emp) REFERENCES emp(id), FOREIGN KEY (mat) REFERENCES mat(id),
			FOREIGN KEY (origin) REFERENCES origin(id), FOREIGN KEY (clas) REFERENCES clas(id), 
			FOREIGN KEY (repo) REFERENCES repo(id), FOREIGN KEY (prev_repo) REFERENCES repo(id),
			FOREIGN KEY (corp) REFERENCES corp(id)  
		);
		
		CREATE TABLE IF NOT EXISTS cons(
			prime INTEGER PRIMARY KEY, id INTEGER, quant INTEGER, nprice INTEGER, hprice INTEGER, doc INTEGER, doc_date TEXT, repo INTEGER, sell INTEGER,
			FOREIGN KEY (id) REFERENCES al(id),
			FOREIGN KEY (repo) REFERENCES repo(id)
			);
		
		CREATE TABLE IF NOT EXISTS corr(
			prime INTEGER PRIMARY KEY, id INTEGER, quant INTEGER, doc INTEGER, doc_date TEXT, repo INTEGER,
			FOREIGN KEY (id) REFERENCES al(id)
			FOREIGN KEY (repo) REFERENCES repo(id)
			);
			
		CREATE TABLE IF NOT EXISTS sold(
			prime INTEGER PRIMARY KEY, id INTEGER, id2 INTEGER, price INTEGER, quant INTEGER, hprice INTEGER, doc INTEGER, doc_date TEXT,
			FOREIGN KEY (id) REFERENCES al(id), FOREIGN KEY (id2) REFERENCES cons(prime)
			);
			
		INSERT OR IGNORE INTO repo VALUES(1, 'المخزن الرئيسي'); 
		INSERT OR IGNORE INTO clas VALUES(1, 'الكل'); 
		""")

	def fetch1(self):
		#data = []

		self.cursor.execute("SELECT name, id FROM repo;")
		repo = self.cursor.fetchall()
		self.repo = {i[0]:i[1] for i in repo}

		self.cursor.execute("SELECT name, id FROM clas;")
		clas = self.cursor.fetchall()
		self.clas = {i[0]:i[1] for i in clas}

		self.cursor.execute("SELECT name, id FROM emp;")
		emp = self.cursor.fetchall()
		self.emp = {i[0]:i[1] for i in emp}

		self.cursor.execute("SELECT name, id FROM mat;")
		mat = self.cursor.fetchall()
		self.mat = {i[0]:i[1] for i in mat}

		self.cursor.execute("SELECT name, id FROM corp;")
		corp = self.cursor.fetchall()
		self.corp = {i[0]:i[1] for i in corp}

		self.cursor.execute("SELECT name, id FROM origin;")
		origin = self.cursor.fetchall()
		self.origin = {i[0]:i[1] for i in origin}

	def cn_close(self):
		self.conn.commit()
		self.conn.close()

	def fetch_al(self):
		data = {}
		self.cursor.execute("""SELECT al.id, emp.name, mat.name, al.sn, origin.name, al.price, al.quant, al.h_price,
								al.b_date, al.indoc, al.indoc_date, al.outdoc, al.outdate, clas.name, corp.name, 
								al.prod_date, al.exp_date, repo2.name, repo.name FROM al 
								JOIN emp ON al.emp = emp.id
								JOIN mat ON al.mat = mat.id
								JOIN origin ON al.origin = origin.id
								JOIN clas ON al.clas = clas.id
								JOIN repo ON al.repo = repo.id
								LEFT JOIN corp ON al.corp = corp.id
								LEFT JOIN repo AS repo2 ON al.prev_repo = repo2.id											  
								where booln = 1;""")

		indx = self.indcs[0]
		db_data = self.cursor.fetchall()
		#print([i[0] for i in db_data])
		self.cursor.execute("SELECT MAX(id) FROM al")
		m = self.cursor.fetchone()[0]
		self.last = m if m is not None else 0

		data[self.date[:4]] = {"e": [], "srch":[]}
		data[self.date[:4]]["e"].append(('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'المخزن الرئيسي'))
		for j in self.repo.keys():
			data[self.date[:4]][j] = [0]
		for j in self.clas.keys():
			data[self.date[:4]][j] = [0]

		i =0
		length = len(db_data)
		i2 = {self.date[:4]: 1}
		while i < length:
			year = db_data[i][indx['indate']][:4]
			if year in data:
				data[year]["e"].append(db_data[i])
				data[year]['الكل'].append(i2[year])
				data[year][db_data[i][indx['clas']]].append(i2[year])
				data[year][db_data[i][indx['repo']]].append(i2[year])
				#print(i2, end=', ')
				i2[year] += 1
			else:
				data[year] = {"e": [], "srch":[]}
				i2[year] = 1
				data[year]["e"].append(('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'المخزن الرئيسي'))
				for j in self.repo.keys():
					data[year][j] = [0]
				for j in self.clas.keys():
					data[year][j] = [0]
				i -= 1
			i += 1

		if self.date[:4] not in data:
			print("hello useless")
			data[self.date[:4]] = {"e": [], "srch": []}
			for j in self.repo.keys():
				data[self.date[:4]][j] = []
			for j in self.clas.keys():
				data[self.date[:4]][j] = []
		self.al = data
		self.data = self.al

	def fetch_cons(self, cursor=None):
		data = {}
		cursor = cursor if cursor else self.cursor
		
		cursor.execute("""SELECT cons.prime, emp.name, mat.name, al.sn, origin.name, al.price, al.quant, al.h_price,
								al.b_date, al.indoc, al.indoc_date, al.outdoc, al.outdate, clas.name, corp.name,
								al.prod_date, al.exp_date, cons.quant, cons.nprice, cons.hprice, cons.doc, cons.doc_date,
								repo2.name, repo.name, cons.sell, cons.id FROM cons 
								JOIN al ON cons.id = al.id
								JOIN emp ON al.emp = emp.id
								JOIN mat ON al.mat = mat.id
								JOIN origin ON al.origin = origin.id
								JOIN clas ON al.clas = clas.id
								JOIN repo ON cons.repo = repo.id

								LEFT JOIN corp ON al.corp = corp.id
								LEFT JOIN repo AS repo2 ON al.prev_repo = repo2.id
								
								where sell == 1;
								""")


		db_data = cursor.fetchall()

		cursor.execute("SELECT MAX(prime) FROM cons")
		m = cursor.fetchone()[0]
		self.last_cons = m if m is not None else 0
		
		indx = self.indcs[1]
		i =0
		length = len(db_data)

		i2 = {self.date[:4]: 0}
		while i < length:
			year = db_data[i][indx['cdate']][:4]
			if year in data:
				#print(db_data[i])
				data[year]["e"].append(db_data[i])
				data[year]["الكل"].append(i2[year])
				data[year][db_data[i][indx['clas']]].append(i2[year])
				data[year][db_data[i][indx['repo']]].append(i2[year])
				i2[year] += 1
			else:
				data[year] = {"e": [], "srch":[]}
				i2[year] = 0
				for j in self.repo.keys():
					data[year][j] = []
				for j in self.clas.keys():
					data[year][j] = []
				i -= 1
			i += 1

		if self.date[:4] not in data:
			data[self.date[:4]] = {"e": [], "srch": []}
			for j in self.repo.keys():
				data[self.date[:4]][j] = []
			for j in self.clas.keys():
				data[self.date[:4]][j] = []

		self.cons = data
		#print(data)

	def fetch_corr(self, cursor=None):
		cursor = cursor if cursor else self.cursor
		data = {}
								
		cursor.execute("""SELECT corr.prime, emp.name, mat.name, al.sn, origin.name,
								al.price, al.quant, al.h_price, al.b_date, al.indoc, al.indoc_date,
								al.outdoc, al.outdate, clas.name, corp.name, al.prod_date, al.exp_date, corr.quant,
								corr.doc, corr.doc_date, repo2.name, repo.name, corr.id FROM corr 

								JOIN al ON corr.id = al.id
								JOIN emp ON al.emp = emp.id
								JOIN mat ON al.mat = mat.id
								JOIN origin ON al.origin = origin.id
								JOIN clas ON al.clas = clas.id
								JOIN repo ON corr.repo = repo.id
								LEFT JOIN corp ON al.corp = corp.id
								LEFT JOIN repo AS repo2 ON al.prev_repo = repo2.id;
								""")

		db_data = cursor.fetchall()

		cursor.execute("SELECT MAX(prime) FROM corr")
		m = cursor.fetchone()[0]
		self.last_corr = m if m is not None else 0
		
		indx = self.indcs[2]
		i =0
		length = len(db_data)
		i2 = {self.date[:4]: 0}
		while i < length:
			year = db_data[i][indx['cdate']][:4]
			if year in data:
				data[year]["e"].append(db_data[i])
				data[year]["الكل"].append(i2[year])
				data[year][db_data[i][indx['clas']]].append(i2[year])
				data[year][db_data[i][indx['repo']]].append(i2[year])
				i2[year] += 1
			else:
				data[year] = {"e": [], "srch":[]}
				i2[year] = 0
				for j in self.repo.keys():
					data[year][j] = []
				for j in self.clas.keys():
					data[year][j] = []
				i -= 1
			i += 1

		if self.date[:4] not in data:
			data[self.date[:4]] = {"e": [], "srch": []}
			for j in self.repo.keys():
				data[self.date[:4]][j] = []
			for j in self.clas.keys():
				data[self.date[:4]][j] = []

		self.corr = data

	def fetch_sold(self, cursor=None):
		cursor = cursor if cursor else self.cursor
		
		data = {}
		cursor.execute("""SELECT sold.prime, emp.name, mat.name, al.sn, origin.name, al.price, al.quant, al.h_price,
								al.b_date, al.indoc, al.indoc_date, al.outdoc, al.outdate, clas.name, corp.name,
								al.prod_date, al.exp_date, cons.quant, cons.nprice, cons.hprice, cons.doc, cons.doc_date,
								sold.quant, sold.price, sold.hprice, sold.doc, sold.doc_date,
								repo2.name, repo.name, sold.id2 FROM sold 
								JOIN al ON sold.id = al.id
								JOIN cons ON sold.id2 = cons.prime
								JOIN emp ON al.emp = emp.id
								JOIN mat ON al.mat = mat.id
								JOIN origin ON al.origin = origin.id
								JOIN clas ON al.clas = clas.id
								JOIN repo ON cons.repo = repo.id
								LEFT JOIN corp ON al.corp = corp.id
								LEFT JOIN repo AS repo2 ON al.prev_repo = repo2.id
								""")


		db_data = cursor.fetchall()

		cursor.execute("SELECT MAX(prime) FROM sold")
		m = cursor.fetchone()[0]
		self.last_sold = m if m is not None else 0
		
		indx = self.indcs[3]
		i =0
		length = len(db_data)
		i2 = {self.date[:4]: 0}
		while i < length:
			year = db_data[i][indx['sdate']][:4]
			if year in data:
				#print(db_data[i])
				data[year]["e"].append(db_data[i])
				data[year]['الكل'].append(i2[year])
				data[year][db_data[i][indx['clas']]].append(i2[year])
				data[year][db_data[i][indx['repo']]].append(i2[year])
				i2[year] += 1
			else:
				data[year] = {"e": [], "srch":[]}
				i2 [year] = 0
				for j in self.repo.keys():
					data[year][j] = []
				for j in self.clas.keys():
					data[year][j] = []
				i -= 1
			i += 1

		if self.date[:4] not in data:
			data[self.date[:4]] = {"e": [], "srch": []}
			for j in self.repo.keys():
				data[self.date[:4]][j] = []
			for j in self.clas.keys():
				data[self.date[:4]][j] = []

		self.sold = data

	def db_insert(self, d, cmt=True):
		indx = self.indcs[0]
		
		self.insert_new(d)		
		
		t = (d[indx['seq']], self.emp[d[indx['emp']]], self.mat[d[indx['mat']]], d[indx['serial']], self.origin[d[indx['origin']]],
			 d[indx['price']], d[indx['quant']], d[indx['hprice']], d[indx['bdate']], d[indx['indoc']], d[indx['indate']],
			 d[indx['outdoc']], d[indx['outdate']], self.clas[d[indx['clas']]], self.corp[d[indx['corp']]] if d[indx['corp']] else None,
			 d[indx['pdate']], d[indx['edate']], self.repo[d[indx['prepo']]] if d[indx['prepo']] else None, self.repo[d[indx['repo']]], 1)
			 
		self.cursor.execute("INSERT INTO al VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", t)
		if cmt: self.conn.commit()

	def full_export(self, prepo, repo, iD):
		if not repo in self.repo.keys():
			self.cursor.execute("INSERT INTO repo(name) VALUES(?)", (repo,))
			self.repo[repo] = self.cursor.lastrowid
			for i in list(self.al.keys()):
				self.al[i][repo] = [0]
			for i in list(self.cons.keys()):
				self.cons[i][repo] = []
			for i in list(self.corr.keys()):
				self.corr[i][repo] = []
			for i in list(self.sold.keys()):
				self.sold[i][repo] = []

		self.cursor.execute(f"UPDATE al SET repo = {self.repo[repo]}, prev_repo = {self.repo[prepo]} where id = {iD};")	   
		self.conn.commit()

	def partial_export(self, quant, hprice, iD):   # update quant, hprice of original row.
		self.cursor.execute(f"UPDATE al SET quant = {quant}, h_price = {hprice} where id = {iD};")	   
		self.conn.commit()

	def cons_corr(self, c, nd, q, seq):
		if c:
			self.cursor.execute("INSERT INTO cons(prime, id, quant, nprice, hprice, doc, doc_date, repo, sell) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", nd)
		else:
			self.cursor.execute("INSERT INTO corr(prime, id, quant, doc, doc_date, repo) VALUES(?, ?, ?, ?, ?, ?);", nd)

		self.cursor.execute(f"UPDATE al SET quant = {q} ,booln={1 if q else 0} where id = {seq};")
		self.conn.commit()

	def fetch_bdate(self, id):
		self.cursor.execute(f"SELECT b_date from al where id = {id};")
		return self.cursor.fetchone()[0]

	def sell(self, d, id):
		indx = self.indcs[3]
		t = [d[indx['seq']], d[indx['alseq']], d[indx['cseq']], d[indx['sprice']], d[indx['squant']], d[indx['s_hprice']], d[indx['sdoc']], d[indx['sdate']]]
		self.cursor.execute("INSERT INTO sold(prime, id, id2, price, quant, hprice, doc, doc_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", t)

		self.cursor.execute(f"UPDATE cons SET quant = {d[indx['cquant']]} , sell={1 if d[indx['cquant']] else 0} where prime = {str(id)};")
		self.conn.commit()

	def delete(self, id, emp, mat, origin, clas, repo, prepo, corp):
		try:
			self.cursor.execute("delete from al where id = "+ str(id) + ";")
		except Exception as e:
			print("fk")
			print(e)
			return False
		
		self.delete_old(emp, mat, origin, clas, repo, prepo, corp)
		self.conn.commit()
		return True


	def edit(self, d, old_d):
		indx = self.indcs[0]
		self.insert_new(d)		
		self.delete_old(old_d[indx['emp']], old_d[indx['mat']], old_d[indx['origin']], old_d[indx['clas']], old_d[indx['repo']], old_d[indx['prepo']], old_d[indx['corp']])
		
		t = (
			 self.emp[d[indx['emp']]],
			 self.mat[d[indx['mat']]],
			 d[indx['serial']],
			 self.origin[d[indx['origin']]],
			 d[indx['price']],
			 d[indx['quant']],
			 d[indx['hprice']],
			 d[indx['bdate']],
			 d[indx['indoc']],
			 d[indx['indate']],
			 d[indx['outdoc']],
			 d[indx['outdate']],			 
			 self.clas[d[indx['clas']]],
			 self.corp[d[indx['corp']]] if d[indx['corp']] else None,
			 d[indx['pdate']],
			 d[indx['edate']],
			 self.repo[d[indx['prepo']]] if d[indx['prepo']] else None,
		 )
			 
		self.cursor.execute(f"UPDATE al SET emp=?, mat=?, sn=?, origin=?, price=?, quant=?, h_price=?, b_date=?, indoc=?, indoc_date=?, outdoc=?, outdate=?, clas=?, corp=?, prod_date=?, exp_date=?, prev_repo=? where id={d[0]}", t)
		self.conn.commit()
		
		self.thrd = self.cons_corr_sold_thrd(self)
		self.thrd.start()
		
	def insert_new(self, d):
		indx = self.indcs[0]
		
		if not d[indx['emp']] in self.emp.keys():
			self.cursor.execute("INSERT INTO emp(name) VALUES(?)", (d[indx['emp']],))
			self.emp[d[indx['emp']]] = self.cursor.lastrowid
		if not d[indx['mat']] in self.mat.keys():
			self.cursor.execute("INSERT INTO mat(name) VALUES(?)", (d[indx['mat']],))
			self.mat[d[indx['mat']]] = self.cursor.lastrowid
		if not d[indx['corp']] in self.corp.keys():
			self.cursor.execute("INSERT INTO corp(name) VALUES(?)", (d[indx['corp']],))
			self.corp[d[indx['corp']]] = self.cursor.lastrowid
		if not d[indx['origin']] in self.origin.keys():
			self.cursor.execute("INSERT INTO origin(name) VALUES(?)", (d[indx['origin']],))
			self.origin[d[indx['origin']]] = self.cursor.lastrowid
		if not d[indx['clas']] in self.clas.keys():
			self.cursor.execute("INSERT INTO clas(name) VALUES(?)", (d[indx['clas']],))
			self.clas[d[indx['clas']]] = self.cursor.lastrowid
			for i in list(self.al.keys()):
				self.al[i][d[indx['clas']]] = [0]
			for i in list(self.cons.keys()):
				self.cons[i][d[indx['clas']]] = []
			for i in list(self.corr.keys()):
				self.corr[i][d[indx['clas']]] = []
			for i in list(self.sold.keys()):
				self.sold[i][d[indx['clas']]] = []
		if not d[indx['repo']] in self.repo.keys():
			self.cursor.execute("INSERT INTO repo(name) VALUES(?)", (d[indx['repo']],))
			self.repo[d[indx['repo']]] = self.cursor.lastrowid
			for i in list(self.al.keys()):
				self.al[i][d[indx['repo']]] = [0]
			for i in list(self.cons.keys()):
				self.cons[i][d[indx['repo']]] = []
			for i in list(self.corr.keys()):
				self.corr[i][d[indx['repo']]] = []
			for i in list(self.sold.keys()):
				self.sold[i][d[indx['repo']]] = []
		if d[indx['prepo']] and not d[indx['prepo']] in self.repo.keys():
			self.cursor.execute("INSERT INTO repo(name) VALUES(?)", (d[indx['prepo']],))
			self.repo[d[indx['prepo']]] = self.cursor.lastrowid
			for i in list(self.al.keys()):
				self.al[i][d[indx['prepo']]] = [0]
			for i in list(self.cons.keys()):
				self.cons[i][d[indx['prepo']]] = []
			for i in list(self.corr.keys()):
				self.corr[i][d[indx['prepo']]] = []
			for i in list(self.sold.keys()):
				self.sold[i][d[indx['prepo']]] = []

	def new_clas(self, clas):
		if not clas in self.clas.keys():
			self.cursor.execute("INSERT INTO clas(name) VALUES(?)", (clas,))
			self.clas[clas] = self.cursor.lastrowid
			for i in list(self.al.keys()):
				self.al[i][clas] = [0]
			for i in list(self.cons.keys()):
				self.cons[i][clas] = []
			for i in list(self.corr.keys()):
				self.corr[i][clas] = []
			for i in list(self.sold.keys()):
				self.sold[i][clas] = []

	def delete_old(self, emp, mat, origin, clas, repo, prepo, corp):
		try:
			self.cursor.execute("delete from emp where id = "+ str(self.emp[emp]) + ";")
			del self.emp[emp]
		except:
			pass
		try:
			self.cursor.execute("delete from mat where id = "+ str(self.mat[mat]) + ";")
			del self.mat[mat]
		except:
			pass
		try:
			self.cursor.execute("delete from origin where id = "+ str(self.origin[origin]) + ";")
			del self.origin[origin]
		except:
			pass
		try:
			self.cursor.execute("delete from clas where id = "+ str(self.clas[clas]) + ";")
			del self.clas[clas]
		except:
			pass
		try:
			self.cursor.execute("delete from repo where id = " + str(self.repo[repo]) + ";")
			del self.repo[repo]
		except:
			pass
	
		try:
			self.cursor.execute("delete from repo where id = " + str(self.repo[prepo]) + ";")
			del self.repo[prepo]
		except:
			pass
			
		try:
			self.cursor.execute("delete from corp where id = " + str(self.corp[corp]) + ";")
			del self.corp[corp]
		except:
			pass

	def check_integrity(self, t, doc, date):
		dic = {
			0 : {'table': 'al', 'doc': 'indoc', 'date': 'indoc_date'},
			1 : {'table': 'cons', 'doc': 'doc', 'date': 'doc_date'},
			2 : {'table': 'corr', 'doc': 'doc', 'date': 'doc_date'},
			3 : {'table': 'sold', 'doc': 'doc', 'date': 'doc_date'}
		}
		self.cursor.execute(f"SELECT * FROM {dic[t]['table']} WHERE {dic[t]['doc']} = ? AND {dic[t]['date']} = ?", (doc, date))
		if self.cursor.fetchone() : return False
		else: return True
		

	class cons_corr_sold_thrd(QThread):
		def __init__(self, db):
			super().__init__(None)
			self.db = db
		def run(self):
			conn = sqlite3.connect("db6.db")
			cursor = conn.cursor()
			#self.db.fetch_corr()
			#self.db.fetch_sold()
			self.db.fetch_cons(cursor)
			self.db.fetch_corr(cursor)
			self.db.fetch_sold(cursor)
			print("Wowwwwwwwwww")
			
#print(fetch1())
#clasf_lst = ["اثاث", "كهربائيات", "ادوات مكتبية", "مواد قابلة للإشتعال"]
#departs_lst = ["المخزن الرئيسي", "قسم المختبر", "قسم التحليلات", "قسم الاشعة"]
#start = time.time()
#x = fetch_al(departs_lst, clasf_lst)
#end = time.time()

#execution_time = end - start
#print(f"Execution time: {execution_time:.6f} seconds")
#print(x)
