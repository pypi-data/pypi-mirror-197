from datetime import datetime
from collections.abc import Sequence


class Date(Sequence):
    """
    Classe que representa uma data.

    ...

    Atributos
    ---------
    datas: dict
        Dicionário que armazena as datas.
    index: int
        Índice do dicionário de datas.
    next_index: int
        Índice do próximo elemento do dicionário de datas.

    Métodos
    -------
    validate(date):
        Função que valida uma data e retorna True ou False.
    generate():
        Gera uma data válida.
    add(date):
        Adiciona uma data ao dicionário de datas.
    __repr__():
        Método que retorna a representação do objeto.
    __len__():
        Método que retorna o tamanho do dicionário de datas.
    __getitem__(index):
        Método que retorna a data de acordo com o índice.
    __iter__():
        Método que retorna o iterador do dicionário de datas.
    __next__():
        Método que retorna a próxima data do dicionário de datas.
    """

    def __init__(self, date=None):
        """
        Construtor da classe.

        Parâmetros
        ----------
            date: str
                Data a ser validada.

        Retorno
        -------
            None
        """
        if date is None:
            self._datas = {}
            self._index = 0
        else:
            try:
                request = self.validate(date)
            except:
                raise ValueError("Formato inválido")
            self._datas = {0: request[1]}
            self._index = 1
        self._next_index = 0

    @property
    def datas(self):
        return self._datas

    @datas.setter
    def datas(self, args):
        try:
            date = self.validate(args)[1]
        except ValueError:
            raise ValueError("Formato inválido")
        else:
            self._datas[self._index] = date
            self._index += 1

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
        if len(self._datas) > 1:
            return f"Datas: {list(map(lambda x: f'{x}', self.datas.values()))}"
        if len(self.datas) == 1:
            return f"Data: {self._datas[0]}"
        return f"Datas: {self._datas}"

    def __len__(self):
        """
        Método que retorna o tamanho do dicionário de datas.

        Parâmetros
        ----------
            None

        Retorno
        -------
            int
                Tamanho do dicionário de datas.
        """
        return len(self._datas)

    def __getitem__(self, index):
        """
        Método que retorna a data de acordo com o índice.

        Parâmetros
        ----------
            index: int
                Índice do dicionário de datas.

        Retorno
        -------
            str
                Data de acordo com o índice.
        """
        if index >= len(self._datas):
            raise IndexError
        return self._datas[index]

    def __iter__(self):
        """
        Método que retorna o iterador do dicionário de datas.

        Parâmetros
        ----------
            None

        Retorno
        -------
            iter
                Iterador do dicionário de datas.
        """
        return self

    def __next__(self):
        """
        Método que retorna a próxima data do dicionário de datas.

        Parâmetros
        ----------
            None

        Retorno
        -------
            str
                Próxima data do dicionário de datas.
        """
        if self._next_index >= self._index:
            self._next_index = 0
            raise StopIteration
        self._next_index += 1
        return self._datas[self._next_index - 1]

    def add(self, date):
        """
        Adiciona uma data ao dicionário de datas.

        Parâmetros
        ----------
            date: str
                Data a ser adicionada.

        Retorno
        -------
            None
        """
        try:
            self.datas = date
        except ValueError:
            raise ValueError("Formato inválido")

    def validate(self, date):
        """
        Função que valida uma data e retorna True ou False.

        Parâmetros
        ----------
            date: str
                Data a ser validada.

        Retorno
        -------
            bool
                True se a data for válida, False se a data for inválida.
        """
        try:
            # Converte a string em um objeto datetime
            datetime.strptime(date, "%d/%m/%Y")
            return True, date
        except Exception as E:
            try:
                datetime.strptime(date, "%d-%m-%Y")
                return True, date
            except Exception as E:
                try:
                    datetime.strptime(date, "%d %m %y")
                    return True, date
                except Exception as E:
                    raise ValueError("Formato inválido")


def read(date: str) -> Date:
    """
    Função que lê uma data e retorna um objeto Date.

            Parâmetros
                    date (str): Data a ser lida.

            Retorno
                    Date: Objeto Date.
    """
    try:
        obj = Date(date)
        return obj
    except ValueError:
        raise ValueError("Formato inválido")
