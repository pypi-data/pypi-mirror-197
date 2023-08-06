import random
import string
from collections.abc import Sequence


class PassPort(Sequence):
    """
    Classe que representa um número de passaporte.

    Parâmetros
    ----------
    passport: str
        Número de passaporte a ser validado, com ou sem o prefixo do Brasil, mas com o DDD.
    index: int
        Índice do dicionário de números de passaporte.

    Métodos
    -------
    validate(passport):
        Função que valida um número de passaporte e retorna True ou False.
    generate():
        Gera um número de passaporte válido.
    add(passport):
        Adiciona um número de passaporte ao dicionário de números de passaporte.
    __repr__():
        Método que retorna a representação do objeto.
    __len__():
        Método que retorna o tamanho do dicionário de números de passaporte.
    __getitem__(index):
        Método que retorna o número de passaporte de acordo com o índice.
    __iter__():
        Método que retorna o iterador do dicionário de números de passaporte.
    """

    def __init__(self, passport=None):
        """
        Construtor da classe.

        Parâmetros
        ----------
            passport: str
                Número de passaporte a ser validado, com ou sem o prefixo do Brasil, mas com o DDD.

        Retorno
        -------
            None
        """
        if passport is None:
            self._passports = {}
            self._index = 0
        else:
            try:
                request = self.validate(passport)
            except:
                raise ValueError("Formato inválido")
            self._passports = {0: request[1]}
            self._index = 1
        self._next_index = 0

    @property
    def passports(self):
        return self._passports

    @passports.setter
    def passports(self, args):
        try:
            number = self.validate(args)[1]
        except Exception as E:
            print(str(E))
        else:
            self._passports[self._index] = number
            self._index += 1

    def __repr__(self):
        """
        Método que retorna a representação do objeto.

        Parametros
        ----------
            None

        Returns
        -------
            str: Representação do objeto.
        """
        if len(self.passports) > 1:
            return f"Passports: {list(map(lambda x: f'{x}', self.passports.values()))}"
        if len(self.passports) == 1:
            return f"Passport: {self.passports[0]}"
        return f"Passports: {self.passports}"

    def __len__(self):
        """
        Método que retorna o tamanho do dicionário de números de passaporte.

        Parametros
        ----------
            None

        Retorno
        -------
            int: Tamanho do dicionário de números de passaporte.
        """
        return len(self.passports)

    def __getitem__(self, index):
        """
        Método que retorna o número de passaporte de acordo com o índice.

        Parâmetros
        ----------
            index: int
                Índice do dicionário de números de passaporte.

        Retorno
        -------
            str: Número de passaporte.
        """
        if index >= len(self.passports):
            raise IndexError
        return self.passports[index]

    def __iter__(self):
        """
        Método que retorna o iterador do dicionário de números de passaporte.

        Parâmetros
        ----------
            None

        Retorno
        -------
            iter: Iterador do dicionário de números de passaporte.
        """
        return self

    def __next__(self):
        """
        Método que retorna o próximo número de passaporte do dicionário de números de passaporte.

        Parâmetros
        ----------
            None

        Retorno
        -------
            str: Próximo número de passaporte do dicionário de números de passaporte.
        """
        if self._next_index >= self._index:
            self._next_index = 0
            raise StopIteration
        self._next_index += 1
        return self.passports[self._next_index - 1]

    def add(self, passport):
        """
        Função que adiciona um passaporte ao dicionário de passaportes.

        Parâmetros
        ----------
            passaporte : str
                Passaporte a ser adicionado.

        Retorno
        -------
            None
        """
        try:
            self.passports = passport
        except Exception as E:
            print(str(E))

    def generate(self):
        """
        Função que gera um passaporte aleatório e retorna o mesmo.

        Parâmetros:
            None

        Retorno:
            str: Passaporte aleatório.
        """

        letras = "".join(random.choices(string.ascii_uppercase, k=2))
        numeros = "".join(random.choices(string.digits, k=7))
        self.add(letras + numeros)
        return letras + numeros

    def validate(self, passport):
        """
        Função que valida um passaporte e retorna True ou False.

        Parâmetros:
            passaporte : str
                Passaporte a ser validado.
        Retorno:
                tuple: Tupla contendo True ou False e o passaporte.
        """

        if len(passport) != 9:
            raise ValueError("Formato inválido!")
        letras = passport[:2]
        numeros = passport[2:]
        if not letras.isalpha() or not numeros.isdigit():
            raise ValueError("Formato inválido!")
        if numeros[0] == "0":
            raise ValueError("Formato inválido!")
        return True, passport


def read(passport: str) -> PassPort:
    """
    Função que lê um número de passaporte e retorna um objeto do tipo PassPort.

            Parâmetros
                    passport (str): Número de passaporte a ser validado.

            Retorno
                    PassPort: Objeto do tipo PassPort.
    """

    try:
        obj = PassPort(passport)
        return obj
    except ValueError:
        raise ValueError("Formato inválido")
