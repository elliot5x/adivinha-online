import socket
import threading

host = '127.0.0.1'
porta = 5555

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, porta))

nome = input("Digite seu nome: ")
cliente.send(nome.encode('utf-8'))

def receber():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            print(mensagem)
            if mensagem == "iniciar":
                palpite = input("Adivinhe um número entre 1 e 100 (ou 'sair' para encerrar): ")

                if palpite.lower() in ['sair', 'q']:
                    cliente.send('sair'.encode('utf-8'))
                    break

                palpite = int(palpite)
                cliente.send(f"palpite:{palpite}".encode('utf-8'))
            elif mensagem == "correto":
                print("Parabéns! Você acertou o número.")
            elif mensagem == "maior":
                print("Tente um número maior.")
            elif mensagem == "menor":
                print("Tente um número menor.")
        except:
            break

threading.Thread(target=receber).start()

while True:
    pass
