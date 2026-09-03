# ⏱️ Temporizador & Cronómetro Cute

Aplicación de escritorio desarrollada en **Python** para gestionar temporizadores y cronómetros de forma sencilla, ligera y visualmente agradable.

El proyecto está pensado para permanecer visible mientras se realizan otras actividades, permitiendo controlar el tiempo mediante **atajos de teclado personalizables**.

## ✨ Características

* ⏱️ Temporizador con cuenta regresiva.
* ⏲️ Modo cronómetro.
* 🎹 Atajos de teclado personalizables.
* 📌 Ventana siempre visible sobre otras aplicaciones.
* ⚙️ Configuración persistente mediante `config.json`.
* 🎨 Interfaz visual personalizada.
* 🖼️ Recursos gráficos incluidos en `timer_assets/`.
* 🖥️ Compatible con Windows.
* 📦 Generación de ejecutable mediante PyInstaller.

## 🛠️ Tecnologías

* **Python 3**
* **Tkinter**
* **PyInstaller**
* **JSON** para almacenamiento de configuración.

## 📁 Estructura del proyecto

```text
Temporizador-Cronometro-Cute/
│
├── docs/                  # Documentación
├── timer_assets/          # Recursos gráficos y archivos utilizados por la aplicación
│
├── config.json            # Configuración de la aplicación
├── main.py                # Código principal
├── main.spec              # Configuración de PyInstaller
├── reloj.ico              # Icono de la aplicación
├── requirements.txt       # Dependencias de Python
├── .gitignore
└── README.md
```

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/guitarra155/Temporizador-Cronometro-Cute.git
cd Temporizador-Cronometro-Cute
```

### 2. Crear un entorno virtual

En Windows:

```powershell
python -m venv .venv
```

### 3. Activar el entorno virtual

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

CMD:

```cmd
.venv\Scripts\activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar

Con el entorno virtual activado:

```bash
python main.py
```

## 📦 Crear el ejecutable

El proyecto incluye el archivo `main.spec`, utilizado para definir la configuración de compilación con PyInstaller.

Para generar el ejecutable:

```bash
pyinstaller main.spec
```

Los archivos generados aparecerán en:

```text
dist/
```

El directorio `build/` contiene archivos temporales generados durante el proceso de compilación y no forma parte del código fuente.

## ⚙️ Configuración

La configuración de la aplicación se encuentra en:

```text
config.json
```

Este archivo permite mantener determinadas preferencias de la aplicación entre ejecuciones.

Si modificas su estructura, asegúrate de mantener la compatibilidad con el código de `main.py`.

## 🎹 Atajos de teclado

Los atajos disponibles y su configuración dependen de la configuración actual de la aplicación.

Puedes personalizarlos desde la configuración de la aplicación y mantenerlos almacenados en `config.json`.

## 🖼️ Recursos

Los recursos utilizados por la interfaz se encuentran en:

```text
timer_assets/
```

El icono de la aplicación se encuentra en:

```text
reloj.ico
```

## 🔒 Archivos ignorados

El repositorio no incluye archivos generados o específicos del entorno de desarrollo, como:

```text
.venv/
build/
dist/
__pycache__/
```

Estos archivos se generan localmente cuando son necesarios.

## 📋 Requisitos

Se recomienda utilizar:

* Python 3.10 o superior
* Windows 10/11
* `pip`
* PyInstaller

Las dependencias adicionales se encuentran en:

```text
requirements.txt
```

## 🧑‍💻 Desarrollo

Para trabajar sobre el proyecto:

```bash
git clone https://github.com/guitarra155/Temporizador-Cronometro-Cute.git
cd Temporizador-Cronometro-Cute

python -m venv .venv
```

Activar el entorno virtual e instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
python main.py
```

## 📌 Estado del proyecto

🚧 **En desarrollo**

El proyecto puede recibir modificaciones relacionadas con la interfaz, configuración, funcionamiento del temporizador y nuevas funcionalidades.

## 📄 Licencia

La licencia del proyecto aún no está definida.

Si posteriormente se decide publicar el proyecto bajo una licencia de código abierto, se recomienda añadir el archivo `LICENSE` correspondiente al repositorio.

## 👤 Autor

**Guitarra Jhon**

GitHub:
https://github.com/guitarra155
