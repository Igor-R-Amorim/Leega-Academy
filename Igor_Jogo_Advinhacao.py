import random
from IPython.core.display import clear_output

print('+-----------------------------------+')
print('| Bem-vindo ao jogo da adivinhação! |')
print('+-----------------------------------+')



while True:
    modalidade = input("\nEscolha sua modalidade:\n1. Advinhar Numeros \n2. Adivinhar Letras \nEscolha: ")
    if modalidade == "1":
        print(f'\nVocê Escolheu a modalidade "Advinhar Numeros"')
        numero_secreto = random.randint(1, 200) 
        pontuacao = 1000
        break
    elif modalidade == "2":
        print(f'\nVocê Escolheu a modalidade "Advinhar Letras"')
        alfabeto = ("abcdefghijklmnopqrstuvwxyz").upper()
        letra = ''.join(random.choices(alfabeto, k=1))
        pontuacao = 1000
        break
    else:
        clear_output(wait=True)
        print("Valor inválido! Tente novamente")

if modalidade == "1": #MODALIDADE NUMERO
  while True:
      dificuldade = input('''
Escolha sua dificuldade:
1. Muito Fácil
2. Fácil
3. Médio
4. Difícil
5. Muito Difícil
Escolha: ''')
      if dificuldade == "1":
          tentativas = 25
          print(f'\nFácil: Você tem {tentativas} tentativas para descobrir o número secreto...')
          break
      elif dificuldade == "2":
          tentativas = 20
          print(f'\nMédio: Você tem {tentativas} tentativas para descobrir o número secreto...')
          break
      elif dificuldade == "3":
          tentativas = 15
          print(f'\nDifícil: Você tem {tentativas} tentativas para descobrir o número secreto...')
          break
      elif dificuldade == "4":
          tentativas = 10
          print(f'\nDifícil: Você tem {tentativas} tentativas para descobrir o número secreto...')
          break
      elif dificuldade == "5":
          tentativas = 5
          print(f'\nDifícil: Você tem {tentativas} tentativas para descobrir o número secreto...')
          break
      else:
          clear_output(wait=True)
          print("Valor inválido! Tente novamente")

else: #MODALIDADE LETRA
  while True:
      dificuldade = input('''
Escolha sua dificuldade:
1. Fácil
2. Médio
3. Difícil
Escolha: ''')
      if dificuldade == "1":
          tentativas = 20
          print(f"\nFácil: Você tem {tentativas} tentativas para descobrir a letra secreta...")
          break
      elif dificuldade == "2":
          tentativas = 10
          print(f"\nMédio: Você tem {tentativas} tentativas para descobrir a letra secreta...")
          break
      elif dificuldade == "3":
          tentativas = 5
          print(f"\nDifícil: Você tem {tentativas} tentativas para descobrir a letra secreta...")
          break
      else:
          clear_output(wait=True)
          print("Valor inválido! Tente novamente")


if modalidade == "1": #MODALIDADE NUMERO
  for rodada in range(1, tentativas + 1):
      print(f'\nRODADA {rodada}')
      palpite = input("Qual é o seu palpite?\nDigite um número entre 1 e 200: ")

      if palpite.isdecimal():
          palpite = int(palpite)

          # Palpite fora do intervalo
          if palpite < 1 or palpite > 200:
              print("\nFora do Intervalo!\n")
              tentativas = tentativas - 1
              if tentativas > 0:
                  print(f"Tente novamente!\nTentativas restantes: {tentativas}")
              continue
      else:
          print("\nVocê perdeu uma tentativa!")
          print("Digite apenas valores inteiros!\n")
          tentativas = tentativas - 1
          print(f"Tente novamente!\nTentativas restantes: {tentativas}")
          continue

      palpite_certo = (numero_secreto == palpite)
      palpite_menor = (numero_secreto > palpite)
      palpite_maior = (numero_secreto < palpite)

      if palpite_certo:
          print(f"\nParabéns! Você acertou, o número secreto é: {numero_secreto}")
          print(f"Pontuação: {pontuacao}")
          break
      else:
          if palpite_menor:
              print(f"\nSeu palpite {palpite} é MENOR que o número secreto.")
          elif palpite_maior:
              print(f"\nSeu palpite {palpite} é MAIOR que o número secreto.")

          tentativas = tentativas - 1
          pontuacao = pontuacao - (abs(numero_secreto - palpite))

          if tentativas > 0:
              print(f"Tente novamente!\nTentativas restantes: {tentativas}")
          else:
              print('\n################')
              print('# Fim de Jogo! #')
              print('################')
              print(f'O número secreto era {numero_secreto}')
              print(f'Sua pontuação: {pontuacao}')

  if tentativas == 0 and pontuacao == 1000:
      print('\n################')
      print('# Fim de Jogo! #')
      print('################')
      print(f'O número secreto era {numero_secreto}')
      print('Sua pontuação: 0')

else: #MODALIDADE LETRA
  for rodada in range(1, tentativas + 1):
      print(f'\nRODADA {rodada}')
      palpite = input('''
Entre (a b c d e f g h i j k l m n o p q r s t u v w x y z)
Digite o seu palpite: ''')
    
      if palpite.isalpha():
        palpite = str(palpite.upper())
        if len(palpite)>1:
          print("\nFora do Intervalo!")
          tentativas = tentativas - 1
          if tentativas > 0:
            print(f'Tente de novo!\nTentativas restantes: {tentativas}')
          continue

      else:
        print("\nVocê perdeu uma tentativa")
        print("Digite apenas caracteres Alpha! (letras sem acentos)")
        tentativas-= 1
        print(f"Tente novamente!\nTentativas restantes: {tentativas}")
        continue
      
      palpite_certo = (alfabeto.find(letra) == alfabeto.find(palpite))
      palpite_menor = (alfabeto.find(letra)  > alfabeto.find(palpite))
      palpite_maior = (alfabeto.find(letra)  < alfabeto.find(palpite))

      if palpite_certo:
          print(f"\nParabéns! Você acertou, o número secreto é: {letra}")
          print(f"Pontuação: {pontuacao}")
          break
      else:
          if palpite_menor:
              print(f"\nSeu palpite {palpite} é MENOR que o número secreto.")
          elif palpite_maior:
              print(f"\nSeu palpite {palpite} é MAIOR que o número secreto.")

          tentativas = tentativas - 1
          pontuacao = pontuacao - (abs(alfabeto.find(letra) - alfabeto.find(palpite)))

          if tentativas > 0:
              print(f"Tente novamente!\nTentativas restantes: {tentativas}")
          else:
              print('\n################')
              print('# Fim de Jogo! #')
              print('################')
              print(f'\nO número secreto era: {letra}')
              print(f'Sua pontuação: {pontuacao}')

  if tentativas == 0 and pontuacao == 1000:
      print('\n################')
      print('# Fim de Jogo! #')
      print('################')
      print(f'\nO número secreto era: {letra}')
      print('Sua pontuação: 0')  
