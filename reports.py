from modules import canvas, letter, A4
from modules import pdfmetrics, TTFont
from modules import SimpleDocTemplate, Image
from modules import webbrowser

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
