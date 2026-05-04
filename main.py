from functions import construct_payload, get_only_answers
import os

while True:
    article_number = int(input("Informe o número de artigos: "))
    construct_payload(article_number)
    op = input("Deseja enviar payloads? [S/N]").upper()

    if op in("S", "SIM",):
        os.system("cls")
        get_only_answers()
    else:
        print("Resposta inválida")
        continue