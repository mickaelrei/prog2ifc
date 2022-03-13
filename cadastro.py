# Pegar nome, e-mail e telefone do usuário

print("\n+==========================+")
print("|     Cadastro simples     |")
print("+==========================+\n")

nome = ""
while nome == "":
    nome = input("Digite seu nome: ")
    if nome == "":
        # Nome vazio
        print("Nome vazio; digite novamente.\n")

email = ""
while email == "":
    email = input("Digite seu e-mail: ")
    if email == "":
        print("Email vazio; digite novamente.\n")

telefone = ""
while telefone == "":
    telefone = input("Digite seu número de telefone: ")
    if telefone == "":
        print("Número vazio; digite novamente.\n")

print("\nCadastro concluído! Suas informações:")

print(f"・ Nome: {nome}")
print(f"・ E-mail: {email}")
print(f"・ Telefone: {telefone}\n")