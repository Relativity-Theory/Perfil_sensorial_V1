import tkinter as tk
from tkinter import simpledialog
import json
import os
from PIL import Image, ImageTk

# --- CONFIGURACIÓN ---
print("\n=== MAPEADOR DE RESULTADOS Y TOTALES ===")
num_pag = input("👉 ¿Qué página es la hoja de resultados? (Normalmente es la 6): ")

IMAGEN_A_MAPEAR = f"images/pagina_{num_pag}.jpg"
ARCHIVO_SALIDA = "templates/coordenadas_textos.json"

if not os.path.exists(IMAGEN_A_MAPEAR):
    print(f"\n❌ Error: No se encontró {IMAGEN_A_MAPEAR}.")
    exit()

root = tk.Tk()
root.title(f"Mapeador de Textos - Página {num_pag}")

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

# Diccionario para guardar todo y lista para deshacer
coordenadas_textos = {}
historial_dibujos = []

def on_click(event):
    # Obtener coordenadas relativas al Canvas
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)

    # Calcular el porcentaje para que sea universal
    x_pct = (x / img_tk.width()) * 100
    y_pct = (y / img_tk.height()) * 100

    # Preguntar al usuario qué representa este cuadro
    identificador = simpledialog.askstring(
        "Identificador de Cuadro", 
        "¿Qué va aquí?\n\nEjemplos:\n- Si es el ítem 3, escribe: 3\n- Si es un total, escribe: total_registro",
        parent=root
    )

    if identificador:
        identificador = identificador.strip().lower()
        
        # Guardar en el diccionario
        coordenadas_textos[identificador] = {
            "x_pct": round(x_pct, 3),
            "y_pct": round(y_pct, 3),
            # Guardamos también el valor absoluto pensando en si luego usamos PyMuPDF para estampar el PDF original
            # Como la imagen se guardó con zoom x2 (mat = fitz.Matrix(2.0, 2.0)), dividimos por 2 para la escala real del PDF
            "x_pdf_real": round((x_pct / 100) * (img_width / 2.0), 2),
            "y_pdf_real": round((y_pct / 100) * (img_height / 2.0), 2)
        }

        # Dibujar un texto rojo para confirmación visual
        texto_id = canvas.create_text(x, y, text=identificador, fill="red", font=("Arial", 10, "bold"))
        circulo_id = canvas.create_oval(x-3, y-3, x+3, y+3, fill="red", outline="red")
        
        # Guardar en historial por si queremos borrar
        historial_dibujos.append({
            "id": identificador, 
            "dibujos": (texto_id, circulo_id)
        })
        
        print(f"✅ Registrado [{identificador}]")

def deshacer(event):
    if historial_dibujos:
        ultimo = historial_dibujos.pop()
        identificador = ultimo["id"]
        texto_id, circulo_id = ultimo["dibujos"]
        
        # Borrar del canvas
        canvas.delete(texto_id)
        canvas.delete(circulo_id)
        
        # Borrar del diccionario
        if identificador in coordenadas_textos:
            del coordenadas_textos[identificador]
            
        print(f"⏪ Borrado [{identificador}]")

def guardar(event):
    if not coordenadas_textos:
        print("Error: No has mapeado nada aún.")
        return
        
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        json.dump(coordenadas_textos, f, indent=4)
        
    print(f"\n🎉 ¡Guardado exitosamente en '{ARCHIVO_SALIDA}'!")
    root.destroy()

# Vincular eventos
canvas.bind("<Button-1>", on_click)
root.bind("z", deshacer)
root.bind("<Return>", guardar)

print("\n--- INSTRUCCIONES ---")
print("1. Haz clic en un recuadro.")
print("2. Escribe a qué ítem o total corresponde.")
print("3. Tecla 'Z' para deshacer el último clic.")
print("4. Tecla 'Enter' para guardar y salir.\n")

root.mainloop()
