import fitz  # PyMuPDF
import os

# 1. Asegurar que las carpetas existan
os.makedirs("images", exist_ok=True)
os.makedirs("templates", exist_ok=True)

pdf_path = "Perfil_sensorial.pdf"
html_path = "index.html"

print("Extrayendo imágenes del PDF...")
doc = fitz.open(pdf_path)
html_paginas = []

# 2. Convertir cada página en imagen de alta resolución
for i in range(len(doc)):
    num_pag = i + 1
    page = doc.load_page(i)
    # Zoom x2 para que se vea nítido en cualquier pantalla
    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat)
    
    img_filename = f"images/pagina_{num_pag}.jpg"
    pix.save(img_filename)
    print(f"✅ Guardada: {img_filename}")
    
    # Crear el bloque HTML para esta página
    html_paginas.append(f'''
        <div class="contenedor-hoja">
            <img src="{img_filename}" alt="Página {num_pag}" class="imagen-pdf">
            <div class="capa-botones" id="capa_pag_{num_pag}"></div>
        </div>
    ''')

# 3. Generar el archivo index.html con el diseño estético
html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfil Sensorial - Evaluación TO</title>
    <style>
        body {{
            background-color: #F3F4F6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            margin: 0;
        }}
        .contenedor-hoja {{
            position: relative;
            margin-bottom: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-radius: 8px;
            background-color: white;
            /* El ancho se ajustará al 100% de la pantalla hasta un máximo */
            max-width: 900px; 
            width: 100%;
        }}
        .imagen-pdf {{
            width: 100%;
            display: block;
            border-radius: 8px;
        }}
        .capa-botones {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
        }}
        /* Diseño de los botones modernos */
        input[type="radio"] {{
            appearance: none;
            -webkit-appearance: none;
            width: 1.8vw; /* Tamaño relativo a la pantalla */
            max-width: 22px; height: 1.8vw; max-height: 22px;
            border: 2px solid #D1D5DB;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, 0.8);
            cursor: pointer;
            position: absolute;
            transform: translate(-50%, -50%);
            transition: all 0.2s ease;
            margin: 0;
        }}
        input[type="radio"]:hover {{ background-color: #FCE7F3; }}
        input[type="radio"]:checked {{
            border: 6px solid #FF71A4;
            background-color: white;
        }}
        .btn-guardar {{
            margin: 30px 0; padding: 15px 40px; font-size: 18px; font-weight: bold;
            color: white; background-color: #FF71A4; border: none;
            border-radius: 30px; cursor: pointer;
            box-shadow: 0 4px 6px rgba(255, 113, 164, 0.3); transition: 0.2s;
        }}
        .btn-guardar:hover {{ background-color: #E05B8D; transform: scale(1.05); }}
    </style>
</head>
<body>

    {''.join(html_paginas)}

    <button class="btn-guardar" onclick="procesarResultados()">Guardar Respuestas</button>

    <script src="templates/coordenadas.js"></script>

    <script>
        // Dibujar botones basados en el archivo coordenadas.js
        if (typeof coordenadasGlobales !== 'undefined') {{
            for (const [pag_id, datosPagina] of Object.entries(coordenadasGlobales)) {{
                const capa = document.getElementById(pag_id);
                if (!capa) continue;

                for (const [casilla, puntos] of Object.entries(datosPagina)) {{
                    puntos.forEach((coord, index) => {{
                        const radioBtn = document.createElement('input');
                        radioBtn.type = 'radio';
                        radioBtn.name = casilla;
                        radioBtn.value = index + 1;
                        // Las coordenadas vienen en % para que sea Responsive
                        radioBtn.style.left = coord[0] + '%';
                        radioBtn.style.top = coord[1] + '%';
                        capa.appendChild(radioBtn);
                    }});
                }}
            }}
        }}

        function procesarResultados() {{
            const resultados = {{}};
            const inputsSeleccionados = document.querySelectorAll('input[type="radio"]:checked');
            inputsSeleccionados.forEach(input => {{
                resultados[input.name] = parseInt(input.value);
            }});
            console.log("--- PUNTUACIONES ---", resultados);
            alert("Respuestas capturadas. Revisa la consola.");
        }}
    </script>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\n🎉 ¡Proyecto inicializado! Se generó el archivo {html_path}")