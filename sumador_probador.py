# probador_sumas.py

print("\n=== TEST DE VALIDACIÓN MATEMÁTICA ===")
print("Vamos a simular que respondiste todas las preguntas de una columna con el mismo valor.\n")

cuadrantes = {
    "Bajo Registro": [3, 6, 12, 15, 21, 23, 36, 37, 39, 41, 44, 45, 52, 55, 59],
    "Búsqueda Sensorial": [2, 4, 8, 10, 14, 17, 19, 28, 30, 32, 40, 42, 47, 50, 58],
    "Sensibilidad Sensorial": [7, 9, 13, 16, 20, 22, 25, 27, 31, 33, 34, 48, 51, 54, 60],
    "Evitación Sensorial": [1, 5, 11, 18, 24, 26, 29, 35, 38, 43, 46, 49, 53, 56, 57]
}

respuestas_simuladas = {}

# 1. Pedirle al usuario qué valor quiere asignar a cada columna
for nombre, items in cuadrantes.items():
    while True:
        try:
            valor = int(input(f"👉 ¿Qué puntaje (1 al 5) pondrás en todas las opciones de '{nombre}'?: "))
            if 1 <= valor <= 5:
                break
            else:
                print("Por favor, ingresa un número entre 1 y 5.")
        except ValueError:
            print("Entrada inválida. Ingresa un número.")
            
    # Asignamos ese valor a todos los ítems de este cuadrante
    for item in items:
        respuestas_simuladas[item] = valor

print("\n" + "="*40)
print(" RESULTADOS ESPERADOS EN LA WEB")
print("="*40)

# 2. Calcular y mostrar los resultados
for nombre, items in cuadrantes.items():
    suma_total = sum(respuestas_simuladas[item] for item in items)
    cantidad_items = len(items)
    valor_usado = respuestas_simuladas[items[0]]
    
    print(f"🔸 {nombre}:")
    print(f"   Fórmula: {cantidad_items} ítems x {valor_usado} puntos")
    print(f"   TOTAL ESPERADO: {suma_total} puntos\n")

print("💡 Instrucción:")
print("Ve a tu página web, llena las columnas con los mismos valores que ingresaste aquí")
print("y presiona 'Calcular'. ¡Los totales de la página 6 deben ser exactamente estos!")# probador_sumas.py

print("\n=== TEST DE VALIDACIÓN MATEMÁTICA ===")
print("Vamos a simular que respondiste todas las preguntas de una columna con el mismo valor.\n")

cuadrantes = {
    "Bajo Registro": [3, 6, 12, 15, 21, 23, 36, 37, 39, 41, 44, 45, 52, 55, 59],
    "Búsqueda Sensorial": [2, 4, 8, 10, 14, 17, 19, 28, 30, 32, 40, 42, 47, 50, 58],
    "Sensibilidad Sensorial": [7, 9, 13, 16, 20, 22, 25, 27, 31, 33, 34, 48, 51, 54, 60],
    "Evitación Sensorial": [1, 5, 11, 18, 24, 26, 29, 35, 38, 43, 46, 49, 53, 56, 57]
}

respuestas_simuladas = {}

# 1. Pedirle al usuario qué valor quiere asignar a cada columna
for nombre, items in cuadrantes.items():
    while True:
        try:
            valor = int(input(f"👉 ¿Qué puntaje (1 al 5) pondrás en todas las opciones de '{nombre}'?: "))
            if 1 <= valor <= 5:
                break
            else:
                print("Por favor, ingresa un número entre 1 y 5.")
        except ValueError:
            print("Entrada inválida. Ingresa un número.")
            
    # Asignamos ese valor a todos los ítems de este cuadrante
    for item in items:
        respuestas_simuladas[item] = valor

print("\n" + "="*40)
print(" RESULTADOS ESPERADOS EN LA WEB")
print("="*40)

# 2. Calcular y mostrar los resultados
for nombre, items in cuadrantes.items():
    suma_total = sum(respuestas_simuladas[item] for item in items)
    cantidad_items = len(items)
    valor_usado = respuestas_simuladas[items[0]]
    
    print(f"🔸 {nombre}:")
    print(f"   Fórmula: {cantidad_items} ítems x {valor_usado} puntos")
    print(f"   TOTAL ESPERADO: {suma_total} puntos\n")

print("💡 Instrucción:")
print("Ve a tu página web, llena las columnas con los mismos valores que ingresaste aquí")
print("y presiona 'Calcular'. ¡Los totales de la página 6 deben ser exactamente estos!")# probador_sumas.py

print("\n=== TEST DE VALIDACIÓN MATEMÁTICA ===")
print("Vamos a simular que respondiste todas las preguntas de una columna con el mismo valor.\n")

cuadrantes = {
    "Bajo Registro": [3, 6, 12, 15, 21, 23, 36, 37, 39, 41, 44, 45, 52, 55, 59],
    "Búsqueda Sensorial": [2, 4, 8, 10, 14, 17, 19, 28, 30, 32, 40, 42, 47, 50, 58],
    "Sensibilidad Sensorial": [7, 9, 13, 16, 20, 22, 25, 27, 31, 33, 34, 48, 51, 54, 60],
    "Evitación Sensorial": [1, 5, 11, 18, 24, 26, 29, 35, 38, 43, 46, 49, 53, 56, 57]
}

respuestas_simuladas = {}

# 1. Pedirle al usuario qué valor quiere asignar a cada columna
for nombre, items in cuadrantes.items():
    while True:
        try:
            valor = int(input(f"👉 ¿Qué puntaje (1 al 5) pondrás en todas las opciones de '{nombre}'?: "))
            if 1 <= valor <= 5:
                break
            else:
                print("Por favor, ingresa un número entre 1 y 5.")
        except ValueError:
            print("Entrada inválida. Ingresa un número.")
            
    # Asignamos ese valor a todos los ítems de este cuadrante
    for item in items:
        respuestas_simuladas[item] = valor

print("\n" + "="*40)
print(" RESULTADOS ESPERADOS EN LA WEB")
print("="*40)

# 2. Calcular y mostrar los resultados
for nombre, items in cuadrantes.items():
    suma_total = sum(respuestas_simuladas[item] for item in items)
    cantidad_items = len(items)
    valor_usado = respuestas_simuladas[items[0]]
    
    print(f"🔸 {nombre}:")
    print(f"   Fórmula: {cantidad_items} ítems x {valor_usado} puntos")
    print(f"   TOTAL ESPERADO: {suma_total} puntos\n")

print("💡 Instrucción:")
print("Ve a tu página web, llena las columnas con los mismos valores que ingresaste aquí")
print("y presiona 'Calcular'. ¡Los totales de la página 6 deben ser exactamente estos!")
