import pytest
from pathlib import Path
from usuarios import GerenciadorUsuarios
from livros import GerenciadorLivros
from emprestimos import GerenciadorEmprestimos
from utils import SemExemplaresDisponiveis, UsuarioNaoEncontrado, LivroNaoEncontrado

def test_fluxo_emprestimo(tmp_path: Path):
    gu = GerenciadorUsuarios(tmp_path / "u.json")
    gl = GerenciadorLivros(tmp_path / "l.json")
    ge = GerenciadorEmprestimos(tmp_path / "e.json", gu, gl)

    u = gu.cadastrar_usuario("Carlos", "999")
    l = gl.cadastrar_livro("Algo", "Cormen", 2009, 1)

    emp = ge.emprestar(u.cpf, l.id)
    assert gl.obter_livro(l.id).disponiveis == 0
    
    with pytest.raises(SemExemplaresDisponiveis):
        ge.emprestar(u.cpf, l.id)

    ge.devolver(emp.id)
    assert gl.obter_livro(l.id).disponiveis == 1

    with pytest.raises(UsuarioNaoEncontrado):
        ge.emprestar("000", l.id)
    
    with pytest.raises(LivroNaoEncontrado):
        ge.emprestar(u.cpf, 999)