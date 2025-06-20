import serial
import keyboard
import time
import matplotlib.pyplot as plt


PORTA_SERIAL = '/dev/ttyACM0'
VELOCIDADE_SERIAL = 9600
TIMEOUT_SERIAL = 1 

print("Iniciando o script de coleta de tempo de resposta...")

tempos_de_resposta = []

ser = None

try:
    ser = serial.Serial(PORTA_SERIAL, VELOCIDADE_SERIAL, timeout=TIMEOUT_SERIAL)
    print(f"Sucesso! Conectado à porta serial {PORTA_SERIAL}.")
    print("Comece a interagir com o dispositivo. Pressione 'Esc' a qualquer momento para parar e gerar o gráfico.")

    while not keyboard.is_pressed('esc'):
        
        if ser.in_waiting > 0:
            try:
                linha_recebida = ser.readline().decode('utf-8').strip()
                
                if linha_recebida.isdigit():
                    tempo = int(linha_recebida)
                    if tempo >1100:
                        tempos_de_resposta.append(tempo)
                    print(f"  -> Tempo de resposta recebido: {tempo} ms")
                else:
                    if linha_recebida: 
                        print(f"  -> Dado ignorado (não numérico): '{linha_recebida}'")

            except UnicodeDecodeError:
                print("  -> Erro de decodificação da serial. Um caractere inválido foi recebido.")
            except ValueError:
                print("  -> Erro ao converter dado da serial para inteiro.")

        time.sleep(0.01)

except serial.SerialException as e:
    print(f"\nERRO: Não foi possível abrir a porta serial '{PORTA_SERIAL}'.")
    print("Por favor, verifique os seguintes pontos:")
    print("  1. O Arduino está conectado ao computador?")
    print("  2. A porta serial no script está correta?")
    print("  3. Você tem permissão para acessar a porta? (No Linux, pode ser necessário 'sudo' ou adicionar seu usuário ao grupo 'dialout').")
    print(f"Detalhe do erro do sistema: {e}")

except Exception as e:
    print(f"\nOcorreu um erro inesperado durante a execução: {e}")

finally:
    if ser and ser.is_open:
        ser.close()
        print("\nColeta de dados interrompida. Porta serial fechada.")

if tempos_de_resposta:
    print(f"Gerando gráfico com {len(tempos_de_resposta)} pontos de dados...")
    
    plt.figure(figsize=(12, 7))
    
    plt.plot(range(1, len(tempos_de_resposta) + 1), tempos_de_resposta, marker='o', linestyle='-', color='b', label='Tempo de Resposta')
    
    plt.title('Evolução do Tempo de Resposta do Piloto')
    plt.xlabel('Número da Tentativa')
    plt.ylabel('Tempo de Resposta (ms)')
    plt.legend()
    plt.grid(True)
    
    plt.xticks(range(1, len(tempos_de_resposta) + 1))
    
    plt.show()
else:
    print("Nenhum tempo de resposta foi coletado. O gráfico não será gerado.")

print("Script finalizado.")