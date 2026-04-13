import random

numero_secreto = random.randint(1, 20)

for tentativa in range(1, 6):
    print("Tentativa " + str(tentativa) + ": Adivinhe o numero de 1 a 20:")
    palpite = int(input())

    if palpite == numero_secreto:
        print("Parabens! Voce acertou!")
        break
    elif palpite < numero_secreto:
        print("O numero secreto e maior.")
    else:
        print("O numero secreto e menor.")

else:
    print("Nao ha mais tentativas. O numero secreto era " + str(numero_secreto) + ".")
