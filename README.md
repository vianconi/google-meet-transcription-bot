# Google Meet Transcription Bot

Un bot automatizado desarrollado en Python para transcribir conversaciones de reuniones de Google Meet en tiempo real y almacenarlas localmente. Diseñado para uso personal, privado y con foco en la confidencialidad.

## 🎯 Objetivos Principales

*   Automatizar la conexión a reuniones de Google Meet.
*   Capturar el audio del sistema en tiempo real.
*   Transcribir conversaciones con marcas de tiempo precisas.
*   Generar archivos de texto organizados y legibles.
*   Garantizar la total privacidad y procesamiento local de los datos.

## ✨ Características (MVP - Mínimo Producto Viable)

*   **Conexión básica a Google Meet:** Utilizando automatización web.
*   **Captura de audio fundamental:** Del sistema operativo.
*   **Transcripción básica:** Conversión de voz a texto.
*   **Almacenamiento de archivos:** Guardado local de las transcripciones.

## ⚠️ Limitaciones Conocidas

*   Identificación de hablantes aproximada (no perfecta).
*   Dependiente de conexión estable a internet para Google Meet.
*   Requiere permisos de administrador para audio del sistema.
*   Sensible a ruido ambiente y calidad del micrófono.
*   Calidad de transcripción dependiente del audio original.

## 🛠️ Tecnologías Utilizadas

*   **Python 3.8+**
*   **Automatización Web:** Selenium, WebDriver-Manager
*   **Captura y Procesamiento de Audio:** PyAudio, Pydub
*   **Transcripción (ASR Local):** Vosk (Offline)
*   **Framework de Aplicación:** FastAPI (para la orquestación)
*   **Base de Datos Local:** SQLite con SQLModel (ORM)
*   **Gestión de Dependencias:** Poetry

## 🚀 Guía de Configuración e Inicio

Sigue estos pasos para poner en marcha el bot en tu máquina local.

### 1. Prerrequisitos

Asegúrate de tener instalado lo siguiente:

*   **Python 3.8 o superior.**
*   **Git.**
*   **Google Chrome o Chromium Browser** (el bot lo usará para conectarse a Meet).
*   **Configuración de Audio del SO:** Puede requerir la configuración de un dispositivo de "mezcla estéreo" o "bucle de audio" para capturar el audio del sistema (ej., "Stereo Mix" en Windows, Soundflower/BlackHole en macOS, PulseAudio loopback en Linux).

### 2. Clonar el Repositorio

Abre tu terminal y ejecuta:

```bash
git clone https://github.com/tu-usuario/google-meet-transcription-bot.git
cd google-meet-transcription-bot
```
(Reemplaza tu-usuario con tu nombre de usuario de GitHub).

### 3. Instalar Poetry

Si aún no tienes Poetry, instálalo con:

Linux/macOS/WSL:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Windows (PowerShell):

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
Asegúrate de que Poetry esté en tu PATH.

### 4. Instalar Dependencias

Dentro de la carpeta google-meet-transcription-bot, instala todas las dependencias usando Poetry:

```bash
poetry install
```
Esto creará un entorno virtual y descargará todas las librerías necesarias.

### 5. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto y configura las variables de entorno necesarias. Puedes usar el archivo `.env.example` como guía.

### 6. Iniciar el Bot

Una vez configurado, podrás ejecutar el bot desde la raíz del proyecto usando Poetry:
```bash
poetry run python src/main.py
```