import os
import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

# Añade esta línea al principio del archivo, después de las importaciones
wkhtmltopdf_path = r'C:\Archivos de programa\wkhtmltopdf\bin\wkhtmltopdf.exe'

def convertir_html_a_imagen(ruta_html, ruta_imagen):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(f"file:///{ruta_html}")
        
        # Esperar a que la página se cargue completamente
        driver.implicitly_wait(5)  # Reducido de 10 a 5 segundos
        
        # Obtener las dimensiones de la página
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        
        # Establecer el tamaño de la ventana
        driver.set_window_size(width, height)
        
        # Capturar la pantalla
        png = driver.get_screenshot_as_png()
        
        # Guardar la imagen
        imagen = Image.open(io.BytesIO(png))
        imagen.save(ruta_imagen)
    finally:
        driver.quit()

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        procesar_carpeta(carpeta)

def procesar_archivo(args):
    ruta_html, carpeta_destino = args
    archivo = os.path.basename(ruta_html)
    nombre_imagen = os.path.splitext(archivo)[0] + '.png'
    ruta_imagen = os.path.join(carpeta_destino, nombre_imagen)
    try:
        convertir_html_a_imagen(ruta_html, ruta_imagen)
        print(f"Convertido: {archivo}")
        return ruta_imagen
    except Exception as e:
        print(f"Error al convertir {archivo}: {str(e)}")
        return None

def procesar_carpeta(carpeta):
    archivos_html = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith('.html')]
    if not archivos_html:
        messagebox.showinfo("Información", "No se encontraron archivos HTML en la carpeta seleccionada.")
        return

    nombre_carpeta = os.path.basename(carpeta)
    carpeta_destino = os.path.join(os.path.dirname(carpeta), f"{nombre_carpeta}_conversion")
    os.makedirs(carpeta_destino, exist_ok=True)

    num_workers = multiprocessing.cpu_count()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        archivos_convertidos = list(filter(None, executor.map(procesar_archivo, [(ruta, carpeta_destino) for ruta in archivos_html])))

    if archivos_convertidos:
        messagebox.showinfo("Éxito", f"Se han convertido {len(archivos_convertidos)} archivos HTML a imágenes y se han guardado en {carpeta_destino}")
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
