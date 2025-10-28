from typing import Dict, List
from pathlib import Path
from dataclasses import asdict, dataclass
from persistencia import load_json, save_json
from utils import next_id, UsuarioNaoEncontrado

@dataclass
class Usuario:
    id: int
    nome: str
    cpf: str

class GerenciadorUsuarios:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self._store: Dict[str, Dict] = load_json(self.storage_path, default={})

    def _persist(self) -> None:
        save_json(self.storage_path, self._store)

    def cadastrar_usuario(self, nome: str, cpf: str) -> Usuario:
        for v in self._store.values():
            if v["cpf"] == cpf:
                return Usuario(**v)
        new_id = next_id(self._store)
        usuario = Usuario(id=new_id, nome=nome, cpf=cpf)
        self._store[str(new_id)] = asdict(usuario)
        self._persist()
        return usuario

    def obter_por_cpf(self, cpf: str) -> Usuario:
        for v in self._store.values():
            if v["cpf"] == cpf:
                return Usuario(**v)
        raise UsuarioNaoEncontrado(f"Usuário com CPF {cpf} não encontrado.")

    def listar_usuarios(self) -> List[Usuario]:
        return [Usuario(**v) for v in self._store.values()]