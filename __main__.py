import tkinter as tk
from tkinter import filedialog as fd
import json
from threading import Thread, Event
import os.path
from playMod import play
import re

class SoundBoard:

    nombres = ["","","","","","","","",""]
    texto = ""
    audios = ["","","","","","","","",""]
    numero = 1
    patron = r'.*/([^/]+)\..*'
    contenido = None

    def __init__(self, root, file):
        self.stop_event = Event()
        self.file = file
        botones = []

        with open(self.file, 'r') as file:
            data = json.load(file)
            self.contenido = data
            n=0
            for key,value in data.items():
                self.audios[n]=value
                if value:
                    if os.path.isfile(value):
                        con=re.match(self.patron, value)
                        self.nombres[n]=(con.group(1))
                n+=1
        n=1
        for nombre in self.nombres:
            if nombre != "":
                self.texto += f"{n}.-"+nombre+"\r\n"
            n+=1

        self.root = root
        self.root.title("SoundBoard")
        self.root.geometry("700x500")
        self.root.resizable(width=False,height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.killWindow)

        p1 = tk.Frame(self.root, bg="#c3cedb", width=200)
        p1.pack(side="right",fill="y")

        p2 = tk.Frame(self.root, bg="#e3e8e8")
        p2.pack(side="left",fill="both", expand=True)

        pTitle = tk.Frame(p2, bg="#e3e8e8",height=100)
        pTitle.pack(side="top",fill="x")

        pBtn1 = tk.Frame(p2, bg="#e3e8e8",height=100)
        pBtn1.pack(side="top",fill="x")

        pBtn2 = tk.Frame(p2, bg="#e3e8e8",height=100)
        pBtn2.pack(side="top",fill="x")

        pBtn3 = tk.Frame(p2, bg="#e3e8e8",height=100)
        pBtn3.pack(side="top",fill="x")

        lbl = tk.Label(pTitle,text="Simple Digital SoundBoard",bg="#e3e8e8",font="Banchcrift")
        lbl.pack(pady=20)

        for i in range(3):
            boton = tk.Button(pBtn1, text=f"Botón {i+1}",width=15,height=7, command=lambda i=i: self.iniciar_reproduccion(self.audios[i],))
            boton.pack(padx=10,pady=5,side="left")
            botones.append(boton)
        for i in range(3):
            boton = tk.Button(pBtn2, text=f"Botón {3+i+1}",width=15,height=7, command=lambda i=i: self.iniciar_reproduccion(self.audios[i+3],))
            boton.pack(padx=10,pady=5,side="left")
            botones.append(boton)
        for i in range(3):
            boton = tk.Button(pBtn3, text=f"Botón {6+i+1}",width=15,height=7, command=lambda i=i: self.iniciar_reproduccion(self.audios[i+6],))
            boton.pack(padx=10,pady=5,side="left")
            botones.append(boton)
        btnKill = tk.Button(p1,text="Detener",width=15,height=5,command=self.kill)
        btnKill.pack(pady=12,side="top")
        
        lblNombres = tk.Label(p1,text=self.texto)
        lblNombres.pack(pady=10)

        #dropbar
        opciones = ["1","2","3","4","5","6","7","8","9"]
        clicked = tk.StringVar()
        clicked.set("1")
        drop=tk.OptionMenu(p1,clicked,*opciones,command=self.cam_numero)
        drop.pack()

        #file Dialog
        btnFile = tk.Button(p1,text="import",width=15,height=4,command=lambda: self.abrir_dialogo(lblNombres,self.file))
        btnFile.pack(pady=12,side="top")
        #-------------
    
    def iniciar_reproduccion(self, audio):
        if self.stop_event.is_set():
            self.stop_event.clear()
        Thread(target=play, args=(audio, self.stop_event)).start()
    def cam_numero(self,num):
        # print(num)
        self.numero =int(num)
        

    def abrir_dialogo(self,label,file):
        filetypes = (
        ('wav files', '*.wav'),
        ('All files', '*.*')
        )
        archivo = fd.askopenfilename(title='Open a file',initialdir="/",filetypes=filetypes)
        if archivo:
            nombre = os.path.abspath(archivo)
            path = nombre.replace(f'\\','/')
            print(path)
            con=re.match(self.patron, path)
            self.audios[self.numero-1] = path
            self.nombres[self.numero-1] = con.group(1)

            self.contenido["btn"+str(self.numero)] = path
            with open(file, 'w') as f:
                json.dump(self.contenido,f)
            n=1
            self.texto=""
            for nombre in self.nombres:
                if nombre != "":
                    self.texto += f"{n}.-"+nombre+"\r\n"
                n+=1
            label.config(text=self.texto)

    
    def kill(self):
        if hasattr(self, 'stop_event'):
            self.stop_event.set()
    
    def killWindow(self):
        if hasattr(self, 'stop_event'):
            self.stop_event.set()
        self.root.destroy()


def run(root):
    root.geometry()
    root.mainloop()
        
if __name__ == "__main__":
    root = tk.Tk()
    file = "audioFiles.json"
    app = SoundBoard(root,file)
    td = Thread(target=run(root=root))
    td.daemon=True
    td.start()