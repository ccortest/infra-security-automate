import os
import datetime
import webbrowser
from dotenv import load_dotenv
from jinja2 import Template
from modules.connector import conectar_ssh, conectar_winrm

load_dotenv()

def generar_reporte_html(acciones):
    """Genera un reporte de remediación basado en la plantilla Jinja2."""
    template_path = 'templates/remediacion_template.html'
    with open(template_path, 'r') as f:
        plantilla_contenido = f.read()
    
    t = Template(plantilla_contenido)
    html_content = t.render(
        acciones=acciones, 
        fecha=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    filename = f"outputs/remediacion_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, "w") as f:
        f.write(html_content)
    return filename

def ejecutar_remediacion():
    linux_ip, linux_user, linux_pass = os.getenv("LINUX_IP"), os.getenv("LINUX_USER"), os.getenv("LINUX_PASS")
    windows_ip, windows_user, windows_pass = os.getenv("WINDOWS_IP"), os.getenv("WINDOWS_USER"), os.getenv("WINDOWS_PASS")

    acciones_realizadas = []

    print("=" * 60)
    print("      SISTEMA DE REMEDIACIÓN Y HARDENING AUTOMATIZADO      ")
    print("=" * 60)
    print(f"[*] Aplicando políticas de seguridad en:")
    print(f"    - Objetivo Linux (Ubuntu MATE)      | IP: {linux_ip}")
    print(f"    - Objetivo Windows (Windows 10 Pro) | IP: {windows_ip}")
    print("-" * 60)

    # --- REMEDIACIÓN LINUX (DETALLADA) ---
    print(f"\n[*] Aplicando Hardening en Ubuntu MATE ({linux_ip})...")
    try:
        ssh = conectar_ssh(linux_ip, linux_user, linux_pass)
        
        # 1. Obtenemos la lista de nombres de paquetes pendientes
        comando_lista = f"echo {linux_pass} | sudo -S apt list --upgradable 2>/dev/null | cut -d/ -f1 | grep -v 'Listing' | paste -sd, -"
        stdin, stdout, stderr = ssh.exec_command(comando_lista)
        lista_paquetes = stdout.read().decode().strip()
        
        print(f"[+] Actualizando paquetes en Ubuntu MATE ({linux_ip}): {lista_paquetes if lista_paquetes else 'Ninguno'}...")
        
        # 2. Ejecutar la actualización y Firewall
        comando_linux = f"echo {linux_pass} | sudo -S ufw --force enable && echo {linux_pass} | sudo -S apt-get update && echo {linux_pass} | sudo -S apt-get upgrade -y"
        stdin, stdout, stderr = ssh.exec_command(comando_linux)
        
        if stdout.channel.recv_exit_status() == 0:
            print(f"[✅] Linux (Ubuntu MATE | {linux_ip}): Hardening aplicado.")
            with open(".estado_final", "w") as f: f.write("1")
            detalle_ubuntu = f"Firewall activado. Paquetes actualizados: {lista_paquetes if lista_paquetes else 'Ninguno'}"
            acciones_realizadas.append({"sistema": f"Ubuntu MATE ({linux_ip})", "detalle": detalle_ubuntu})
        ssh.close()
    except Exception as e:
        print(f"[❌] Error en Linux ({linux_ip}): {e}")

    # --- REMEDIACIÓN WINDOWS (MEJORADA) ---
    print(f"\n[*] Aplicando Hardening en Windows 10 Pro ({windows_ip})...")
    try:
        session = conectar_winrm(windows_ip, windows_user, windows_pass)
        
        comando_ps = '''
        Stop-Service -Name RemoteRegistry -Force -ErrorAction SilentlyContinue; 
        Set-Service -Name RemoteRegistry -StartupType Disabled;
        & auditpol /set /subcategory:"Inicio de sesión" /success:enable /failure:enable;
        net accounts /maxpwage:42 /minpwlen:12;
        '''
        
        r = session.run_ps(comando_ps)
        
        if r.status_code == 0:
            print(f"[✅] Windows (Windows 10 Pro | {windows_ip}): Hardening aplicado con éxito.")
            acciones_realizadas.append({
                "sistema": f"Windows 10 Pro ({windows_ip})", 
                "detalle": "RemoteRegistry detenido/deshabilitado, Auditoría Logon activada, Política de contraseñas (12 chars)."
            })
        else:
            print(f"[❌] Windows ({windows_ip}): El script devolvió código {r.status_code}. Salida: {r.std_err}")
            
    except Exception as e:
        print(f"[❌] Error crítico en Windows ({windows_ip}): {e}")

    # --- GENERACIÓN DE REPORTE ---
    if acciones_realizadas:
        respuesta = input("\n[*] ¿Deseas generar y abrir el reporte detallado de remediación? (y/n): ")
        if respuesta.lower() == 'y':
            archivo = generar_reporte_html(acciones_realizadas)
            print(f"💾 Reporte generado: {archivo}")
            webbrowser.open(f"file://{os.path.abspath(archivo)}")
            print("[*] Abriendo reporte en navegador...")

if __name__ == "__main__":
    ejecutar_remediacion()
