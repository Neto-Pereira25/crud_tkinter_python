from tkinter import *

root = Tk()

class Application():
    def __init__(self):
        self.root = root
        self.window()
        root.mainloop()
    
    def window(self):
        self.root.title('Clientes')
        self.root.configure(background='#1e3743')
        self.root.geometry('700x500+300+100')
        self.root.resizable(True, True)
        self.root.maxsize(width = 900, height = 700)
        self.root.minsize(width = 400, height = 300)


if __name__ == "__main__":
    Application()