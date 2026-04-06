import tkinter as tk
import json
import os
from PIL import Image, ImageTk

# --- CONFIGURACIÓN DINÁMICA ---
print("\n=== MAPEADOR DE BOTONES WEB ===")
num_pag = input("👉 ¿Qué número de página deseas mapear ahora? (ej. 3, 4, 5, 6): ")

IMAGEN_A_MAPEAR = f"images/pagina_{num_pag}.jpg"
ID_CAPA_HTML = f"capa_pag_{num_pag}"
ARCHIVO_SALIDA = "templates/coordenadas.js"

if not os.path.exists(IMAGEN_A_MAPEAR):
    print(f"\n❌ Error: No se encontró la imagen {IMAGEN_A_MAPEAR}. Asegúrate de haber ejecutado el creador de HTML primero.")
    exit()

root = tk.Tk()
root.title(f"Mapeando Página {num_pag} - Clic para agregar")

# Cargar imagen generada
img = Image.open(IMAGEN_A_MAPEAR)
img_width, img_height = img.size

# Reducir un poco en la interfaz de Python si es muy grande para la pantalla
escala_visual = 0.6 
img_resized = img.resize((int(img_width * escala_visual), int(img_height * escala_visual)))
img_tk = ImageTk.PhotoImage(img_resized)

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)
canvas = tk.Canvas(frame, width=img_tk.width(), height=700, scrollregion=(0, 0, img_tk.width(), img_tk.height()))
vbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
vbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas.config(yscrollcommand=vbar.set)
canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

# Variables de estado
x_columnas_pct = []
y_filas_pct = []
y_temp_primeros = []
botones_por_fila = []
clicks_primera_fila = []

# ID inicial para las casillas (Para que la pág 4 no sobreescriba el "Item 1" de la pág 3)
# Preguntamos en qué número de ítem empieza esta hoja para que el HTML los agrupe bien
inicio_item = int(input(f"👉 ¿En qué número de ítem empieza esta página? (Ej. Si la hoja anterior terminó en 14, escribe 15): "))

def on_click(event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)

    x_pct = (x / img_tk.width()) * 100
    y_pct = (y / img_tk.height()) * 100

    if len(x_columnas_pct) < 5:
        x_columnas_pct.append(x_pct)
        y_temp_primeros.append(y_pct)
        
        rb = tk.Radiobutton(canvas, value=1, bg="red")
        win = canvas.create_window(x, y, window=rb)
        clicks_primera_fila.append(win)

        if len(x_columnas_pct) == 5:
            y_promedio_pct = sum(y_temp_primeros) / 5
            y_filas_pct.append(y_promedio_pct)
            
            y_promedio_real = (y_promedio_pct / 100) * img_tk.height()
            for i, w in enumerate(clicks_primera_fila):
                x_real = (x_columnas_pct[i] / 100) * img_tk.width()
                canvas.coords(w, x_real, y_promedio_real)
            botones_por_fila.append(clicks_primera_fila.copy())
            print(f"✅ Columnas fijadas. Fila 1 lista.")

    else:
        y_filas_pct.append(y_pct)
        nueva_fila_btns = []
        for col_x_pct in x_columnas_pct:
            x_real = (col_x_pct / 100) * img_tk.width()
            rb = tk.Radiobutton(canvas, value=1, bg="blue")
            win = canvas.create_window(x_real, y, window=rb)
            nueva_fila_btns.append(win)
        botones_por_fila.append(nueva_fila_btns)
        print(f"✅ Fila {len(y_filas_pct)} agregada.")

def deshacer(event):
    if len(y_filas_pct) > 1:
        y_filas_pct.pop()
        btns_a_borrar = botones_por_fila.pop()
        for btn in btns_a_borrar:
            canvas.delete(btn)
        print("⏪ Última fila borrada.")

def guardar(event):
    if len(x_columnas_pct) < 5:
        print("Error: Necesitas marcar al menos la primera fila.")
        return
        
    datos_pagina = {}
    for i, y_pct in enumerate(y_filas_pct):
        # Nombramos la casilla según el número real del ítem
        casilla = f"casilla_{inicio_item + i}"
        puntos = []
        for x_pct in x_columnas_pct:
            puntos.append([round(x_pct, 3), round(y_pct, 3)])
        datos_pagina[casilla] = puntos

    coordenadas_globales = {}
    if os.path.exists(ARCHIVO_SALIDA):
        with open(ARCHIVO_SALIDA, "r", encoding="utf-8") as f:
            contenido = f.read().replace("const coordenadasGlobales = ", "").rstrip(";")
            if contenido:
                coordenadas_globales = json.loads(contenido)
    
    # Agregar/Actualizar la capa actual
    coordenadas_globales[ID_CAPA_HTML] = datos_pagina

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write("const coordenadasGlobales = ")
        json.dump(coordenadas_globales, f, indent=4)
        f.write(";")
        
    print(f"\n🎉 ¡Página {num_pag} guardada exitosamente en '{ARCHIVO_SALIDA}'!")
    root.destroy()

canvas.bind("<Button-1>", on_click)
root.bind("z", deshacer)
root.bind("<Return>", guardar)

print(f"\n--- INSTRUCCIONES PÁGINA {num_pag} ---")
print("1. 5 clics en la primera fila (para fijar las columnas).")
print("2. 1 clic por cada una de las filas siguientes.")
print("3. Presiona 'Enter' para guardar esta página.")
root.mainloop()