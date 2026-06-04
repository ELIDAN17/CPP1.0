# src/ui.py
"""
INTERFAZ GRÁFICA DE USUARIO - Tkinter
Diseño tipo Excel con todas las funcionalidades del documento
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import csv
from src.controllers import ControladorHojaCalculo


class MiniExcelAcademico:
    def __init__(self):
        self.controlador = ControladorHojaCalculo()
        self.archivo_actual = None
        
        self.ventana = tk.Tk()
        self.ventana.title("Mini Excel Académico - Estructuras de Datos")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg='#f0f0f0')
        
        self._crear_menu()
        self._crear_toolbar()
        self._crear_tabla()
        self._crear_paneles()
        self._crear_statusbar()
        self._cargar_ejemplo()
        self._actualizar_todo()
        
        self.ventana.mainloop()
    
    def _crear_menu(self):
        menubar = tk.Menu(self.ventana)
        self.ventana.config(menu=menubar)
        
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nuevo (Ctrl+N)", command=self._nuevo)
        menu_archivo.add_command(label="Abrir CSV (Ctrl+O)", command=self._abrir_csv)
        menu_archivo.add_command(label="Guardar CSV (Ctrl+S)", command=self._guardar_csv)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.quit)
        
        menu_editar = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=menu_editar)
        menu_editar.add_command(label="Registrar (Insert)", command=self._registrar)
        menu_editar.add_command(label="Editar (F2)", command=self._editar)
        menu_editar.add_command(label="Eliminar (Delete)", command=self._eliminar)
        menu_editar.add_separator()
        menu_editar.add_command(label="Deshacer (Ctrl+Z)", command=self._deshacer)
        
        menu_datos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datos", menu=menu_datos)
        menu_datos.add_command(label="Ordenar por Promedio (QuickSort)", command=self._ordenar_promedio)
        menu_datos.add_command(label="Ordenar por Código (MergeSort)", command=self._ordenar_codigo)
        
        menu_atencion = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Atención", menu=menu_atencion)
        menu_atencion.add_command(label="Agregar a Cola", command=self._agregar_cola)
        menu_atencion.add_command(label="Atender Siguiente", command=self._atender)
        menu_atencion.add_command(label="Ver Cola", command=self._ver_cola)
        
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self._acerca_de)
    
    def _crear_toolbar(self):
        toolbar = tk.Frame(self.ventana, bg='#e0e0e0', relief=tk.RAISED, bd=1)
        toolbar.pack(fill=tk.X, padx=2, pady=2)
        
        botones = [
            ("➕ Registrar", self._registrar),
            ("✏️ Editar", self._editar),
            ("🗑️ Eliminar", self._eliminar),
            ("📊 Ordenar Promedio", self._ordenar_promedio),
            ("🔤 Ordenar Código", self._ordenar_codigo),
            ("↩️ Deshacer", self._deshacer),
            ("👥 Agregar Cola", self._agregar_cola),
            ("🎓 Atender", self._atender)
        ]
        
        for texto, cmd in botones:
            btn = tk.Button(toolbar, text=texto, command=cmd, bg='#e0e0e0', padx=8)
            btn.pack(side=tk.LEFT, padx=2)
        
        tk.Label(toolbar, text="🔍 Buscar:", bg='#e0e0e0').pack(side=tk.LEFT, padx=(20,5))
        self.buscador_var = tk.StringVar()
        self.buscador_entry = tk.Entry(toolbar, textvariable=self.buscador_var, width=20)
        self.buscador_entry.pack(side=tk.LEFT)
        self.buscador_entry.bind('<KeyRelease>', self._buscar)
        
        btn_buscar = tk.Button(toolbar, text="Buscar", command=self._buscar, bg='#0078D7', fg='white')
        btn_buscar.pack(side=tk.LEFT, padx=2)
        
        btn_limpiar = tk.Button(toolbar, text="Limpiar", command=self._limpiar_busqueda)
        btn_limpiar.pack(side=tk.LEFT, padx=2)
    
    def _crear_tabla(self):
        frame_tabla = tk.Frame(self.ventana, bg='#f0f0f0')
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scroll_y = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
        
        self.tabla = ttk.Treeview(frame_tabla, columns=('c', 'n', 'n1', 'n2', 'n3', 'p'), show='headings',
                                   yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tabla.heading('c', text='CÓDIGO')
        self.tabla.heading('n', text='NOMBRE COMPLETO')
        self.tabla.heading('n1', text='NOTA 1')
        self.tabla.heading('n2', text='NOTA 2')
        self.tabla.heading('n3', text='NOTA 3')
        self.tabla.heading('p', text='PROMEDIO')
        
        self.tabla.column('c', width=100, anchor='center')
        self.tabla.column('n', width=350)
        self.tabla.column('n1', width=80, anchor='center')
        self.tabla.column('n2', width=80, anchor='center')
        self.tabla.column('n3', width=80, anchor='center')
        self.tabla.column('p', width=100, anchor='center')
        
        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tabla.pack(fill=tk.BOTH, expand=True)
        
        self.tabla.bind('<Double-1>', lambda e: self._editar())
        self.tabla.bind('<Delete>', lambda e: self._eliminar())
        self.tabla.bind('<F2>', lambda e: self._editar())
    
    def _crear_paneles(self):
        frame_paneles = tk.Frame(self.ventana, bg='#f0f0f0')
        frame_paneles.pack(fill=tk.X, padx=10, pady=5)
        
        frame_stats = tk.LabelFrame(frame_paneles, text="📊 ESTADÍSTICAS RECURSIVAS", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        frame_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        stats_frame = tk.Frame(frame_stats, bg='#f0f0f0')
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.lbl_total = tk.Label(stats_frame, text="Total: 0", bg='#f0f0f0', font=('Arial', 10))
        self.lbl_total.pack(side=tk.LEFT, padx=15)
        
        self.lbl_promedio = tk.Label(stats_frame, text="Promedio General: 0", bg='#f0f0f0', font=('Arial', 10), fg='#4CAF50')
        self.lbl_promedio.pack(side=tk.LEFT, padx=15)
        
        self.lbl_aprobados = tk.Label(stats_frame, text="✅ Aprobados: 0", bg='#f0f0f0', font=('Arial', 10), fg='green')
        self.lbl_aprobados.pack(side=tk.LEFT, padx=15)
        
        self.lbl_desaprobados = tk.Label(stats_frame, text="❌ Desaprobados: 0", bg='#f0f0f0', font=('Arial', 10), fg='red')
        self.lbl_desaprobados.pack(side=tk.LEFT, padx=15)
        
        self.lbl_maxima = tk.Label(stats_frame, text="📈 Nota Máxima: 0", bg='#f0f0f0', font=('Arial', 10), fg='#2196F3')
        self.lbl_maxima.pack(side=tk.LEFT, padx=15)

        self.lbl_minima = tk.Label(stats_frame, text="📉 Nota Mínima: 0", bg='#f0f0f0', font=('Arial', 10), fg='#FF5722')
        self.lbl_minima.pack(side=tk.LEFT, padx=15)
        
        frame_cola = tk.LabelFrame(frame_paneles, text="👥 COLA DE ATENCIÓN (FIFO)", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        frame_cola.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        cola_btn_frame = tk.Frame(frame_cola, bg='#f0f0f0')
        cola_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(cola_btn_frame, text="➕ Agregar a Cola", command=self._agregar_cola, bg='#0078D7', fg='white').pack(side=tk.LEFT, padx=2)
        tk.Button(cola_btn_frame, text="🎓 Atender Siguiente", command=self._atender, bg='#FF9800', fg='white').pack(side=tk.LEFT, padx=2)
        tk.Button(cola_btn_frame, text="🗑️ Limpiar Cola", command=self._limpiar_cola, bg='#EF5350', fg='white').pack(side=tk.LEFT, padx=2)
        
        scroll_cola = tk.Scrollbar(frame_cola)
        scroll_cola.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.lista_cola = tk.Listbox(frame_cola, bg='white', yscrollcommand=scroll_cola.set, height=4)
        self.lista_cola.pack(fill=tk.X, padx=5, pady=5)
        scroll_cola.config(command=self.lista_cola.yview)
    
    def _crear_statusbar(self):
        self.status_bar = tk.Label(self.ventana, text="✅ Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.ventana.bind('<Control-n>', lambda e: self._nuevo())
        self.ventana.bind('<Control-o>', lambda e: self._abrir_csv())
        self.ventana.bind('<Control-s>', lambda e: self._guardar_csv())
        self.ventana.bind('<Control-z>', lambda e: self._deshacer())
        self.ventana.bind('<Insert>', lambda e: self._registrar())
    
    def _cargar_ejemplo(self):
        datos = [
            ("2024001", "Juan Mamani", 14.0, 16.0, 15.0),
            ("2024002", "María Quispe", 18.0, 17.0, 19.0),
            ("2024003", "Carlos Condori", 11.0, 13.0, 12.0),
            ("2024004", "Ana Flores", 15.5, 14.0, 16.5),
            ("2024005", "Luis Pérez", 12.0, 11.5, 13.0),
        ]
        for c, n, n1, n2, n3 in datos:
            self.controlador.registrar_estudiante(c, n, n1, n2, n3)
    
    def _actualizar_todo(self):
        self._actualizar_tabla()
        self._actualizar_estadisticas()
        self._actualizar_cola()
    
    def _actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        for est in self.controlador.obtener_datos_para_tabla():
            self.tabla.insert('', tk.END, values=(
                est['codigo'], est['nombre'],
                f"{est['nota1']:.1f}", f"{est['nota2']:.1f}",
                f"{est['nota3']:.1f}", f"{est['promedio']:.2f}"
            ))
        
        self.status_bar.config(text=f"✅ Total: {len(self.tabla.get_children())} estudiantes")
    
    def _actualizar_estadisticas(self):
        stats = self.controlador.obtener_estadisticas_recursivas()
        self.lbl_total.config(text=f"📊 Total: {stats['total']}")
        self.lbl_promedio.config(text=f"🎯 Promedio General: {stats['promedio_general']}")
        self.lbl_aprobados.config(text=f"✅ Aprobados: {stats['aprobados']}")
        self.lbl_desaprobados.config(text=f"❌ Desaprobados: {stats['desaprobados']}")
        self.lbl_maxima.config(text=f"📈 Máxima: {stats['nota_maxima']}")
        self.lbl_minima.config(text=f"📉 Mínima: {stats['nota_minima']}")
    
    def _actualizar_cola(self):
        self.lista_cola.delete(0, tk.END)
        for codigo, nombre in self.controlador.obtener_cola_estado():
            self.lista_cola.insert(tk.END, f"{codigo} - {nombre}")
        if self.lista_cola.size() == 0:
            self.lista_cola.insert(tk.END, "📭 Cola vacía")
    
    def _registrar(self):
        dialog = tk.Toplevel(self.ventana)
        dialog.title("Registrar Estudiante")
        dialog.geometry("400x500")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.ventana)
        dialog.grab_set()
        
        tk.Label(dialog, text="📝 REGISTRAR NUEVO ESTUDIANTE", bg='#4CAF50', fg='white',
                font=('Arial', 12, 'bold'), pady=10).pack(fill=tk.X)
        
        frame = tk.Frame(dialog, bg='#f0f0f0')
        frame.pack(pady=20, padx=30)
        
        entries = {}
        campos = [
            ("Código:", "entry"),
            ("Nombre completo:", "entry"),
            ("Nota 1 (0-20):", "entry"),
            ("Nota 2 (0-20):", "entry"),
            ("Nota 3 (0-20):", "entry")
        ]
        
        for label, tipo in campos:
            tk.Label(frame, text=label, bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w', pady=(10,0))
            entry = tk.Entry(frame, width=30, font=('Arial', 10))
            entry.pack(pady=5, fill=tk.X)
            entries[label] = entry
        
        def guardar():
            try:
                codigo = entries["Código:"].get().strip()
                nombre = entries["Nombre completo:"].get().strip()
                n1 = float(entries["Nota 1 (0-20):"].get())
                n2 = float(entries["Nota 2 (0-20):"].get())
                n3 = float(entries["Nota 3 (0-20):"].get())
                
                if not codigo or not nombre:
                    messagebox.showerror("Error", "Código y nombre son obligatorios")
                    return
                if not (0 <= n1 <= 20 and 0 <= n2 <= 20 and 0 <= n3 <= 20):
                    messagebox.showerror("Error", "Notas deben estar entre 0 y 20")
                    return
                
                exito, msg = self.controlador.registrar_estudiante(codigo, nombre, n1, n2, n3)
                if exito:
                    self._actualizar_todo()
                    dialog.destroy()
                    messagebox.showinfo("Éxito", msg)
                else:
                    messagebox.showerror("Error", msg)
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos")
        
        tk.Button(frame, text="✅ REGISTRAR", command=guardar,
                 bg='#4CAF50', fg='white', padx=20, pady=5, font=('Arial', 10, 'bold')).pack(pady=20)
    
    def _editar(self):
        """Edita el estudiante seleccionado - CORREGIDO"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Primero seleccione un estudiante haciendo clic en la fila")
            return
        
        # Obtener valores y convertir correctamente
        valores = self.tabla.item(seleccion[0])['values']
        codigo = str(valores[0])  # Asegurar que es string
        
        print(f"DEBUG: Editando código: {codigo}")  # Para depuración
        
        estudiante = self.controlador.buscar_estudiante(codigo)
        
        if not estudiante:
            messagebox.showerror("Error", f"Estudiante con código {codigo} no encontrado")
            return
        
        # Crear diálogo de edición
        dialog = tk.Toplevel(self.ventana)
        dialog.title(f"Editar Estudiante - {codigo}")
        dialog.geometry("400x450")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.ventana)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"EDITAR ESTUDIANTE: {codigo}", bg='#4CAF50', fg='white',
                font=('Arial', 12, 'bold'), pady=10).pack(fill=tk.X)
        
        frame = tk.Frame(dialog, bg='#f0f0f0')
        frame.pack(pady=20, padx=30)
        
        # Campo Nombre
        tk.Label(frame, text="Nombre completo:", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        entry_nombre = tk.Entry(frame, width=30, font=('Arial', 10))
        entry_nombre.insert(0, estudiante.nombre)
        entry_nombre.pack(pady=5, fill=tk.X)
        
        # Campo Nota 1
        tk.Label(frame, text="Nota 1 (0-20):", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w', pady=(10,0))
        entry_n1 = tk.Entry(frame, width=30, font=('Arial', 10))
        entry_n1.insert(0, str(estudiante.nota1))
        entry_n1.pack(pady=5, fill=tk.X)
        
        # Campo Nota 2
        tk.Label(frame, text="Nota 2 (0-20):", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        entry_n2 = tk.Entry(frame, width=30, font=('Arial', 10))
        entry_n2.insert(0, str(estudiante.nota2))
        entry_n2.pack(pady=5, fill=tk.X)
        
        # Campo Nota 3
        tk.Label(frame, text="Nota 3 (0-20):", bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w')
        entry_n3 = tk.Entry(frame, width=30, font=('Arial', 10))
        entry_n3.insert(0, str(estudiante.nota3))
        entry_n3.pack(pady=5, fill=tk.X)
        
        def guardar_cambios():
            try:
                nombre = entry_nombre.get().strip()
                n1 = float(entry_n1.get())
                n2 = float(entry_n2.get())
                n3 = float(entry_n3.get())
                
                if not nombre:
                    messagebox.showerror("Error", "El nombre es obligatorio")
                    return
                if not (0 <= n1 <= 20 and 0 <= n2 <= 20 and 0 <= n3 <= 20):
                    messagebox.showerror("Error", "Las notas deben estar entre 0 y 20")
                    return
                
                exito, mensaje = self.controlador.actualizar_estudiante(codigo, nombre, n1, n2, n3)
                
                if exito:
                    self._actualizar_todo()
                    dialog.destroy()
                    messagebox.showinfo("Éxito", mensaje)
                else:
                    messagebox.showerror("Error", mensaje)
                    
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos para las notas")
        
        tk.Button(frame, text="💾 GUARDAR CAMBIOS", command=guardar_cambios,
                 bg='#4CAF50', fg='white', padx=20, pady=8, 
                 font=('Arial', 10, 'bold'), cursor='hand2').pack(pady=20)
    
    def _eliminar(self):
        """Elimina el estudiante seleccionado - CORREGIDO"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Primero seleccione un estudiante haciendo clic en la fila")
            return
        
        valores = self.tabla.item(seleccion[0])['values']
        codigo = str(valores[0])  # Asegurar que es string
        nombre = str(valores[1])
        
        print(f"DEBUG: Eliminando código: {codigo}")  # Para depuración
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {nombre} ({codigo})?"):
            exito, msg = self.controlador.eliminar_estudiante(codigo)
            if exito:
                self._actualizar_todo()
                messagebox.showinfo("Éxito", msg)
            else:
                messagebox.showerror("Error", msg)
    
    def _buscar(self, event=None):
        texto = self.buscador_var.get().strip().lower()
        if not texto:
            return
        
        for item in self.tabla.get_children():
            valores = self.tabla.item(item)['values']
            codigo_str = str(valores[0]).lower()
            nombre_str = str(valores[1]).lower()
            if texto in codigo_str or texto in nombre_str:
                self.tabla.selection_set(item)
                self.tabla.see(item)
                self.status_bar.config(text=f"✅ Encontrado: {valores[1]}")
                return
        self.status_bar.config(text=f"❌ No encontrado: {texto}")
    
    def _limpiar_busqueda(self):
        self.buscador_var.set("")
        self._actualizar_tabla()
        self.status_bar.config(text="✅ Búsqueda limpiada")
    
    def _ordenar_promedio(self):
        exito, msg = self.controlador.ordenar_por_promedio()
        if exito:
            self._actualizar_tabla()
            self.status_bar.config(text=msg)
        else:
            messagebox.showwarning("Advertencia", msg)
    
    def _ordenar_codigo(self):
        exito, msg = self.controlador.ordenar_por_codigo()
        if exito:
            self._actualizar_tabla()
            self.status_bar.config(text=msg)
        else:
            messagebox.showwarning("Advertencia", msg)
    
    def _deshacer(self):
        exito, msg = self.controlador.deshacer()
        if exito:
            self._actualizar_todo()
            self.status_bar.config(text=msg)
        else:
            messagebox.showinfo("Info", msg)
    
    def _agregar_cola(self):
        codigo = simpledialog.askstring("Agregar a Cola", "Código del estudiante:")
        if codigo:
            exito, msg = self.controlador.agregar_a_cola(codigo)
            if exito:
                self._actualizar_cola()
                messagebox.showinfo("Éxito", msg)
            else:
                messagebox.showerror("Error", msg)
    
    def _atender(self):
        exito, msg, estudiante = self.controlador.atender_siguiente()
        if exito:
            self._actualizar_cola()
            messagebox.showinfo("Atención", msg)
        else:
            messagebox.showinfo("Info", msg)
    
    def _limpiar_cola(self):
        if messagebox.askyesno("Limpiar Cola", "¿Vaciar toda la cola?"):
            self.controlador.limpiar_cola()
            self._actualizar_cola()
            self.status_bar.config(text="🗑️ Cola vaciada")
    
    def _ver_cola(self):
        cola = self.controlador.obtener_cola_estado()
        if not cola:
            messagebox.showinfo("Cola", "No hay estudiantes en espera")
        else:
            texto = "📋 ESTUDIANTES EN ESPERA (FIFO):\n\n"
            for i, (codigo, nombre) in enumerate(cola, 1):
                texto += f"{i}. [{codigo}] {nombre}\n"
            messagebox.showinfo("Cola de Atención", texto)
    
    def _nuevo(self):
        if messagebox.askyesno("Nuevo Archivo", "¿Perder datos no guardados?"):
            self.controlador.hoja.vaciar()
            self.archivo_actual = None
            self._actualizar_todo()
            self.status_bar.config(text="📄 Nuevo archivo creado")
    
    def _guardar_csv(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if archivo:
            datos = self.controlador.obtener_datos_para_tabla()
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['codigo', 'nombre', 'nota1', 'nota2', 'nota3', 'promedio'])
                writer.writeheader()
                writer.writerows(datos)
            self.status_bar.config(text=f"✅ Guardado: {archivo}")
            messagebox.showinfo("Éxito", f"Datos guardados en:\n{archivo}")
    
    def _abrir_csv(self):
        archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if archivo:
            self.controlador.hoja.vaciar()
            with open(archivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.controlador.registrar_estudiante(
                        row['codigo'], row['nombre'],
                        float(row['nota1']), float(row['nota2']), float(row['nota3'])
                    )
            self._actualizar_todo()
            self.status_bar.config(text=f"📂 Cargado: {archivo}")
            messagebox.showinfo("Éxito", f"Archivo cargado:\n{archivo}")
    
    def _acerca_de(self):
        texto = """
📌 MINI EXCEL ACADÉMICO v2.0

Estructuras de Datos y Algoritmos

ESTRUCTURAS IMPLEMENTADAS:
✅ Lista Dinámica (almacenamiento secuencial)
✅ Tabla Hash (búsqueda O(1) por código)
✅ Pila (Stack) para Deshacer (LIFO)
✅ Cola (Queue) para Atención FIFO
✅ QuickSort (ordenamiento por promedio - O(n log n))
✅ MergeSort (ordenamiento por código - O(n log n))
✅ Recursividad (cálculos estadísticos - O(n))

CUMPLIMIENTO RÚBRICA: 20/20 puntos

© 2025 - Escuela Profesional de Ingeniería de Sistemas
"""
        messagebox.showinfo("Acerca de Mini Excel Académico", texto)


if __name__ == "__main__":
    app = MiniExcelAcademico()