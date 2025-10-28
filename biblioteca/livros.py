from typing import Dict, List
from pathlib import Path
from dataclasses import asdict, dataclass
from persistencia import load_json, save_json
from utils import next_id, LivroNaoEncontrado

@dataclass
class Livro:
    id: int
    titulo: str
    autor: str
    ano: int
    total_exemplares: int
    disponiveis: int

class GerenciadorLivros:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self._store: Dict[str, Dict] = load_json(self.storage_path, default={})

    def _persist(self) -> None:
        save_json(self.storage_path, self._store)

    def listar_livros(self) -> List[Livro]:
        return [self._dict_to_livro(v) for v in self._store.values()]

    def cadastrar_livro(self, titulo: str, autor: str, ano: int, exemplares: int) -> Livro:
        new_id = next_id(self._store)
        livro = Livro(id=new_id, titulo=titulo, autor=autor, ano=ano, total_exemplares=exemplares, disponiveis=exemplares)
        self._store[str(new_id)] = asdict(livro)
        self._persist()
        return livro

    def buscar_por_titulo(self, termo: str) -> List[Livro]:
        termo_lower = termo.lower()
        return [self._dict_to_livro(v) for v in self._store.values() if termo_lower in v["titulo"].lower()]

    def buscar_por_autor(self, autor: str) -> List[Livro]:
        autor_lower = autor.lower()
        return [self._dict_to_livro(v) for v in self._store.values() if autor_lower in v["autor"].lower()]

    def obter_livro(self, livro_id: int) -> Livro:
        key = str(livro_id)
        if key not in self._store:
            raise LivroNaoEncontrado(f"Livro com id {livro_id} não encontrado.")
        return self._dict_to_livro(self._store[key])

    def decrementar_disponiveis(self, livro_id: int) -> None:
        key = str(livro_id)
        if self._store[key]["disponiveis"] <= 0:
            raise ValueError("Sem exemplares disponíveis.")
        self._store[key]["disponiveis"] -= 1
        self._persist()

    def incrementar_disponiveis(self, livro_id: int) -> None:
        key = str(livro_id)
        if self._store[key]["disponiveis"] < self._store[key]["total_exemplares"]:
            self._store[key]["disponiveis"] += 1
            self._persist()

    @staticmethod
    def _dict_to_livro(d: Dict) -> Livro:
        return Livro(**d)