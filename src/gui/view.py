import tkinter as tk
from src.code import process_files as pf
import threading


class FuncionThread(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__()
        self.target = target
        self.args = args
        self.res = []


def search_files(U_red, S_red, VT_red, vocabulario_dict, docs, entrada_consulta, resultados):
    consulta = entrada_consulta.get()

    if consulta:
        consulta = pf.process_docs({'c':consulta})
        documentos_relevantes = pf.procesar_consulta(consulta, U_red, S_red, VT_red, vocabulario_dict, docs,
                                                     4)
        mostrar_resultados(documentos_relevantes, resultados, docs)


def mostrar_resultados(index_doc, resultados, docs):
    resultados.delete(1.0, tk.END)
    l = []
    for i, key in enumerate(docs):
        l.append((i,key))

    for i in index_doc:
        for k in l:
            if i == k[0]:
                resultados.insert(tk.END, k[1] + "\n"+docs[k[1]][0:100] + "\n")


def pre_process(data):
    k = 10
    docs = pf.load_files(data)
    t_docs = pf.process_docs(docs)
    matriz_td, vocabulario_dict = pf.construir_matriz_termino_documento(t_docs)
    U_red, S_red, VT_red = pf.aplicar_SVD(matriz_td, k)

    return U_red, S_red, VT_red, vocabulario_dict, docs


def init(data):
    t = FuncionThread(target=pre_process)
    t.start()

    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Search Docs")

    # Crear entrada de texto para la consulta
    entrada_consulta = tk.Entry(ventana, width=50)
    entrada_consulta.pack(pady=10)

    # Botón para procesar la consulta
    boton_consultar = tk.Button(ventana, text="Search",
                                command=lambda: search_files(U_red, S_red, VT_red, vocabulario_dict, docs, entrada_consulta, resultados))
    boton_consultar.pack()

    # Crear recuadro para mostrar los resultados
    resultados = tk.Text(ventana, height=10, width=50)
    resultados.pack(pady=10)

    t.join()

    U_red, S_red, VT_red, vocabulario_dict, docs = t.target(data)

    # Ejecutar la ventana
    ventana.mainloop()
