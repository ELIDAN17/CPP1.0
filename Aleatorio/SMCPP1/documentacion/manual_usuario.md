# Manual de Usuario - SMCPP
## Sistema de Monitoreo y Control de Prácticas Preprofesionales (UNA PUNO)

¡Bienvenido al **SMCPP**! Este manual ha sido redactado con un enfoque paso a paso para guiar a los usuarios principiantes en el uso del sistema. Sigue las secciones correspondientes a tu rol en la plataforma.

---

## 1. Acceso al Portal (Todos los Roles)
Para ingresar al sistema:
1. Abra su navegador web e ingrese a la dirección del portal (generalmente `http://localhost:5173`).
2. Introduzca su **Correo Institucional** y **Contraseña**.
   * *Estudiantes:* Es obligatorio el uso de la estructura su DNI seguido de la nomenclatura institucional: `DNI@est.unap.edu.pe` (ejemplo: `70835765@est.unap.edu.pe`).
   * *Docentes/Coordinadores:* Deben usar su correo institucional `usuario@unap.edu.pe`.
   * *Tutores:* Correos validados por la empresa (ejemplo: `supervisor.empresa@gmail.com`).
3. Presione el botón **"Ingresar al Portal"**. El sistema detectará automáticamente su rol y lo redirigirá al panel apropiado.

---

## 2. Guía para el Estudiante (id_rol = 3)
El Estudiante es responsable de reportar diariamente sus actividades y cargar sus documentos entregables de prácticas.

### A. Reportar Jornada de Actividades (Bitácora)
En el menú lateral, diríjase a **"Mi Bitácora de Prácticas"**:
1. En la columna **"Reportar Jornada"**, elija la **Fecha de la Actividad**.
2. Indique el número de **Horas Invertidas** (ej. 4, 8, etc.).
3. Escriba una **Descripción detallada de labores** explicando qué tareas backend, frontend, diseño o base de datos realizó.
4. Haga clic en **"Subir a Bitácora"**. La actividad aparecerá en su **Línea de Tiempo de Actividades** con el estado de `Pendiente`.

### B. Cargar Entregables (Expediente Digital)
En el menú lateral, diríjase a **"Repositorio de Entregables"**:
1. Verá la plantilla de sus 4 documentos obligatorios:
   * **Convenio de Prácticas**
   * **Plan de Trabajo Inicial**
   * **Informe Inicial de Prácticas**
   * **Informe Final de Prácticas**
2. Haga clic en **"Seleccionar PDFs"** al lado del requisito correspondiente.
3. Elija su archivo local en formato `.pdf`.
4. Visualizará el archivo en cola. Confirme la carga haciendo clic en **"Confirmar Envío"**. El documento pasará al estado de `Pendiente` para la correspondiente revisión por parte del Coordinador Académico.
5. Si el Coordinador registra observaciones, las visualizará en una caja con borde rojo justo debajo del estado del documento para que pueda corregir el archivo y volverlo a subir haciendo clic en **"Reenviar Corrección"**.

---

## 3. Guía para el Tutor Externo (id_rol = 4)
El Tutor es el supervisor directo de la empresa externa asignado al estudiante. Se encarga de validar el día a día en la bitácora.

### A. Supervisión y Horas Aprobadas
1. Al acceder, ingresará automáticamente a **"Supervisión de Estudiantes asignados"**.
2. Verá la tarjeta de cada estudiante asignado con el avance de sus horas acumuladas validadas sobre el total requerido.

### B. Validar la Bitácora Diaria
1. En la tarjeta del estudiante asignado, presione **"Inspeccionar Bitácora"**. Se desplegará un modal con el historial diario del alumno.
2. Identifique las actividades con estado `Pendiente`.
3. Dispone de dos opciones de validación inmediata:
   * **Aprobar (Check verde):** Si las actividades y horas corresponden a la realidad. Las horas se sumarán automáticamente y de forma dinámica al conteo general del estudiante.
   * **Observar (Icono de alerta rojo):** Si el registro necesita aclaraciones. Deberá escribir el motivo obligatorio detallando las correcciones necesarias y presionar "Guardar Observación". El alumno verá este feedback inmediato.

---

## 4. Guía para el Coordinador Académico (id_rol = 2)
El Coordinador supervisa el avance general y realiza la evaluación de los entregables iniciales y finales.

### A. Monitorear Avances Generales
1. Desde el **"Panel de Coordinación Académica"**, visualice las métricas de control:
   * Cantidad general de estudiantes asignados bajo su tutela.
   * Listado de procesos **En Proceso / Enviados**.
   * Procesos **Pendientes** de inicio.

### B. Evaluar Expediente y Dictaminar Proceso
1. Expanda la tarjeta **"Prácticas en Proceso / Enviadas"**.
2. En la fila del alumno seleccionado, presione el icono del **"Ojito"** para evaluar.
3. Se abrirá la ventana con los enlaces a los documentos subidos por el alumno (ej. Plan de Trabajo Inicial, Informe Final). Al hacer clic en ellos, podrá abrirlos en una pestaña nueva para su inspección técnica.
4. **Registrar Dictamen:**
   * Modifique el **Estado General** a `Aceptado` (si todo es conforme), `Rechazado` (si los documentos no cumplen con la rigurosidad o las firmas), o `En Proceso` (si requiere correcciones).
   * Inserte sus **Comentarios de Revisión Académica** detallando su veredicto.
   * Presione **"Registrar Dictamen Real"**. La base de datos y el panel del alumno se actualizarán en tiempo real.

---

## 5. Guía para el Administrador (id_rol = 1)
El Administrador de infraestructura posee control general del sistema:
* Crear y modificar registros de usuarios y contraseñas.
* Monitorear que la conexión local al servicio PostgreSQL corre fluidamente. (En caso de incidencias de autenticación en desarrollo, recuerde ejecutar el script `node src/restablecer.js` para reconfigurar credenciales de prueba por defecto).
