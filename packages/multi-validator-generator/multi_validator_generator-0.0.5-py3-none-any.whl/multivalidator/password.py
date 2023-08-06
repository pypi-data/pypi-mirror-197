import random
import string
from collections.abc import Sequence


class PassWord(Sequence):
    """
    Classe que representa as senhas.

    Atributos
    ----------
    password: str
        Senha a ser validada, com ou sem o prefixo do Brasil, mas com o DDD.
    index: int
        Índice do dicionário de senhas.

    Métodos
    -------
    validate(password):
        Função que classifica uma senha passada pelo pelo usuário ou gerada e retorna True ou False.
    generate():
        Gera uma senha aleatória e retorna a mesma.
    add(password):
        Adiciona uma senha ao dicionário de senhas.
    __repr__():
        Método que retorna a representação do objeto.
    __len__():
        Método que retorna o tamanho do dicionário de senhas.
    __getitem__(index):
        Método que retorna a senha de acordo com o índice.
    __iter__():
        Método que retorna o iterador do dicionário de senhas.
    """

    def __init__(self, password=None):
        """
        Construtor da classe.

        Parâmetros
        ----------
            password: str
                Senha a ser validada, com ou sem o prefixo do Brasil, mas com o DDD.

        Retorno
        -------
            None
        """
        if password is None:
            self._passwords = {}
            self._index = 0
        else:
            try:
                request = self.validate(password)
            except:
                raise ValueError("Formato inválido")
            self._passwords = {0: request[1]}
            self._index = 1
        self._next_index = 0

    @property
    def passwords(self):
        return self._passwords

    @passwords.setter
    def passwords(self, args):
        try:
            password = self.validate(args)[1]
        except Exception as E:
            raise print(str(E))
        else:
            self._passwords[self._index] = password
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
        if len(self.passwords) > 1:
            return f"Passwords: {list(map(lambda x: f'{x}', self.passwords.values()))}"
        if len(self.passwords) == 1:
            return f"Password: {self.passwords[0]}"
        return f"Passwords: {self.passwords}"

    def __len__(self):
        """
        Método que retorna o tamanho do dicionário de senhas.

        Parametros
        ----------
            None

        Retorno
        -------
            int: Tamanho do dicionário de senhas.
        """
        return len(self.passwords)
        return len(self.passwords)

    def __getitem__(self, index):
        """
        Método que retorna a senha de acordo com o índice.

        Parametros
        ----------
            index: int
                Índice do dicionário de senhas.

        Retorno
        -------
            str: Senha de acordo com o índice.
        """
        if index >= len(self.passwords):
            raise IndexError
        return self.passwords[index]

    def __iter__(self):
        """
        Método que retorna o iterador do dicionário de senhas.

        Parametros
        ----------
            None

        Retorno
        -------
            iter: Iterador do dicionário de senhas.
        """
        return self

    def __next__(self):
        """
        Método que retorna a próxima senha do dicionário de senhas.

        Parametros
        ----------
            None

        Retorno
        -------
            str: Próxima senha do dicionário de senhas.
        """
        if self._next_index >= self._index:
            self._next_index = 0
            raise StopIteration
        self._next_index += 1
        return self.passwords[self._next_index - 1]

    def add(self, password):
        """
        Função que adiciona uma senha ao dicionário de senhas.

        Parâmetros
        ----------
            password: str
                Senha a ser adicionada ao dicionário de senhas.

        Retorno
        -------
            None
        """
        try:
            self.passwords = password
        except ValueError:
            raise ValueError("Formato inválido")

    def generate(self, level):
        """
        Função que gera uma senha aleatória e retorna a mesma.

        Parâmetros
        ----------
            level : int
                Nível de complexidade da senha.
                1 - Letras minúsculas e maiúsculas.
                2 - Letras minúsculas, maiúsculas e números.
                3 - Letras minúsculas, maiúsculas, números e símbolos.

        Retorno
            str: Senha aleatória.
        """

        letters = string.ascii_letters
        numbers = string.digits
        simbols = string.punctuation

        if level == 1:
            caracters = letters
            lenght = 6
        elif level == 2:
            caracters = letters + numbers
            lenght = 9
        elif level == 3:
            caracters = letters + numbers + simbols
            lenght = 12

        senha = "".join(random.choice(caracters) for i in range(lenght))
        self.add(senha)
        return senha

    def validate(self, password):
        """
        Função que valida uma senha e retorna uma mensagem de acordo com a complexidade da senha.

        Parâmetros
            password : str
                Senha a ser validada.

        Retorno
            tuple: Mensagem de acordo com a complexidade da senha e dicionário com a senha e a complexidade.
        """

        if len(password) < 6:
            return "A senha é muito curta. A senha deve ter pelo menos 6 caracteres."
        there_is_a_lower = False
        there_is_a_number = False
        there_is_a_upper = False
        there_is_a_simbol = False
        for c in password:
            if c.isupper():
                there_is_a_upper = True
            if c.islower():
                there_is_a_lower = True
            if c.isdigit():
                there_is_a_number = True
            if c in string.punctuation:
                there_is_a_simbol = True

        complexity = 0
        if there_is_a_upper:
            complexity += 1
        if there_is_a_lower:
            complexity += 1
        if there_is_a_number:
            complexity += 1
        if there_is_a_simbol:
            complexity += 1

        if complexity < 2:
            return (
                "A senha é muito fraca. A senha deve ter pelo menos 2 das seguintes características: letras maiúsculas, letras minúsculas, números ou símbolos.",
                {"password": password, "complexity": "fraca"},
            )
        elif complexity == 2:
            return (
                "A senha é moderada. A senha tem pelo menos 2 das seguintes características: letras maiúsculas, letras minúsculas, números ou símbolos.",
                {"password": password, "complexity": "moderada"},
            )
        elif complexity == 3:
            return (
                "A senha é forte. A senha tem pelo menos 3 das seguintes características: letras maiúsculas, letras minúsculas, números ou símbolos.",
                {"password": password, "complexity": "forte"},
            )
        else:
            return (
                "A senha é muito forte. A senha tem pelo menos 4 das seguintes características: letras maiúsculas, letras minúsculas, números ou símbolos.",
                {"password": password, "complexity": "muito forte"},
            )


def read(password: str) -> PassWord:
    """
    Função que lê uma senha e retorna um objeto do tipo PassWord.

            Parâmetros
                    password (str): Senha a ser lida.

            Retorno
                    obj: Objeto do tipo PassWord.
    """
    try:
        obj = PassWord(password)
        return obj
    except ValueError:
        raise ValueError("Formato inválido")
