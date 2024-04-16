# Laura da Costa dos Santos
import bcrypt
import os
import getpass

acao_usuario = ""
nome_arquivo = ""
hash_password = None
username = None


def opcao_cadastrar():
    print("CRIANDO USUÁRIO")
    username = input("Digite o nome do seu usuario:")
    password = getpass.getpass("Digite a senha").encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password, salt)
    with open("credenciais.txt", "a") as arquivo:
        arquivo.write(f"{username},{hash_password}\n")
    p1 = "0"
    p2 = "0"
    p3 = "0"
    with open("permissoes.txt", "a") as arquivo_permissoes:
        arquivo_permissoes.write(f"{username},{p1},{p2},{p3}\n")
    print("Cadastro feito com sucesso!")
    return hash_password, username, p1, p2, p3


def opcao_login(username_fornecido, senha_fornecida, hash_password):
    print("AUTENTICANDO USUÁRIO")
    username_fornecido = input("digite o nome:")
    senha_fornecida = getpass.getpass("Informe sua senha")
    with open("credenciais.txt", "r") as arquivo:
        usuarios = arquivo.readlines()
        usuarios_registrados = False

        for linha in usuarios:
            dados = linha.strip().split(",")
            if username_fornecido == dados[0] and bcrypt.checkpw(senha_fornecida, dados[1].encode('utf-8')):
                usuario_registrado = True
                print("Autenticação feita com sucesso!")
                break
            else:
                print("Usuário ou senha incorretos.")

def listar_opcoes():
    print("Comandos disponiveis:\n1- Listar Arquivo\n2- Criar arquivo\n3- Ler Arquivo\n4- Excluir arquivo\n5- Executar arquivo\n6- Sair")
    acao_usuario = int(input("Digite qual ação você deseja realizar:"))
    print("="*30)
    if acao_usuario == 1:
        diretorios_filhos = os.listdir()
        print("Arquivos no diretório")
        for diretorio in diretorios_filhos:
            print(diretorio)
    elif acao_usuario == 2:
        nome_arquivo = input("Digite o nome do arquivo com tipo:")
        with open(nome_arquivo, 'w') as arquivo:
            pass
        print("novo arquivo criado com sucesso!")
    elif acao_usuario == 3:
        nome_arquivo = input("Digite o nome do arquivo para ser lido:")
        with open(nome_arquivo, 'r') as arquivo_para_ler:
            conteudo = arquivo_para_ler.read()
            print("Conteúdo:")
            print(conteudo)
    elif acao_usuario == 4:
        nome_arquivo = input("Digite o nome do arquivo para ser excluido:")
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)
            print(f"O arquivo '{nome_arquivo}' foi excluído com sucesso.")
        else:
            print(f"O arquivo '{nome_arquivo}' não existe.")
    elif acao_usuario == 5:
        nome_arquivo = input("Digite o nome do arquivo que você deseja executar: ")
        if os.path.exists(nome_arquivo):
            os.system(nome_arquivo)
            print(f"O arquivo '{nome_arquivo}' foi executado.")
        else:
            print(f"O arquivo '{nome_arquivo}' não existe.")
    else:
        print("Tchau")


while True:
    acao_usuario = int(
        input("Digite 1 para cadastrar, 2 para logar ou 0 para sair:"))
    if acao_usuario == 1:
        hash_password, username, p1, p2, p3 = opcao_cadastrar()
    elif acao_usuario == 2:
        if hash_password is not None and username is not None:
            username_fornecido = input("Digite o nome do usuario:")
            senha_fornecida = getpass.getpass("Digite a senha:")
            print(f"Usuário {username_fornecido} cadastrado com sucesso!")
            listar_opcoes()
        else:
            print("Nenhum usuário cadastrado.")
    elif acao_usuario == 0:
        print("Tchau")
        break
