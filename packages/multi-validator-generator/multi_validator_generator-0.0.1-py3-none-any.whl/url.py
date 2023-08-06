import random
import re
import string
from collections.abc import Sequence


class URL(Sequence):
    """
    Classe que representa as urls passadas pelo usúario ou geradas pela própria
    classe.

    Atributos
    ----------
    url: str
        url a ser validada.
    index: int
        Índice do dicionário de urls.

    Métodos
    -------
    validate(url):
        Valida uma url.
    generate(name, random_lenght):
        Gera uma url aleatória.
    add(url):
        Adiciona uma url ao dicionário de urls.
    __repr__():
        Método que retorna a representação do objeto.
    __len__():
        Método que retorna o tamanho do dicionário de números de telefone.
    __getitem__(index):
        Método que retorna o número de telefone de acordo com o índice.
    __iter__():
        Método que retorna o iterador do dicionário de números de telefone.
    """

    def __init__(self, url=None):
        """
        Construtor da classe.

        Parâmetros
        ----------
        url: str
            url a ser validada.

        Retorno
        -------
            None
        """
        if url is None:
            self._urls = {}
            self._index = 0
        else:
            try:
                request = self.validate(url)
            except:
                raise ValueError("Formato inválido")
            self._urls = {0: request[1]}
            self._index = 1
        self._next_index = 0

    @property
    def urls(self):
        return self._urls

    @urls.setter
    def urls(self, args):
        try:
            url = self.validate(args)[1]
        except ValueError:
            raise ValueError("Formato inválido")
        else:
            self._urls[self._index] = url
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
        if len(self.urls) > 1:
            return f"URLs: {list(map(lambda x: f'{x}', self.urls.values()))}"
        if len(self.urls) == 1:
            return f"URL: {self.urls[0]}"
        return f"URLs: {self.urls}"

    def __len__(self):
        """
        Método que retorna o tamanho do dicionário de urls.

        Parametros
        ----------
            None

        Returns
        -------
            int: Tamanho do dicionário de urls.
        """
        return len(self.urls)

    def __getitem__(self, index):
        """
        Método que retorna a url de acordo com o índice.

        Parametros
        ----------
        index: int
            Índice do dicionário de urls.

        Returns
        -------
            str: url.
        """
        if index >= len(self.urls):
            raise IndexError
        return self.urls[index]

    def __iter__(self):
        """
        Retorna o iterador do dicionário de urls.

        Parametros
        ----------
            None

        Returns
        -------
            self: Iterador do dicionário de urls.
        """
        return self

    def __next__(self):
        """
        Retorna a próxima url do dicionário de urls.

        Parametros
        ----------
            None

        Returns
        -------
            str: Próxima url do dicionário de números de telefone.
        """
        if self._next_index >= self._index:
            self._next_index = 0
            raise StopIteration
        self._next_index += 1
        return self.urls[self._next_index - 1]

    def add(self, url):
        """
        Função que adiciona uma url ao dicionário de urls.

        Parâmetros
        ----------
            url : str
                URL a ser adicionada.

        Retorno
        -------
            None
        """
        try:
            self.urls = url
        except ValueError:
            raise ValueError("Formato inválido")

    def generate(self, name, random_lenght=0):
        """
        Função que gera uma URL aleatória e retorna a mesma.

        Parâmetros
        ----------
            name : str
                Nome da URL.
            random_lenght : int
                Comprimento da parte aleatória da URL.

        Retorno
        -------
            str: URL aleatória.
        """

        caracteres = string.ascii_lowercase + string.digits
        parte_aleatoria = "".join(
            random.choice(caracteres) for i in range(random_lenght)
        )
        self.add(f"http://www.{name}.com/{parte_aleatoria}")
        return f"http://www.{name}.com/{parte_aleatoria}"

    def validate(self, url):
        """
        Função que valida uma URL e retorna True ou False.

        Parâmetros
        ----------
            url : str
                URL a ser validada.

        Retorno
        -------
            tuple: (True, url)
                Retorna True e a URL caso a mesma seja válida.
        """
        padrao = re.compile(r"^https?://(www\.)?\w+\.\w{2,3}(/\S*)?$")
        if padrao.match(url):
            return True, url
        else:
            raise ValueError("Formato inválido")


def read(url: str) -> URL:
    """
    Função que lê uma URL e retorna a mesma.

            Parâmetros:
                    url (str): URL a ser lida.
            
            Retorno:
                    obj (URL): Objeto da classe URL.
    """
    try:
        obj = URL(url)
        return obj
    except ValueError:
        raise ValueError("Formato inválido")
