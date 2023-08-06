
# multivalidator

Um validador e gerador para os seguintes parâmetros:

- Bank Card
- CNPJ
- CPF
- Date
- Email
- FoneNumber
- PassPort
- PassWord
- Url

## Instalação

```bash
  pip install multi-validator-generator
```

## Exemplos

1. Importanto biblioteca
```python
  import multivalidator as mv
```
**read**
```python
  # read: Retorna um objeto iterável que contém o parâmetro escolhido
  # Exemplo:
  cpf = mv.cpf.read("529.982.247-25")
  cnpj = mv.cnpj.read("92.639.324/0001-92")
  date = mv.date.read("08-04-2021")
  email = mv.emails.read("teste@gmail.com")
  fone = mv.fone_number.read("11999999999")
  passport = mv.passport.read("AB1234567")
  password = mv.password.read("123456789")
  url = mv.url.read("https://www.google.com")
  bank_card = mv.bank_card.read("5555666677778884")
```
**generate**
```python
  # Gera um cpf válido e adiciona-o no objeto iterável
  cpf.generate()
  # Saida: ['529.982.247-25', '262.848.575-35']
  # Aviso: Alguns geradores necessitam de parâmetros na sua chamada(Consulte a documentação)
```

**validate**
```python
  # Retorna uma tupla com um valor booleano indicando se é valido, e o cpf formatado
  cpf.validate('529.982.247-25')
  #Saída: (True, '529.982.247-25')
```

**add**
```python
  # Adiciona um cpf no objeto iterável existente.
  cpf.add('529.982.247-25')
  #Saída: ['529.982.247-25', '262.848.575-35', '171.414.230-28']
```