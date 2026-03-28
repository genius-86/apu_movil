# APU Móvil

APU Móvil es una aplicación móvil desarrollada con **React Native (Expo)** y respaldada por un backend robusto construido en **Python (Django)** y conectado a una base de datos **MySQL**. El proyecto está orientado a la gestión de actividades, materiales y otros registros operativos en terreno.

Esta guía documenta los pasos necesarios para instalar, configurar y ejecutar el proyecto en su totalidad de manera local.

---

## Requisitos Previos

Asegúrese de contar con las siguientes herramientas instaladas en su entorno de desarrollo:

- [Node.js](https://nodejs.org/) (Versión LTS recomendada).
- [Python 3.x](https://www.python.org/downloads/).
- Un servidor de base de datos MySQL. Puede utilizar paquetes como [XAMPP](https://www.apachefriends.org/) (como está sugerido por la ruta `htdocs`), WAMP o MySQL Server nativo.
- La aplicación **Expo Go** descargada en su dispositivo móvil (disponible para iOS y Android) para previsualizar y probar el proyecto, o bien, usar un emulador de dispositivo desde el equipo.

---

## 1. Configuración de la Base de Datos (MySQL)

1. Inicie el servicio de su motor MySQL (por ejemplo, desde el panel de control de XAMPP).
2. Cree una base de datos nueva, preferiblemente llamada `iluled1` (como sugiere el entorno predeterminado).
3. En la raíz del proyecto encontrará archivos o *dumps* de la base de datos (por ejemplo, `iluled1_schema.sql`, `iluled1_schema2.sql` o `iluled_schema.sql`). 
4. Importe el esquema deseado dentro de su base de datos `iluled1` empleando herramientas visuales como phpMyAdmin, DBeaver, o desde la consola de comandos de MySQL:
   ```bash
   mysql -u root -p iluled1 < iluled1_schema.sql
   ```

---

## 2. Configuración del Backend (Django)

1. Abra una terminal y ubíquese en el directorio del backend:
   ```bash
   cd backend
   ```

2. **(Opcional pero muy recomendado)** Cree y active un entorno virtual para las dependencias de Python:
   ```bash
   # En Windows
   python -m venv venv
   venv\Scripts\activate

   # En macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale las dependencias de Python:
   *Si existe un archivo de requerimientos:*
   ```bash
   pip install -r requirements.txt
   ```
   *Nota: Si no existe, asegúrese de tener por lo menos las librerías base para trabajar: `pip install django mysqlclient djangorestframework django-cors-headers python-dotenv`.*

4. Configure las variables de entorno:
   Edite el archivo `.env` que se encuentra en la carpeta del backend.
   Asegúrese de que los parámetros de la base de datos coincidan con su servidor MySQL local:
   ```env
   DB_NAME=iluled1
   DB_USER=root
   DB_PASSWORD=         # Si no tiene clave (ej. XAMPP default), déjelo vacío
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```
   Además, cerciórese de que su IP local figure en los dominios permitidos (`ALLOWED_HOSTS`).

5. Ejecute las migraciones de Django para sincronizar tablas faltantes o actualizaciones de la base de datos (y luego cree un superusuario si lo desea):
   ```bash
   python manage.py migrate
   ```

6. Inicie el servidor backend permitiendo conexiones externas (necesario si probará en un celular que se conecte a este backend vía WiFi):
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
   *Tenga claro cuál es la IP local de este equipo (ej: `192.168.1.15`), ya que el Frontend la necesitará para llamar a los endpoints.*

---

## 3. Configuración del Frontend (React Native & Expo)

1. Abra una nueva terminal (manteniendo el backend corriendo) y diríjase al directorio del frontend:
   ```bash
   cd frontend
   ```

2. Instale todas las dependencias del proyecto de Node con NPM (o utilice su gestor de preferencia como Yarn o PNPM):
   ```bash
   npm install
   ```

3. **Configuración de Conexión:**
   Asegúrese de que en el código de su Frontend, el cliente HTTP o los servicios (Ej. utilidades `api.js` o configuraciones HTTP de Axios/Fetch) apunten a la IP específica local en lugar de `localhost`. Las pruebas reales o simuladores fallan si estas apuntan solo a `localhost`.
   - Ejemplo a configurar: `http://192.168.x.x:8000/api/...`

4. Ejecute el servidor de desarrollo de Expo. Puede hacerlo empleando:
   ```bash
   npm start
   ```
   o bien
   ```bash
   npx expo start
   ```

5. **Apertura de la App:**
   Se generará un código QR en la consola. Desde su dispositivo móvil físico conectado **a la misma red WiFi** que este equipo:
   - Para Android: Escanee el código QR desde la App nativa de "Expo Go".
   - Para iOS: Utilice la cámara del dispositivo móvil para escanear el QR y abrirlo por allí a través de Expo.

---

## Problemas Frecuentes

- **Expo NO conecta o muestra "Network Response Timed Out"**:
  - Confirme que el computador (que corre el dev server y backend) y su celular están conectados en la misma red o segmento de subred.
  - Verifique si el Firewall de Windows / Mac está bloqueando los puertos `8000` (Django), `8081` o `19000` (Expo/Metro). Agregue excepciones si es necesario.
- **Errores de dependencias cacheadas en Expo**:
  - Inicie Expo limpiando la memoria caché: `npx expo start -c`
- **Problemas de conectividad base de datos / `MySQL client` error**:
  - Asegúrese de tener herramientas de construcción instaladas (Build Tools de Visual Studio o dependientes de OS) para compilar los drives de Python de MySQL como `mysqlclient`.
