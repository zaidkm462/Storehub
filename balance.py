import arabic_reshaper
from bidi.algorithm import get_display
import db2

dic = {}

def arabify(text):
    return get_display(arabic_reshaper.reshape(text))

def generate(path, db, mat, repo, clas, rtype, start, end):
    global dic
    dic = {
          0: {'mat': 2, 'date': 10, 'clas': 13, 'q': 6, 'ds': db.al},
          1: {'mat': 2, 'date': 21, 'clas': 13 , 'q': 17, 'ds': db.cons},
          2: {'mat': 2, 'date': 19, 'clas': 13 , 'q': 17, 'ds': db.corr},
          3: {'mat': 2, 'date': 26, 'clas': 13 , 'q': 22, 'ds': db.sold}
}

    from fpdf import FPDF	
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=0)
    pdf.b_margin = 2.5
    pdf.add_font("Noto", fname="Noto.ttf", uni=True)
    pdf.add_page()
   
    
    text = arabify("رصيد " + mat if mat != "الكل" else "رصيد جميع المواد")
    pdf.set_font("Noto", size=18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(pdf.w, 10, text, ln=True, align='C')
    pdf.ln(10)
    
    mats = []
    if mat == "الكل": mats = list(db.mat.keys())
    else: mats = [mat]
    
    for m in mats: gen_mat(pdf, m, repo, clas, rtype, start, end)
    
    

    pdf.output(path+"/"+"رصيد "+".pdf")

def gen_mat(pdf, mat, repo, clas, rtype, start, end):   
    # mat name print.    
    text = arabify(mat)
    pdf.set_font("Noto", size=16)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(196, 10, text, ln=True, align='R')
    
    print_right_16(pdf, "الموجودات : " + str(get_count(0, mat, repo, clas, rtype, start, end)))
    print_right_16(pdf, "المستهلكات : " + str(get_count(1, mat, repo, clas, rtype, start, end)))
    print_right_16(pdf, "المتلفات : " + str(get_count(2, mat, repo, clas, rtype, start, end)))
    print_right_16(pdf, "المبيعات : " + str(get_count(3, mat, repo, clas, rtype, start, end)))
    
    pdf.ln(10)
    
def get_count(t, mat, repo, clas, rtype, start, end):
    global dic
    count = 0
    
    all_yrs = list(dic[t]['ds'].keys())
    if rtype == 0: yrs = all_yrs
    else: yrs  = [y for y in all_yrs if y >= start[:4] and y <= end[:4]]
    
    for year in yrs:
        
        if not year in dic[t]['ds'].keys(): continue
        
        for i in dic[t]['ds'][year][repo]:
            row = dic[t]['ds'][year]['e'][i]
            
            if clas != "الكل" and row[dic[t]['clas']] != clas: continue
            
            if not match_date(rtype, start, end, row[dic[t]['date']]): continue
            
            if row[dic[t]['mat']] != mat: continue
            
            count += row[dic[t]['q']]
    return count
        

def match_date(rtype, start, end, dt2): 
    if rtype == 1:         
        if dt2[:4] == start[:4] and dt2[5:7] < start[5: 7]: return False
        elif dt2[:4] == end[:4] and dt2[5:7] > end[5: 7]: return False        
               
        if dt2[5:7] == start[5:7] and dt2[8:10] < start[8: 10]: return False
        elif dt2[5:7] == end[5:7] and dt2[8:10] > end[8: 10]: return False
                  
    return True

def print_right_16(pdf, txt):
    text = arabify(txt)
    pdf.set_font("Noto", size=16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(190, 10, text, ln=True, align='R')


"""
db3 = db2.DB("2025")
mat = "مواد تلميع"
repo = "الكل"
clas = "الكل"
generate(".", db3, mat, repo, clas, 0, "2024-01-01")"""

    
    

