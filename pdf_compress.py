import fitz
import os
from PIL import Image
from glob import glob
from time import time
import glob
import fitz
import os
import shutil


def pdftojpg(pdffile):
    doc = fitz.open(pdffile)
    width, height = fitz.PaperSize("a4")
    
    totaling = doc.pageCount
    
    if not os.path.exists("pdf"):  #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs("pdf")
    for pg in range(totaling):
        page = doc[pg]
        zoom = int(500)
        rotate = int(0)
        print(page)
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
    
        lurl='pdf/%s.jpg' % str(pg+1)
        pm.writePNG(lurl)
    doc.close()

def pictopdf(newpdf):
    doc = fitz.open()
    for img in sorted(glob.glob("pdf/*")):  # 读取图片，确保按文件名排序
        imgdoc = fitz.open(img)                 # 打开图片
        pdfbytes = imgdoc.convertToPDF()        # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)                   # 将当前页插入文档
    if os.path.exists(newpdf):        # 若文件存在先删除
        os.remove(newpdf)
    doc.save(newpdf)                   # 保存pdf文件
    doc.close()
    shutil.rmtree("pdf")

def getFileName(filepath):

    file_list = []

    for root,dirs,files in os.walk(filepath):
        for filespath in files:
            if filespath[-3:]=="pdf":
                file_list.append(os.path.abspath(os.path.join(root,filespath)))

    return file_list


pdf_file_list=getFileName(".")

for file in pdf_file_list:
    pdftojpg(file)
    pictopdf("compress_"+os.path.basename(file))

