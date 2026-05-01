# -*- coding: utf-8 -*-
import math

def funcion_hash_polinomial(clave, tamanio):
    """
    Implementación de la Función Hash Polinomial para Cadenas.
    h(s) = sum(s[i] * p^(n-1-i)) mod m, donde p=31.
    """
    p = 31
    hash_val = 0
    for caracter in str(clave):
        hash_val = (hash_val * p + ord(caracter)) % tamanio
    return hash_val

class TablaHashEncadenamiento:
    """
    Resolución por Encadenamiento Separado (Chaining).
    Complejidad promedio de búsqueda: O(1 + λ).
    """
    def __init__(self, tamanio):
        self.tamanio = tamanio
        self.tabla = [[] for _ in range(tamanio)] # Lista de listas
        self.colisiones = 0
        self.elementos = 0

    def insertar(self, clave, valor):
        idx = funcion_hash_polinomial(clave, self.tamanio)
        if self.tabla[idx]: # Si la lista no está vacía, hay colisión
            self.colisiones += 1
        
        # Insertar o actualizar
        for i, (c, v) in enumerate(self.tabla[idx]):
            if c == clave:
                self.tabla[idx][i] = (clave, valor)
                return
        self.tabla[idx].append((clave, valor))
        self.elementos += 1

class TablaHashSondeo:
    """
    Resolución por Direccionamiento Abierto.
    Soporta Sondeo Lineal y Sondeo Cuadrático.
    """
    def __init__(self, tamanio, tipo="lineal"):
        self.tamanio = tamanio
        self.tabla = [None] * tamanio
        self.tipo = tipo
        self.colisiones = 0
        self.elementos = 0

    def insertar(self, clave, valor):
        # Umbral de carga recomendado: 0.75 para evitar degradación
        if self.elementos >= self.tamanio * 0.75:
            return False 

        idx_base = funcion_hash_polinomial(clave, self.tamanio)
        
        for i in range(self.tamanio):
            if self.tipo == "lineal":
                # Sondeo Lineal: h(k, i) = (h(k) + i) mod m
                idx = (idx_base + i) % self.tamanio
            else:
                # Sondeo Cuadrático: h(k, i) = (h(k) + c1*i + c2*i^2) mod m
                # Simplificado a i^2 para la práctica
                idx = (idx_base + i**2) % self.tamanio
            
            if self.tabla[idx] is None:
                if i > 0: self.colisiones += 1 # Hubo intentos previos, hubo colisión
                self.tabla[idx] = (clave, valor)
                self.elementos += 1
                return True
            elif self.tabla[idx][0] == clave:
                self.tabla[idx] = (clave, valor) # Actualización
                return True
        return False