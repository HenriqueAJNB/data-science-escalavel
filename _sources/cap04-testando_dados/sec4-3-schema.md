[![View the code](https://img.shields.io/badge/GitHub-View_the_Code-blue?logo=GitHub)](https://github.com/khuyentran1401/Data-science/blob/master/data_science_tools/schema.ipynb)

## Introdução ao Schema: Uma Biblioteca Python para Validar seus Dados

![](https://miro.medium.com/max/700/0*HSqvCAEj62jir0Lq)

Foto por [Nonsap Visuals](https://unsplash.com/@nonsapvisuals?utm_source=medium&utm_medium=referral) no [Unsplash](https://unsplash.com/?utm_source=medium&utm_medium=referral)

### O que é o Schema?

Nas duas últimas seções, aprendemos como validar um DataFrame Pandas. No entanto, às vezes você pode querer validar estruturas de dados Python em vez de um DataFrame Pandas. É aí que o Schema se faz útil.

[**Schema**](https://github.com/keleshev/schema) é uma biblioteca para validação de estruturas de dados em Python.

Instale o Schema com:

```bash
pip install schema
```

ou, se estiver usando o Poetry:

```bash
poetry add schema
```


### Valide Tipos de Dados

Imagine que esses dados apresentam as informações sobre seus amigos.


```python
data = [
            {'name': 'Norma Fisher',  'city': 'South Richard',  'closeness (1-5)': 4,  'extrovert': True,  'favorite_temperature': -45.74}, 
            {'name': 'Colleen Taylor',  'city': 'North Laurenshire',  'closeness (1-5)': 4,  'extrovert': False,  'favorite_temperature': 93.9}, 
            {'name': 'Melinda Kennedy',  'city': 'South Cherylside',  'closeness (1-5)': 1,  'extrovert': True,  'favorite_temperature': 66.33}
        ]
```

Podemos usar o Schema para validar tipos de dados:

```python
from schema import Schema

schema = Schema([{'name': str,
                 'city': str, 
                 'closeness (1-5)': int,
                 'extrovert': bool,
                 'favorite_temperature': float}])
                 
schema.validate(data)
```

Como a saída não gera erros, sabemos que nossos dados são válidos.

Vejamos o que acontece se os tipos de dados não forem como o que esperamos:
```python
schema = Schema([{'name': int,
                 'city': str, 
                 'closeness (1-5)': int,
                 'extrovert': bool,
                 'favorite_temperature': float}])

schema.validate(data)
```
```bash
SchemaError: Or({'name': <class 'int'>, 'city': <class 'str'>, 'closeness (1-5)': <class 'int'>, 'extrovert': <class 'bool'>, 'favorite_temperature': <class 'float'>}) did not validate {'name': 'Norma Fisher', 'city': 'South Richard', 'closeness (1-5)': 3, 'extrovert': True, 'favorite_temperature': -45.74}
Key 'name' error:
'Norma Fisher' should be instance of 'int'
```

A partir do erro, sabemos exatamente qual coluna e valor dos dados são diferentes do que esperamos. Assim, podemos voltar aos dados para corrigir ou excluir esse valor.

Se tudo o que importa é se os dados são válidos ou não, use:

```python
schema.is_valid(data)
```

Isso retornará `True` se os dados estiverem conforme o esperado ou `False` caso contrário.

### Valide o Tipo de Dado de Algumas Colunas Enquanto Ignora o Resto

Mas e se não nos importarmos com os tipos de dados de todas as colunas, mas apenas nos preocuparmos com o valor de algumas colunas? Podemos especificar isso com `str: object`
```python
schema = Schema([{'name': str,
                 'city': str, 
                 'favorite_temperature': float,
                  str: object
                 }])
                
schema.is_valid(data)
```

```bash
Output: True
```

Como você pode ver, tentamos validar os tipos de dados 'name', 'city' e 'favorite\_temperature', ignorando os tipos de dados do restante dos recursos em nossos dados.

Os dados são válidos porque os tipos de dados dos 3 recursos especificados estão corretos.

### Valide com uma Função

E se quisermos determinar se os dados em uma coluna atendem a uma condição específica, como o intervalo dos valores em uma coluna?

O Schema permite que você use uma função para especificar a condição para os seus dados.

Se quisermos verificar se os valores na coluna ‘closeness (1-5)’ estão entre 1 e 5, podemos usar `lambda` como abaixo:

```python
schema = Schema([{'name': str,
                 'city': str, 
                 'favorite_temperature': float,
                  'closeness (1-5)': lambda n : 1 <= n <= 5,
                  str: object
                 }])

schema.is_valid(data)
```

```bash
Output: True
```

Como você pode ver, especificamos `n`, o valor em cada linha da coluna 'closeness (1-5)', entre 1 e 5 com `lambda n: 1 <= n <=5`. Legal!

### Valide Vários Schemas

#### And

E se você quiser garantir que sua coluna "closeness (1-5)" esteja entre 1 e 5 **e** o tipo de dado seja um número inteiro?

É quando `And` pode ser usado:

```python
from schema import And

schema = Schema([{'name': str,
                 'city': str, 
                 'favorite_temperature': float,
                  'closeness (1-5)': And(lambda n : 1 <= n <= 5, float),
                  str: object
                 }])

schema.is_valid(data)
```

```bash
Output: False
```

Embora todos os valores estejam entre 1 e 5, o tipo de dado não é flutuante (decimal). Como uma das condições não foi satisfeita, os dados são inválidos.

#### Or

Se quisermos que os dados da coluna sejam válidos se qualquer uma das condições for satisfeita, podemos usar `Or`.

Por exemplo, se quisermos que o nome da cidade contenha 1 ou 2 palavras, podemos usar:

```python
from schema import Or

schema = Schema([{'name': str,
                 'city': Or(lambda n: len(n.split()) == 2, lambda n: len(n.split()) == 1), 
                 'favorite_temperature': float,
                  'closeness (1-5)': int,
                  str: object
                 }])

schema.is_valid(data)
```

```bash
Output: True
```

#### Combinação de And e Or

E se quisermos que o tipo de dado da coluna 'city' seja string, mas o comprimento pode ser 1 ou 2? Felizmente, isso pode ser tratado facilmente combinando `And` e `Or`:

```python
schema = Schema([{'name': str,
                 'city': And(str, Or(lambda n: len(n.split()) == 2, lambda n: len(n.split()) == 1)), 
                 'favorite_temperature': float,
                  'closeness (1-5)': int,
                  str: object
                 }])

schema.is_valid(data)
```

```bash
Output: True
```

### Optional

E se **não tivermos** as informações detalhadas sobre **alguns** de seus amigos?

```python
data = [
            {'name': 'Norma Fisher',  'city': 'South Richard',  'closeness (1-5)': 4,  'detailed_info': {'favorite_color': 'Pink',   'phone number': '7593824219489'}}, 
            {'name': 'Emily Blair',  'city': 'Suttonview',  'closeness (1-5)': 4,  'detailed_info': {'favorite_color': 'Chartreuse',   'phone number': '9387784080160'}}, 
            {'name': 'Samantha Cook', 'city': 'Janeton', 'closeness (1-5)': 3}
        ]
```

Como o 'detailed\_info' de Samantha Cook não está disponível para todos os seus amigos, queremos tornar esta coluna opcional. Schema nos permite definir essa condição com `Optional`.

```python
from schema import Optional

schema = Schema([{'name': str,
                 'city': str, 
                 'closeness (1-5)': int,
                 Optional('detailed_info'): dict}])

schema.is_valid(data)
```

```bash
Output: True
```

### Forbidden

Às vezes, também podemos querer garantir que um determinado tipo de dado não esteja em nossos dados, como informações privadas. Podemos especificar qual coluna é proibida com `Forbidden`:

```python
from schema import Forbidden

schema = Schema([{'name': str,
                 'city':str,  
                  'closeness (1-5)': int,
                  Forbidden('detailed_info'): dict
                 }])

schema.validate(data)
```

```bash
Forbidden key encountered: 'detailed_info' in {'name': 'Norma Fisher', 'city': 'South Richard', 'closeness (1-5)': 4, 'detailed_info': {'favorite_color': 'Pink', 'phone number': '7593824219489'}}
```

Agora estamos cientes da existência da coluna proibida toda vez que o esquema lança um erro!

### Dicionário Aninhado

Até agora, o esquema nos permitiu realizar muitas validações sofisticadas em várias linhas de código. Mas na realidade, podemos lidar com uma estrutura de dados mais sofisticada do que o exemplo acima.

Podemos usá-lo para dados com uma estrutura mais complicada? Como um dicionário dentro de um dicionário? Sim, nós podemos.

Imagine que nossos dados se parecem abaixo:


```python
data = [
            {'name': 'Norma Fisher',  'city': 'South Richard',  'closeness (1-5)': 4,  'detailed_info': {'favorite_color': 'Pink',   'phone number': '7593824219489'}}, 
            {'name': 'Emily Blair',  'city': 'Suttonview',  'closeness (1-5)': 4,  'detailed_info': {'favorite_color': 'Chartreuse',   'phone number': '9387784080160'}}
        ]
```

Podemos validar com um dicionário aninhado:

```python
schema = Schema([{'name': str,
                 'city':str,  
                  'closeness (1-5)': int,
                  'detailed_info': {'favorite_color': str, 'phone number': str}
                 }])
                 
schema.is_valid(data)
```

```bash
Output: True
```

A sintaxe é direta! Só precisamos escrever outro dicionário e especificar o tipo de dado para cada chave.

### Converter Tipo de Dado

O Schema pode não somente ser usado para validar dados, mas também para converter o tipo de dado se não for o que esperávamos!

Por exemplo, podemos converter a string '123' para o inteiro 123 com `Use(int)`:

```python
from schema import Use

Schema(Use(int)).validate('123')
```

```bash
123
```
