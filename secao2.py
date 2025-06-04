# aluno: João Pedro Cardoso de Liz

import hashlib
import json
import itertools
import string
import time

with open('usuarios.json', 'r') as f:
    usuarios = json.load(f)

charset = string.ascii_letters + string.digits
tamanho_maximo = 64

def sha256_string(s):
    return hashlib.sha256(s.encode()).hexdigest()


def forca_bruta(hash_alvo):
    for tamanho in range(1, tamanho_maximo + 1):
        for tentativa in itertools.product(charset, repeat=tamanho):
            senha_tentativa = ''.join(tentativa)
            hash_tentativa = sha256_string(senha_tentativa)
            if hash_tentativa == hash_alvo:
                return senha_tentativa
    return None

#minha implementação    
tempo_total = 0

for usuario in usuarios:
    print(f"\nTentando descobrir a senha de {usuario['nome']}...")
    hash_alvo = usuario['senha'] 

    #minha implementação
    quebra_inicio = time.time()

    if len(hash_alvo) == 64:
        senha_encontrada = forca_bruta(hash_alvo)
    else:
        senha_encontrada = forca_bruta(sha256_string(hash_alvo))

    #minha implementação
    quebra_fim = time.time()
    quebra_tempo = quebra_fim - quebra_inicio
    tempo_total += quebra_tempo

    if senha_encontrada:
        print(f"Senha encontrada: {senha_encontrada}\n"
                #minha implementação
              f"Tempo de quebra: {quebra_tempo:.2f} segundos")
    else:
        print("O algoritmo não conseguiu decifrar a senha.")

    

#minha implementação
print(f"\nTempo total de quebra de senhas: {tempo_total:.2f} segundos")

print("\nProcesso concluído.")
