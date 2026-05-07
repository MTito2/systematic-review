from functions import construct_payload, send_openai, wait_processing, get_only_answers
import os

while True:
    construct_payload()
    op = input("Deseja enviar payloads? [S/N] ").upper()

    if op in("S", "SIM",):
        os.system("cls")
        send_openai()
        wait_processing()
        get_only_answers()
    else:
        print("Resposta inválida")
        continue