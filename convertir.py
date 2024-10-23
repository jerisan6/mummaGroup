import os
import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io
import pdfkit

# Añade esta línea al principio del archivo, después de las importaciones
wkhtmltopdf_path = r'C:\Archivos de programa\wkhtmltopdf\bin\wkhtmltopdf.exe'

def convertir_html_a_imagen(ruta_html, ruta_imagen):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)
    driver.get(f"file:///{ruta_html}")
    
    # Esperar a que la página se cargue completamente
    driver.implicitly_wait(10)
    
    # Obtener las dimensiones de la página
    width = driver.execute_script("return document.body.scrollWidth")
    height = driver.execute_script("return document.body.scrollHeight")
    
    # Establecer el tamaño de la ventana
    driver.set_window_size(width, height)
    
    # Capturar la pantalla
    png = driver.get_screenshot_as_png()
    
    # Guardar la imagen
    imagen = Image.open(io.BytesIO(png))
    imagen.save(ruta_imagen)
    
    driver.quit()

def convertir_html_a_pdf(ruta_html, ruta_pdf):
    try:
        pdfkit.from_file(ruta_html, ruta_pdf, options={'enable-local-file-access': None})
    except Exception as e:
        print(f"Error al convertir {ruta_html} a PDF: {str(e)}")
        raise

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        procesar_carpeta(carpeta)

def procesar_carpeta(carpeta):
    archivos_html = [f for f in os.listdir(carpeta) if f.endswith('.html')]
    if not archivos_html:
        messagebox.showinfo("Información", "No se encontraron archivos HTML en la carpeta seleccionada.")
        return

    nombre_carpeta_conversion = os.path.basename(carpeta) + "_conversion"
    carpeta_conversion = os.path.join(os.path.dirname(carpeta), nombre_carpeta_conversion)
    os.makedirs(carpeta_conversion, exist_ok=True)

    archivos_convertidos = []
    for archivo in archivos_html:
        ruta_html = os.path.join(carpeta, archivo)
        ruta_pdf = os.path.join(carpeta_conversion, os.path.splitext(archivo)[0] + '.pdf')
        try:
            convertir_html_a_pdf(ruta_html, ruta_pdf)
            archivos_convertidos.append(ruta_pdf)
            print(f"Convertido: {archivo}")
        except Exception as e:
            print(f"Error al convertir {archivo}: {str(e)}")

    if archivos_convertidos:
        messagebox.showinfo("Éxito", f"Se han convertido {len(archivos_convertidos)} archivos HTML a PDF y se han guardado en {carpeta_conversion}")
    else:
        messagebox.showwarning("Advertencia", "No se pudo convertir ningún archivo.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Conversor HTML a Imagen")
ventana.geometry("300x100")

# Crear y colocar el botón
boton = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton.pack(expand=True)

# Iniciar el bucle de eventos
ventana.mainloop()
