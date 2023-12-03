from tkinter import *
from tkinter import ttk
import sqlite3

# Para gerarmos relatórios em pdf é necessário instalar a lib
# reportlab com o comando: pip install reportlab
# e fazer sua chamada
# e também usar a biblioteca webbrowser

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

root = Tk()

class Reports():
    def printClient(self):
        webbrowser.open('cliente.pdf')
    
    def generateReport(self):
        self.client = canvas.Canvas('client.pdf')
        
        self.codeReport = self.entry_code.get()
        self.nameReport = self.entry_name.get()
        self.phoneReport = self.entry_phone.get()
        self.cityReport = self.entry_city.get()
        
        self.client.setFont('Helvetica-Bold', 24)
        self.client.drawString(200, 790, 'Ficha do Cliente')
        
        self.client.setFont('Helvetica-Bold', 18)
        self.client.drawString(50, 700, 'Codigo: ')
        self.client.drawString(50, 670, 'Nome: ')
        self.client.drawString(50, 640, 'Telefone: ')
        self.client.drawString(50, 610, 'Cidade: ')
        
        self.client.setFont('Helvetica', 18)
        self.client.drawString(150, 700, self.codeReport)
        self.client.drawString(150, 670, self.nameReport)
        self.client.drawString(150, 640, self.phoneReport)
        self.client.drawString(150, 610, self.cityReport)
        
        # os parametros do rect são posição, altura, largura e borda
        self.client.rect(20, 550, 550, 5, fill = True, stroke = False)
        
        self.client.showPage()
        self.client.save()
        self.printClient()

    def generate_report_all_clients(self):
            self.get_connection()
            people_list = self.cursor.execute(
                """
                    SELECT id, nome, telefone, cidade FROM clientes
                    ORDER BY nome ASC;
                """
            )
            
            list_of_all_client = people_list.fetchall()
            
            with open('all_clients.txt', 'w', encoding='utf-8') as arquivo:
                for i in list_of_all_client:
                    self.codeReport, self.nameReport, self.phoneReport, self.cityReport = i
                    client: str = f"""Codigo: {self.codeReport}\nNome: {self.nameReport}\nTelefone: {self.phoneReport}\nCidade: {self.cityReport}\n------------------------------------------------------------\n\n"""
                    arquivo.write(client)
            self.disconnect_db()

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

    def _insert_default_client(self):
        
        self.variables()
        
        self.get_connection()
        self.cursor.execute(
        """
            INSERT INTO clientes 
                (nome, telefone, cidade) 
            VALUES
                ('João Silva', '123456789', 'São Paulo'),
                ('Maria Oliveira', '987654321', 'Rio de Janeiro'),
                ('Pedro Santos', '111222333', 'Belo Horizonte'),
                ('Ana Pereira', '444555666', 'Salvador'),
                ('Carlos Souza', '777888999', 'Fortaleza'),
                ('Julia Rodrigues', '111333555', 'Brasília'),
                ('Rafaela Costa', '666333999', 'Curitiba'),
                ('Fernando Martins', '888999111', 'Porto Alegre'),
                ('Luciana Ferreira', '222111444', 'Recife'),
                ('Gustavo Almeida', '999888777', 'Manaus'),
                ('Bianca Oliveira', '123789456', 'Belém'),
                ('Diego Santos', '789456123', 'Goiânia'),
                ('Patrícia Lima', '456123789', 'Florianópolis'),
                ('Marcelo Gomes', '789123456', 'Natal'),
                ('Mariana Carvalho', '555666777', 'Vitória'),
                ('Antônio Silva', '111222444', 'João Pessoa'),
                ('Camila Ribeiro', '222444666', 'Aracaju'),
                ('Luiz Pereira', '333555777', 'Cuiabá'),
                ('Tatiane Souza', '777555333', 'Campo Grande'),
                ('Anderson Santos', '333777555', 'Teresina');
        """)
        self.conn.commit()
        self.disconnect_db()

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
            (self.code,)
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

    def find_a_client(self):
        self.get_connection()
        
        self.list_cli.delete(*self.list_cli.get_children())
        self.entry_name.insert(END, '%')
        name = self.entry_name.get()
        self.cursor.execute(
            """ SELECT id, nome, telefone, cidade FROM clientes 
            WHERE nome LIKE '%s' ORDER BY nome ASC""" % name
        )
        find_client_name = self.cursor.fetchall()
        
        for i in find_client_name:
            self.list_cli.insert("", END, values=i)
        
        self.clean_screen()
        self.disconnect_db()

class Application(Functions, Reports):
    def __init__(self):
        self.root = root
        self.window()
        self.screen_frames()
        self.widgets_frame_1()
        self.client_list_frame_2()
        self.create_tables()
        self.select_list()
        self.menus()
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
                            command = self.clean_screen)
        self.bt_clear.place(relx = 0.2, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        self.bt_search = Button(self.frame_1, text='Buscar', 
                                bd = 3, bg = '#107db2', fg = 'white', font = ('verdana', 8, 'bold'),
                                command = self.find_a_client)
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

    def menus(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        filemenu1 = Menu(menu_bar)
        filemenu2 = Menu(menu_bar)
        
        def quit_menu(): self.root.destroy()
        
        menu_bar.add_cascade(label= "Opções", menu = filemenu1)
        menu_bar.add_cascade(label = "Relatorios", menu = filemenu2)
        
        filemenu1.add_command(label = "Sair", command = quit_menu)
        filemenu1.add_command(label = "Limpar Cliente", command = self.clean_screen)
        filemenu1.add_command(label = "Inserir Clientes Padrão", command = self._insert_default_client)
        
        filemenu2.add_command(label = "Ficha do Cliente", command = self.generateReport)
        filemenu2.add_command(label = "Todos os Cliente", command = self.generate_report_all_clients)

if __name__ == "__main__":
    Application()