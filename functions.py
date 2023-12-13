from modules import *
from modules import sqlite3

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
        
    def create_table_products(self):
        self.get_connection()
            
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY,
            nome_produto VARCHAR(100) NOT NULL,
            preco DECIMAL(10, 2));
            """)
        
        self.conn.commit(); print('tabela criada')
        self.disconnect_db()

    def create_table_orders(self):
        self.get_connection()
            
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY,
                cliente_id INTEGER,
                produto_id INTEGER,
                quantidade INTEGER,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id));
            """)
        self.conn.commit(); print('tabela criada')
        self.disconnect_db()

    def drop_table(self):
        self.get_connection()
        
        self.cursor.execute(""" DROP TABLE IF EXISTS clientes""")
        self.conn.commit()
        print('Tabela apagada com sucesso')
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

    def _insert_default_products(self):
        self.get_connection()
        
        self.cursor.execute(
            """
            INSERT INTO produtos 
                (nome_produto, preco) 
            VALUES
                ('Camisa Polo', 39.99),
                ('Tênis Esportivo', 79.95),
                ('Calça Jeans', 49.50),
                ('Camiseta Básica', 15.99),
                ('Sapatênis Casual', 59.75),
                ('Vestido Floral', 69.99),
                ('Jaqueta de Couro', 89.50),
                ('Sandália Rasteira', 29.95),
                ('Bermuda Surf', 35.25),
                ('Blusa de Moletom', 45.99),
                ('Óculos de Sol', 59.50),
                ('Sapato Social', 99.99),
                ('Saia Midi', 25.75),
                ('Cinto de Couro', 19.95),
                ('Pijama Conforto', 34.50),
                ('Bolsa Tote', 49.99),
                ('Blazer Slim', 79.75),
                ('Colar Elegance', 29.25),
                ('Chapéu Panamá', 39.50),
                ('Relógio Analógico', 89.99);

            """
        )
        
        self.conn.commit()
        self.disconnect_db()
    
    def _insert_default_order(self):
        self.get_connection()
        
        self.cursor.execute(
            """
            INSERT INTO pedidos 
                (cliente_id, produto_id, quantidade) 
            VALUES
                (1, 1, 3),
                (2, 5, 2),
                (3, 9, 1),
                (4, 2, 4),
                (5, 7, 5),
                (1, 15, 2),
                (2, 18, 3),
                (3, 11, 1),
                (4, 3, 2),
                (5, 19, 4),
                (1, 4, 2),
                (2, 10, 1),
                (3, 13, 3),
                (4, 6, 2),
                (5, 20, 1),
                (1, 8, 4),
                (2, 14, 3),
                (3, 16, 2),
                (4, 12, 1),
                (5, 17, 5);
            """
        )
        
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
    
    
