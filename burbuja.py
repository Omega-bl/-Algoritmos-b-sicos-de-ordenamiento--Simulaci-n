import tkinter as tk

METODO = 'Burbuja'
PRECIOS = [50, 20, 40, 10, 30]
pasos = []
actual = 0


# Guardar cómo queda la lista en cada paso.
def guardar_paso(lista, texto, activos=(), clave=None, hueco=None):
    pasos.append({"lista": lista.copy(), "texto": texto,
                  "activos": activos, "clave": clave, "hueco": hueco})


# Esta es la parte que cambia en cada método.
def ordenar(datos):
    pasos.clear()
    lista = datos.copy()
    guardar_paso(lista, "Lista inicial. Comparamos vecinos y movemos el mayor a la derecha.")
    for pasada in range(len(lista) - 1):
        cambio = False
        for j in range(len(lista) - 1 - pasada):
            guardar_paso(lista, f"Comparamos {lista[j]} y {lista[j + 1]} en las posiciones {j} y {j + 1}.", (j, j + 1))
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                cambio = True
                guardar_paso(lista, "Intercambiamos los vecinos porque el primero era mayor.", (j, j + 1))
        if not cambio:
            break
    guardar_paso(lista, "Lista ordenada. Puedes pulsar Reiniciar para repetir.")
    return lista


# Mostrar el paso actual en la ventana.
def mostrar():
    paso = pasos[actual]
    for i, valor in enumerate(paso["lista"]):
        color = "white"
        texto = str(valor)
        if i in paso["activos"]:
            color = "lightblue"
        if i == paso["hueco"]:
            color = "moccasin"
            texto += "*"
        casillas[i].config(text=texto, bg=color)
    explicacion.config(text=paso["texto"])
    temporal.config(text=f"Clave temporal: {paso['clave']} | Hueco: posición {paso['hueco']}"
                    if paso["clave"] is not None else "Clave temporal: sin usar")
    contador.config(text=f"Paso {actual + 1} de {len(pasos)}")
    siguiente.config(state="normal" if actual < len(pasos) - 1 else "disabled")


def avanzar():
    global actual
    if actual < len(pasos) - 1:
        actual += 1
        mostrar()


def reiniciar():
    global actual
    actual = 0
    mostrar()


# Crear la misma ventana sencilla para cualquiera de los tres métodos.
if __name__ == "__main__":
    ordenar(PRECIOS)
    ventana = tk.Tk()
    ventana.title("Ordenamiento por " + METODO)
    ventana.geometry("760x440")
    ventana.minsize(720, 440)
    tk.Label(ventana, text=METODO, font=("Arial", 18, "bold")).pack(pady=12)
    tk.Label(ventana, text=f"Precios originales: {PRECIOS}", font=("Arial", 11)).pack()
    memoria = tk.Frame(ventana)
    memoria.pack(pady=15)
    casillas = []
    for i in range(len(PRECIOS)):
        tk.Label(memoria, text=f"Posición {i}").grid(row=0, column=i)
        casilla = tk.Label(memoria, width=4, height=2, font=("Arial", 22),
                           relief="solid", borderwidth=1, bg="white", fg="black")
        casilla.grid(row=1, column=i, padx=8, pady=5)
        casillas.append(casilla)
    temporal = tk.Label(ventana, font=("Arial", 11))
    temporal.pack()
    explicacion = tk.Label(ventana, wraplength=680, height=3, font=("Arial", 11))
    explicacion.pack(padx=15, pady=5)
    contador = tk.Label(ventana)
    contador.pack()
    botones = tk.Frame(ventana)
    botones.pack(pady=10)
    siguiente = tk.Button(botones, text="Siguiente paso", command=avanzar, padx=12, pady=5)
    siguiente.pack(side="left", padx=5)
    tk.Button(botones, text="Reiniciar", command=reiniciar, padx=12, pady=5).pack(side="left")
    tk.Label(ventana, text="Azul: posiciones activas. Naranja y *: hueco lógico.\n"
             "En Inserción se repiten valores temporalmente mientras la clave está guardada.").pack()
    mostrar()
    ventana.mainloop()
