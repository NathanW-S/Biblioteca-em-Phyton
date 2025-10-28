import pytest
from pathlib import Path
from livros import GerenciadorLivros
from utils import LivroNaoEncontrado

def test_cadastrar_buscar_livro(tmp_path: Path):
    p = tmp_path / "livros.json"
    gl = GerenciadorLivros(p)
    l1 = gl.cadastrar_livro("Python 101", "Guido", 2010, 3)
    assert gl.obter_livro(l1.id).titulo == "Python 101"
    assert len(gl.buscar_por_titulo("python")) == 1
    assert len(gl.buscar_por_autor("Guido")) == 1
    with pytest.raises(LivroNaoEncontrado):
        gl.obter_livro(999)