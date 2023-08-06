import random
import re


class CreditCard:
    """
    Classe que representa os números de cartão.

    Parâmetros
    ----------
    card_number: str
        Número de cartão a ser validado, com ou sem o prefixo do Brasil, mas com o DDD.
    index: int
        Índice do dicionário de números de cartão.

    Métodos
    -------
    validate(card_number):
        Função que valida um número de cartão e retorna True ou False.
    generate():
        Gera um número de cartão válido.
    add(card_number):
        Adiciona um número de cartão ao dicionário de números de cartão.
    __repr__():
        Método que retorna a representação do objeto.
    __len__():
        Método que retorna o tamanho do dicionário de números de cartão.
    __getitem__(index):
        Método que retorna o número de cartão de acordo com o índice.
    __iter__():
        Método que retorna o iterador do dicionário de números de cartão.
    """
    def __init__(self, card_number = None):
        """
        Construtor da classe.

        Parâmetros
        ----------
            card_number: str
                Número de cartão a ser validado.

        Returns
        -------
            None
        """
        if card_number is None:
            self._cards = {}
            self._index = 0
        else:
            try:
                request = self.validate(card_number)
            except:
                raise ValueError("Formato inválido")
            else:
                self._cards = {0: {"type":request[1][0], "number": request[1][1]}}
                self._index = 1
        
        self._next_index = 0
    
    @property
    def cards(self):
        return self._cards
    
    @cards.setter
    def cards(self, card_number):
        try:
            card_number = self.validate(card_number)[1]
        except ValueError:
            raise ValueError("Formato inválido")
        else:
            self._cards[self._index] = card_number
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
        if len(self._cards) > 1:
            return f"Cards: {list(map(lambda x: f'{x}', self.cards.values()))}"
        if len(self.cards) == 1:
            return f"Cards: {self.cards[0]}"
        return f"Cards: {self.cards}"
    
    def __len__(self):
        """
        Método que retorna o tamanho do dicionário de cartões de crédito.

        Parametros
        ----------
            None

        Returns
        -------
            int: Tamanho do dicionário de cartões de crédito.
        """
        return len(self.cards)
    
    def __getitem__(self, index):
        """
        Método que retorna o número de cartão de acordo com o índice.

        Parametros
        ----------
            index: int
                Índice do dicionário de números de cartões de crédito.

        Returns
        -------
            str: Número de cartão.
        """
        if index >= len(self.cards):
            raise IndexError
        return self.cards[index]
    
    def __iter__(self):
        """
        Retorna o iterador do dicionário de cartões de crédito.

        Parametros
        ----------
            None

        Returns
        -------
            self: Iterador do dicionário de cartões de crédito.
        """
        return self
    
    def __next__(self):
        """
        Retorna o próximo número do cartão do dicionário de cartões.

        Parametros
        ----------
            None

        Returns
        -------
            str: Próximo número do cartão do dicionário de números de cartão.
        """
        if self._next_index >= self._index:
            self._next_index = 0
            raise StopIteration
        self._next_index += 1
        return self.cards[self._next_index - 1]
    
    def add(self, card_number):
        """
        Adiciona um número de cartão ao dicionário de números de cartão.

        Parâmetros
        ----------
            numero : str
                Número de cartão a ser validado, com ou sem o prefixo do Brasil, mas com o DDD.

        Retorno
        -------
            None
        """
        try:
            self.cards = card_number
        except ValueError:
            raise ValueError("Formato inválido")
    
    def generate(self):
        """
        Função que gera um número de cartão.

        Parâmetros
        ----------
            None

        Retorno
        -------
            str: Número de cartão gerado.
        """
        def search_combination():
            """
            Função busca por uma combinação de números que resulte em um número de cartão válido.

            Parâmetros
            ----------
                None

            Retorno
            -------
                tuple: Tupla contendo uma lista de números operados e uma lista de números fixos.
            """
            fixos = [random.randint(0, 9) for _ in range(8)]
            while True:
                operados = [(random.randint(0, 9)) for _ in range(8)]
                number = [num * 2 for idx, num in enumerate(operados)]
                number = [num - 9 if num > 9 else num for idx, num in enumerate(number)]
                if (sum(number) + sum(fixos)) % 10 == 0:
                    break
            return operados, fixos
        
        operados, fixos = search_combination()
        new_number = []
        for i in range(0,16):
            if i % 2 != 0:
                new_number.append(str(fixos[0]))
                fixos.pop(0)
            else:
                new_number.append(str(operados[0]))
                operados.pop(0)
        new_number = "".join(new_number)                           
        try:
            self.validate(new_number)
        except Exception as E:
            print(E)
        else:
            self.cards = new_number
        return new_number
    
    def validate(self, card_number):
        """
        Função que valida um número de cartão.
            
        Parâmetros
        ----------
            card_number : str
                Número de cartão a ser validado.

        Retorno
        -------
            tuple: (True, card_number)        
        """
        def card_tag(number: str):
            """
            Função que identifica o tipo de cartão de crédito.

            Parâmetros
            ----------
                number : str
                
            Retorno
            -------
                str: Tipo de cartão de crédito.
            """
            if number[0] == "4":
                return "Visa"
            elif number[:2] in ["51", "52", "53", "54", "55"]:
                return "MasterCard"
            elif number[:2] in ["34", "37"]:
                return "American Express"
            elif number[:4] == "6011" or number[:2] in ["65", "64"]:
                return "Discover"
            elif number[:2] == "35":
                return "JCB"
            else: return "Other"

        """This function validates a credit card number."""
        temp = list(map(lambda x: x.isdigit(), card_number))
        if not all(temp):
            raise ValueError("Formato inválido")
        temp = list(filter(lambda x: x.isdigit(), card_number))
        # 1. Change datatype to list[int]
        card_type = card_tag(card_number)
        card_number = [int(num) for num in card_number if num.isdigit()]
        
        # 2. Remove the last digit:
        checkDigit = card_number.pop()
        # 3. Reverse the remaining digits:
        card_number.reverse()
        # 4. Double digits at even indices
        card_number = [num * 2 if idx % 2 == 0 \
                    else num for idx, num in enumerate(card_number)]

        # 5. Subtract 9 at even indices if digit is over 9
        # (or you can add the digits)
        card_number = [num - 9 if idx % 2 == 0 and num > 9
                    else num for idx, num in enumerate(card_number)]

        # 6. Add the checkDigit back to the list:
        card_number.append(checkDigit)
        # 7. Sum all digits:
        checkSum = sum(card_number)
        if checkSum % 10 != 0:
            raise ValueError("Formato inválido")
        temp = "".join(temp)
        # 8. If checkSum is divisible by 10, it is valid.
        return checkSum % 10 == 0, (card_type, temp)

def read(card_number : str) -> CreditCard:
    """
    Método que lê um número de cartão de crédito e retorna um objeto da classe CreditCard.

            Parâmetros
                    card_number (str): Número de cartão a ser validado.

            Retorno
                    (CreditCard): Objeto da classe CreditCard.
    """
    try:
        obj = CreditCard(card_number)  
        return obj
    except ValueError:
        raise ValueError("Formato inválido")
    
    
if __name__ == "__main__":
    a = CreditCard()
    a.generate()