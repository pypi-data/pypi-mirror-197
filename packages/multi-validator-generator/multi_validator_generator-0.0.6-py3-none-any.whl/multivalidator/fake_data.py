from collections.abc import Sequence

from multivalidator import bank_card
from multivalidator import cnpj
from multivalidator import cpf
from multivalidator import fone_number
from multivalidator import passport
from multivalidator import password

class FakeData(Sequence):
    """
    Classe que representa um conjunto de dados falsos gerados aleatoriamente.

    Atributos
    ----------
    quantity: int
        Quantidade de dados falsos a serem gerados.
    cpf: CPF
        Objeto da classe CPF.
    cnpj: CNPJ
        Objeto da classe CNPJ.
    bank_card: CreditCard
        Objeto da classe CreditCard.
    date: Date
        Objeto da classe Date.
    email: Email
        Objeto da classe Email.
    fone_number: TelPhone
        Objeto da classe TelPhone.
    passport: PassPort
        Objeto da classe PassPort.
    password: PassWord
        Objeto da classe PassWord.
    url: URL
        Objeto da classe URL.
    datas: dict
        Dicionário que armazena os dados falsos gerados.
    index: int
        Índice do dicionário de dados falsos.
    next_index: int
        Índice do próximo dado falso a ser retornado.

    Métodos
    -------
    datas:
        Retorna o dicionário de dados falsos.
    __repr__():
        Método que retorna a representação do objeto.
    __len__():
        Método que retorna o tamanho do dicionário de dados falsos.
    __getitem__(index):
        Método que retorna o dado falso de acordo com o índice.
    __iter__():
        Método que retorna o iterador do dicionário de dados falsos.
    __next__():
        Método que retorna o próximo dado falso.
    add(quantity):
        Adiciona dados falsos ao dicionário de dados falsos.
    """

    def __init__(self, quantity=1):
        """
        Construtor da classe FakeData.

        Parâmetros
        ----------
        quantity: int
            Quantidade de dados falsos a serem gerados.

        Retorno
        -------
            None
        """

        self._quantity = quantity
        self._cpf = cpf.CPF()
        self._cnpj = cnpj.CNPJ()
        self._bank_card = bank_card.CreditCard()
        self._fone_number = fone_number.TelPhone()
        self._passport = passport.PassPort()
        self._password = password.PassWord()
        self._datas = {}
        self._index = 0
        for i in range(quantity):
            self._datas[self._index] = {
                "cpf": self._cpf.generate(),
                "cnpj": self._cnpj.generate(),
                "bank_card": self._bank_card.generate(),
                "fone_number": self._fone_number.generate(),
                "passport": self._passport.generate(),
                "password": self._password.generate(3),
            }
            self._index += 1
        self._next_index = 0

    @property
    def datas(self):
        return self._datas

    def __repr__(self):
        """
        Método que retorna a representação do objeto.

        Parâmetros
        ----------
            None

        Retorno
        -------
            str
                Representação do objeto.
        """
        if len(self.datas) > 1:
            buffer = ""
            for i in self.datas.values():
                buffer += "\t" + str(i) + "\n"
            return f"""Fakes: {buffer}"""
        if len(self.datas) == 1:
            return f"Fake:\n{self.datas}"
        return f"Fakes: {self.datas}"

    def __len__(self):
        """
        Método que retorna o tamanho do dicionário de dados falsos.

        Parâmetros
        ----------
            None

        Retorno
        -------
            int
                Tamanho do dicionário de dados falsos.
        """
        return len(self.datas)

    def __getitem__(self, index):
        """
        Método que retorna o dado falso de acordo com o índice.

        Parâmetros
        ----------
        index: int
            Índice do dado falso.

        Retorno
        -------
            dict
                Dado falso.
        """
        if index >= len(self.datas):
            raise IndexError
        return self.datas[index]

    def __iter__(self):
        """
        Método que retorna o iterador do dicionário de dados falsos.

        Parâmetros
        ----------
            None

        Retorno
        -------
            iter
                Iterador do dicionário de dados falsos.
        """
        return self

    def __next__(self):
        """
        Método que retorna o próximo dado falso.

        Parâmetros
        ----------
            None

        Retorno
        -------
            dict
                Próximo dado falso.
        """
        if self._next_index >= self._index:
            self._next_index = 0
            raise StopIteration
        self._next_index += 1
        return self.datas[self._next_index - 1]

    def add(self, quantity=1):
        """
        Adiciona dados falsos ao dicionário de dados falsos.

        Parâmetros
        ----------
        quantity: int
            Quantidade de dados falsos a serem gerados.

        Retorno
        -------
            None
        """
        for i in range(quantity):
            self._datas[self._index] = {
                "cpf": self._cpf.generate(),
                "cnpj": self._cnpj.generate(),
                "bank_card": self._bank_card.generate(),
                "passport": self._passport.generate(),
                "password": self._password.generate(3),
            }
            self._index += 1
