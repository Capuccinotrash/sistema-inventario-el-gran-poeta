# Sistema de Control de Inventario - "El Gran Poeta"

Proyecto final para la asignatura **Taller de desarrollo de aplicaciones** de INACAP Sede Curicó. 
Este sistema permite gestionar sucursales, catalogar libros, controlar traslados de stock con validación matemática y auditar movimientos con exportación a Excel.

---

## 1. Manual de Instalación

### Requisitos Previos
- Python 3.8 o superior instalado en el equipo.
- Servidor MySQL activo (puede ser a través de XAMPP, WAMP o MySQL Workbench).

### Paso a Paso
1. **Descargar el proyecto:**
   En la página principal de este repositorio, haz clic en el botón verde "Code" y selecciona "Download ZIP". Extrae la carpeta en tu computador.
2. **Instalar dependencias:**
   Abre la terminal en la carpeta del proyecto extraído y ejecuta el siguiente comando para instalar las librerías necesarias:
   `pip install mysql-connector-python pillow`
3. **Configurar la Base de Datos:**
   - Monta la base de datos importando el archivo `el_gran_poeta.sql` adjunto en este repositorio hacia tu servidor local.
   - Abre el archivo principal `login.py`.
   - Dirígete a la línea de conexión de la base de datos (función `conectar_db()`) y asegúrate de que el campo `password` tenga la contraseña de tu servidor local.
4. **Ejecutar la aplicación:**
   Inicia el sistema ejecutando:
   `python login.py`

---

## 2. Manual de Usuario

El sistema cuenta con un Control de Acceso Basado en Roles (RBAC). Dependiendo del usuario, se habilitarán o bloquearán ciertos módulos.

### Pantalla de Inicio y Menú Principal
Para acceder, el usuario debe ingresar las credenciales provistas por Jefatura. Una vez dentro, el sistema adapta las opciones según el cargo y permite alternar entre Modo Claro y Oscuro.

<img width="1017" height="710" alt="login" src="https://github.com/user-attachments/assets/6098e06b-e172-48ca-b0ae-d88cbe95c6f1" />

### Perfiles de Acceso
- **Jefe de Bodega:** Acceso total al sistema. Puede crear sucursales, catalogar productos, auditar reportes y gestionar a otros usuarios.
- **Bodeguero:** Perfil operativo. Solo tiene acceso al módulo de Control de Inventario y Traslados.

### Uso de los Módulos
1. **Administración y Catálogo (Solo Jefatura):** Permite registrar nuevas bodegas y añadir productos al catálogo seleccionando su tipo y editorial.

<img width="1017" height="709" alt="Bodegas" src="https://github.com/user-attachments/assets/9f974c04-ba47-4b7c-8bdd-452994433c6a" />
<img width="1018" height="708" alt="Catalogo" src="https://github.com/user-attachments/assets/0a1ed7ae-10ca-4204-ac2d-12155faf90f8" />

2. **Traslados de Stock (Operativo):** 
   - *Inyección:* Ingresa stock desde cero a un local.
   - *Transferencia:* Mueve inventario entre dos bodegas. El sistema aborta la operación si el stock de origen es menor a la cantidad solicitada.

<img width="1011" height="676" alt="stock" src="https://github.com/user-attachments/assets/a8979606-a782-4188-b8c6-54dc7cc830fe" />

3. **Auditoría y Reportes (Solo Jefatura):** Registra automáticamente qué usuario movió qué producto, cuándo y dónde. Cuenta con filtros por fecha y un botón para **Exportar a Excel**, lo que genera un archivo CSV formateado en `utf-8-sig` para análisis sin pérdida de caracteres en español.

<img width="1026" height="721" alt="Auditoria" src="https://github.com/user-attachments/assets/bc370023-8931-40d7-8f26-a4bf0f2e775a" />

4. **Gestión de Usuarios (Solo Jefatura):** Permite crear credenciales nuevas y asignarles un rol. Por seguridad, el sistema impide que el usuario elimine su propia cuenta mientras tiene la sesión activa.

<img width="1006" height="699" alt="usuarios" src="https://github.com/user-attachments/assets/795c354e-2455-4b56-80b8-b1405e47746d" />

---

## 3. Términos y Condiciones de Uso

1. **Propósito Académico:** Este software ha sido desarrollado con fines netamente académicos y evaluativos para INACAP. No está diseñado para transacciones financieras reales.
2. **Responsabilidad de Credenciales:** El usuario con perfil de "Jefe de Bodega" es el responsable de la asignación de roles.
3. **Integridad de los Datos:** Queda estrictamente prohibida la manipulación de la base de datos por fuera de la interfaz gráfica. Cualquier alteración manual en MySQL corrompe la precisión del módulo de Auditoría y la trazabilidad del stock.

```
