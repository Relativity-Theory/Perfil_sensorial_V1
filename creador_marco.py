import tkinter as tk
from tkinter import simpledialog
import json
import os
from PIL import Image, ImageTk

# --- CONFIGURACIÓN ---
print("\n=== MAPEADOR DE MARCOS ROJOS (ÁREAS Y RANGOS ETARIOS) ===")
num_pag = input("👉 ¿En qué página están las tablas a enmarcar? (Normalmente es la 8): ")

IMAGEN_A_MAPEAR = f"images/pagina_{num_pag}.jpg"
ARCHIVO_SALIDA = "templates/coordenadas_marcos.json"

if not os.path.exists(IMAGEN_A_MAPEAR):
    print(f"\n❌ Error: No se encontró {IMAGEN_A_MAPEAR}.")
    exit()

root = tk.Tk()
root.title(f"Mapeador de Marcos - Página {num_pag} (Arrastra el mouse)")

img = Image.open(IMAGEN_A_MAPEAR)
img_width, img_height = img.size

escala_visual = 0.6 
img_resized = img.resize((int(img_width * escala_visual), int(img_height * escala_visual)))
img_tk = ImageTk.PhotoImage(img_resized)

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)
canvas = tk.Canvas(frame, width=img_tk.width(), height=700, scrollregion=(0, 0, img_tk.width(), img_tk.height()), cursor="cross")
vbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
vbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas.config(yscrollcommand=vbar.set)
canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

# Variables para el dibujo del rectángulo
rect_dibujando = None
start_x = start_y = 0

# Diccionario para guardar todo
coordenadas_marcos = {}
historial_dibujos = []

if os.path.exists(ARCHIVO_SALIDA):
    with open(ARCHIVO_SALIDA, "r", encoding="utf-8") as f:
        coordenadas_marcos = json.load(f)

def on_button_press(event):
    global start_x, start_y, rect_dibujando
    start_x = canvas.canvasx(event.x)
    start_y = canvas.canvasy(event.y)
    # Crear un rectángulo temporal que se irá expandiendo
    rect_dibujando = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=3)

def on_move_press(event):
    global rect_dibujando
    cur_x = canvas.canvasx(event.x)
    cur_y = canvas.canvasy(event.y)
    # Actualizar el tamaño del rectángulo mientras se arrastra el mouse
    canvas.coords(rect_dibujando, start_x, start_y, cur_x, cur_y)

def on_button_release(event):
    global rect_dibujando
    end_x = canvas.canvasx(event.x)
    end_y = canvas.canvasy(event.y)

    # Evitar clics accidentales sin arrastrar
    if abs(end_x - start_x) < 5 or abs(end_y - start_y) < 5:
        canvas.delete(rect_dibujando)
        return

    # Calcular posiciones y tamaños en porcentajes (ideal para CSS web)
    x_min, x_max = sorted([start_x, end_x])
    y_min, y_max = sorted([start_y, end_y])
    
    x_pct = (x_min / img_tk.width()) * 100
    y_pct = (y_min / img_tk.height()) * 100
    width_pct = ((x_max - x_min) / img_tk.width()) * 100
    height_pct = ((y_max - y_min) / img_tk.height()) * 100

    identificador = simpledialog.askstring(
        "Identificador del Marco", 
        "¿Qué significa este recuadro?\n\nEjemplos: 11_17_registro, 18_64_busqueda, etc.",
        parent=root
    )

    if identificador:
        identificador = identificador.strip().lower()
        
        if str(num_pag) not in coordenadas_marcos:
            coordenadas_marcos[str(num_pag)] = {}
            
        # Guardamos top, left, width y height para inyectar un <div> exacto en HTML
        coordenadas_marcos[str(num_pag)][identificador] = {
            "x_pct": round(x_pct, 3),
            "y_pct": round(y_pct, 3),
            "width_pct": round(width_pct, 3),
            "height_pct": round(height_pct, 3)
        }

        texto_id = canvas.create_text(x_min, y_min - 10, text=identificador, fill="red", font=("Arial", 12, "bold"), anchor="w")
        
        historial_dibujos.append({
            "pag": str(num_pag),
            "id": identificador, 
            "dibujos": (texto_id, rect_dibujando)
        })
        print(f"✅ Marco registrado [{identificador}] en página {num_pag}")
    else:
        # Si cancela, borramos el rectángulo que estaba dibujando
        canvas.delete(rect_dibujando)

def deshacer(event):
    if historial_dibujos:
        ultimo = historial_dibujos.pop()
        pag = ultimo["pag"]
        identificador = ultimo["id"]
        texto_id, rect_id = ultimo["dibujos"]
        
        canvas.delete(texto_id)
        canvas.delete(rect_id)
        
        if pag in coordenadas_marcos and identificador in coordenadas_marcos[pag]:
            del coordenadas_marcos[pag][identificador]
            
        print(f"⏪ Marco [{identificador}] borrado.")

def guardar(event):
    if not coordenadas_marcos:
        print("Error: No has dibujado ningún marco aún.")
        return
        
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        json.dump(coordenadas_marcos, f, indent=4)
        
    print(f"\n🎉 ¡Guardado exitosamente en '{ARCHIVO_SALIDA}'!")
    root.destroy()

canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_move_press)
canvas.bind("<ButtonRelease-1>", on_button_release)
root.bind("z", deshacer)
root.bind("<Return>", guardar)

print("\n--- INSTRUCCIONES ---")
print("1. Haz CLIC Y ARRASTRA el mouse para dibujar un rectángulo sobre la zona a resaltar.")
print("2. Suelta el clic y escribe a qué corresponde (ej. 'rango_18_64_registro').")
print("3. Tecla 'Z' para deshacer el último dibujo.")
print("4. Tecla 'Enter' para guardar y salir.\n")

root.mainloop()
