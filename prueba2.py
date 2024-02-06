import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import re
import pdfplumber
import csv
import tabula
class DataFrameManipulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manipulador de DataFrame")
        
        self.df = None
        self.file_path = None

        self.load_button = tk.Button(master, text="Cargar Excel", command=self.load_excel)
        self.load_button.pack(pady=10)

        # Crear la etiqueta para la ruta del archivo
        self.file_path_label = tk.Label(master, text="Ruta del archivo Excel:")
        self.file_path_label.pack()

        self.tabulation_label = tk.Label(master, text="Seleccione el tipo de tabulación:")
        self.tabulation_label.pack()

        self.tabulation_var = tk.StringVar()
        self.tabulation_var.set("\t")  
        self.tabulation_options = ["\t", ",", ";"]  

        self.tabulation_menu = tk.OptionMenu(master, self.tabulation_var, *self.tabulation_options)
        self.tabulation_menu.pack(pady=5)

        self.column_label = tk.Label(master, text="Ingrese la ubicación de las columnas (separadas por coma):")
        self.column_label.pack()

        self.column_entry = tk.Entry(master)
        self.column_entry.pack(pady=10)

        self.process_button = tk.Button(master, text="Procesar", command=self.process_data)
        self.process_button.pack(pady=10)

    def load_excel(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            self.file_path = file_path
            self.file_path_label.config(text=f"Ruta del archivo Excel: {file_path}")
            try:
                self.df = pd.read_excel(file_path)
                print("Archivo Excel cargado exitosamente.")
            except Exception as e:
                print(f"Error al cargar el archivo Excel: {e}")
                messagebox.showerror("Error", f"Error al cargar el archivo Excel:\n{e}")

    def process_data(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Por favor, carga un archivo Excel primero.")
            return

        tabulation = self.tabulation_var.get()
        columns_str = self.column_entry.get()
        columns = [col.strip() for col in columns_str.split(',')]

        try:
            result_df = self.df[columns]

            # Solicitar al usuario la ubicación y el nombre del archivo CSV
            file_path = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
                title="Guardar DataFrame como CSV"
            )

            if file_path:
                result_df.to_csv(file_path, index=False)
                messagebox.showinfo("Éxito", f"DataFrame manipulado guardado en:\n{file_path}")

        except KeyError as e:
            messagebox.showerror("Error", f"La columna '{e.args[0]}' no existe en el DataFrame.")

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

def excel_a_csv():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=(("Archivos de Excel", "*.xlsx"), ("Todos los archivos", "*.*")))
    
    if not file_path:
        print("No se ha seleccionado ningún archivo Excel.")
        return
    else:
        df = pd.read_excel(file_path, engine='openpyxl', sheet_name=None)
        sheet_names = list(df.keys())
    
        for sheet_name in sheet_names:
            selected_df = df[sheet_name]
            array = selected_df.to_numpy()
        
            csv_file_name = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
        
            if csv_file_name:
                selected_df.to_csv(csv_file_name, index=False)
                print(f"Se ha convertido la hoja '{sheet_name}' a CSV con éxito.")

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

    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages
        data_frames = []
        for page in pages:
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                data_frames.append(df)

    if data_frames:
        result_df = pd.concat(data_frames, ignore_index=True)
    
        writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
        result_df.to_excel(writer, index=False, sheet_name="Sheet1")
        writer.close()
        print("El archivo PDF se ha convertido a Excel con éxito.")
    else:
        print("No se encontraron tablas en el PDF.")

def menu():
    root = tk.Tk()
    root.configure(background="#1294a7")
    root.geometry("500x500")
    global label
    frame = tk.Frame(root, bg="#1294a7") 
    frame.pack()

    label = tk.Label(root, text="Seleccione una opción:", background="#1294a7", fg="white")
    label.pack()
    label.config(font=('Helvetica', 13))

    button_registrar = tk.Button(root, text="Registrar usuario", command=registrar_usuario_interfaz, pady=5, background="lightblue", font=("Helvetica", 8))
    button_registrar.pack(side="top", padx=15, pady=8)

    button_excel = tk.Button(root, text="Convertir Excel a CSV", command=excel_a_csv, pady=5, background="lightblue", font=("Helvetica", 8))
    button_excel.pack(side="top", padx=15, pady=8)

    boton_convertir = tk.Button(root, text="Convertir de PDF a CSV", command=convertir_pdf_a_csv, pady=5, background="lightblue", font=("Helvetica", 8))
    boton_convertir.pack(side="top", padx=15, pady=8)

    boton_convertir_pdf_excel = tk.Button(root, text="Convertir de PDF a Excel", command=pdf_a_excel, pady=5, background="lightblue", font=("Helvetica", 8))
    boton_convertir_pdf_excel.pack(side="top", padx=15, pady=8)

    boton_df_manipulator = tk.Button(root, text="Manipular DataFrame", command=mostrar_df_manipulator, pady=5, background="lightblue", font=("Helvetica", 8))
    boton_df_manipulator.pack(side="top", padx=15, pady=8)

    root.title("Conversor de datos")
    root.mainloop()

def mostrar_df_manipulator():
    df_manipulator_root = tk.Toplevel()
    df_manipulator_root.geometry("500x500")
    df_manipulator_root.title("Manipulador de DataFrame")
    df_manipulator_app = DataFrameManipulator(df_manipulator_root)

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
    root = tk.Tk()
    app = DataFrameManipulator(root)
    root.mainloop()
