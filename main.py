from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()

class Functions():
    def clean_screen(self):
        self.entry_code.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_phone.delete(0, END)
        self.entry_city.delete(0, END)
    
    def get_connection(self):
        self.conn = sqlite3.connect('clientes.db')
        self.cursor = self.conn.cursor()
        print('Conectando ao banco de dados')
    
    def disconnect_db(self):
        self.conn.close()
        print('Desconectando ao banco de dados')
        
    def create_tables(self):
        self.get_connection()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                telefone INTEGER(12),
                cidade VARCHAR(40)
            );
            """)
        self.conn.commit(); print('tabela criada')
        self.disconnect_db()

    def variables(self):
        self.code = self.entry_code.get()
        self.name = self.entry_name.get()
        self.phone = self.entry_phone.get()
        self.city = self.entry_city.get()

    def insert_client(self):
        
        self.variables()
        
        self.get_connection()
        self.cursor.execute(
        """
            INSERT INTO clientes 
                (nome, telefone, cidade)
            VALUES 
                (?, ?, ?)
        """, (self.name, self.phone, self.city))
        self.conn.commit()
        self.disconnect_db()
        self.select_list()
        self.clean_screen()
        
    def select_list(self):
        self.list_cli.delete(*self.list_cli.get_children())
        self.get_connection()
        people_list = self.cursor.execute(
            """
                SELECT id, nome, telefone, cidade FROM clientes
                ORDER BY nome ASC;
            """
        )
        
        for i in people_list:
            self.list_cli.insert("", END, values = i)
        self.disconnect_db()

    def onDoubleClick(self, event):
        self.clean_screen()
        self.list_cli.selection()
        
        for n in self.list_cli.selection():
            col1, col2, col3, col4 = self.list_cli.item(n, 'values')
            self.entry_code.insert(END, col1)
            self.entry_name.insert(END, col2)
            self.entry_phone.insert(END, col3)
            self.entry_city.insert(END, col4)

    def delete_client(self):
        self.variables()
        self.get_connection()
        self.cursor.execute(
            """
                DELETE FROM clientes WHERE id = ?
            """,
            (self.code)
        )
        self.conn.commit()
        self.disconnect_db()
        self.clean_screen()
        self.select_list()

    def modify_client(self):
        self.variables()
        self.get_connection()
        
        self.cursor.execute(
            """
                UPDATE clientes SET nome = ?, telefone = ?, cidade = ?
                WHERE id = ?
            """, (self.name, self.phone, self.city, self.code)
        )
        self.conn.commit()
        self.disconnect_db()
        self.select_list()
        self.clean_screen()

class Application(Functions):
    def __init__(self):
        self.root = root
        self.window()
        self.screen_frames()
        self.widgets_frame_1()
        self.client_list_frame_2()
        self.create_tables()
        self.select_list()
        root.mainloop()
    
    def window(self):
        self.root.title('Clientes')
        self.root.configure(background='#1e3743')
        self.root.geometry('700x500+300+100')
        self.root.resizable(True, True)
        self.root.maxsize(width = 900, height = 700)
        self.root.minsize(width = 500, height = 400)
        
    def screen_frames(self):
        self.frame_1 = Frame(self.root, bd = 4, bg = '#dfe3ee',
                            highlightbackground = '#759fe6', highlightthickness = 3)
        self.frame_1.place(relx = 0.02, rely = 0.02, relwidth = 0.96, relheight = 0.46)
        
        self.frame_2 = Frame(self.root, bd = 4, bg = '#dfe3ee',
                            highlightbackground = '#759fe6', highlightthickness = 3)
        self.frame_2.place(relx = 0.02, rely = 0.5, relwidth = 0.96, relheight = 0.46)

    def widgets_frame_1(self):
        self.bt_clear = Button(self.frame_1, text='Limpar',
                            bd = 3, bg = '#107db2', fg = 'white', font = ('verdana', 8, 'bold'),
                            command=self.clean_screen)
        self.bt_clear.place(relx = 0.2, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        self.bt_search = Button(self.frame_1, text='Buscar', bd = 3, bg = '#107db2', fg = 'white', font = ('verdana', 8, 'bold'))
        self.bt_search.place(relx = 0.3, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        self.bt_new = Button(self.frame_1, text='Cadastrar', 
                            bd = 3, bg = '#107db2', fg = 'white', font = ('verdana', 8, 'bold'),
                            command = self.insert_client)
        self.bt_new.place(relx = 0.6, rely = 0.1, relwidth = 0.12, relheight = 0.15)
        
        self.bt_change = Button(self.frame_1, text='Alterar', 
                                bd = 3, bg = '#107db2', fg = 'white', font = ('verdana', 8, 'bold'),
                                command = self.modify_client)
        self.bt_change.place(relx = 0.72, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        self.bt_delete = Button(self.frame_1, text='Apagar', bd = 3, 
                                bg = '#107db2', fg = 'white', font = ('verdana', 8, 'bold'),
                                command = self.delete_client)
        self.bt_delete.place(relx = 0.82, rely = 0.1, relwidth = 0.1, relheight = 0.15)

        # Screen Labes and Entries
        # # Code
        self.lb_code = Label(self.frame_1, text = 'Código', bg = '#dfe3ee', fg = '#107db2', font = ('Arial', 10, 'bold'))
        self.lb_code.place(relx = 0.05, rely = 0.05)
        
        self.entry_code = Entry(self.frame_1, relief = 'groove')
        self.entry_code.place(relx = 0.05, rely = 0.15, relwidth = 0.085)
        
        # # Name
        self.lb_name = Label(self.frame_1, text = 'Nome', bg = '#dfe3ee', fg = '#107db2', font = ('Arial', 10, 'bold'))
        self.lb_name.place(relx = 0.05, rely = 0.35)
        
        self.entry_name = Entry(self.frame_1, relief = 'groove')
        self.entry_name.place(relx = 0.05, rely = 0.45, relwidth = 0.85)
        
        # # Phone
        self.lb_phone = Label(self.frame_1, text = 'Telefone', bg = '#dfe3ee', fg = '#107db2', font = ('Arial', 10, 'bold'))
        self.lb_phone.place(relx = 0.05, rely = 0.6)
        
        self.entry_phone = Entry(self.frame_1, relief = 'groove')
        self.entry_phone.place(relx = 0.05, rely = 0.7, relwidth = 0.4)
        
        # # City
        self.lb_city = Label(self.frame_1, text = 'Cidade', bg = '#dfe3ee', fg = '#107db2', font = ('Arial', 10, 'bold'))
        self.lb_city.place(relx = 0.5, rely = 0.6)
        
        self.entry_city = Entry(self.frame_1, relief = 'groove')
        self.entry_city.place(relx = 0.5, rely = 0.7, relwidth = 0.4)

    def client_list_frame_2(self):
        self.list_cli = ttk.Treeview(self.frame_2, height = 3, columns = ('col1', 'col2', 'col3', 'col4'))
        self.list_cli.heading('#0', text='')
        self.list_cli.heading('#1', text='Código')
        self.list_cli.heading('#2', text='Nome')
        self.list_cli.heading('#3', text='Telefone')
        self.list_cli.heading('#4', text='Cidade')
        
        self.list_cli.column('#0', width = 1)
        self.list_cli.column('#1', width = 50)
        self.list_cli.column('#2', width = 250)
        self.list_cli.column('#3', width = 100)
        self.list_cli.column('#4', width = 100)
        
        self.list_cli.place(relx = 0.01, rely = 0.01, relwidth = 0.95, relheight = 0.85)
        
        self.scrool_bar = Scrollbar(self.frame_2, orient = 'vertical')
        self.list_cli.configure( yscroll = self.scrool_bar.set)
        self.scrool_bar.place(relx = 0.96, rely = 0.01, relwidth = 0.04, relheight = 0.85)
        self.list_cli.bind("<Double-1>", self.onDoubleClick)

if __name__ == "__main__":
    Application()