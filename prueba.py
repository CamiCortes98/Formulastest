import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re
import csv
import tabula
from tkinter import Label
import pdfplumber



#Funcion para registrar usuarios, solo deja crear el usuario y lo almacena si el correo esta bien escrito y la contraseña posee una minuscula, una mayuscula, un numero y un minimo de 8 caracteres.

def registrar_usuario(email, contraseña):
    usuario = {}
    if re.match(r'^\S+@', email) and ' ' not in email and re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', contraseña):
        if email in usuario:
            print("El usuario ya existe")
        else:
            with open('usuarios.csv', mode='a', newline='') as file:
                userwriter = csv.writer(file)
                userwriter.writerow([email, contraseña])
                print("Usuario registrado exitosamente")
    else:
        print("El usuario no pudo ser creado")

#Funcion para realizar el cambio de archivo excel a csv

def excel_a_csv():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=(("Archivos de Excel", "*.xlsx"), ("Todos los archivos", "*.*")))
    if file_path:
        df = pd.read_excel(file_path, sheet_name=None)
        sheet_names = list(df.keys())
        num_sheets = len(sheet_names)
        num_sheets_to_convert = 1  # Puedes modificar esto para permitir al usuario seleccionar la cantidad de hojas a convertir
        selected_sheet_names = sheet_names[:num_sheets_to_convert]
        for sheet_name in selected_sheet_names:
            selected_df = df[sheet_name]
            array = selected_df.to_numpy()
            csv_file_name = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
            if csv_file_name:
                selected_df.to_csv(csv_file_name, index = False)
                print(array)

#Funcion para convertir de PDF a Csv
                
def convertir_pdf_a_csv():
    file_path = filedialog.askopenfilename(title="Seleccionar archivo PDF", filetypes=(("Archivos de PDF", "*.pdf"), ("Todos los archivos", "*.*")))
    if file_path:
        output_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
        if output_path:
            tabula.convert_into(file_path, output_path, output_format="csv", pages='all')


def pdf_a_excel():
    file_path = filedialog.askopenfilename(title="Seleccionar archivo PDF", filetypes=(("Archivos de PDF", "*.pdf"), ("Todos los archivos", "*.*")))
    
    if not file_path:
        print("No se ha seleccionado ningún archivo PDF.")
        return
    
    output_path = filedialog.asksaveasfilename(title="Guardar como archivo Excel", defaultextension=".xlsx", filetypes=(("Archivos de Excel", "*.xlsx"), ("Todos los archivos", "*.*")))
    
    if not output_path:
        print("No se ha seleccionado ninguna ubicación para guardar el archivo Excel.")
        return

    # Extraer datos del PDF y organizarlos en una lista de DataFrames
    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages
        data_frames = []
        for page in pages:
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                data_frames.append(df)

    # Concatenar todos los DataFrames en uno solo
    if data_frames:
        result_df = pd.concat(data_frames, ignore_index=True)
        
        # Escribir los datos en un archivo Excel
        writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
        result_df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()  # Utilizar solo esta línea, eliminar la línea duplicada
        print("El archivo PDF se ha convertido a Excel con éxito.")
    else:
        print("No se encontraron tablas en el PDF.")       

def menu():
    root = tk.Tk()
    root.configure(background="#1294a7")
    root.geometry("500x500")
    global label
    frame = tk.Frame(root, bg="#1294a7")  # Cambia el color de fondo del frame a un tono específico
    frame.pack()
  

    label = tk.Label(root, text="Seleccione una opción:", background="#1294a7", fg= "white")
    label.pack()
    label.config(font=('Helvetica', 13))
    #Boton registrar usuario
    button_registrar = tk.Button(root, text="Registrar usuario", command=registrar_usuario_interfaz, pady=5, background="lightblue", font=("Helvetica", 8))
    button_registrar.pack(side= "top", padx= 15, pady= 8)
    #Boton conversor
    button_excel = tk.Button(root, text="Convertir Excel a CSV", command=excel_a_csv, pady = 5, background="lightblue",font=("Helvetica", 8))
    button_excel.pack(side= "top", padx= 15, pady= 8)

    #Boton conversor
    
    boton_convertir = tk.Button(root, text="Convertir de PDF a CSV", command=convertir_pdf_a_csv, pady= 5, background="lightblue", font=("Helvetica", 8))
    boton_convertir.pack(side= "top", padx= 15, pady= 8)
    #Boton conversor
    root.title("Conversor de datos")
    boton_convertir = tk.Button(root, text="Convertir de PDF a Excel", command=pdf_a_excel, pady = 5, background="lightblue", font=("Helvetica", 8))
    boton_convertir.pack(side= "top", padx= 15, pady= 8)

    root.mainloop()

def registrar_usuario_interfaz():
   
    ventana = tk.Toplevel()
    ventana.title("Registrar usuario")
    ventana.geometry("500x300")

    label_email = tk.Label(ventana, text="Email:")
    label_email.pack()

    entry_email = tk.Entry(ventana)
    entry_email.pack()

    label_contraseña = tk.Label(ventana, text="Contraseña:")
    label_contraseña.pack()

    entry_contraseña = tk.Entry(ventana, show="*")
    entry_contraseña.pack()

    button_aceptar = tk.Button(ventana, text="Aceptar", command=lambda: registrar_usuario(entry_email.get(), entry_contraseña.get()))
    button_aceptar.pack()

if __name__ == "__main__":
    menu()
    