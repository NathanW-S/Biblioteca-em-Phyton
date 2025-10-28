from pathlib import Path
from livros import GerenciadorLivros
from usuarios import GerenciadorUsuarios
from emprestimos import GerenciadorEmprestimos
import sys

DATA_DIR = Path("data")
PATH_LIVROS = DATA_DIR / "livros.json"
PATH_USUARIOS = DATA_DIR / "usuarios.json"
PATH_EMPRESTIMOS = DATA_DIR / "emprestimos.json"

def menu():
    ger_livros = GerenciadorLivros(PATH_LIVROS)
    ger_usuarios = GerenciadorUsuarios(PATH_USUARIOS)
    ger_emprestimos = GerenciadorEmprestimos(PATH_EMPRESTIMOS, ger_usuarios, ger_livros)

    while True:
        print("\n=== Biblioteca ===")
        print("1) Cadastrar livro")
        print("2) Cadastrar usuário")
        print("3) Realizar empréstimo")
        print("4) Devolver livro")
        print("5) Consultar livros (título/autor)")
        print("6) Listar empréstimos de usuário (por CPF)")
        print("7) Listar todos livros")
        print("0) Sair")
        escolha = input("Escolha: ").strip()
        try:
            if escolha == "1":
                titulo = input("Título: ").strip()
                autor = input("Primeiro autor: ").strip()
                ano = int(input("Ano: ").strip())
                exemplares = int(input("Nº exemplares: ").strip())
                livro = ger_livros.cadastrar_livro(titulo, autor, ano, exemplares)
                print(f"Livro cadastrado com id {livro.id}.")
            elif escolha == "2":
                nome = input("Nome: ").strip()
                cpf = input("CPF: ").strip()
                usuario = ger_usuarios.cadastrar_usuario(nome, cpf)
                print(f"Usuário cadastrado/confirmado: {usuario.nome} (id {usuario.id}).")
            elif escolha == "3":
                cpf = input("CPF do usuário: ").strip()
                livro_id = int(input("ID do livro: ").strip())
                emprestimo = ger_emprestimos.emprestar(cpf, livro_id)
                print(f"Empréstimo realizado. ID empréstimo: {emprestimo.id}")
            elif escolha == "4":
                emprestimo_id = int(input("ID do empréstimo: ").strip())
                ger_emprestimos.devolver(emprestimo_id)
                print("Devolução efetuada.")
            elif escolha == "5":
                termo = input("Buscar por (digite título ou autor): ").strip()
                resultados = ger_livros.buscar_por_titulo(termo) + ger_livros.buscar_por_autor(termo)
                if not resultados:
                    print("Nenhum livro encontrado.")
                else:
                    for l in resultados:
                        print(f"[{l.id}] {l.titulo} — {l.autor} ({l.ano}) | Disponíveis: {l.disponiveis}/{l.total_exemplares}")
            elif escolha == "6":
                cpf = input("CPF: ").strip()
                emprestimos = ger_emprestimos.listar_emprestimos_por_cpf(cpf)
                if not emprestimos:
                    print("Nenhum empréstimo ativo para esse usuário.")
                else:
                    for e in emprestimos:
                        print(f"ID Emprestimo: {e.id} | Livro ID: {e.livro_id} | Data: {e.data_emprestimo}")
            elif escolha == "7":
                for l in ger_livros.listar_livros():
                    print(f"[{l.id}] {l.titulo} — {l.autor} ({l.ano}) | Disponíveis: {l.disponiveis}/{l.total_exemplares}")
            elif escolha == "0":
                sys.exit(0)
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    menu()