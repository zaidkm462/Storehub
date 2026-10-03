import arabic_reshaper
from bidi.algorithm import get_display
import db2

dic = {}


def generate(path, db, mat, repo, clas, rtype, st, end, cols, hdr):
    from fpdf import FPDF
	
    global dic
    pdf = FPDF(orientation='L', format='A4')
    pdf.set_auto_page_break(auto=True, margin=0)
    pdf.l_margin = 2.5
    pdf.b_margin = 2.5

    pdf.add_font("Noto", fname="Noto.ttf", uni=True)
    
    dic = {
    0: {
    	"hdr": hdr[0],
    	"hdr_indx": cols[0],
    	"tot_indx": 7,
    	"tit": "تقرير الموجودات",
    	"sum": "المبلغ الأجمالي للموجودات: ",
    	"ds": db.al,
    	'clas': 13,
    	'dt': 10
    },
    1: {
    	"hdr": hdr[1],
    	"hdr_indx": cols[1],
    	"tot_indx": 19,
    	"tit": "تقرير المستهلكات",
    	"sum": "المبلغ الأجمالي للمستهلكات: ",
    	"ds": db.cons,
    	'clas': 13,
    	'dt': 21
    },
    2: {
    	"hdr": hdr[2],
    	"hdr_indx": cols[2],
    	"tot_indx": None,
    	"tit": "تقرير المتلفات",
    	"sum": "المبلغ الأجمالي للمتلفات: ",
    	"ds": db.corr,
    	'clas': 13,
    	'dt': 19
    },
    3: {
    	"hdr": hdr[3],
    	"hdr_indx": cols[3],
    	"tot_indx": 24,
    	"tit": "تقرير المبيعات",
    	"sum": "المبلغ الأجمالي للمبيعات: ",
    	"ds": db.sold,
    	'clas': 13,
    	'dt': 26
    }

    }
    
    all_yrs = sorted(set(list(db.al.keys()) + list(db.cons.keys()) + list(db.corr.keys()) + list(db.sold.keys()))) 
    
    if rtype == 0:
    	yrs = all_yrs
    else:
        yrs  = [y for y in all_yrs if y >= st[:4] and y <= end[:4]]
 
    for y in yrs:
        pdf.add_page()
        text = arabify("تقرير سنة "+ y)
        pdf.set_font("Noto", size=18)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(297, 10, text, ln=True, align='C')
        pdf.ln(10)
        gen_exist(pdf, db, y, 0, mat, repo, clas, rtype, st, end)
        gen_exist(pdf, db, y, 1, mat, repo, clas, rtype, st, end)
        gen_exist(pdf, db, y, 2, mat, repo, clas, rtype, st, end)
        gen_exist(pdf, db, y, 3, mat, repo, clas, rtype, st, end)

    pdf.output(path+"/"+"تقرير "+".pdf")

def arabify(text):
    return get_display(arabic_reshaper.reshape(text))

def gen_exist(pdf, db, year, n, mat, repo, clas, rtype, st, end):
    cell_width = 292/len(dic[n]['hdr'])  #48.6 if n <= 1 else 58.3
    line_height = 10
    text = arabify(dic[n]['tit'])
    pdf.set_font("Noto", size=18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(297, 10, text, ln=True, align='C')
    pdf.ln(10)
    
    # check the whole year is empty.
    if  not year in dic[n]['ds'] or len(dic[n]['ds'][year]['e']) < (2 if not n else 1):
        pdf.set_font("Noto", size=16)
        pdf.cell(285, 10, arabify(str("لا يوجد عناصر متبقية!")), ln=True, align='R')
        pdf.ln(5)
        return
    
    # check and continue if repo is empty.
    if repo  == "الكل":
        repos = db.repo.keys()
    else:
        repos = [repo]
    for r in repos:
        data = {}
        rf = dic[n]['ds'][year][r]
        if len(rf) < (2 if not n else 1):
            continue

        # print repo name.
        pdf.set_font("Noto", size=16)
        pdf.cell(285, 10, arabify(str(r)), ln=True, align='R')
        pdf.ln(5)
		
        if clas == "الكل":
            clases = db.clas.keys()
        else:
            clases = [clas]
        # iterate through repo data and classify them according to class.
        for i in rf[1 if not n else 0:]:
            var = dic[n]['ds'][year]['e'][i][dic[n]['clas']]                  
            if not var in clases:
                continue
            if not var in data:
                data[var] = [dic[n]['ds'][year]['e'][i]]
            else:
                data[var].append(dic[n]['ds'][year]['e'][i])

        # iterate through repo classes.
        s = 0
        for c in data.keys():
            # print class name.
            pdf.set_font("Noto", size=16)
            pdf.cell(275, 10, arabify(str(c)), ln=True, align='R')
            pdf.ln(5)

            # print header.
            pdf.set_font("Noto", size=11)
            for c2 in dic[n]['hdr']:
                pdf.cell(cell_width, 10, arabify(c2), border=1, align='C')
            pdf.ln()
            
            # iterate through data of current class>
            s = 0
            for i in data[c]:   # for each row.
                dt = i[dic[n]['dt']]
                if mat != "الكل" and i[2 if not n else 1] != mat:
                    continue
                if not match_date(rtype, st, end, dt): continue
                
                wrapped_columns = []   # each cell will be diveded into lines.
                max_lines = 1
                
                if n != 2 : s+= i[dic[n]['tot_indx']]
                else: s+= i[5] * i[17]
                
                for j in dic[n]['hdr_indx']:
                    value = str(i[j])
                    lines = wrap_text(value, int(cell_width/1.94))
                    wrapped_columns.append(lines)
                    max_lines = max(max_lines, len(lines))                	
                    
                # Pad all columns to max_lines.
                for idx in range(len(wrapped_columns)):  # number of cells (cell 0 -> idx=0). 
                    lines = wrapped_columns[idx]
                    if len(lines) < max_lines:
                        lines += [''] * (max_lines - len(lines))
                    wrapped_columns[idx] = lines

                needed_height = max_lines * line_height
                if pdf.get_y() + needed_height > pdf.h - pdf.b_margin: pdf.add_page()
                
                # Store current position
                x_start = pdf.get_x()
                y_start = pdf.get_y()

                # Draw each column manually
                for col_idx, lines in enumerate(wrapped_columns):
                    x = x_start + col_idx * cell_width
                    y = y_start
                    pdf.set_xy(x, y)
                    for line in lines:
                        pdf.cell(cell_width, line_height, arabify(line), border=0, align='C')
                        y += line_height
                        pdf.set_xy(x, y)

                    # Draw border rectangle around full cell height
                    pdf.rect(x, y_start, cell_width, max_lines * line_height)

                # Move to next row
                pdf.set_y(y_start + max_lines * line_height)

            pdf.set_font("Noto", size=14)
            pdf.cell(285, 20, arabify(dic[n]['sum'] + str(s)), ln=True, align='R')
            pdf.ln()




def wrap_text(text, max_len):
    lines = []
    while len(text) > max_len:
        split_pos = text.rfind(' ', 0, max_len)
        if split_pos == -1:
            split_pos = max_len
        lines.append(text[:split_pos])
        text = text[split_pos:].lstrip()
    lines.append(text)
    return lines


def match_date(rtype, start, end, dt2):
    if rtype == 1:         
        if dt2[:4] == start[:4] and dt2[5:7] < start[5: 7]: return False
        elif dt2[:4] == end[:4] and dt2[5:7] > end[5: 7]: return False        
               
        if dt2[5:7] == start[5:7] and dt2[8:10] < start[8: 10]: return False
        elif dt2[5:7] == end[5:7] and dt2[8:10] > end[8: 10]: return False
                  
    return True


#db3 = db2.DB("2025")
#generate("C://users/zaid/desktop", db3)


