import random

caracteres = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

comprimento = int(input("Digite o comprimento da senha desejada: "))

senha_gerada = ""

for _ in range(comprimento):
    caractere_aleatorio = random.choice(caracteres)
    senha_gerada += caractere_aleatorio

print(f"Sua senha gerada é: {senha_gerada}")
