from typing import Dict, List
from pathlib import Path
from dataclasses import asdict, dataclass
from datetime import datetime
from persistencia import load_json, save_json
from utils import next_id, EmprestimoNaoEncontrado, UsuarioNaoEncontrado, LivroNaoEncontrado, SemExemplaresDisponiveis
from usuarios import GerenciadorUsuarios
from livros import GerenciadorLivros

@dataclass
class Emprestimo:
    id: int
    usuario_id: int
    livro_id: int
    data_emprestimo: str

class GerenciadorEmprestimos:
    def __init__(self, storage_path: Path, ger_usuarios: GerenciadorUsuarios, ger_livros: GerenciadorLivros):
        self.storage_path = storage_path
        self._store: Dict[str, Dict] = load_json(self.storage_path, default={})
        self.ger_usuarios = ger_usuarios
        self.ger_livros = ger_livros

    def _persist(self) -> None:
        save_json(self.storage_path, self._store)

    def emprestar(self, cpf_usuario: str, livro_id: int) -> Emprestimo:
        usuario = self.ger_usuarios.obter_por_cpf(cpf_usuario)
        livro = self.ger_livros.obter_livro(livro_id)
        if livro.disponiveis <= 0:
            raise SemExemplaresDisponiveis("Não há exemplares disponíveis.")
        
        new_id = next_id(self._store)
        emprestimo = Emprestimo(id=new_id, usuario_id=usuario.id, livro_id=livro_id, data_emprestimo=datetime.utcnow().isoformat())
        self._store[str(new_id)] = asdict(emprestimo)
        self.ger_livros.decrementar_disponiveis(livro_id)
        self._persist()
        return emprestimo

    def devolver(self, emprestimo_id: int) -> None:
        key = str(emprestimo_id)
        if key not in self._store:
            raise EmprestimoNaoEncontrado(f"Empréstimo {emprestimo_id} não encontrado.")
        record = self._store.pop(key)
        self.ger_livros.incrementar_disponiveis(record["livro_id"])
        self._persist()

    def listar_emprestimos_por_cpf(self, cpf: str) -> List[Emprestimo]:
        usuario = self.ger_usuarios.obter_por_cpf(cpf)
        return [Emprestimo(**v) for v in self._store.values() if v["usuario_id"] == usuario.id]