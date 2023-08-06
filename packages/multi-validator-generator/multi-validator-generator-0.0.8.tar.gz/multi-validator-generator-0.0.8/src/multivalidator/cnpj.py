import re
import random


class CNPJ:
    """
    Esse módulo é responsável por gerar e validar CNPJs.

    ...

    Atributos
    ---------
    cnpjs : dict
        Dicionário com os CNPJs gerados ou validados.
    index : int
        Índice do dicionário de CNPJs.

    Métodos
    -------
    validate(cnpj)
        Valida um CNPJ.
    generate()
        Gera um CNPJ válido.
    add(cnpj)
        Adiciona um CNPJ ao dicionário de CNPJs.
    __repr__()
        Método que retorna a representação do objeto.
    __len__()
        Método que retorna o tamanho do dicionário de CNPJs.
    __getitem__(index)
        Método que retorna o CNPJ de acordo com o índice.
    __iter__()
        Método que retorna o iterador do dicionário de CNPJs.
    __next__()
        Método que retorna o próximo CNPJ do dicionário de CNPJs.
    """

    def __init__(self, cnpj=None):
        """
        Construtor da classe.

        Parâmetros
        ----------
            cnpj : str
                CNPJ a ser validado.

        Retorno
        -------
            None
        """
        if cnpj is None:
            self._cnpjs = {}
            self._index = 0
        else:
            try:
                request = self.validate(cnpj)
            except:
                raise ValueError("Formato inválido")
            self._cnpjs = {0: cnpj}
            self._index = 1
        self._next_index = 0
        if cnpj is None:
            self._cnpjs = {}
            self._index = 0
        else:
            try:
                request = self.validate(cnpj)
            except:
                raise ValueError("Formato inválido")
            self._cnpjs = {0: cnpj}
            self._index = 1
        self._next_index = 0

    @property
    def cnpjs(self):
        return self._cnpjs

    @cnpjs.setter
    def cnpjs(self, cnpj):
        try:
            cnpj = self.validate(cnpj)[1]
        except ValueError:
            raise ValueError("Formato inválido")
        else:
            self._cnpjs[self._index] = cnpj
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
        if len(self._cnpjs) > 1:
            return f"CNPJs: {list(map(lambda x: f'{x}', self.cnpjs.values()))}"
        if len(self.cnpjs) == 1:
            return f"CNPJ: {self.cnpjs[0]}"
        return f"CNPJs: {self.cnpjs}"

    def __len__(self):
        """
        Método que retorna o tamanho do dicionário de CNPJs.

        Parâmetros
        ----------
            None

        Retorno
        -------
            int
                Tamanho do dicionário de CNPJs.
        """
        return len(self.cnpjs)
        return len(self.cnpjs)

    def __getitem__(self, index):
        """
        Método que retorna o CNPJ de acordo com o índice.

        Parâmetros
        ----------
            index : int
                Índice do dicionário de CNPJs.

        Retorno
        -------
            str
                CNPJ de acordo com o índice.
        """
        if index >= len(self.cnpjs):
            raise IndexError
        return self.cnpjs[index]

    def __iter__(self):
        """
        Método que retorna o iterador do dicionário de CNPJs.

        Parâmetros
        ----------
            None

        Retorno
        -------
            iter
                Iterador do dicionário de CNPJs.
        """
        return self

    def __next__(self):
        """
        Método que retorna o próximo CNPJ do dicionário de CNPJs.

        Parâmetros
        ----------
            None

        Retorno
        -------
            str
                Próximo CNPJ do dicionário de CNPJs.
        """
        if self._next_index >= self._index:
            self._next_index = 0
            raise StopIteration
        self._next_index += 1
        return self.cnpjs[self._next_index - 1]

    def add(self, cnpj):
        """
        Adiciona um CNPJ ao dicionário de CNPJs.

        Parâmetros
        ----------
            cnpj : str
                CNPJ a ser adicionado.

        Retorno
        -------
            None
        """
        try:
            self.cnpjs = cnpj
        except ValueError:
            raise ValueError("Formato inválido")

    def generate(self):
        """
        Gera um CNPJ válido, de acordo com a formatação.

        Parâmetros
        ----------
            None

        Retorno
        -------
            str
                CNPJ válido.
        """

        def calculate_special_digit(l):
            digit = 0
            for i, v in enumerate(l):
                digit += v * (i % 8 + 2)
            digit = 11 - digit % 11
            return digit if digit < 10 else 0

        cnpj = [1, 0, 0, 0] + [random.randint(0, 9) for x in range(8)]
        for _ in range(2):
            cnpj = [calculate_special_digit(cnpj)] + cnpj
        cnpj = "%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s" % tuple(cnpj[::-1])
        self.cnpjs = cnpj
        return cnpj

    def validate(self, cnpj):
        """
        Valida um CNPJ.

        Parâmetros
        ----------
            cnpj : str
                CNPJ a ser validado.

        Retorno
        -------
            (bool, str)
                Tupla contendo o resultado da validação e o CNPJ formatado.
        """
        # Verifica a formatação do cnpj
        temp = list(map(lambda x: x if x.isdigit() else False, list(cnpj)))
        if all(temp):
            temp.insert(2, ".")
            temp.insert(6, ".")
            temp.insert(10, "/")
            temp.insert(15, "-")
            cnpj = "".join(list(map(lambda x: str(x), temp)))
            del temp

        if not re.match(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", cnpj):
            raise ValueError("Formato inválido")

        # Obtém apenas os números do cnpj, ignorando pontuações
        numbers = [int(digit) for digit in cnpj if digit.isdigit()]

        # Verifica se o cnpj possui 14 números ou se todos são iguais:
        if len(numbers) != 14 or len(set(numbers)) == 1:
            raise ValueError("Formato inválido")

        # Validação do primeiro dígito verificador:
        pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_of_products = sum(a * b for a, b in zip(numbers[0:12], pesos))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if expected_digit != numbers[12]:
            raise ValueError("Formato inválido")

        # Validação do segundo dígito verificador:
        pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_of_products = sum(a * b for a, b in zip(numbers[0:13], pesos))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if expected_digit != numbers[13]:
            raise ValueError("Formato inválido")

        return True, cnpj


def read(cnpj: str) -> CNPJ:
    """
    Lê um CNPJ.

            Parâmetros
                    cnpj (str): CNPJ a ser lido.

            Retorno
                    obj (CNPJ): Objeto CNPJ.
    """
    try:
        obj = CNPJ(cnpj)
        return obj
    except ValueError:
        raise ValueError("Formato inválido")
