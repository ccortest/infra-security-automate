import os
from dotenv import load_dotenv

load_dotenv()

# Obtener IPs para los mensajes
linux_ip = os.getenv("LINUX_IP", "IP_NO_CONFIGURADA")
windows_ip = os.getenv("WINDOWS_IP", "IP_NO_CONFIGURADA")

# Archivos de control de flujo
archivos_a_limpiar = [".flujo_auditoria", ".estado_final"]
limpiado = False

for archivo in archivos_a_limpiar:
    if os.path.exists(archivo):
        os.remove(archivo)
        limpiado = True

if limpiado:
    # Mensaje técnico profesional sin mostrar los archivos eliminados
    print("[*] Parámetros de auditoría restablecidos con éxito.")
    print(f"    - Estado de los nodos operativos: Preparados para el despliegue del flujo de auditoría.")
else:
    # Mensaje técnico cuando ya no hay nada que limpiar
    print("[*] No se han detectado auditorías previas registradas en el sistema.")
    print(f"    - Ubuntu MATE ({linux_ip}): Sin auditoría previa.")
    print(f"    - Windows 10 Pro ({windows_ip}): Sin auditoría previa.")
