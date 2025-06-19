# src/automation/meet_controller.py
import os
from pathlib import Path # Necesitamos importar Path para verificar si el archivo existe
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# Importar utilidades del proyecto
from src.utils.config import Settings
from src.utils.logger import get_logger

# Configurar el logger para este módulo
logger = get_logger(__name__)

class MeetController:
    """
    Clase encargada de controlar y automatizar las interacciones con Google Meet
    a través de un navegador web (Selenium).

    Gestiona el lanzamiento, configuración y cierre del navegador,
    así como la preparación para la interacción con la interfaz de Meet.
    """

    def __init__(self):
        """
        Inicializa el controlador del navegador.
        Obtiene la configuración global del bot y prepara las opciones del navegador Chrome.
        """
        self.config = Settings()
        self.driver = None
        self.chrome_options = self._setup_chrome_options()
        logger.info("MeetController inicializado con opciones de Chrome.")

    def _setup_chrome_options(self) -> Options:
        """
        Configura las opciones del navegador Chrome antes de su lanzamiento.

        Establece propiedades clave como el modo headless (sin interfaz gráfica),
        el directorio del perfil de usuario (para mantener la sesión y cookies),
        y desactiva elementos que podrían interferir con la automatización
        (ej. notificaciones, permisos de micrófono/cámara).

        Returns:
            Options: Un objeto Options con todas las configuraciones aplicadas para Chrome.
        """
        options = Options()

        if self.config.get("browser.headless", True):
            options.add_argument("--headless")
            logger.info("Navegador configurado en modo headless (sin interfaz gráfica).")
        else:
            logger.info("Navegador configurado en modo con interfaz gráfica (no headless).")

        options.add_argument("--disable-notifications")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")

        user_data_dir = self.config.get("browser.user_data_dir")
        if user_data_dir:
            os.makedirs(user_data_dir, exist_ok=True)
            options.add_argument(f"--user-data-dir={user_data_dir}")
            logger.info(f"Usando directorio de perfil de usuario: {user_data_dir}")
        else:
            logger.warning("No se ha especificado 'browser.user_data_dir' en la configuración. Las sesiones de navegador no se mantendrán entre ejecuciones.")

        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        })
        logger.info("Permisos de micrófono/cámara pre-otorgados y otras configuraciones de preferencias aplicadas.")

        return options

    def launch_browser(self):
        """
        Inicia una instancia del navegador Chrome utilizando el driver adecuado.

        Prioriza el uso de un chromedriver especificado en la configuración
        (ideal para ARM/Raspberry Pi). Si no se especifica o no se encuentra,
        intenta descargar uno automáticamente con webdriver-manager (ideal para x64).
        """
        if self.driver is None:
            try:
                # Intenta obtener el path del chromedriver desde la configuración
                configured_driver_path = self.config.get("browser.chromedriver_path")
                driver_to_use = None

                if configured_driver_path and Path(configured_driver_path).is_file():
                    # Si el path está configurado y el archivo existe, lo usamos.
                    driver_to_use = configured_driver_path
                    logger.info(f"Usando chromedriver especificado en configuración: {driver_to_use}")
                else:
                    # Si no está configurado o no existe, intentamos con webdriver-manager.
                    # Esto es más común en entornos de desarrollo x64 donde se quiere conveniencia.
                    logger.info("Chromedriver no especificado o no encontrado. Intentando descargar con webdriver-manager...")
                    # webdriver-manager puede tardar la primera vez
                    driver_to_use = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
                    logger.info(f"Chromedriver descargado por webdriver-manager: {driver_to_use}")

                # Asegurarse de que tenemos un driver para usar
                if not driver_to_use:
                    raise FileNotFoundError("No se encontró un Chromedriver válido para iniciar el navegador.")

                # Crear el objeto Service con el path del driver
                service = Service(executable_path=driver_to_use)

                # Inicializa el WebDriver pasando el objeto Service y las opciones.
                self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
                logger.info("Navegador Chrome iniciado exitosamente.")
            except Exception as e:
                logger.error(f"Error al iniciar el navegador Chrome: {e}")
                self.driver = None
                raise
        else:
            logger.info("El navegador ya está iniciado. No se requiere iniciar uno nuevo.")

    def close_browser(self):
        """
        Cierra la instancia del navegador Chrome si está abierta.
        Libera todos los recursos del sistema asociados con el proceso del navegador.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Navegador Chrome cerrado exitosamente.")
        else:
            logger.info("El navegador no está iniciado. No se requiere cerrar.")


if __name__ == "__main__":
    """
    Este bloque permite probar la funcionalidad de MeetController de forma aislada.
    Al ejecutar 'poetry run python -m src.automation.meet_controller',
    se intentará lanzar y luego cerrar una instancia de Chrome.

    Asegúrate de tener Chrome instalado en tu sistema para que esta prueba funcione.
    También, verifica la configuración en 'config/settings.json' para el modo headless
    y el directorio del perfil de usuario.
    """

    controller = None
    try:
        logger.info("**************************************************")
        logger.info("Iniciando prueba de MeetController (simulación).")
        logger.info("**************************************************")

        controller = MeetController()
        controller.launch_browser()

        logger.info("Navegador iniciado. Esperando 5 segundos para que puedas verlo (si no es headless)...")
        import time
        time.sleep(5)

        logger.info("Finalizando prueba de MeetController.")
    except Exception as e:
        logger.error(f"La prueba de MeetController falló inesperadamente: {e}")
    finally:
        if controller:
            controller.close_browser()
            logger.info("Recursos del navegador liberados en la prueba.")
        logger.info("**************************************************")
        logger.info("Prueba de MeetController finalizada.")
        logger.info("**************************************************")
        