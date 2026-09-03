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

## 📦 Si quieres usar mediante ejecutable tienes que hacer lo siguiente

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

## 📌 Estado del proyecto

🚧 **En desarrollo**

El proyecto puede recibir modificaciones relacionadas con la interfaz, configuración, funcionamiento del temporizador y nuevas funcionalidades.


**guitarra155**

GitHub:
https://github.com/guitarra155
