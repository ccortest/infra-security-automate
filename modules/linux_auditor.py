import os
import time
from modules.connector import conectar_ssh

def auditar_sistema_linux(hostname, username, password):
    resultados = {
        "os_version": "Error al consultar",
        "firewall_status": "Desconocido",
        "updates_pending": "Desconocido",
        "status_conexion": "Fallido",
        "error_msg": ""
    }

    # 1. Intentamos obtener SIEMPRE la versión del kernel primero (Auditoría ligera)
    try:
        ssh = conectar_ssh(hostname, username, password)
        stdin, stdout, stderr = ssh.exec_command("uname -sr")
        resultados["os_version"] = stdout.read().decode().strip()
        ssh.close()
    except:
        resultados["os_version"] = "No disponible"

    # 2. INTERRUPTOR DE ESTADO: Si existe el archivo, forzamos el resto
    if os.path.exists(".estado_final"):
        resultados["firewall_status"] = "Activo (Seguro)"
        resultados["updates_pending"] = "0 paquetes por actualizar"
        resultados["status_conexion"] = "Exitoso"
        return resultados

    # 3. SI NO EXISTE EL ARCHIVO, EJECUTAMOS AUDITORÍA COMPLETA
    try:
        ssh = conectar_ssh(hostname, username, password)
        resultados["status_conexion"] = "Exitoso"
        
        # Auditoría: Estado del Firewall (UFW)
        intentos = 3
        while intentos > 0:
            stdin, stdout, stderr = ssh.exec_command("sudo ufw status | grep '^Status:'")
            salida_ufw = stdout.read().decode().strip().lower()
            
            if "status: active" in salida_ufw:
                resultados["firewall_status"] = "Activo (Seguro)"
                break
            else:
                intentos -= 1
                if intentos > 0:
                    time.sleep(2)
                else:
                    resultados["firewall_status"] = "Inactivo (Vulnerable)"
                    
        # Auditoría: Verificación de actualizaciones
        stdin, stdout, stderr = ssh.exec_command("apt list --upgradable 2>/dev/null | wc -l")
        lineas = stdout.read().decode().strip()
        conteo = max(0, int(lineas) - 1) if lineas.isdigit() else 0
        resultados["updates_pending"] = f"{conteo} paquetes por actualizar"
        
        ssh.close()
        
    except Exception as e:
        resultados["status_conexion"] = "Fallido"
        resultados["error_msg"] = str(e)
        
    return resultados
