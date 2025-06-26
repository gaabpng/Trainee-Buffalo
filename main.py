import serial
import keyboard
import time
import matplotlib.pyplot as plt
import os

# --- CONFIGURAÇÕES ---
PORTA_SERIAL = '/dev/ttyACM0'  # Altere conforme necessário
VELOCIDADE_SERIAL = 9600
TIMEOUT_SERIAL = 1  # segundos

print("Iniciando o script de coleta de tempo de resposta...\n")

# Lista para armazenar os tempos de resposta
tempos_de_resposta = []

# Inicializa a variável 'ser' para garantir que ela exista no bloco 'finally'
ser = None

try:
    # Tenta abrir a porta serial
    ser = serial.Serial(PORTA_SERIAL, VELOCIDADE_SERIAL, timeout=TIMEOUT_SERIAL)
    print(f"Sucesso! Conectado à porta serial {PORTA_SERIAL}.")
    print("Comece a interagir com o dispositivo. Pressione 'Esc' para encerrar a coleta.\n")

    # Loop de leitura da serial
    while not keyboard.is_pressed('esc'):
        if ser.in_waiting > 0:
            try:
                linha_recebida = ser.readline().decode('utf-8').strip()

                if linha_recebida.isdigit():
                    tempo = int(linha_recebida)
                    if tempo > 1100:
                        tempos_de_resposta.append(tempo)
                        print(f"  -> Tempo de resposta recebido: {tempo} ms")
                else:
                    if linha_recebida:
                        print(f"  -> Dado ignorado (não numérico): '{linha_recebida}'")
            except UnicodeDecodeError:
                print("  -> Erro de decodificação da serial.")
            except ValueError:
                print("  -> Erro ao converter dado da serial para inteiro.")

        time.sleep(0.01)

except serial.SerialException as e:
    print(f"\nERRO: Não foi possível abrir a porta serial '{PORTA_SERIAL}'.")
    print("Verifique se o Arduino está conectado e se a porta está correta.")
    print(f"Detalhe do erro: {e}")

except Exception as e:
    print(f"\nErro inesperado: {e}")

finally:
    if ser and ser.is_open:
        ser.close()
        print("\nColeta finalizada. Porta serial fechada.")

# --- PROCESSAMENTO E SALVAMENTO ---
if tempos_de_resposta:
    print(f"\n{len(tempos_de_resposta)} tempos de resposta coletados.")

    # Cálculo da média
    media = sum(tempos_de_resposta) / len(tempos_de_resposta)
    print(f"Média dos tempos de resposta: {media:.2f} ms")

    # Solicita nome do piloto
    nome_piloto = input("\nDigite o nome do piloto: ").strip()

    # Geração do gráfico
    plt.figure(figsize=(12, 7))
    plt.plot(range(1, len(tempos_de_resposta) + 1), tempos_de_resposta,
             marker='o', linestyle='-', color='b', label='Tempo de Resposta')
    plt.title(f'Tempos de Resposta - {nome_piloto}')
    plt.xlabel('Tentativa')
    plt.ylabel('Tempo (ms)')
    plt.legend()
    plt.grid(True)
    plt.xticks(range(1, len(tempos_de_resposta) + 1))
    plt.show()

    # --- Atualização do ranking ---
    nome_arquivo = "ranking_pilotos.txt"
    ranking = []

    # Lê ranking existente (se houver)
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(" ms - ")
                if len(partes) == 2:
                    try:
                        media_existente = float(partes[0])
                        nome_existente = partes[1]
                        ranking.append((media_existente, nome_existente))
                    except ValueError:
                        continue  # Ignora linhas inválidas

    # Adiciona novo piloto e ordena por média crescente
    ranking.append((media, nome_piloto))
    ranking.sort()

    # Salva ranking atualizado
    with open(nome_arquivo, 'w') as arquivo:
        for media_valor, nome in ranking:
            arquivo.write(f"{media_valor:.2f} ms - {nome}\n")

    print(f"\nRanking atualizado salvo em '{nome_arquivo}' com sucesso!")

else:
    print("\nNenhum tempo válido foi coletado. Nenhum dado será salvo.")

print("\nScript finalizado.")
