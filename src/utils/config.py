# src/utils/config.py
import json
from pathlib import Path

# Define la ruta base del proyecto (una forma segura de obtenerla)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Ruta al archivo de configuración
CONFIG_FILE_PATH = BASE_DIR / "config" / "settings.json"

class Settings:
    """
    Clase para cargar y gestionar la configuración del bot desde settings.json.
    """
    _instance = None
    _settings = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._load_settings()
        return cls._instance

    def _load_settings(self):
        """
        Carga la configuración desde el archivo JSON.
        """
        if not CONFIG_FILE_PATH.exists():
            print(f"Error: El archivo de configuración no se encontró en '{CONFIG_FILE_PATH}'.")
            # Podrías crear un archivo por defecto aquí o salir.
            exit(1)

        try:
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                self._settings = json.load(f)
            print(f"Configuración cargada desde: {CONFIG_FILE_PATH}")
        except json.JSONDecodeError as e:
            print(f"Error al parsear el archivo JSON de configuración: {e}")
            exit(1)
        except Exception as e:
            print(f"Error inesperado al cargar la configuración: {e}")
            exit(1)

    def get(self, key: str, default=None):
        """
        Obtiene un valor de configuración usando una clave de notación de punto (ej. "audio.sample_rate").
        """
        keys = key.split('.')
        value = self._settings
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default # La clave no es un diccionario, no se puede seguir navegando
            if value is None:
                return default # La clave no se encontró
        return value

    def reload(self):
        """
        Recarga la configuración desde el archivo.
        """
        self._load_settings()
        print("Configuración recargada.")

# Para acceder a la configuración en cualquier parte de tu código:
# settings = Settings()
# sample_rate = settings.get("audio.sample_rate")
# channels = settings.get("audio.channels")
# language = settings.get("transcription.language")