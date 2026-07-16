# -*- coding: utf-8 -*-
import random

class DiscoSimulado:
    def __init__(self, total_bloques):
        self.total_bloques = total_bloques
        # El disco se representa como una lista donde None = Libre, o guarda el nombre del archivo
        self.bloques = [None] * total_bloques
        # Registro de archivos: { nombre: { "tipo": tipo, "bloques": [...], "color": color } }
        self.archivos = {}
        # Guardamos un bloque índice especial para la asignación indexada
        self.bloques_indices = {} # { nombre: bloque_indice }

    def obtener_bloques_libres(self):
        return [i for i, b in enumerate(self.bloques) if b is None]

    def _generar_color(self):
        # Evitamos colores extremadamente claros para que se lea el texto
        return f"#{random.randint(50, 200):02x}{random.randint(50, 200):02x}{random.randint(50, 200):02x}"

    def eliminar_archivo(self, nombre):
        if nombre in self.archivos:
            # Liberamos bloques en el disco
            for b in self.archivos[nombre]["bloques"]:
                self.bloques[b] = None
            if nombre in self.bloques_indices:
                idx_bloque = self.bloques_indices[nombre]
                self.bloques[idx_bloque] = None
                del self.bloques_indices[nombre]
            del self.archivos[nombre]
            return True
        return False

    def asignar_contigua(self, nombre, tam):
        # Buscar el primer hueco contiguo que encaje (First Fit)
        bloques_libres_consecutivos = 0
        inicio_idx = -1
        
        for i in range(self.total_bloques):
            if self.bloques[i] is None:
                if bloques_libres_consecutivos == 0:
                    inicio_idx = i
                bloques_libres_consecutivos += 1
                if bloques_libres_consecutivos == tam:
                    # Encontrado. Reservamos.
                    color = self._generar_color()
                    rango_bloques = list(range(inicio_idx, inicio_idx + tam))
                    for b in rango_bloques:
                        self.bloques[b] = nombre
                    self.archivos[nombre] = {
                        "tipo": "Contigua",
                        "bloques": rango_bloques,
                        "color": color
                    }
                    return True, f"Asignado exitosamente en los bloques contiguos: {rango_bloques}"
            else:
                bloques_libres_consecutivos = 0
                inicio_idx = -1
        return False, "Error: No se encontró un espacio contiguo lo suficientemente grande (Fragmentación Externa)."

    def asignar_enlazada(self, nombre, tam):
        libres = self.obtener_bloques_libres()
        if len(libres) < tam:
            return False, f"Error: No hay suficientes bloques libres en el disco (Requeridos: {tam}, Libres: {len(libres)})."
        
        # Seleccionamos bloques dispersos de forma aleatoria o secuencial para simular el enlace real
        bloques_elegidos = libres[:tam]
        color = self._generar_color()
        
        for b in bloques_elegidos:
            self.bloques[b] = nombre
            
        self.archivos[nombre] = {
            "tipo": "Enlazada",
            "bloques": bloques_elegidos,
            "color": color
        }
        return True, f"Asignado de forma enlazada en los bloques: {bloques_elegidos}"

    def asignar_indexada(self, nombre, tam):
        libres = self.obtener_bloques_libres()
        # Requiere tam bloques de datos + 1 bloque de índice
        total_requerido = tam + 1
        if len(libres) < total_requerido:
            return False, f"Error: Se requieren {total_requerido} bloques (1 para índice y {tam} para datos). Solo quedan {len(libres)} libres."
        
        # El primer bloque libre será nuestro Bloque Índice
        bloque_indice = libres[0]
        bloques_datos = libres[1:total_requerido]
        color = self._generar_color()
        
        # Marcar en el disco
        self.bloques[bloque_indice] = f"ÍNDICE_{nombre}"
        for b in bloques_datos:
            self.bloques[b] = nombre
            
        self.bloques_indices[nombre] = bloque_indice
        self.archivos[nombre] = {
            "tipo": "Indexada",
            "bloques": bloques_datos,
            "color": color,
            "bloque_indice": bloque_indice
        }
        return True, f"Asignado de forma indexada. Bloque Índice: {bloque_indice}. Bloques de Datos: {bloques_datos}"