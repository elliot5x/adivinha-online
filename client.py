import socket
import threading
import random

host = '127.0.0.1'
porta = 5555

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, porta))
servidor.listen()

print(f"Servidor ouvindo em {host}:{porta}")

clientes = []
numeros = {}

def lidar_com_cliente(cliente):
    while True:
        try:
            dados = cliente.recv(1024).decode('utf-8')
            if dados == 'sair':
                break
            elif dados.startswith('palpite:'):
                palpite = int(dados.split(':')[1])
                if palpite == numeros[cliente]:
                    cliente.send("correto".encode('utf-8'))
                    break
                elif palpite < numeros[cliente]:
                    cliente.send("maior".encode('utf-8'))
                else:
                    cliente.send("menor".encode('utf-8'))
        except:
            break

    clientes.remove(cliente)
    cliente.close()

def transmitir(mensagem):
    for cliente in clientes:
        try:
            cliente.send(mensagem.encode('utf-8'))
        except:
            continue

def jogo():
    while True:
        numero = random.randint(1, 100)
        for cliente in clientes:
            numeros[cliente] = numero
            cliente.send("iniciar".encode('utf-8'))

        while any(cliente in numeros and numeros[cliente] != 0 for cliente in clientes):
            pass

        transmitir(f"O número era {numero}. Tente novamente!")

        for cliente in clientes:
            if cliente in numeros:
                numeros[cliente] = 0

threading.Thread(target=jogo).start()

while True:
    cliente, endereco = servidor.accept()
    clientes.append(cliente)

    print(f"Conexão de {endereco} estabelecida.")
    threading.Thread(target=lidar_com_cliente, args=(cliente,)).start()
