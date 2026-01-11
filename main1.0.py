from customtkinter import *
from PIL import Image
import socket
import threading

import os
import sys

def resource_path(relative_path):
    try:
    
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    p = os.path.join(base_path,"img")
    p = os.path.join(p,relative_path)

    return p


#створи картинки CTKImage
FON = CTkImage(light_image=Image.open(resource_path("fon.png")),size=(350,400))#fon 350,400
CONF = CTkImage(light_image=Image.open(resource_path("conf.png")),size=(24,24))#conf 24,24
USER = CTkImage(light_image=Image.open(resource_path("user.png")),size=(24,24))#user 24,24
ICONS = [] #user icons 24,24
for i in range(7):
    ICONS.append(CTkImage(light_image=Image.open(resource_path(f"{i}.png")),size=(70,70)))
#кольори
BLUE= "#5D89EA"
CYAN = "#2EB3E4"
PURPULE = "#B43EF5"
MEDIUMBLUE = "#8D60F0"
PHLOX = "#EB0EFC"

class MyLbl(CTkLabel):
    def __init__(self, master, text = "CTkLabel",size= 16,image = None):
        super().__init__(master,  text_color = PHLOX, text=text,
                          font = ("Arial",size ,"bold"), image=image)
    
        
        

class MyBtn(CTkButton):
    def __init__(self, master,image=None,height = 40,width= 140,text = "text",command=None ):
        super().__init__(master, width = width, height = height,
                         text =text,corner_radius=24,fg_color=PURPULE,
                         hover_color=MEDIUMBLUE,font = ("Arial",16,"bold"),
                         text_color="white",image=image,command=command )
        

class Mess(CTkLabel):
    def __init__(self, master,user,icon,text,anchor):
        icon = CTkImage(light_image=Image.open(f"{icon}.png"),size=(25,25))
        super().__init__(master = master, fg_color="#f2f2f2",
                         text_color="#000000",font=("Arial",16,"bold"),
                         image=icon,compound= "left",corner_radius=24,padx = 10,pady=10,text=f"{user}: {text}")
        self.pack(anchor=anchor,padx=50,pady=2)

        

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.configure(fg_color= "#4C474B")
        self.title("LogikTalk")
        self.iconbitmap(resource_path("icon.ico"))
        self.resizable(False,False)

        self.USER = "ananim"
        self.ICON = 0
        self.HOST = "0"
        self.PORT = 8080


        self.lbl = MyLbl(self,text = "WELCOM",size = 40,image=FON)
        self.lbl.place(x=0,y=0)


        lbl2 = MyLbl(self,text = "LogikTalk",size = 30)
        lbl2.place(x = 405,y = 50)


        self.btn_name = MyBtn(self,text="Enter Name",image=USER,command=self.open_name)
        self.btn_name.place(x = 405,y = 124)

        self.btn_icon = MyBtn(self,text="Enter icon",image=CONF,command=self.open_icon)
        self.btn_icon.place(x = 405,y = 188)

        self.btn_chat = MyBtn(self,width=100,text="Enter chat",command=self.open_chat)
        self.btn_chat.configure(fg_color = PHLOX,text_color="grey")
        self.btn_chat.place(x = 431,y = 260)

        self.frame_name = CTkFrame(self,fg_color=PHLOX,width=350,height=400)
        self.frame_name.place(x=-350,y=0)

        lbl3 = MyLbl(self.frame_name,text = "your name")
        lbl3.configure(text_color = "white")
        lbl3.place(x = 75,y=100)
        self.input_name = CTkEntry(self.frame_name,width=150,height=30,fg_color="white",corner_radius=30)
        self.input_name.place(x = 75,y = 150)

        self.btn_save_name = MyBtn(self.frame_name,text ="save_name",command=self.save_name)
        self.btn_save_name.place(x =100,y=240)

        self.frame_icon= CTkFrame(self,fg_color=PHLOX,width=350,height=400)
        self.frame_icon.place(x=-350,y=0)

        btn = MyBtn(self.frame_icon,width=75,height=75,image = ICONS[1],
                    command= lambda i=1: self.save_icon(i),text="")
        btn.grid(row=0,column = 0 ,padx = 31,pady = 24 )
        btn = MyBtn(self.frame_icon,width=75,height=75,image = ICONS[2],
                    command= lambda i=2: self.save_icon(i),text="")
        btn.grid(row=0,column = 1,padx = 31,pady = 24 )
        btn = MyBtn(self.frame_icon,width=75,height=75,image = ICONS[3],
                    command= lambda i=3: self.save_icon(i),text="")
        btn.grid(row=1,column = 0 ,padx = 31,pady = 24 )
        btn = MyBtn(self.frame_icon,width=75,height=75,image = ICONS[4],
                    command= lambda i=4: self.save_icon(i),text="")
        btn.grid(row=1,column = 1 ,padx = 31,pady = 24 )
        btn = MyBtn(self.frame_icon,width=75,height=75,image = ICONS[5],
                    command= lambda i=5: self.save_icon(i),text="")
        btn.grid(row=2,column = 0 ,padx = 31,pady = 24 )
        btn = MyBtn(self.frame_icon,width=75,height=75,image = ICONS[6],
                    command= lambda i=6: self.save_icon(i),text="")
        btn.grid(row=2,column = 1 ,padx = 31,pady = 24 )

        self.frame_chat = CTkFrame(self,fg_color="#c78888",width=600,height=400)
        
        self.frame_chat.place(x = 0,y =-400)

        self.all_mess = CTkScrollableFrame(self.frame_chat,fg_color="#c78888",width=500,height=300)

        self.all_mess.place(x = 0 ,y=0)

        self.inp_mess = CTkTextbox(self.frame_chat,width=350,height=50,fg_color=BLUE,corner_radius=30)
        self.inp_mess.place(x = 24,y = 324)
        self.btn_send_mess = MyBtn(self.frame_chat,width=50,height=50,text="send",command=self.send_mess)
        self.btn_send_mess.place(x = 400,y= 324)

        self.frame_start = CTkFrame(self,600,400,fg_color="#4C474B")
        self.frame_start.place(x=0,y=0)
        self.input_port = CTkEntry(self.frame_start,width=150,height=30,fg_color="white",corner_radius=30,placeholder_text="port")
        self.input_port.place(x = 100,y = 150)

        self.input_host = CTkEntry(self.frame_start,width=150,height=30,fg_color="white",corner_radius=30,placeholder_text="host")
        self.input_host.place(x = 100,y = 220)

        self.btn_begin = MyBtn(self.frame_start,text ="begin",command=self.begin)
        self.btn_begin.place(x =100,y=280)

    def begin(self):
        self.PORT = int(self.input_port.get())
        self.HOST = int(self.input_host.get())
        self.frame_start.destroy()

    def start(self):
        self.HOST = self.input_host.get()
        self.PORT = int(self.input_port.get())
        self.frame_start.destroy()



    def open_name(self):
        self.nx = -350
        def anim():
            self.nx +=10
            self.frame_name.place(x = self.nx,y = 0)
            if self.nx < 0:
                self.after(10,anim)
        anim()

    def close_name(self):
        self.nx = 0
        def anim():
            self.nx -=10
            self.frame_name.place(x = self.nx,y = 0)
            if self.nx >-350:
                self.after(10,anim)
        anim()
    def save_name(self):
        self.USER = self.input_name.get()
        self.close_name()

    def open_icon(self):
        self.nx = -350
        def anim():
            self.nx +=10
            self.frame_icon.place(x = self.nx,y = 0)
            if self.nx < 0:
                self.after(10,anim)
        anim()

    def close_icon(self):
        self.nx = 0
        def anim():
            self.nx -=10
            self.frame_icon.place(x = self.nx,y = 0)
            if self.nx >-350:
                self.after(10,anim)
        anim()
    def save_icon(self,i):
        self.ICON=i
        self.close_icon()

    def open_chat(self):

        try:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.socket.connect((f"{self.HOST}.tcp.eu.ngrok.io",self.PORT))
            self.socket.send(f"{self.USER}|{self.ICON}".encode())
            Mess(self.all_mess,self.USER,self.ICON,"welcome to chat","w")
            input = threading.Thread(target=self.input_mess,daemon=True)
            input.start()
            self.ny = -400
            def anim():
                self.ny +=10
                self.frame_chat.place(x = 0,y = self.ny)
                if self.ny < 0:
                    self.after(10,anim)
            anim()
        except:
            self.lbl.configure(text = "sorry,chat dont working")

    def input_mess(self):
        file = self.socket.makefile("r",encoding="UTF-8",newline="\n")
        while True:
            try:
                mess = file.readline()
                user,icon,mess = mess.split("|")
                Mess(self.all_mess,USER,icon,mess,"w")
            except:
                self.after(100, self.close)
    def close(self):
        self.socket.close()
        self.destroy()
    def send_mess(self):
        mess = self.inp_mess.get("1.0","end").strip()
        self.inp_mess.delete("1.0","end")
        try:
            self.socket.send(mess.encode())
            Mess(self.all_mess,self.USER,self.ICON,mess,"w")
        except:
            Mess(self.all_mess,"server",0,"Goodby")
            self.after(100,self.close)



           
        
        







app = App()
app.mainloop()