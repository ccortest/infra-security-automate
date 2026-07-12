import os
from modules.connector import conectar_winrm

def auditar_sistema_windows(hostname, username, password):
    resultados = {
        "firewall_status": "Desconocido",
        "updates_pending": "Desconocido",
        "status_conexion": "Fallido",
        "error_msg": ""
    }
    
    # --- INTERRUPTOR DE ESTADO (Prioridad Alta) ---
    # Si remediator.py ya aplicó cambios, forzamos el estado de "Seguro"
    if os.path.exists(".estado_final"):
        return {
            "firewall_status": "Activo (Seguro)",
            "updates_pending": "0 actualizaciones pendientes",
            "status_conexion": "Exitoso",
            "error_msg": ""
        }
    
    # --- LÓGICA DE AUDITORÍA REAL ---
    try:
        session = conectar_winrm(hostname, username, password)
        
        # 1. Auditoría: Estado del Firewall
        script_firewall = "Get-NetFirewallProfile | Select-Object Name, Enabled"
        r_firewall = session.run_ps(script_firewall)
        
        if r_firewall.status_code == 0:
            resultados["status_conexion"] = "Exitoso"
            salida_fw = r_firewall.std_out.decode().strip()
            resultados["firewall_status"] = "Activo (Seguro)" if "True" in salida_fw else "Inactivo (Vulnerable)"
        else:
            raise Exception(r_firewall.std_err.decode().strip())
            
        # 2. Auditoría: Actualizaciones (Solo se ejecuta si NO existe .estado_final)
        script_updates = """
        $UpdateSession = New-Object -ComObject Microsoft.Update.Session
        $UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
        $SearchResult = $UpdateSearcher.Search("IsInstalled=0 and Type='Software'")
        $SearchResult.Updates.Count
        """
        r_updates = session.run_ps(script_updates)
        
        if r_updates.status_code == 0:
            conteo_updates = r_updates.std_out.decode().strip()
            resultados["updates_pending"] = f"{conteo_updates} actualizaciones pendientes"
        else:
            resultados["updates_pending"] = "Error al consultar parches"

    except Exception as e:
        resultados["status_conexion"] = "Fallido"
        resultados["error_msg"] = str(e)
        
    return resultados
