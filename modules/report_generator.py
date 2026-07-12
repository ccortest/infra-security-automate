import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv # Importar para leer las IPs

load_dotenv()

def guardar_reporte_local(res_linux, res_windows):
    """
    Genera el entregable visual inyectando los datos de auditoría 
    y las direcciones IP de los activos auditados.
    """
    os.makedirs("outputs", exist_ok=True)
    
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('reporte_template.html')
    
    # Inyectamos las IPs desde las variables de entorno para que el HTML las pueda mostrar
    datos_render = {
        "fecha": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "linux": res_linux,
        "linux_ip": os.getenv("LINUX_IP"),
        "windows": res_windows,
        "windows_ip": os.getenv("WINDOWS_IP")
    }
    
    html_final = template.render(datos_render)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_salida = f"outputs/reporte_seguridad_{timestamp}.html"
    
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(html_final)
        
    return ruta_salida
