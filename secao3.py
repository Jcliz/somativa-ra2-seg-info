# aluno: João Pedro Cardoso de Liz

import json
import json.tool
import hashlib

def cifrar_senha(senha):
    senha_cifrada = senha.encode()
    hash1 = hashlib.sha256(senha_cifrada).hexdigest()

    hash2 = hashlib.sha256(hash1.encode()).hexdigest()
    return hash2

def ler_arquivo_matriz():
    with open("matriz_controle_acesso.json", mode="r") as arquivo:
        # Lê o conteúdo do arquivo (arquivo.read()) e deserializa o
        # JSON para dicionário do Python (json.loads())
        return json.loads(arquivo.read())


def ler_arquivo_usuarios():
    with open("usuarios.json", "r") as arquivo:
        return json.loads(arquivo.read())


def listar_arquivos(usuario):
    arquivo_permitido = usuario['permissoes'].get('geral')

    if not arquivo_permitido:
        print("\nSem arquivos criados.")
        return

    for arquivo in arquivo_permitido:
        print(f"- {arquivo}")


def salvar_resultados(permissoes):
    # Abre arquivo para escrita para salvarmos o resultado das nossas operações
    with open('matriz_controle_acesso.json', mode='w') as arquivo:
        permissoes_serializado = json.dumps(permissoes, indent=4)
        arquivo.write(permissoes_serializado)


def registrar_usuario(dados_json):
    permissoes = ler_arquivo_matriz()

    login = str(input("\nDigite o login: "))

    if not len(login) == 4:
        print(f"\nO login precisa ter 4 dígitos.")
        return dados_json

    if buscar_usuario(login, dados_json) is not None:
        print("\nO usuário já foi criado anteriormente.")
        return dados_json 

    senha = str(input("Digite a senha: "))

    if not len(senha) == 4:
        print(f"\nA senha precisa ter 4 dígitos.")
        return dados_json

    usuario = {
        'nome': login,
        'senha': cifrar_senha(senha)
    }

    usuarios = ler_arquivo_usuarios()
    usuarios.append(usuario)

    with open("usuarios.json", "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)

    #recarrega os dados
    dados_json = ler_arquivo_usuarios()

    novo_usuario_permissoes = {
        'nome': login,
        'permissoes': {
            'leitura': [],
            'escrita': [],
            'exclusao': [],
            'geral': []
        }
    }

    permissoes.append(novo_usuario_permissoes)
    salvar_resultados(permissoes)
    print("\nUsuário cadastrado com sucesso!")

    return dados_json #dados atualizados


def buscar_usuario(login, dados_json):
    for usuario in dados_json:
        if usuario['nome'] == login:
            return dados_json.index(usuario)

    return None


def buscar_usuario_matriz(login):
    permissoes = ler_arquivo_matriz()
    for usuario in permissoes:
        if usuario['nome'] == login:
            return permissoes.index(usuario), usuario

    return None, None


def criar_arquivo(nome_arquivo, index, usuario, permissoes, nome):
    if buscar_arquivo(nome):
        print(f"\nO arquivo '{nome}' já existe!")
        return

    if usuario is not None:
        permissoes[index]['permissoes']['leitura'].append(nome_arquivo)
        permissoes[index]['permissoes']['escrita'].append(nome_arquivo)
        permissoes[index]['permissoes']['exclusao'].append(nome_arquivo)
        permissoes[index]['permissoes']['geral'].append(nome_arquivo)

        print(f"\nArquivo '{nome}' criado.")
        salvar_resultados(permissoes)


def excluir_arquivo(index, usuario, nome_arquivo, permissoes):
    if usuario is not None and nome_arquivo in permissoes[index]['permissoes']['exclusao']:
        permissoes[index]['permissoes']['leitura'].remove(nome_arquivo)
        permissoes[index]['permissoes']['escrita'].remove(nome_arquivo)
        permissoes[index]['permissoes']['exclusao'].remove(nome_arquivo)
        permissoes[index]['permissoes']['geral'].remove(nome_arquivo)

        print(f"\n'{nome_arquivo}' excluído com sucesso.")
        salvar_resultados(permissoes)

    elif nome_arquivo not in permissoes[index]['permissoes']['geral']:
        print("\nArquivo inexistente.")
        return

    else:
        print("\nAcesso negado.")
        return


def buscar_arquivo(nome_arquivo):
    permissoes = ler_arquivo_matriz()

    for usuario in permissoes:
        if nome_arquivo in usuario['permissoes'].get('leitura') or \
           nome_arquivo in usuario['permissoes'].get('escrita') or \
           nome_arquivo in usuario['permissoes'].get('exclusao') or \
           nome_arquivo in usuario['permissoes'].get('geral'):
            return True

    return False


def buscar_permissoes(permissao, usuario):
    return usuario['permissoes'].get(permissao)


def menu_opcoes(login):
    _d, usuario = buscar_usuario_matriz(login)
    arquivos = buscar_permissoes("geral", usuario)

    print("\nSelecione o arquivo para excluir: \n")
    for arquivo in arquivos:
        print(f"[{arquivos.index(arquivo) + 1}] - {arquivo}")

    print("\n[0] - Voltar")
    return arquivos


def __init__():
    try:
        dados_json = ler_arquivo_usuarios()

        print("\n Seja bem-vindo ao controle de acesso! :D")

        anonimo = True
        while anonimo:
            print("""
            -_--_--_--_--_--_--_--_--_--_-
            [1] - Autenticação
            [2] - Cadastro
                
            [0] - Sair
            -_--_--_--_--_--_--_--_--_--_-
                """)
            try:
                opcao = int(input("===>>> "))

            except ValueError:
                print("\nEntrada inválida. Apenas números são aceitos.")
                continue

            if opcao == 1.0:
                login = str(input("\nDigite o login: "))
                senha = str(input("Digite a senha: "))

                busca = buscar_usuario(login, dados_json)

                if busca is not None:
                    login_cadastrado = dados_json[busca]['nome']
                    senha_cadastrada = dados_json[busca]['senha']

                    if login == login_cadastrado and cifrar_senha(senha) == senha_cadastrada:
                        print(f"\nBem vindo(a) {login}!")
                        anonimo = False

                        autenticado = True
                        while autenticado:
                            print("""
            -_--_--_--_--_--_--_--_--_--_-
            Opções de manipulação de arquivos:
                
            [1] - Listar
            [2] - Criar
            [3] - Excluir
            [4] - Leitura
            [5] - Escrita
                
            [0] - Voltar
            -_--_--_--_--_--_--_--_--_--_-
                                """)

                            permissoes = ler_arquivo_matriz()

                            try:
                                opcao = int(input("===>>> "))

                            except ValueError:
                                print(
                                    "\nEntrada inválida. Apenas números são aceitos.")
                                continue

                            if opcao == 1:
                                print("\nArquivos:")
                                _a, usuario = buscar_usuario_matriz(login)
                                listar_arquivos(usuario)

                            elif opcao == 2:
                                index, usuario = buscar_usuario_matriz(login)
                                nome = str(
                                    input("\nInforme o nome do arquivo: "))
                                criar_arquivo(
                                    nome, index, usuario, permissoes, nome)

                            elif opcao == 3:
                                index, usuario = buscar_usuario_matriz(login)
                                arquivos = menu_opcoes(login)

                                try:
                                    escolha = int(input("\n===>>> "))

                                except ValueError:
                                    print("\nEntrada inválida. Apenas números são aceitos.")
                                    continue

                                if 1 <= escolha <= len(arquivos):
                                    nome = arquivos[escolha - 1]
                                    excluir_arquivo(index, usuario, nome, permissoes)

                                elif escolha == 0:
                                    print("\nVoltando...")

                                else:
                                    print("\nOpção inválida.")

                            elif opcao == 4:
                                _b, usuario = buscar_usuario_matriz(login)
                                arquivos = menu_opcoes(login)
                                arquivos_gerais = buscar_permissoes("geral", usuario)
                                arquivos_leitura = buscar_permissoes("leitura", usuario)

                                try:
                                    leitura = int(input("\n===>>> "))

                                except ValueError:
                                    print("\nEntrada inválida. Apenas números são aceitos.")
                                    continue

                                if 1 <= leitura <= len(arquivos):
                                    nome_arquivo = arquivos_gerais[leitura - 1]

                                    if nome_arquivo not in arquivos_leitura:
                                        print("\nAcesso negado.")
                                        continue

                                    else:
                                        print(f"""
            Lendo o {nome_arquivo}...
                                    
            ==>>
                                    ,..........   ..........,         
                                ,..,'          '.'          ',..,     
                                ,' ,'            :            ', ',    
                                ,' ,'             :             ', ',   
                                ,' ,'              :              ', ',  
                                ,' ,'............., : ,.............', ', 
                                ,'  '............   '.'   ............'  ',
                                '''''''''''''''''';''';'''''''''''''''''' 
                                                    '''            
                                            
                                                """)
                                elif leitura == 0:
                                    print("\nVoltando...")

                                else:
                                    print("\nOpção inválida.")

                            elif opcao == 5:
                                _c, usuario = buscar_usuario_matriz(login)

                                escrita_permitida = buscar_permissoes("escrita", usuario)
                                arquivos = buscar_permissoes("geral", usuario)

                                print("\n Selecione o arquivo desejado: \n")
                                for arquivo in arquivos:
                                    print(f"[{arquivos.index(arquivo) + 1}] - {arquivo}")
                                    if arquivo in escrita_permitida:
                                        permitido = arquivo

                                print("\n[0] - Voltar")

                                try:
                                    leitura = int(input("===>>> "))

                                except ValueError:
                                    print("\nEntrada inválida. Apenas números são aceitos.")
                                    continue

                                if 1 <= leitura <= len(arquivos):
                                    if arquivos.index(permitido) + 1 == leitura:
                                        print("\nAcesso liberado.")
                                        escrita = str(input("\nDigite suas alterações desejadas: "))
                                        print("\nArquivo alterado.")

                                    else:
                                        print("\nAcesso negado.")

                                elif leitura == 0:
                                    print("\nVoltando...")

                                else:
                                    print("Opção inválida!")

                            elif opcao == 0:
                                print("\nVoltando à tela de autenticação e cadastro...")
                                autenticado = False
                                anonimo = True

                            else:
                                print("\nOpção inválida!")

                    else:
                        print("\nSenha incorreta!")

                else:
                    print("\nUsuário inexistente!")

            elif opcao == 2.0:
                #atualiza dados para o cadastro
                dados_json = registrar_usuario(dados_json)

            elif opcao == 0.0:
                print("\nAté mais! :( \n")
                break

            else:
                print("\nOpção inválida! Tente novamente.")
    except Exception as e:
        print(f"\nErro: {e}")

__init__()