# Código feito por Laura da Costa dos Santos
#Sistemas de informação | 2024 | 3 período
import bcrypt
import os
import getpass

acao_usuario = ""
nome_arquivo = ""
hash_password = None
username = None

per1= 0
per2= 0
per3= 0

def opcao_cadastrar():
    print("───── ⋆  ⋆ ─────")
    print("CRIANDO USUÁRIO")
    username = input("Digite o nome do seu usuario:")
    password = getpass.getpass("Digite a senha").encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password, salt)
    with open("credenciais.txt", "a") as arquivo:
        arquivo.write(f"{username},{hash_password}\n")
    with open("permissoes.txt", "a") as arquivo_permissoes:
        arquivo_permissoes.write(f"{username},{per1},{per2},{per3}\n")
    print("Cadastro feito com sucesso!")
    return hash_password, username, per1, per2, per3

def opcao_login(username_fornecido, senha_fornecida):
    print("───── ⋆  ⋆ ─────")
    print("AUTENTICANDO USUÁRIO")
    autenticacao_sucesso = False

    if isinstance(senha_fornecida, str):
        senha_fornecida_bytes = senha_fornecida.encode('utf-8')
    else:
        senha_fornecida_bytes = senha_fornecida
    
    try:
        with open("credenciais.txt", "r") as arquivo:
            usuarios = arquivo.readlines()
        
        for linha in usuarios:
            dados = linha.strip().split(",")
            if len(dados) == 2 and username_fornecido == dados[0]:
                hash_senha_armazenada = dados[1]

                hash_senha_armazenada_byte = hash_senha_armazenada.encode('utf-8')
                
                if not hash_senha_armazenada.startswith('$2b$'):
                    if senha_fornecida == senha_fornecida_bytes:
                        autenticacao_sucesso = True
                        print("Autenticação feita com sucesso!")
                    else:
                        return ("diferentes")
                    # print(senha_fornecida_bytes,senha_fornecida)

    except FileNotFoundError:
        print("Arquivo credenciais.txt não encontrado.")
    return autenticacao_sucesso

def listar_opcoes():
    print("="*30)
    print("Comandos disponiveis:\n1- Listar Arquivo\n2- Criar arquivo\n3- Ler Arquivo\n4- Excluir arquivo\n5- Sair")
    print("───〃★")
    acao_usuario = int(input("Digite qual ação você deseja realizar:"))
    if acao_usuario == 1:
        diretorios_filhos = os.listdir()
        print("Arquivos no diretório")
        for diretorio in diretorios_filhos:
            print(diretorio)
    elif acao_usuario == 2:
        nome_arquivo = input("Digite o nome do arquivo com tipo:")
        validacao = False
        with open ('permissoes.txt','r') as permissoes1:
            linhas = permissoes1.readlines()
            for linha in linhas:
                acesso = linha.strip().split(",")
                if acesso[2] == '1':
                    validacao = True
                    break
        if validacao:
            with open(nome_arquivo, 'w') as arquivo:
                print(f"{nome_arquivo} criado com sucesso!")
        else:
            print(f"Sem autorização para criar {nome_arquivo}")
    elif acao_usuario == 3:
        nome_arquivo = input("Digite o nome do arquivo para ser lido:")
        validacao = False
        if os.path.exists(nome_arquivo):
            with open ('permissoes.txt', 'r') as permissoes2:
                linhas = permissoes2.readlines()
                for linha in linhas:
                    acesso = linha.strip().split(",")
                    if acesso[1] == '1':
                        validacao = True
                        break
            if validacao:
                with open(nome_arquivo, 'r') as arquivo_para_ler:
                    conteudo = arquivo_para_ler.read()
                    print("="*30)
                    print("Conteúdo do arquivo:")
                    print(conteudo)
                    print("="*30)
            else:
                print(f"Sem permissão para ler o arquivo {nome_arquivo}")
        else:
            print("arquivo não existe")      

    elif acao_usuario == 4:
        nome_arquivo = input("Digite o nome do arquivo para ser excluido:")
        if os.path.exists(nome_arquivo):
            with open ('permissoes.txt','r') as permissoes:
                linhas = permissoes.readlines()
                validacao = False
                for linha in linhas:
                    acesso = linha.strip().split(",")
                    if acesso[3] == '1':
                        validacao=True
                        os.remove(nome_arquivo)
                        print(f"O arquivo '{nome_arquivo}' foi excluído com sucesso!")
                        break
                if validacao == False:
                    print(f"Sem autorização para excluir {nome_arquivo}")
        else:
            print(f"O arquivo '{nome_arquivo}' não existe.")
    else:
        print("Tchau")

while True:
    acao_usuario = int(
        input("Digite 1 para cadastrar 2 para logar 0 para sair:"))
    if acao_usuario == 1:
        hash_password, username, per1, per2, per3 = opcao_cadastrar()

    elif acao_usuario == 2:
        if hash_password is not None and username is not None:
            username_fornecido = input("Digite o nome do usuario:")
            senha_fornecida = getpass.getpass("Digite a senha:").encode('utf-8')
            autenticado = opcao_login(username_fornecido, senha_fornecida)

            if autenticado:
                print(f"Usuário {username_fornecido} autenticado com sucesso!")
                listar_opcoes()
            else:
                print("Falha na autenticação.")
        else:
            print("Faça ao menos 1 cadastro")
            
    elif acao_usuario == 0:
        print("Até mais !")
        break
    else:
        print("Selecione apenas opções válidas!")
