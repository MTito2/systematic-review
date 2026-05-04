from functions import construct_payload, get_only_answers

while True:
    article_number = int(input("Informe o número de artigos: "))
    construct_payload(article_number)
    get_only_answers()
