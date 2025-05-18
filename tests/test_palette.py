import re
import pytest
from palette import extrair_cores


def test_extrair_cores_returns_hex_strings():
    cores = extrair_cores('1.PNG', n_cores=3)
    assert len(cores) == 3
    for cor in cores:
        assert re.match(r'^#[0-9a-fA-F]{6}$', cor)


def test_imagem_inexistente():
    with pytest.raises(FileNotFoundError):
        extrair_cores('imagem_inexistente.png')


@pytest.mark.parametrize('valor', [0, -1, 2.5])
def test_n_cores_invalido(valor):
    with pytest.raises(ValueError):
        extrair_cores('1.PNG', n_cores=valor)
