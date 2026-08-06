# 🚀 Simulador Dinámico del Sistema Operativo

> **Plataforma Web Interactiva para la Visualización y Simulación en Tiempo Real de Procesadores (CPU), Memoria RAM y Sistemas de Archivos en Disco.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://simulador-cpu-lab-elitesnow.streamlit.app/)

![License](https://img.shields.io/badge/license-MIT-green.svg)

---

Estudiar la arquitectura interna de un Sistema Operativo a través de libros de texto suele ser abstracto y complejo. Conceptos como el **Efecto Convoy en la CPU**, la **Fragmentación Externa en la RAM** o el rastreo de archivos mediante **Índices Jerárquicos en Disco** requieren visualización práctica. Pero los conceptos profundos y basicos estan en los textos.

Este simulador resuelve esta brecha cognitiva **interactivo, cinemático y configurable en la nube**.

---

## ✨ Características Principales

### ⚡ Módulo 1: Planificación del Procesador (CPU)

- **Algoritmos Sin Desalojo:**
  - **FCFS (First-Come, First-Served):** Demostración práctica del orden de llegada y visualización del _Efecto Convoy_.
  - **SPN / SJF (Shortest Process Next):** Optimización del tiempo de espera seleccionando el proceso con menor ráfaga de CPU.
- **Métricas en Tiempo Real:** Cálculo automático de Tiempos de Retorno ($T_r$), Tiempos de Espera ($T_e$), promedios globales y **Diagrama de Gantt** dinámico.

### 🧠 Módulo 2: Administración de Memoria Principal (RAM)

- **Simulación de Particionamiento:** Asignación visual de bloques de memoria para procesos entrantes.
- **Diagnóstico de Fragmentación:** Identificación y cuantificación en tiempo real de la **Fragmentación Interna y Externa**.

### 💾 Módulo 3: Sistemas de Archivos y Almacenamiento (Disco)

- **Matriz de Bloques de 4 KB:** Representación del espacio secundario estructurado en sectores físicos.
- **7 Políticas de Asignación:** Contigua, Extensiones, Enlazadas, Tabla de Asignación de Archivos (FAT), Indexada y **Multinivel**.
- **Simulador de Fragmentación ("Ensuciar Disco"):** Generación de estados de ocupación previa (35% y 65%) con bloques del sistema operativo (`[S.O.]`) para forzar escenarios de prueba.
- **Motor Cinemático y Auditoría Paso a Paso:** Animación en vivo del movimiento del cabezal y reproductor (_Slider Replay_) para auditar el historial de cambios fotograma por fotograma.

---

## 🌲 Profundización Técnica: Asignación Indexada Multinivel

Para resolver el límite físico de un bloque índice único al almacenar archivos masivos (ej. bases de datos o videos 4K), el simulador implementa una **estructura jerárquica en árbol** inspirada en los sistemas de archivos Unix/Linux (`ext3`/`ext4`).

### Niveles de Direccionamiento e Identificación Visual:

| Elemento                   | Código de Color               | Descripción Técnica                                                         |
| :------------------------- | :---------------------------- | :-------------------------------------------------------------------------- |
| **Índice N1 (Raíz)**       | 🟪 Púrpura Oscuro (`#7e22ce`) | Bloque maestro inicial que almacena punteros de primer nivel.               |
| **Índice N2 (Secundario)** | 🟪 Púrpura Medio (`#a855f7`)  | Bloque intermedio de direcciones activado cuando N1 se completa.            |
| **Índice N3 (Terciario)**  | 🟪 Púrpura Claro (`#c084fc`)  | Hojas de control de tercer nivel para direccionamiento masivo.              |
| **Bloques de Datos**       | 🟩 Verde Dinámico             | Sectores físicos de $4\text{ KB}$ que almacenan la información del archivo. |
| **Sistema Operativo**      | ⬛ Gris Oscuro (`#94a3b8`)    | Sectores previamente ocupados por el sistema (`[S.O.]`).                    |

> **Capacidad Teórica:** En bloques de $4\text{ KB}$ con direcciones de $4\text{ bytes}$, un solo bloque alberga hasta $1,024$ punteros. La estructura de tres niveles ($1024^3$) permite direccionar **hasta 4 Terabytes por archivo** sin causar fragmentación externa.

---

**Elidan Dev**
