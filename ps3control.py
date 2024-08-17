import requests
import sys
import requests
import time
from bs4 import BeautifulSoup
from os import system, name

def get_temp(ip):
    url = f'http://{ip}/cpursx_ps3'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    temp = soup.find('font', color="#fff").text.strip()

def fan_control(ip, temp):
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
    
    print(f"Conectado a la IP {ip}")
    print(f"Temperatura actual del sistema: {temp}")
    speed = input("\nIntroduce la velocidad del ventilador deseada (Para salir introduzca 'Salir'): ")
    if speed <= 100:
        requests.get(f'http://192.168.1.50/cpursx.ps3?fan={speed}', verify=False)
    elif speed < 0:
        print("No se puede poner velocidad negativa")
        time.sleep(2)
    elif speed > 100:
        print("La velocidad máxima es el 100%")
        time.sleep(2)
    elif speed == "Salir":
        sys.exit(0)
    else:
        print("Introduzca un valor numérico")
        time.sleep(2)
def controller(ip, temp):
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
    print(f"Conectado a la IP {ip}")
    print(f"Temperatura actual del sistema: {temp}")
    print("\nEscoge la acción a realizar:")
    print("1. Establecer la velocidad del ventilador manualmente")
    print("2. Apagar el sistema PS3")
    print("3. Reiniciar el sistema PS3")

    seleccion = input("Introduce la acción que se debe realizar: ")
    if seleccion == 1:
        fan_control()
    elif seleccion == 2:
        requests.get(f'http://{ip}/shutdown.ps3', verify=False)
    elif seleccion == 3:
        requests.get(f'http://{ip}/restart.ps3', verify=False)

def obtain_ip():
    ip = input("Introduce la IP de tu PS3: ")
    r = requests.get(f'http://{ip}')
    if r.status_code != 200:
        print(f"Error {r.status_code} al conectarse")
        sys.exit(1)
    elif "wMAN MOD" not in r.text:
        print(f"Error: La IP dada no es de una PS3 o no se esta ejecutando WebMAN Mod en ella.")
        sys.exit(1)

if __name__ == "__main__":
    obtain_ip()
    get_temp()
    controller()
    while True:
        fan_control()
