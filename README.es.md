# **Python Reservation Manager**

Aplicación desarrollada en **Python 3** usando **Streamlit** para la gestión de reservas, recursos y ubicaciones.  
Este proyecto permite crear, inspeccionar y administrar reservas con restricciones y precios asociados.

---

### Dominio Elegido
El dominio elegido es la gestión de reservas de recursos y ubicaciones.  
Este dominio fue seleccionado porque es ampliamente aplicable: desde la reserva de salas de reuniones, espacios de coworking o instalaciones deportivas, hasta la gestión de alquileres de equipos o locales. Naturalmente involucra gestión del tiempo, asignación de recursos y reglas de precios, lo que lo hace ideal para demostrar cómo Python puede manejar programación, restricciones y persistencia de datos.

---

### Arquitectura
El **Reservation Manager** se centra en tres pilares: eventos (reservas), recursos (ubicaciones y recursos) y restricciones.  
Las restricciones son la parte más crítica del sistema, garantizando que cada reserva respete las reglas de compatibilidad y la disponibilidad de recursos.

1. **Eventos (Reservas)**  
   Cada reserva es un evento que une:  
   - Una ubicación (ejemplo: “Sala de Conferencias A”).  
   - Un intervalo de tiempo (fecha de inicio y fin).  
   - Un conjunto de recursos: requisitos (por defecto) y opcionales (elegidos por el usuario).  

   Las reservas se validan contra las restricciones antes de ser aceptadas.  

   **Ejemplo:**  
   Reserva de la Sala de Conferencias A del 5 al 7 de enero con requisitos Mesa, Sillas y opcional Proyector.

2. **Recursos (Ubicaciones y Recursos)**  
   - **Ubicaciones** definen:  
     - Un precio base.  
     - Correquisitos: recursos por defecto que siempre se incluyen.  
     - Opcionales: recursos que pueden añadirse por el usuario.  

   - **Recursos** definen:  
     - Nombre, cantidad y precio.  
     - Exclusiones: recursos que no pueden combinarse con ciertos otros.  

   **Ejemplo:**  
   - Ubicación: Sala de Conferencias A → requisitos: Mesa, Sillas; opcionales: Proyector, Altavoces.  
   - Recurso: Proyector → precio: $10/día; excluye: Pantalla Exterior.

3. **Restricciones (Núcleo del Sistema)**  
   Las restricciones son las reglas que garantizan reservas válidas. El sistema las gestiona activamente cada vez que se crea, actualiza o elimina una reserva.  

   - **Exclusión Mutua entre Recursos**  
     - Ciertos recursos no pueden usarse juntos.  
     - Ejemplo: Proyector excluye Pantalla Exterior.  
       → Si ambos se seleccionan, la reserva es rechazada.  

   - **Correquisitos entre Ubicaciones y Recursos**  
     - Cada ubicación requiere recursos específicos por defecto.  
     - Ejemplo: La Sala de Conferencias A siempre incluye Mesa y Sillas.  
       → Estos requisitos se añaden automáticamente a cada reserva de esa ubicación.  

   - **Recursos Opcionales con Restricciones**  
     - Incluso los recursos opcionales pueden tener exclusiones.  
     - Ejemplo: Altavoces excluyen Equipo de Modo Silencioso.  
       → Si un usuario selecciona ambos, la reserva es inválida.  

   - **Validación de Fechas**  
     - Fecha de inicio ≤ Fecha de fin.  
     - Fecha de inicio ≥ hoy.  
     - Ejemplo: Reservar del 2026-01-01 al 2025-12-31 → rechazado.  

   - **Cantidades de Recursos**  
     - Las reservas no pueden exceder las cantidades disponibles.  
     - Ejemplo: Solo existen 2 proyectores; si 3 reservas simultáneas los solicitan → rechazado.  

   - **Manejo de Colisiones**  
     - Las reservas para la misma ubicación no pueden solaparse.  
     - Si ocurre solapamiento, el sistema desplaza la reserva al siguiente espacio disponible.  
     - Ejemplo:  
       - Reserva A: 5 de enero, 10:00-12:00.  
       - Reserva B solicitada para 5 de enero, 11:00-13:00.  
       → La Reserva B se mueve para comenzar a las 12:00.  

---

### Prerrequisitos
- Python 3.8+  
- Librerías:  
  - `streamlit`  
  - `pandas`  
  - `datetime` (incluida en la librería estándar de Python, no requiere instalación)  

---

### Funcionalidades
- Crear reservas con fechas de inicio/fin  
- Calcular el precio total automáticamente  
- Inspeccionar reservas en una tabla  
- Editar ubicaciones y recursos  
- Eliminar reservas, ubicaciones y recursos  
- Aplicar restricciones (sin solapamientos, duraciones válidas, límites de capacidad, horarios de apertura)  

---

### Estructura del Proyecto
```
project/
│── main.py          # Punto de entrada de la app Streamlit
│── manager.py       # Lógica de negocio
│── loader.py        # Cargar/guardar datos en JSON
│── save.json        # Archivo de datos de ejemplo
│── requirements.txt # Dependencias
```

---

### Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/lacuentadeadrian57-netizen/Reservation-Manager.git
   cd Reservation-Manager
   ```

2. **Crear un entorno virtual (recomendado)**  
   ```bash
   python3 -m venv enviroment
   source enviroment/bin/activate   # macOS/Linux
   enviroment\Scripts\activate      # Windows
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**  
   ```bash
   python3 -m streamlit run main.py
   ```

5. **Abrir en el navegador**  
   Streamlit iniciará un servidor local (por defecto: http://localhost:8501).  
   Navega al enlace para acceder a la interfaz de Reservation Manager.  

---

### Uso
El **Python Reservation Manager** es una aplicación web construida con Streamlit que ofrece una interfaz sencilla para gestionar reservas, ubicaciones y recursos. La aplicación está organizada en cinco secciones principales, accesibles desde el panel lateral de navegación:

1. **Formulario de Reservas**  
   - Permite crear una nueva reserva especificando:  
     - Fecha de inicio y fin  
     - Ubicación  
     - Recursos opcionales  
   - Muestra los recursos por defecto que siempre se incluyen con la ubicación elegida.  
   - Calcula y muestra el precio total, combinando el costo base de la ubicación con los recursos opcionales seleccionados.  

2. **Detalles de Reservas**  
   - Proporciona una vista tabular de todas las reservas creadas.  
   - Los usuarios pueden inspeccionar detalles como ID, fechas, ubicación, recursos y precio.  
   - Incluye funcionalidad para eliminar reservas cuando ya no sean necesarias.  

3. **Editar Ubicaciones**  
   - Permite añadir nuevas ubicaciones especificando:  
     - Nombre  
     - Precio  
     - Recursos por defecto (requisitos)  
     - Recursos opcionales  
   - Las ubicaciones existentes pueden listarse, inspeccionarse, actualizarse (ej. cambiar precio) o eliminarse.  

4. **Editar Recursos**  
   - Permite gestionar el conjunto de recursos disponibles para las reservas.  
   - Los usuarios pueden añadir nuevos recursos especificando:  
     - Nombre  
     - Cantidad disponible  
     - Precio  
     - Exclusiones (recursos que no pueden combinarse con este)  
   - Los recursos existentes pueden listarse, inspeccionarse, actualizarse (precio y cantidad) o eliminarse.  
   - El sistema aplica reglas de exclusión: si dos recursos que se excluyen entre sí son seleccionados en la misma reserva, la reserva no puede crearse.  

5. **Guardar y Cargar**  
   - Ofrece opciones para guardar el estado actual de la aplicación (ubicaciones, recursos, reservas) en un archivo JSON.  
   - Permite cargar datos desde un archivo para restaurar un estado previo.  
   - Esto asegura la persistencia de datos entre sesiones y facilita compartir o respaldar configuraciones.  
