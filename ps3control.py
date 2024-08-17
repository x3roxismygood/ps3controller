import requests
import sys
import time
from bs4 import BeautifulSoup
from os import system, name

def get_temp(ip):
    url = f'http://{ip}/cpursx_ps3'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    temp = soup.find('font', color="#fff").text.strip()
    return temp

def fan_control(ip, temp):
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
    
    print(f"Conectado a la IP {ip}")
    print(f"Temperatura actual del sistema: {temp}")
    speed = input("\nIntroduce la velocidad del ventilador deseada (Para salir introduzca 'Salir'): ")
    
    try:
        speed = int(speed)
        if 0 <= speed <= 100:
            requests.get(f'http://{ip}/cpursx.ps3?fan={speed}', verify=False)
            print(f"Velocidad del ventilador establecida en {speed}%")
            controller(ip, temp)
        else:
            print("La velocidad debe estar entre 0 y 100%")
            time.sleep(2)
            controller(ip, temp)
    except ValueError:
        if speed.lower() == "salir":
            sys.exit(0)
        else:
            print("Introduzca un valor numérico válido")
            time.sleep(2)
            controller(ip, temp)

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
    print("4. Actualizar las temperaturas")
    print("5. Salir")

    seleccion = input("Introduce la acción que se debe realizar: ")
    
    try:
        seleccion = int(seleccion)
        if seleccion == 1:
            fan_control(ip, temp)
        elif seleccion == 2:
            requests.get(f'http://{ip}/shutdown.ps3', verify=False)
            print("PS3 apagada.")
            sys.exit(0)
        elif seleccion == 3:
            requests.get(f'http://{ip}/restart.ps3', verify=False)
            print("PS3 reiniciada.")
            sys.exit(0)
        elif seleccion == 4:
            controller(ip, temp)
        elif seleccion == 5:
            sys.exit(0)
        else:
            print("Opción no válida.")
            sys.exit(1)
    except ValueError:
        print("Por favor, introduce un número válido.")
        sys.exit(1)

def obtain_ip():
    ip = input("Introduce la IP de tu PS3: ")
    try:
        r = requests.get(f'http://{ip}', verify=False)
        if r.status_code != 200:
            print(f"Error {r.status_code} al conectarse")
            sys.exit(1)
        elif "wMAN MOD" not in r.text:
            print(f"Error: La IP dada no es de una PS3 o no se está ejecutando WebMAN Mod en ella.")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        sys.exit(1)
    
    return ip

if __name__ == "__main__":
    ip = obtain_ip()
    temp = get_temp(ip)
    controller(ip, temp)
