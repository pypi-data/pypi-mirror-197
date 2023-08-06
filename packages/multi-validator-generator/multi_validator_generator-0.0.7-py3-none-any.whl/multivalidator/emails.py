import re
import random
from collections.abc import Sequence


class Email(Sequence):
    """
    Classe que representa um email.

    ...

    Atributos
    ---------
    emails: dict
        Dicionário que armazena os emails.
    index: int
        Índice do dicionário de emails.

    Métodos
    -------
    validate(email):
        Função que valida um email e retorna True ou False.
    generate():
        Gera um email válido.
    add(email):
        Adiciona um email ao dicionário de emails.
    __repr__():
        Método que retorna a representação do objeto.
    __len__():
        Método que retorna o tamanho do dicionário de emails.
    __getitem__(index):
        Método que retorna o email de acordo com o índice.
    __iter__():
        Método que retorna o iterador do dicionário de emails.
    __next__():
        Método que retorna o próximo email do dicionário de emails.
    """

    def __init__(self, email=None):
        """
        Construtor da classe.

        Parâmetros
        ----------
            email: str
                Email a ser validado.

        Retorno
        -------
            None
        """
        if email is None:
            self._emails = {}
            self._index = 0
        else:
            try:
                request = self.validate(email)
            except:
                raise ValueError("Formato inválido")
            self._emails = {0: request[1]}
            self._index = 1
        self._next_index = 0

    @property
    def emails(self):
        return self._emails

    @emails.setter
    def emails(self, args):
        try:
            email = self.validate(args)[1]
        except ValueError:
            raise ValueError("Formato inválido")
        else:
            self._emails[self._index] = email
            self._index += 1

    def __repr__(self):
        """
        Método que retorna a representação do objeto.

        Parâmetros
        ----------
            None

        Retorno
        -------
            str: Representação do objeto.
        """
        if len(self._emails) > 1:
            return f"Emails: {list(map(lambda x: f'{x}', self.emails.values()))}"
        if len(self.emails) == 1:
            return f"Email: {self._emails[0]}"
        return f"Emails: {self._emails}"

    def __len__(self):
        """
        Método que retorna o tamanho do dicionário de emails.

        Parâmetros
        ----------
            None

        Retorno
        -------
            int: Tamanho do dicionário de emails.
        """
        return len(self._emails)

    def __getitem__(self, index):
        """
        Método que retorna o email de acordo com o índice.

        Parâmetros
        ----------
            index: int
                Índice do dicionário de emails.

        Retorno
        -------
            str: Email de acordo com o índice.
        """
        if index >= len(self._emails):
            raise IndexError
        return self._emails[index]

    def __iter__(self):
        """
        Método que retorna o iterador do dicionário de emails.

        Parâmetros
        ----------
            None

        Retorno
        -------
            iter: Iterador do dicionário de emails.
        """
        return self
        return self

    def __next__(self):
        """
        Método que retorna o próximo email do dicionário de emails.

        Parâmetros
        ----------
            None

        Retorno
        -------
            str: Próximo email do dicionário de emails.
        """
        if self._next_index >= self._index:
            self._next_index = 0
            raise StopIteration
        self._next_index += 1
        return self._emails[self._next_index - 1]

    def add(self, email):
        """
        Função que adiciona um email ao dicionário de emails.

        Parâmetros
        ----------
            email: str
                Email a ser adicionado.

        Retorno
        -------
            None
        """
        try:
            self.emails = email
        except ValueError:
            raise ValueError("Formato inválido")

    def generate(self, first_name, last_name):
        """
        Função que gera um email aleatório e retorna o mesmo.

        Parâmetros
            first_name : str
                Nome do usuário.
            last_name : str
                Sobrenome do usuário.

        Retorno:
            str: Email aleatório.
        """

        numeros_aleatorios = "".join([str(random.randint(0, 9)) for _ in range(4)])
        email = (
            first_name.lower()
            + "."
            + last_name.lower()
            + numeros_aleatorios
            + "@gmail.com"
        )
        self.add(email)
        return email

    def validate(self, email):
        """
        Função que valida um email e retorna True ou False.

        Parâmetros
        ----------
            email: str
                Email a ser validado.

        Retorno
        -------
            bool: True ou False.
        """
        # Verificação básica
        if "@" not in email or "." not in email.split("@")[1]:
            return False, email

        # Verificação de sintaxe
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return False, email

        return True, email
        # Verificação básica
        if "@" not in email or "." not in email.split("@")[1]:
            raise ValueError("Formato inválido")

        # Verificação de sintaxe
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise ValueError("Formato inválido")

        return True, email


def read(email: str) -> Email:
    """
    Função que lê um email e retorna o mesmo.

            Parâmetros
                    email (str): Email a ser lido.

            Retorno:
                    Email: Email lido.
    """
    try:
        obj = Email(email)
        return obj
    except ValueError:
        raise ValueError("Formato inválido")
