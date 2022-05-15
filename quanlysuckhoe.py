

import datetime


import os

import matplotlib
import tkcalendar as tkc

from re import L
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
import numpy as np
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pandas as pd
import openpyxl
from PIL import ImageTk, Image
from pandas import ExcelFile, options

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import cx_Oracle


matplotlib.use('TkAgg')
mydb = cx_Oracle.connect('hr', 'hr', 'localhost/orcl')
mycursor = mydb.cursor()
root = Tk()
root.geometry('1080x560')
root.iconbitmap(r"img/6166.ico")
root.title('TRANG SỨC KHỎE')

my_font = "Helvetica 10"
userlogin = True


class App:
    def __init__(self, master):
        self.master = master
        self.master.resizable(1, 1)
        self.navmenu = LabelFrame(self.master)
        self.navmenu.pack(fill=X)
        self.content = LabelFrame(self.master)
        self.content.pack(fill=BOTH, expand=TRUE)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        self.frames = {}

        self.home_button = Button(
            self.navmenu, text="TRANG CHỦ", relief=RIDGE,  bd=0, font=my_font, width=20, command=lambda: self.show_frame(home_page))
        self.home_button.pack(side=LEFT, padx=10, expand=True)

        self.kb_button = Button(
            self.navmenu, text="KHAI BÁO Y TẾ", relief=RIDGE,  bd=0, font=my_font, width=20, command=lambda: self.show_frame(khaibaoyte_page))
        self.kb_button.pack(side=LEFT, padx=10, expand=True)

        self.dktvx_button = Button(
            self.navmenu, text="ĐĂNG KÝ TIÊM VÁC XIN", relief=RIDGE,  bd=0, font=my_font, width=20, command=lambda: self.show_frame(dangkytiem_page))
        self.dktvx_button.pack(side=LEFT, padx=10, expand=True)
        self.dk()
        listpage = [home_page, khaibaoyte_page,
                    dangkytiem_page, thongtinsinhvien, thongtinsuckhoe]
        for F in listpage:

            frame = F(self.content, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(home_page)

    def dk(self):
        self.tkf = Frame(self.navmenu)
        self.tko = Frame(self.navmenu)
        self.log_button = Button(
            self.tkf, text="ĐĂNG NHẬP", relief=RIDGE,  bd=0, font=my_font, width=15, command=self.dang_nhap)
        self.log_button.pack(side=RIGHT, padx=5, pady=10, expand=True)

        self.reg_button = Button(
            self.tkf, text="ĐĂNG KÝ", relief=RIDGE,  bd=0, font=my_font, width=15)
        self.reg_button.pack(side=RIGHT, padx=5, pady=10, expand=True)
        self.drop = Menubutton(self.tko, text="User",
                               relief=RIDGE,  bd=0, font=my_font, width=20)
        self.cmenu = Menu(self.drop, tearoff=0)
        self.cmenu.add_command(label="Thông tin sinh viên",
                               command=lambda: self.show_frame(thongtinsinhvien))
        self.cmenu.add_command(label="Thông tin sức khỏe",
                               command=lambda: self.show_frame(thongtinsuckhoe))
        self.cmenu.add_command(label="Đăng Xuất", command=self.dangxuat)
        self.drop["menu"] = self.cmenu
        self.drop.pack()

        global userlogin
        if userlogin:
            self.tkf.pack_forget()
            self.tko.pack()

        else:
            self.tko.pack_forget()
            self.tkf.pack()
            self.drop.destroy()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def dangxuat(self):
        global userlogin
        userlogin = False
        self.dk()

    def dang_nhap(self):
        global windr
        global main1
        main1 = Toplevel()
        windr = login_page(main1)
        main1.grab_set()
        main1.update()


class login_page:
    def __init__(self, top=None):
        self.top = top
        self.top.resizable(1, 1)
        self.tieu_lab = Label(self.top, text="Đăng Nhập", font=16)
        self.tieu_lab.pack(side=TOP, fill=BOTH, pady=15, padx=15)
        self.tab1 = ttk.Frame(self.top)
        self.tab1.pack(padx=5, pady=5)
        self.cont = Frame(self.tab1)
        self.cont.pack(side=TOP, expand=True)
        self.dang_lab = Label(self.cont, text="Tài Khoản", font=8)
        self.dang_lab.grid(row=1, column=0, padx=5, pady=5)
        self.taikhoan = StringVar()
        self.tk_entr = ttk.Entry(
            self.cont, textvariable=self.taikhoan, width=25)
        self.tk_entr.grid(row=1, column=1, )
        self.mk_lab = Label(self.cont, text="Mật Khẩu", font=8)
        self.mk_lab.grid(row=2, column=0, )
        self.matkhau = StringVar()
        self.mkk_entr = ttk.Entry(
            self.cont, textvariable=self.matkhau, show="*", width=25)
        self.mkk_entr.grid(row=2, column=1, padx=5, pady=5)
        self.but1 = ttk.Button(self.tab1, text='Đăng Nhập',
                               command=self.log_in, width=20)
        self.but1.pack(side=LEFT, expand=True, pady=10)

    def log_in(self):
        global userlogin
        userlogin = True


class home_page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Trang Chủ",).pack()
        lst = [("10/2001", 50), ("11/2021", 200), ("12/2021", 550)]
        data = self.convert_data(lst)
        (data)
        languages = data.keys()
        popularity = data.values()

        # create a figure
        figure = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.bar(languages, popularity)
        axes.set_title('Danh Sách Lượng Người Nghiễm Bệnh')
        axes.set_ylabel('Người Nhiễm Bệnh')

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def convert_data(self, lst):
        lst = np.array(lst)
        lits = lst.flatten()
        res_dct = {lits[i]: int(lits[i + 1]) for i in range(0, len(lits), 2)}
        return res_dct


class khaibaoyte_page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        ngang = 15
        Modues = [("Có", 1), ("Không", 0)]
        self.thoigiandichuyen = IntVar()
        self.thoigiantrieuchung = IntVar()
        self.thoigiantiepxucn = IntVar()
        self.thoigiantiepxucnn = IntVar()
        self.thoigiantiepxucnb = IntVar()
        self.label = Label(self, text="KHAI BÁO Y TẾ", font=my_font)
        self.label.pack(fill=X)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=True)

        self.khaibao = Frame(self)
        self.khaibao.pack()
        self.chuandoan = Frame(self)
        self.chuandoan.pack()
        self.notebook.add(self.khaibao, text="KHAI BÁO COVID")
        self.notebook.add(self.chuandoan, text="KHAI BÁO SỨC KHỎE")
        self.thoigiandichuyen_l = Label(
            self.khaibao, text="Trong vòng 14 ngày qua, Anh/chị có đến khu vức, tỉnh thành phố, quốc gia/vùng lãnh thổ nào(có thể đi qua nhiều nơi) ", anchor=W)
        self.thoigiandichuyen_l.pack(fill=X, padx=ngang)
        for text, mode in Modues:
            Radiobutton(self.khaibao, text=text, variable=self.thoigiandichuyen, value=mode,
                        ).pack(anchor=W, padx=ngang)

        self.thoigiantrieuchung_l = Label(
            self.khaibao, text="Trong vòng 14 ngày qua, Anh/chị có thấy xuất hiện ít nhất 1 trong các dấu hiện sốt, ho, khó thở, viêm phổi, đau họng, mệt mỏi thay đổi vị giác không ", anchor=W)
        self.thoigiantrieuchung_l.pack(fill=X, padx=ngang)
        for text, mode in Modues:
            Radiobutton(self.khaibao, text=text, variable=self.thoigiantrieuchung, value=mode,
                        ).pack(anchor=W, padx=ngang)
        self.thoigiantiepxucn_l = Label(
            self.khaibao, text="Trong vòng 14 ngày qua, Anh/chị có tiếp xúc với người nhiễm Covid-19 không", anchor=W)
        self.thoigiantiepxucn_l.pack(fill=X, padx=ngang)
        for text, mode in Modues:
            Radiobutton(self.khaibao, text=text, variable=self.thoigiantiepxucn, value=mode,
                        ).pack(anchor=W, padx=ngang)

        self.thoigiantiepxucnn_l = Label(
            self.khaibao, text="Trong vòng 14 ngày qua, Anh/chị có tiếp xúc với người từ nước có bệnh Covid-19", anchor=W)
        self.thoigiantiepxucnn_l.pack(fill=X, padx=ngang)
        for text, mode in Modues:
            Radiobutton(self.khaibao, text=text, variable=self.thoigiantiepxucnn, value=mode,
                        ).pack(anchor=W, padx=ngang)
        self.thoigiantiepxucnb_l = Label(
            self.khaibao, text="Trong vòng 14 ngày qua, Anh/chị có tiếp xúc với người có biểu hiện ho sốt, ho, khó thỏ, viêm phổi", anchor=W)
        self.thoigiantiepxucnb_l.pack(fill=X, padx=ngang)
        for text, mode in Modues:
            Radiobutton(self.khaibao, text=text, variable=self.thoigiantiepxucnb, value=mode,
                        ).pack(anchor=W, padx=ngang)
        self.send_kb = Button(self.khaibao, text="Gửi tờ khai", font=my_font)
        self.send_kb.pack()
# ========================================================================================================================
        self.nhietdo_l = Label(self.chuandoan, text="Chỉ số nhiệt độ")
        self.nhietdo_l.pack()
        self.nhietdo_e = Entry(self.chuandoan)
        self.nhietdo_e.pack()
        self.cactrieuchung = LabelFrame(self.chuandoan, text="Các triệu trứng")
        self.cactrieuchung.pack(side=LEFT, fill=BOTH, expand=True)

        self.ho = IntVar()
        self.sot = IntVar()
        self.dauhong = IntVar()
        self.nghetmui = IntVar()
        self.sung = IntVar()
        self.daudau = IntVar()
        self.khochiu = IntVar()
        self.khotho = IntVar()
        self.hatxit = IntVar()
        c1 = Checkbutton(self.cactrieuchung, text='Ho',
                         variable=self.ho, onvalue=1, offvalue=0, command=self.chuandoanbenh, anchor=W)
        c1.grid(column=0, row=0)
        c2 = Checkbutton(self.cactrieuchung, text='Sốt nhẹ', variable=self.sot,
                         onvalue=1, offvalue=0, command=self.chuandoanbenh, anchor=W)
        c2.grid(column=0, row=1)
        c3 = Checkbutton(self.cactrieuchung, text='Đau Họng', variable=self.dauhong,
                         onvalue=1, offvalue=0, command=self.chuandoanbenh, anchor=W)
        c3.grid(column=0, row=2)
        c4 = Checkbutton(self.cactrieuchung, text='Chảy Nước Mũi hoặc nghẹ mũi', variable=self.nghetmui,
                         onvalue=1, offvalue=0, command=self.chuandoanbenh, anchor=W)
        c4.grid(column=0, row=3)
        c5 = Checkbutton(self.cactrieuchung, text='Sưng hạch bạch huyết', variable=self.sung,
                         onvalue=1, offvalue=0, command=self.chuandoanbenh, anchor=W)
        c5.grid(column=0, row=4)
        c6 = Checkbutton(self.cactrieuchung, text='Đau nhức cơ thể nhẹ hoặc đau đầu nhẹ', variable=self.daudau,
                         onvalue=1, offvalue=0, command=self.chuandoanbenh, anchor=W)
        c6.grid(column=0, row=5)
        c7 = Checkbutton(self.cactrieuchung, text='Hắt xì', variable=self.hatxit,
                         onvalue=1, offvalue=0, command=self.chuandoanbenh, anchor=W)
        c7.grid(column=0, row=6)
        c8 = Checkbutton(self.cactrieuchung, text='Cảm thấy không khỏe (khó chịu)', variable=self.khochiu,
                         onvalue=1, offvalue=0, command=self.chuandoanbenh, anchor=W)
        c8.grid(column=0, row=7)
        c9 = Checkbutton(self.cactrieuchung, text='Khó thở', variable=self.khotho,
                         onvalue=1, offvalue=0, command=self.chuandoanbenh, anchor=W)
        c9.grid(column=0, row=8)

        self.ketquabenh = LabelFrame(self.chuandoan, text="Kết quả nhanh")
        self.ketquabenh.pack(side=RIGHT, fill=BOTH, expand=True)
        self.ketquanhanh = Label(
            self.ketquabenh, bg='white', width=20, text="Đang chờ kết quả ")
        self.ketquanhanh.pack()

    def chuandoanbenh(self):
        if (self.ho.get() == 1) & (self.sot.get() == 0):
            self.ketquanhanh.config(text='Mới Ho thôi')
        elif (self.ho.get() == 0) & (self.sot.get() == 1):
            self.ketquanhanh.config(text='Sốt rồi')
        elif (self.ho.get() == 0) & (self.sot.get() == 0):
            self.ketquanhanh.config(text='Bình Thường')
        else:
            self.ketquanhanh.config(text='Covid rồi')


class dangkytiem_page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        ngang = 5
        doc = 5
        width_ = 23
        self.masv = StringVar()
        self.loaithuoc = StringVar()
        self.tenthuoctiem = StringVar()
        self.muitiem = StringVar()
        self.diachitiem = StringVar()
        self.dangkytiem_f = LabelFrame(self, text="Thông tin đăng ký")
        self.dangkytiem_f.pack(fill=BOTH, expand=TRUE, side=TOP)

        self.masv_l = Label(self.dangkytiem_f, text="Mã Sinh Viên",)
        self.masv_l.grid(column=0, row=0, padx=ngang, pady=doc)
        self.masv_e = Entry(self.dangkytiem_f, width=width_,
                            textvariable=self.masv)
        self.masv_e.grid(column=0, row=1, padx=ngang, pady=doc)

        self.loaithuoc_l = Label(
            self.dangkytiem_f, text="Loại Thuốc Tiêm",)
        self.loaithuoc_l.grid(column=1, row=0, padx=ngang, pady=doc)
        self.loaithuoc_e = Entry(
            self.dangkytiem_f, textvariable=self.loaithuoc, width=width_)
        self.loaithuoc_e.grid(column=1, row=1, padx=ngang, pady=doc)

        self.tenthuoctiem_l = Label(
            self.dangkytiem_f, text="Tên Thuốc Tiêm")
        self.tenthuoctiem_l.grid(column=2, row=0, padx=ngang, pady=doc)
        self.tenthuoctiem_e = Entry(
            self.dangkytiem_f, textvariable=self.tenthuoctiem, width=width_)
        self.tenthuoctiem_e.grid(column=2, row=1, padx=ngang, pady=doc)

        self.muitiem_l = Label(
            self.dangkytiem_f, text="Mũi Tiêm", )
        self.muitiem_l.grid(column=3, row=0, padx=ngang, pady=doc)
        self.muitiem_e = Entry(
            self.dangkytiem_f, textvariable=self.muitiem, width=width_)
        self.muitiem_e.grid(column=3, row=1, padx=ngang, pady=doc)

        self.diachitiem_l = Label(
            self.dangkytiem_f, text="Địa Chi Đăng Ký Tiêm", )
        self.diachitiem_l.grid(column=4, row=0, padx=ngang, pady=doc)
        self.diachitiem_e = Entry(
            self.dangkytiem_f, textvariable=self.diachitiem, width=width_)
        self.diachitiem_e.grid(column=4, row=1, padx=ngang, pady=doc)

    #     self.thongtindatiem_f = LabelFrame(self, text="Thông tin mũi tiêm")
    #     self.thongtindatiem_f.pack(fill=BOTH, expand=TRUE, side=LEFT)
    #     self.bangthongtintiem = ttk.Treeview(
    #         self.thongtindatiem_f, selectmode="browse")
    #     self.bangthongtintiem["show"] = 'headings'
    #     self.bangthongtintiem['height'] = "20"
    #     self.bangthongtintiem['columns'] = ("0", "1", "2", "3", "4", "5", "6")
    #     self.bangthongtintiem.heading("0", text="Mã Sinh Viên")
    #     self.bangthongtintiem.heading("1", text="Tên Sinh Viên")
    #     self.bangthongtintiem.heading("2", text="Loại Thuốc")
    #     self.bangthongtintiem.heading("3", text="Tên Thuốc")
    #     self.bangthongtintiem.heading("4", text="Mũi Tiêm")
    #     self.bangthongtintiem.heading("5", text="Thời Gian Tiêm")
    #     self.bangthongtintiem.heading("6", text="Địa Chỉ Tiêm")
    #     self.bangthongtintiem.pack(expand=TRUE, fill=BOTH)
    #     self.hsb = ttk.Scrollbar(
    #         self.thongtindatiem_f, orient=tk.HORIZONTAL, command=self.bangthongtintiem.xview)
    #     self.hsb.pack(side=BOTTOM, fill=X)
    #     self.bangthongtintiem.configure(xscroll=self.hsb.set)
    #     self.bangthongtintiem.pack(expand=YES, fill=BOTH)

    #     mycursor.execute(
    #         "SELECT MAKHACHHANG, TENKHACHHANG, SDT, GIOITINH FROM KHACHHANG")
    #     rows = mycursor.fetchall()
    #     self.update_rows(rows)

    #     self.bangthongtintiem.bind("<ButtonRelease-1>", self.thongtinmuitiem)

    # def thongtinmuitiem(self, event):
    #     selected = self.bangthongtintiem.focus()
    #     values = self.bangthongtintiem.item(selected, 'values')
    #     # self.makhachhang.set(values[0])
    #     # self.tenkhachhang.set(values[1])
    #     # self.sodienthoai.set(values[2])
    #     # self.gioitinh.set(values[3])

    # def update_rows(self, rows):
    #     self.bangthongtintiem.delete(*self.bangthongtintiem.get_children())
    #     for i in rows:
    #         self.bangthongtintiem.insert('', 'end', values=i)


class thongtinsinhvien(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        ngang = 5
        doc = 5
        MDGT = [("Nam", '0'), ("Nữ", "1")]
        self.gioitinh = IntVar()
        self.ngaysinh = StringVar()
        self.masv_l = Label(self, text="Mã Sinh Viên",)
        self.masv_l.grid(column=0, row=0, padx=ngang, pady=doc)
        self.masv_e = Entry(self)
        self.masv_e.grid(column=1, row=0, padx=ngang, pady=doc)

        self.tensv_l = Label(self, text="Tên Sinh Viên",)
        self.tensv_l.grid(column=0, row=1, padx=ngang, pady=doc)
        self.tensv_e = Entry(self)
        self.tensv_e.grid(column=1, row=1, padx=ngang, pady=doc)

        self.ngaysinh_l = Label(self, text="Ngày Sinh",)
        self.ngaysinh_l.grid(column=0, row=2, padx=ngang, pady=doc)
        self.ngaysinh_e = tkc.DateEntry(self, width=17, date_pattern='dd/mm/yyyy',
                                        background='darkblue', foreground='white', borderwidth=2, textvariable=self.ngaysinh)
        self.ngaysinh_e.grid(column=1, row=2, padx=ngang, pady=doc)

        self.gioitinh_l = Label(self, text="Giới tính",)
        self.gioitinh_l.grid(column=0, row=3, padx=ngang, pady=doc)
        self.fgioitinh = Frame(self)
        self.fgioitinh.grid(column=1, row=3, padx=ngang, pady=doc)
        for text, mode in MDGT:
            Radiobutton(self.fgioitinh, text=text, variable=self.gioitinh, value=mode,
                        ).pack(side=LEFT)

        self.tensv_l = Label(self, text="Dân Tộc",)
        self.tensv_l.grid(column=0, row=4, padx=ngang, pady=doc)
        self.tensv_e = Entry(self)
        self.tensv_e.grid(column=1, row=4, padx=ngang, pady=doc)

        self.cccd_l = Label(self, text="CCCD/CMND",)
        self.cccd_l.grid(column=0, row=5, padx=ngang, pady=doc)
        self.cccd_e = Entry(self)
        self.cccd_e.grid(column=1, row=5, padx=ngang, pady=doc)

        self.sdt_l = Label(self, text="SĐT",)
        self.sdt_l.grid(column=0, row=6, padx=ngang, pady=doc)
        self.sdt_e = Entry(self)
        self.sdt_e.grid(column=1, row=6, padx=ngang, pady=doc)

        self.gmail_l = Label(self, text="Email",)
        self.gmail_l.grid(column=0, row=7, padx=ngang, pady=doc)
        self.gmail_e = Entry(self)
        self.gmail_e.grid(column=1, row=7, padx=ngang, pady=doc)

        self.diachithuongtru_l = Label(self, text="Địa chỉ thường trú",)
        self.diachithuongtru_l.grid(column=0, row=8, padx=ngang, pady=doc)
        self.diachithuongtru_e = Entry(self)
        self.diachithuongtru_e.grid(column=1, row=8, padx=ngang, pady=doc)

        self.quequan_l = Label(self, text="Quê quán",)
        self.quequan_l.grid(column=0, row=9, padx=ngang, pady=doc)
        self.quequan_e = Entry(self)
        self.quequan_e.grid(column=1, row=9, padx=ngang, pady=doc)

        self.update_b = Button(self, text="Cập nhật thông tin")


class thongtinsuckhoe(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        ngang = 5
        doc = 5
        width_ = 23
        self.masv = StringVar()
        self.chieucao = StringVar()
        self.cannang = StringVar()
        self.trangthaicothe = StringVar()
        self.nhommau = StringVar()
        self.chisoBMI = StringVar()

        self.khaibao = LabelFrame(self, text="Khai Báo")
        self.khaibao.pack(side=LEFT, fill=BOTH, expand=True)

        self.masv_l = Label(self.khaibao, text="Mã Sinh Viên",)
        self.masv_l.grid(column=0, row=0, padx=ngang, pady=doc)
        self.masv_e = Entry(self.khaibao, width=width_)
        self.masv_e.grid(column=1, row=0, padx=ngang, pady=doc)

        self.chieucao_l = Label(
            self.khaibao, text="Chiều Cao", )
        self.chieucao_l.grid(column=0, row=1, padx=ngang, pady=doc)
        self.chieucao_e = Entry(
            self.khaibao, textvariable=self.chieucao, width=width_)
        self.chieucao_e.grid(column=1, row=1, padx=ngang, pady=doc)
        self.cm_l = Label(self.khaibao, text="CM",)
        self.cm_l.grid(column=2, row=1, padx=ngang, pady=doc)

        self.cannang_l = Label(self.khaibao, text="Cân Nặng",)
        self.cannang_l.grid(column=0, row=2, padx=ngang, pady=doc)
        self.cannang_e = Entry(
            self.khaibao, textvariable=self.cannang, width=width_)
        self.cannang_e.grid(column=1, row=2, padx=ngang, pady=doc)
        self.kg_l = Label(self.khaibao, text="KG",)
        self.kg_l.grid(column=2, row=2, padx=ngang, pady=doc)
        self.cannang_e.bind('<Key-Return>', self.tinhchisoBMI)

        self.nhommau_l = Label(self.khaibao, text="Nhóm Máu",)
        self.nhommau_l.grid(column=0, row=3, padx=ngang, pady=doc)
        self.nhommau_e = ttk.Combobox(self.khaibao, textvariable=self.nhommau)
        self.nhommau_e['values'] = ('A', 'B', 'O', 'AB')
        self.nhommau_e['state'] = 'normal'
        self.nhommau_e.grid(column=1, row=3, padx=ngang, pady=doc)
# //////////////////////////////////////////////////////////////////////////////////////////////////////
        self.ketqua = LabelFrame(self, text="Kết quả")
        self.ketqua.pack(side=LEFT, fill=BOTH, expand=True)

        self.ketquanhanh_l = Label(self.ketqua, text="Chỉ số BMI",)
        self.ketquanhanh_l.grid(column=0, row=0, padx=ngang, pady=doc)
        self.ketquanhanh_e = Entry(
            self.ketqua, textvariable=self.chisoBMI, width=25)
        self.ketquanhanh_e.grid(column=1, row=0, padx=ngang, pady=doc)

        self.thongtinsk_l = Label(self.ketqua, text="Trạng thái",)
        self.thongtinsk_l.grid(column=0, row=1, padx=ngang, pady=doc)
        self.thongtinsk_e = Entry(
            self.ketqua, textvariable=self.trangthaicothe, width=25)
        self.thongtinsk_e.grid(column=1, row=1, padx=ngang, pady=doc)

    def tinhchisoBMI(self, event):
        cc = self.chieucao.get()
        cn = self.cannang.get()

        self.chisoBMI.set(int(cn)/int(cc)**2)
        BMI = self.chisoBMI.get()
        if (float(BMI) * 10000) < 18.5:
            self.trangthaicothe.set("Cân Nặng Thấp (gầy)")
        elif (float(BMI) * 10000) > 18.5 and (float(BMI) * 10000) < 24.9:
            self.trangthaicothe.set("Bình Thường")
        elif (float(BMI) * 10000) > 25 and (float(BMI) * 10000) < 29.9:
            self.trangthaicothe.set("Tiền Béo Phì")
        elif (float(BMI) * 10000) > 30 and (float(BMI) * 10000) < 34.9:
            self.trangthaicothe.set("Béo Phì Cấp Độ I")
        elif (float(BMI) * 10000) > 35 and (float(BMI) * 10000) < 39.9:
            self.trangthaicothe.set("Béo Phì Cấp Độ II")
        else:
            self.trangthaicothe.set("Béo Phì Cấp Độ III")
        return True


# root.attributes('-fullscreen', True)
app1 = App(root)
root.mainloop()
