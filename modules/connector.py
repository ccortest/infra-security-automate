# modules/connector.py
import paramiko
import winrm
import time
import warnings

# Esto silencia específicamente la advertencia de la librería winrm
# que aparecía en la consola al ejecutar los scripts.
warnings.filterwarnings("ignore", category=UserWarning, module="winrm")

def conectar_ssh(hostname, username, password):
    """Establece una conexión SSH y devuelve el objeto cliente."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password, timeout=5)
    return ssh

def conectar_winrm(hostname, username, password):
    """Establece una conexión WinRM con reintentos."""
    max_intentos = 3
    for intento in range(max_intentos):
        try:
            session = winrm.Session(
                target=f"http://{hostname}:5985/wsman",
                auth=(username, password),
                transport='ntlm'
            )
            session.run_cmd('echo', ['connected'])
            return session
        except Exception as e:
            if intento < max_intentos - 1:
                time.sleep(15)
            else:
                raise e
