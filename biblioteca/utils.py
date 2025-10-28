from typing import Dict, Any

class BibliotecaError(Exception):
    """Erro genérico do sistema da biblioteca."""

class LivroNaoEncontrado(BibliotecaError):
    """Livro não encontrado."""

class UsuarioNaoEncontrado(BibliotecaError):
    """Usuário não encontrado."""

class SemExemplaresDisponiveis(BibliotecaError):
    """Não há exemplares disponíveis para empréstimo."""

class EmprestimoNaoEncontrado(BibliotecaError):
    """Empréstimo não encontrado."""

def next_id(store: Dict[str, Any]) -> int:
    """Retorna um próximo ID inteiro simples para um dicionário."""
    if not store:
        return 1
    existing = [int(k) for k in store.keys()]
    return max(existing) + 1