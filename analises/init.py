import pandas as pd
"""
Pacote de análises do projeto Dengue Letalidade.

Este módulo expõe as principais funções de análise
para facilitar importações externas.
"""

from .letalidade_sorotipos import (
    comparar_letalidade_por_tipo,
    SorotipoController
)

__all__ = [
    "comparar_letalidade_por_tipo",
    "SorotipoController"
]