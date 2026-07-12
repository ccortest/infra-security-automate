[README.md](https://github.com/user-attachments/files/29942747/README.md)
# Infra Security Automate

Herramienta diseñada para auditar y remediar la seguridad en entornos Windows y Linux. Ideal para verificar el estado del Firewall, actualizaciones pendientes y aplicar configuraciones base.

## 🚀 Vista previa
![Demostración de ejecución](ruta/a/tu/captura.png)

*(Aquí puedes añadir el enlace a tu video de YouTube o grabar un GIF de la ejecución)*

## ¿Qué hace esta herramienta?
- **Auditoría:** Detecta automáticamente si tu sistema está actualizado y verifica el estado de las defensas (UFW/Firewall).
- **Remediación:** Automatiza la aplicación de parches y configuraciones para dejar el equipo seguro.
- **Reportes:** Genera un resumen visual en HTML de todo lo auditado.

## Instalación rápida
1. Clona este repositorio: `git clone https://github.com/ccortest/infra-security-automate.git`
2. Instala las librerías necesarias:
```
pip install paramiko pywinrm jinja2 python-dotenv
```

## Cómo usarlo
1. Configura tus credenciales creando un archivo llamado `.env` en la carpeta raíz:
```
LINUX_IP=tu_ip_linux
LINUX_USER=tu_usuario
LINUX_PASS=tu_contraseña
WINDOWS_IP=tu_ip_windows
WINDOWS_USER=tu_usuario
WINDOWS_PASS=tu_contraseña
```
2. Ejecuta la auditoría: `python3 auditor.py`
3. Ejecuta la remediación: `python3 remediator.py`

## Evidencias
Puedes encontrar los reportes generados en la carpeta `/outputs`.

### Video de demostración
[Haz clic aquí para ver el proceso de ejecución en video](#)
