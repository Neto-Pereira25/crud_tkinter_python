from tkinter import *

root = Tk()

class Application():
    def __init__(self):
        self.root = root
        self.window()
        self.screen_frames()
        self.screen_buttons()
        root.mainloop()
    
    def window(self):
        self.root.title('Clientes')
        self.root.configure(background='#1e3743')
        self.root.geometry('700x500+300+100')
        self.root.resizable(True, True)
        self.root.maxsize(width = 900, height = 700)
        self.root.minsize(width = 400, height = 300)
        
    def screen_frames(self):
        self.frame_1 = Frame(self.root, bd = 4, bg = '#dfe3ee',
                            highlightbackground = '#759fe6', highlightthickness = 3)
        self.frame_1.place(relx = 0.02, rely = 0.02, relwidth = 0.96, relheight = 0.46)
        
        self.frame_2 = Frame(self.root, bd = 4, bg = '#dfe3ee',
                            highlightbackground = '#759fe6', highlightthickness = 3)
        self.frame_2.place(relx = 0.02, rely = 0.5, relwidth = 0.96, relheight = 0.46)

    def screen_buttons(self):
        self.bt_clear = Button(self.frame_1, text='Limpar')
        self.bt_clear.place(relx = 0.2, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        self.bt_search = Button(self.frame_1, text='Buscar')
        self.bt_search.place(relx = 0.3, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        self.bt_new = Button(self.frame_1, text='Novo')
        self.bt_new.place(relx = 0.6, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        self.bt_change = Button(self.frame_1, text='Alterar')
        self.bt_change.place(relx = 0.7, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        self.bt_delete = Button(self.frame_1, text='Apagar')
        self.bt_delete.place(relx = 0.8, rely = 0.1, relwidth = 0.1, relheight = 0.15)

if __name__ == "__main__":
    Application()