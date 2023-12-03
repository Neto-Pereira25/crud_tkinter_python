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