# src/utils/logger.py
import logging
from pathlib import Path
from src.utils.config import Settings, BASE_DIR # Importa Settings y BASE_DIR

# Obtiene la instancia de la configuración (Singleton)
settings = Settings()

# Define la ruta del archivo de log usando BASE_DIR y la configuración
# Asegúrate de que settings.json tenga la clave 'logging.file'
LOG_FILE_PATH = BASE_DIR / settings.get("logging.file", "logs/bot.log")

# Bandera para asegurar que la configuración base de handlers solo se haga una vez
_logger_initialized = False

def setup_root_logger():
    """
    Configura los handlers (consola y archivo) para el logger principal.
    Esta función está diseñada para ser llamada una única vez al inicializar cualquier logger.
    """
    global _logger_initialized
    if _logger_initialized:
        return

    # Usamos un logger raíz o principal para añadir los handlers.
    # Otros loggers (ej. get_logger(__name__)) heredarán estos handlers.
    root_logger_name = "meet_transcription_bot"
    root_logger = logging.getLogger(root_logger_name)

    # Obtiene el nivel de log desde la configuración (por defecto INFO)
    log_level_str = settings.get("logging.level", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    root_logger.setLevel(log_level)

    # Formato de los mensajes de log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 1. Handler para la consola (salida estándar)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 2. Handler para el archivo de log
    try:
        # Asegura que el directorio para los logs exista
        log_dir = LOG_FILE_PATH.parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        # Si hay un error al configurar el archivo, al menos lo loguea en consola.
        # Usamos print o un logger temporal aquí, ya que el logger principal puede no estar completamente listo.
        print(f"ERROR: No se pudo configurar el archivo de log en '{LOG_FILE_PATH}': {e}")
        print("ADVERTENCIA: El logging continuará solo en consola.")

    _logger_initialized = True

def get_logger(name: str = "meet_transcription_bot"):
    """
    Obtiene una instancia de logger configurada para un módulo específico.
    Asegura que los handlers principales estén configurados llamando a setup_root_logger.

    Args:
        name (str): El nombre del logger. Se recomienda usar '__name__' en cada módulo.

    Returns:
        logging.Logger: La instancia del logger.
    """
    # Asegura que los handlers principales se configuren la primera vez que se solicita un logger.
    setup_root_logger()
    return logging.getLogger(name)

# Ya no necesitamos la línea 'logger = setup_logger()' global aquí.
# Otros módulos ahora importarán 'get_logger' y lo usarán.
