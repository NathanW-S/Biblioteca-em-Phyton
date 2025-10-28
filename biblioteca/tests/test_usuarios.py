import pytest
from pathlib import Path
from usuarios import GerenciadorUsuarios
from utils import UsuarioNaoEncontrado

def test_cadastrar_e_obter_usuario(tmp_path: Path):
    p = tmp_path / "usuarios.json"
    gu = GerenciadorUsuarios(p)
    u1 = gu.cadastrar_usuario("Ana", "111")
    assert gu.obter_por_cpf("111").id == u1.id
    # Não duplica
    u2 = gu.cadastrar_usuario("Ana B", "111")
    assert u1.id == u2.id
    with pytest.raises(UsuarioNaoEncontrado):
        gu.obter_por_cpf("999")