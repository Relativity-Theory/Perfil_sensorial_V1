import tkinter as tk
from tkinter import simpledialog
import json
import os
from PIL import Image, ImageTk

# --- CONFIGURACIÓN ---
print("\n=== MAPEADOR DE CAJAS DE TEXTO (DATOS DEL PACIENTE) ===")
num_pag = input("👉 ¿En qué página están los datos personales? (Normalmente es la 2): ")

IMAGEN_A_MAPEAR = f"images/pagina_{num_pag}.jpg"
ARCHIVO_SALIDA = "templates/coordenadas_inputs.json"

if not os.path.exists(IMAGEN_A_MAPEAR):
    print(f"\n❌ Error: No se encontró {IMAGEN_A_MAPEAR}.")
    exit()

root = tk.Tk()
root.title(f"Mapeador de Inputs - Página {num_pag}")

# Cargar imagen generada
img = Image.open(IMAGEN_A_MAPEAR)
img_width, img_height = img.size

# Reducimos visualmente para que quepa en tu pantalla
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

# Diccionario para guardar todo
coordenadas_inputs = {}
historial_dibujos = []

# Cargar datos anteriores si existen para no sobreescribir
if os.path.exists(ARCHIVO_SALIDA):
    with open(ARCHIVO_SALIDA, "r", encoding="utf-8") as f:
        coordenadas_inputs = json.load(f)

def on_click(event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)

    # Calcular el porcentaje exacto
    x_pct = (x / img_tk.width()) * 100
    y_pct = (y / img_tk.height()) * 100

    identificador = simpledialog.askstring(
        "Identificador de Input", 
        "¿Qué dato se escribirá aquí?\n\nEjemplos: nombre, edad, fecha",
        parent=root
    )

    if identificador:
        identificador = identificador.strip().lower()
        
        # Estructura del JSON corregida
        if str(num_pag) not in coordenadas_inputs:
            coordenadas_inputs[str(num_pag)] = {}
            
        coordenadas_inputs[str(num_pag)][identificador] = {
            "x_pct": round(x_pct, 3),
            "y_pct": round(y_pct, 3)
        }

        # Dibujar un texto azul para diferenciarlo del otro mapeador
        texto_id = canvas.create_text(x, y-10, text=identificador, fill="blue", font=("Arial", 12, "bold"))
        rect_id = canvas.create_rectangle(x, y-5, x+100, y+15, outline="blue", width=2)
        
        historial_dibujos.append({
            "pag": str(num_pag),
            "id": identificador, 
            "dibujos": (texto_id, rect_id)
        })
        
        print(f"✅ Caja de texto registrada [{identificador}] en página {num_pag}")

def deshacer(event):
    if historial_dibujos:
        ultimo = historial_dibujos.pop()
        pag = ultimo["pag"]
        identificador = ultimo["id"]
        texto_id, rect_id = ultimo["dibujos"]
        
        canvas.delete(texto_id)
        canvas.delete(rect_id)
        
        if pag in coordenadas_inputs and identificador in coordenadas_inputs[pag]:
            del coordenadas_inputs[pag][identificador]
            
        print(f"⏪ Borrado [{identificador}]")

def guardar(event):
    if not coordenadas_inputs:
        print("Error: No has mapeado nada aún.")
        return
        
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        json.dump(coordenadas_inputs, f, indent=4)
        
    print(f"\n🎉 ¡Guardado exitosamente en '{ARCHIVO_SALIDA}'!")
    root.destroy()

canvas.bind("<Button-1>", on_click)
root.bind("z", deshacer)
root.bind("<Return>", guardar)

print("\n--- INSTRUCCIONES ---")
print("1. Haz clic justo al inicio de la línea punteada donde Cami deba escribir.")
print("2. Escribe de qué se trata (ej. edad).")
print("3. Tecla 'Z' para deshacer.")
print("4. Tecla 'Enter' para guardar y salir.\n")

root.mainloop()