#!/usr/bin/env python3
"""Editable A5 interior generator for A Little Puzzle Book — Volume One.
Install: pip install reportlab
Run beside puzzle_book_editable_data.json: python a_little_puzzle_book_source.py
Edit the JSON data and PALETTE below to customize the puzzles and visual identity.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import os, json

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/"puzzle_book_editable_data.json").read_text(encoding="utf-8"))
SUDOKUS, WORDSEARCHES=DATA["sudokus"],DATA["wordsearches"]
PALETTE={"ivory":"#F7F3EB","brown":"#342D27","taupe":"#9A8A79","beige":"#DED6CA","sage":"#7D8974"}
W,H=A5
IVORY,BROWN,TAUPE,BEIGE,SAGE=[HexColor(PALETTE[k]) for k in ("ivory","brown","taupe","beige","sage")]
def register_fonts():
    root="/usr/share/fonts/truetype/dejavu/"
    for file,name in [("DejaVuSerif.ttf","Serif"),("DejaVuSerif-Bold.ttf","SerifBold"),
                      ("DejaVuSans.ttf","Sans"),("DejaVuSans-Bold.ttf","SansBold")]:
        if os.path.exists(root+file):
            try: pdfmetrics.registerFont(TTFont(name,root+file))
            except: pass
    n=pdfmetrics.getRegisteredFontNames()
    return ("Serif" if "Serif" in n else "Times-Roman",
            "SerifBold" if "SerifBold" in n else "Times-Bold",
            "Sans" if "Sans" in n else "Helvetica",
            "SansBold" if "SansBold" in n else "Helvetica-Bold")
F,FB,S,SB=register_fonts()
def t(c,x,y,value,size=8,font=S,color=BROWN,align="left"):
    c.setFillColor(color); c.setFont(font,size)
    {"left":c.drawString,"center":c.drawCentredString,"right":c.drawRightString}[align](x,y,str(value))
def bg(c):
    c.setFillColor(IVORY); c.rect(0,0,W,H,fill=1,stroke=0)
def header(c,p):
    t(c,13*mm,H-14*mm,"A LITTLE PUZZLE BOOK",6,SB,TAUPE)
    t(c,W-13*mm,H-14*mm,"VOL. 01",6,S,TAUPE,"right")
    c.setStrokeColor(BEIGE); c.line(13*mm,H-17*mm,W-13*mm,H-17*mm)
    t(c,W/2,7*mm,f"{p:02d}",6,S,TAUPE,"center")
def frame(c):
    c.setStrokeColor(BEIGE); c.rect(10*mm,12*mm,W-20*mm,H-24*mm,fill=0,stroke=1)
def intro(c,p,title,lines):
    header(c,p); y=H-36*mm
    t(c,13*mm,y,"A GENTLE INTRODUCTION",7,SB,TAUPE); t(c,13*mm,y-17*mm,title,25,FB)
    c.setStrokeColor(TAUPE); c.line(13*mm,y-23*mm,38*mm,y-23*mm); y-=43*mm
    for i,line in enumerate(lines):
        t(c,13*mm,y,f"0{i+1}",8,SB,TAUPE)
        words=line.split(); rows=[]; row=""
        for word in words:
            if len(row+" "+word)>43: rows.append(row); row=word
            else: row=(row+" "+word).strip()
        if row: rows.append(row)
        for j,row in enumerate(rows): t(c,25*mm,y-j*5*mm,row,9)
        y-=max(21*mm,(len(rows)+1)*5*mm+10*mm)
def divider(c,p,n,title,sub):
    header(c,p); c.setStrokeColor(BEIGE); c.rect(21*mm,22*mm,W-42*mm,H-34*mm,fill=0,stroke=1)
    t(c,W/2,H/2+27*mm,"COLLECTION  "+n,8,SB,TAUPE,"center")
    t(c,W/2,H/2+8*mm,title,32,FB,BROWN,"center")
    c.setStrokeColor(TAUPE); c.line(W/2-14*mm,H/2-1*mm,W/2+14*mm,H/2-1*mm)
    t(c,W/2,H/2-13*mm,sub,10,F,TAUPE,"center")
def sudoku(c,p,d):
    header(c,p); top=H-30*mm
    t(c,13*mm,top,f"PUZZLE {d['number']:02d}",6,SB,TAUPE)
    t(c,13*mm,top-13*mm,"Sudoku",24,FB)
    t(c,W-13*mm,top-11*mm,d["difficulty"].upper(),7,SB,
      SAGE if d["difficulty"]=="Easy" else TAUPE if d["difficulty"]=="Medium" else BROWN,"right")
    t(c,13*mm,top-20*mm,"Complete each row, column and 3 × 3 box with 1–9.",7,S,TAUPE)
    size=116*mm; x=(W-size)/2; y=top-34*mm-size; cell=size/9
    c.setFillColor(HexColor("#F2EDE4"))
    for r in range(9):
        if r%3==1: c.rect(x,y+(8-r)*cell,size,cell,fill=1,stroke=0)
    for i in range(10):
        c.setStrokeColor(BROWN if i%3==0 else BEIGE); c.setLineWidth(1.15 if i%3==0 else .38)
        c.line(x+i*cell,y,x+i*cell,y+size); c.line(x,y+i*cell,x+size,y+i*cell)
    for r,row in enumerate(d["grid"]):
        for j,v in enumerate(row):
            if v: t(c,x+(j+.5)*cell,y+(8-r+.5)*cell-4.1,v,12,S)
def wordsearch(c,p,d):
    header(c,p); top=H-30*mm
    t(c,13*mm,top,f"PUZZLE {d['number']:02d}",6,SB,TAUPE)
    t(c,13*mm,top-13*mm,d["theme"],20,FB)
    t(c,13*mm,top-20*mm,"Find each word. Look in all directions, forwards or backwards.",7,S,TAUPE)
    size=104*mm; x=(W-size)/2; y=top-31*mm-size; cell=size/12
    c.setStrokeColor(BEIGE); c.rect(x,y,size,size,fill=0,stroke=1)
    for r,row in enumerate(d["grid"]):
        for j,ch in enumerate(row): t(c,x+(j+.5)*cell,y+(11-r+.5)*cell-2.8,ch,8.2,SB)
    t(c,13*mm,y-10*mm,"WORD LIST",6.5,SB,TAUPE)
    c.setStrokeColor(BEIGE); c.line(13*mm,y-12*mm,W-13*mm,y-12*mm)
    mid=(len(d["words"])+1)//2; start=y-19*mm
    for i,w in enumerate(d["words"][:mid]): t(c,13*mm,start-i*5*mm,w.title(),7.2)
    for i,w in enumerate(d["words"][mid:]): t(c,W/2+2*mm,start-i*5*mm,w.title(),7.2)
def build():
    out=HERE/"a_little_puzzle_book_volume_one.pdf"; c=canvas.Canvas(str(out),pagesize=A5)
    c.setTitle("A Little Puzzle Book — Volume One"); c.setAuthor("Independent Puzzle Edition")
    p=1; bg(c); frame(c)
    t(c,W/2,H-47*mm,"A SMALL COLLECTION FOR SLOWER MOMENTS",7,SB,TAUPE,"center")
    t(c,W/2,H-88*mm,"A LITTLE",31,F,BROWN,"center"); t(c,W/2,H-104*mm,"PUZZLE BOOK",32,FB,BROWN,"center")
    c.setStrokeColor(TAUPE); c.line(W/2-16*mm,H-114*mm,W/2+16*mm,H-114*mm)
    t(c,W/2,H-129*mm,"VOLUME ONE",8,SB,TAUPE,"center")
    t(c,W/2,H-143*mm,"SUDOKU  ·  WORD SEARCH",8,S,BROWN,"center")
    t(c,W/2,23*mm,"AN INDEPENDENT PUZZLE EDITION",6.5,S,BROWN,"center"); c.showPage(); p+=1
    bg(c); intro(c,p,"Sudoku",["A Sudoku grid has nine rows and nine columns, divided into nine smaller 3 × 3 boxes.","Fill every empty square with a number from 1 to 9.","Each number must appear exactly once in every row, every column and every 3 × 3 box.","Use the existing numbers as clues. No guessing is needed; work patiently and let each clue narrow your choices."]); c.showPage(); p+=1
    bg(c); intro(c,p,"Word Search",["Find each word from the list hidden in the letter grid.","Words may run horizontally, vertically or diagonally.","They may read forwards or backwards. Each listed word appears once.","Circle or lightly mark each word as you find it."]); c.showPage(); p+=1
    bg(c); divider(c,p,"01","Sudoku",""); c.showPage(); p+=1
    for d in SUDOKUS: bg(c); sudoku(c,p,d); c.showPage(); p+=1
    bg(c); divider(c,p,"02","Word Search",""); c.showPage(); p+=1
    for d in WORDSEARCHES: bg(c); wordsearch(c,p,d); c.showPage(); p+=1
    bg(c); frame(c)
    t(c,W/2,H/2+5*mm,"Thank you for spending",21,F,BROWN,"center"); t(c,W/2,H/2-5*mm,"a little time here.",21,F,BROWN,"center")
    c.setStrokeColor(TAUPE); c.line(W/2-12*mm,H/2-16*mm,W/2+12*mm,H/2-16*mm)
    t(c,W/2,H/2-30*mm,"BRAND NAME",7,S,TAUPE,"center"); t(c,W/2,23*mm,"VOLUME ONE  ·  SUDOKU & WORD SEARCH",6.5,SB,BROWN,"center")
    c.showPage(); c.save(); print("Created",out)
if __name__=="__main__":
    assert len(SUDOKUS)==22 and len(WORDSEARCHES)==12
    build()
