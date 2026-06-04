# Análisis de Complejidades Asintóticas (Big-O)

## Mini Hoja de Cálculo Académica

### Tabla de Complejidades por Operación

| Operación            | Estructura   | Mejor Caso | Caso Promedio | Peor Caso  | Complejidad Espacial |
| -------------------- | ------------ | ---------- | ------------- | ---------- | -------------------- |
| Registrar estudiante | Lista + Hash | O(1)       | O(1)          | O(n)\*     | O(1)                 |
| Buscar por código    | Tabla Hash   | O(1)       | O(1)          | O(n)\*\*   | O(1)                 |
| Mostrar todos        | Lista        | O(n)       | O(n)          | O(n)       | O(1)                 |
| Ordenar por promedio | QuickSort    | O(n log n) | O(n log n)    | O(n²)      | O(log n)             |
| Ordenar por código   | MergeSort    | O(n log n) | O(n log n)    | O(n log n) | O(n)                 |
| Deshacer (Stack)     | Pila         | O(1)       | O(1)          | O(1)       | O(n)\*\*\*           |
| Encolar atención     | Cola         | O(1)       | O(1)          | O(1)       | O(1)                 |
| Despachar atención   | Cola         | O(1)       | O(1)          | O(1)       | O(1)                 |
| Promedio recursivo   | Recursión    | O(n)       | O(n)          | O(n)       | O(n)                 |

\*O(n) solo cuando ocurre rehashing (redimensionamiento de la tabla hash)
**O(n) solo cuando hay muchas colisiones en el hash \***O(n) por el deepcopy del estado completo
