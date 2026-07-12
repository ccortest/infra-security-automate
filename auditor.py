import os
import sys
import webbrowser
from dotenv import load_dotenv 
# Importamos ambos motores de auditoría
from modules.linux_auditor import auditar_sistema_linux
from modules.windows_auditor import auditar_sistema_windows
# Importar el generador de reportes
from modules.report_generator import guardar_reporte_local

def main():
    # Cargar variables de entorno del archivo .env a la memoria RAM
    load_dotenv()

    print("=" * 60)
    print("      SISTEMA AUTOMATIZADO DE AUDITORÍA DE INFRAESTRUCTURA      ")
    print("=" * 60)
    
    # -----------------------------------------------------------------
    # EXTRACCIÓN SEGURA DE CREDENCIALES DESDE EL ENTORNO (.env)
    # -----------------------------------------------------------------
    IP_LINUX = os.getenv("LINUX_IP")
    USER_LINUX = os.getenv("LINUX_USER")
    PASS_LINUX = os.getenv("LINUX_PASS")
    
    IP_WINDOWS = os.getenv("WINDOWS_IP")
    USER_WINDOWS = os.getenv("WINDOWS_USER")
    PASS_WINDOWS = os.getenv("WINDOWS_PASS")
    
    # Control de seguridad: Validar que toda la infraestructura esté mapeada
    if not all([IP_LINUX, USER_LINUX, PASS_LINUX, IP_WINDOWS, USER_WINDOWS, PASS_WINDOWS]):
        print("❌ ERROR CRÍTICO: Faltan configuraciones en el archivo '.env'.")
        print("[!] Asegúrate de tener las credenciales completas de Linux y Windows.")
        sys.exit(1)
    
    print(f"\n[*] Iniciando Fase de Auditoría:")
    print(f"    - Objetivo Linux (Ubuntu MATE)      | IP: {IP_LINUX}")
    print(f"    - Objetivo Windows (Windows 10 Pro) | IP: {IP_WINDOWS}")
    print("-" * 60)
    
    # =================================================================
    # EJECUCIÓN OBJETIVO 1: UBUNTU MATE (LINUX)
    # =================================================================
    print(f"[*] Evaluando entorno objetivo Linux (Ubuntu MATE) | IP: {IP_LINUX} de forma segura...")
    res_linux = auditar_sistema_linux(hostname=IP_LINUX, username=USER_LINUX, password=PASS_LINUX)
    
    # =================================================================
    # EJECUCIÓN OBJETIVO 2: WINDOWS 10 (WINDOWS)
    # =================================================================
    print(f"[*] Evaluando entorno objetivo Windows (Windows 10 Pro) | IP: {IP_WINDOWS} de forma segura...")
    res_windows = auditar_sistema_windows(hostname=IP_WINDOWS, username=USER_WINDOWS, password=PASS_WINDOWS)
    
    # =================================================================
    # CONSOLIDACIÓN Y VISUALIZACIÓN DE RESULTADOS
    # =================================================================
    
    # --- REPORTE LINUX ---
    print("\n" + "-" * 50)
    print(f"📊 RESULTADOS DE LA AUDITORÍA DE LINUX (Ubuntu MATE) | IP: {IP_LINUX}:")
    print("-" * 50)
    print(f"Estado de la Conexión : {res_linux['status_conexion']}")
    if res_linux['status_conexion'] == "Exitoso":
        print(f"Versión del Kernel    : {res_linux['os_version']}")
        print(f"Estado del Firewall   : {res_linux['firewall_status']}")
        print(f"Parches Pendientes    : {res_linux['updates_pending']}")
    else:
        print(f"❌ Error detectado    : {res_linux['error_msg']}")
        
    # --- REPORTE WINDOWS ---
    print("\n" + "-" * 50)
    print(f"📊 RESULTADOS DE LA AUDITORÍA DE WINDOWS (Windows 10 Pro) | IP: {IP_WINDOWS}:")
    print("-" * 50)
    print(f"Estado de la Conexión : {res_windows['status_conexion']}")
    if res_windows['status_conexion'] == "Exitoso":
        print(f"Estado del Firewall   : {res_windows['firewall_status']}")
        print(f"Parches Pendientes    : {res_windows['updates_pending']}")
    else:
        print(f"❌ Error detectado    : {res_windows['error_msg']}")
        
    print("-" * 50)
    print("[*] Auditoría dual finalizada resguardando credenciales.\n")

    # =================================================================
    # GENERACIÓN DE EVIDENCIAS
    # =================================================================
    print("[*] Generando reporte físico de evidencias...")
    ruta_reporte = guardar_reporte_local(res_linux, res_windows)
    
    respuesta = input("[*] ¿Deseas generar y abrir el reporte detallado en el navegador? (y/n): ")
    if respuesta.lower() == 'y':
        print(f"💾 Reporte generado: {ruta_reporte}")
        webbrowser.open(f"file://{os.path.abspath(ruta_reporte)}")
        print("[*] Abriendo reporte en navegador...")

if __name__ == "__main__":
    main()
