import subprocess
import os
import signal
import keyboard
import time

# Lista para almacenar los PID de los procesos
pids = []

# Directorio que contiene los archivos de perfiles
directorio_perfiles = "profiles"

# Obtener la lista de archivos en el directorio
archivos_perfiles = os.listdir(directorio_perfiles)
print(archivos_perfiles)
# Número de comandos a ejecutar (uno por cada archivo en el directorio)
num_comandos = len(archivos_perfiles)

# Comando base a ejecutar
comando_base = "python3 p2p.py"

# Usuarios para no ejecutar pues se testean manual
users = ['Lidia', 'Maria']

# Ejecutar los comandos y obtener los PID
for archivo_perfil in archivos_perfiles:
    if archivo_perfil.split('.')[0] not in users:
        comando = f"{comando_base} {archivo_perfil.split('.')[0]}"
        #print(comando)
        proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        pids.append(proceso.pid)

# Imprimir los PID de los procesos
print("PID de los procesos:", pids)

# Mostrar un menú para cancelar las ejecuciones
while True:
    if input("Para cancelar presiona [N]: "):
        break

# Enviar la señal SIGKILL para finalizar los procesos
for pid in pids:
    try:
        os.kill(pid+1, signal.SIGKILL)
        print(f"Proceso con PID {pid+1} finalizado.")
    except ProcessLookupError:
        print(f"No se pudo encontrar el proceso con PID {pid+1}.")

# Esperar un tiempo para que los procesos tengan tiempo de finalizar
time.sleep(2)

# Verificar si los procesos aún están en ejecución
for pid in pids:
    try:
        os.kill(pid+1, 0)  # 0 no envía una señal, solo verifica si el proceso está en ejecución
        print(f"Proceso con PID {pid+1} aún en ejecución.")
    except ProcessLookupError:
        print(f"Proceso con PID {pid+1} finalizado correctamente.")
