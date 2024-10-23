import os
import pdfkit
import tkinter as tk
from tkinter import filedialog, messagebox

def convertir_html_a_pdf(ruta_html, ruta_pdf):
    opciones = {
        'enable-local-file-access': None,
        'encoding': 'UTF-8',
        'no-outline': None,
        'quiet': ''
    }
    pdfkit.from_file(ruta_html, ruta_pdf, options=opciones)

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        procesar_carpeta(carpeta)

def procesar_carpeta(carpeta):
    archivos_html = [f for f in os.listdir(carpeta) if f.endswith('.html')]
    if not archivos_html:
        messagebox.showinfo("Información", "No se encontraron archivos HTML en la carpeta seleccionada.")
        return

    for archivo in archivos_html:
        ruta_html = os.path.join(carpeta, archivo)
        ruta_pdf = os.path.join(carpeta, os.path.splitext(archivo)[0] + '.pdf')
        try:
            convertir_html_a_pdf(ruta_html, ruta_pdf)
            print(f"Convertido: {archivo}")
        except Exception as e:
            print(f"Error al convertir {archivo}: {str(e)}")

    messagebox.showinfo("Éxito", f"Se han convertido {len(archivos_html)} archivos HTML a PDF.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Conversor HTML a PDF")
ventana.geometry("300x100")

# Crear y colocar el botón
boton = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton.pack(expand=True)

# Iniciar el bucle de eventos
ventana.mainloop()
