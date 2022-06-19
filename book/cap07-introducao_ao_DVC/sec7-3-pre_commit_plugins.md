## 7.3. 4 plugins pré-commit para automatizar a revisão e formatação de código em Python

### 7.3.1. Motivação

Ao enviar seu código Python para o Git, você precisa ter certeza de que seu código:

- parece legal
- está organizado
- está em conformidade com o guia de estilo PEP 8
- inclui docstrings

No entanto, pode ser difícil verificar todos esses critérios antes de confirmar seu código. Não seria legal se você pudesse verificar e formatar automaticamente seu código toda vez que você confirmasse um novo código como abaixo?

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

É aí que o pré-commit é útil. Nesta seção, você aprenderá o que é pré-commit e quais plugins você pode adicionar a um pipeline de pré-commit.

### 7.3.2. O que é pré-commit?

pre-commit é uma estrutura que permite identificar problemas simples em seu código antes de confirmá-lo.

Você pode adicionar plugins diferentes ao seu pipeline de pré-commit. Depois que seus arquivos forem confirmados, eles serão verificados por esses plugins. A menos que todas as verificações sejam aprovadas, nenhum código será confirmado.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Para instalar o pré-commit, digite:

```bash
pip install pre-commit
```

Legal! Agora vamos adicionar alguns plugins úteis ao nosso pipeline de pre-commit.

### 7.3.3. black

<!-- video - https://www.youtube.com/watch?v=fcRC07RJUGI&feature=emb_imp_woyt -->

[black](https://black.readthedocs.io/en/stable/) é um formatador de código em Python.

Para instalar o black, digite:

```bash
pip install black
```

Agora, para ver o que o black pode fazer, escreveremos uma função muito longa, como abaixo. Como há mais de 79 caracteres na primeira linha de código, isso viola o PEP 8.

Vamos tentar formatar o código usando black:

```
$ black long_function.py
```

E o código é formatado automaticamente como abaixo!

```Python
def very_long_function(
    long_variable_name,
    long_variable_name2,
    long_variable_name3,
    long_variable_name4,
    long_variable_name5,
):
    pass
```

Para adicionar o black a um pipeline de pré-confirmação, crie um arquivo chamado `.pre-commit-config.yaml` e insira o seguinte código no arquivo:

```yaml
repos:
-   repo: https://github.com/ambv/black
    rev: 20.8b1
    hooks:
    - id: black
```

Para escolher quais arquivos incluir e excluir ao executar o black, crie um arquivo chamado `pyproject.toml` e adicione o seguinte código ao arquivo `pyproject.toml`:

```toml
[tool.black]
line-length = 79
include = '\.pyi?$'
exclude = '''
/(
	\.git
| \.hg
| \.mypy_cache
| \.tox
| \.venv
| _build
| buck-out
| build   
)/ 
```

### 7.3.4. flake8

flake8 é uma ferramenta python que verifica o estilo e a qualidade do seu código Python. Ele verifica vários problemas não cobertos pelo preto.

Para instalar o flake8, digite:

```bash
pip install flake8
```

Para ver o que o flake8 faz, vamos escrever um código que viole algumas diretrizes do PEP 8.

```Python
def very_long_function_name(var1, var2, var3,
var4, var5):
    print(var1, var2, var3, var4, var5)

very_long_function_name(1, 2, 3, 4, 5)
```

Em seguida, verifique o código usando flake8:

```
$ flake8 flake_example.py
```

```
flake8_example.py:2:1: E128 continuation line under-indented for visual indent
flake8_example.py:5:1: E305 expected 2 blank lines after class or function definition, found 1
flake8_example.py:5:39: W292 no newline at end of file
```

Ah! flake8 detecta 3 erros de formatação PEP 8. Podemos usar esses erros como diretrizes para corrigir o código.

```Python
def very_long_function_name(var1, var2, var3, var4, var5):
    print(var1, var2, var3, var4, var5)

very_long_function_name(1, 2, 3, 4, 5)
```

O código parece muito melhor agora!

Para adicionar flake8 ao pipeline de pré-confirmação, insira o seguinte código no arquivo `.pre-commit-config.yaml`:

```yaml
-   repo: https://gitlab.com/pycqa/flake8
    rev: 3.8.4
    hooks:
    - id: flake8
```

Para escolher quais erros ignorar ou editar outras configurações, crie um arquivo chamado `.flake8` e adicione o seguinte código ao arquivo `.flake8`:

```flake8
[flake8]
ignore = E203, E266, E501, W503, F403, F401
max-line-length = 79
max-complexity = 18
select = B,C,E,F,W,T4,B9
```

### 7.3.5. isort

[isort](https://github.com/PyCQA/isort) é uma biblioteca Python que classifica automaticamente as bibliotecas importadas em ordem alfabética e as separa em seções e tipos.

Para instalar o isort, digite:

```bash
pip install isort
```

Vamos tentar usar isort para classificar importações confusas como abaixo:

```Python
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from flake8_example import very_long_function_name
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, OrderedLogisticRegression, \
    LinearRegression, LogisticRegressionCV, LinearRegressionCV 
```
```bash
$ isort isort_example.py
```

Resultado:
```Python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flake8_example import very_long_function_name
from sklearn.linear_model import (
    LinearRegression,
    LinearRegressionCV,
    LogisticRegression,
    LogisticRegressionCV,
    OrderedLogisticRegression,
)
from sklearn.model_selection import train_test_split
```

Legal! As importações estão muito mais organizadas agora.

Para adicionar isort ao pipeline de pré-confirmação, adicione o seguinte código ao arquivo `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/timothycrosley/isort
    rev: 5.7.0
    hooks:
    -   id: isort
```

### 7.3.6. interrogate

<!-- video - https://www.youtube.com/watch?v=fcRC07RJUGI&feature=emb_imp_woyt -->

[interrogate](https://www.youtube.com/watch?v=m3WDafkpbpM&feature=emb_imp_woyt) verifica sua base de código em busca de docstrings ausentes.

Para instalar o interrogate, digite:

```bash
pip install interrogate
```

Às vezes, podemos esquecer de escrever docstrings para classes e funções como abaixo:

```Python
class MathOperation:
    def __init__(self, num) -> None:
        self.num = num 

    def plus_two(self):
        return self.num + 2

    def multiply_three(self):
        return self.num * 3
```

Em vez de olhar manualmente para todas as nossas funções e classes em busca de docstrings ausentes, podemos executar o interrogate:

```
$ interrogate -vv interrogate_example.py
```

Resultado (output):

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Legal! A partir da saída do terminal, sabemos quais arquivos, classes e funções não possuem docstrings. Como sabemos os locais das docstrings ausentes, é fácil adicioná-las.

```Python
"""Example for interrogate"""

class MathOperation:
    """Perform math operation"""
    def __init__(self, num) -> None:
        self.num = num 

    def plus_two(self):
        """Add 2"""
        return self.num + 2

    def multiply_three(self):
        """Multiply by 3"""
        return self.num * 3
```

```bash
$ interrogate -vv interrogate_example.py
```
<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

A docstring para o método `__init__` está ausente, mas não é necessária. Podemos dizer ao interrogate para ignorar o método `__init__` adicionando `-i` ao argumento:

```
$ interrogate -vv -i interrogate_example.py
```
<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Legal! Para adicionar interrogação ao pipeline de pré-confirmação, insira o seguinte código no arquivo `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/econchick/interrogate
    rev: 1.4.0  
    hooks:
      - id: interrogate
        args: [--vv, -i, --fail-under=80]
```

Para editar as configurações padrão do interrogate, insira o seguinte código no arquivo `pyproject.toml`:

```toml
[tool.interrogate]
ignore-init-method = true
ignore-init-module = false
ignore-magic = false
ignore-semiprivate = false
ignore-private = false
ignore-property-decorators = false
ignore-module = true
ignore-nested-functions = false
ignore-nested-classes = true
ignore-setters = false
fail-under = 95
exclude = ["setup.py", "docs", "build"]
ignore-regex = ["^get$", "^mock_.*", ".*BaseClass.*"]
verbose = 0
quiet = false
whitelist-regex = []
color = true
generate-badge = "."
badge-format = "svg"
```

### 7.3.7. Etapa Final — Adicionar pre-commit ao Git Hooks

<!-- video - https://www.youtube.com/watch?v=1Q1VOIrQ9GA&feature=emb_imp_woyt -->

O código final em seu arquivo `.pre-commit-config.yaml` deve ter a seguinte aparência:

```yaml
repos:
-   repo: https://github.com/ambv/black
    rev: 20.8b1
    hooks:
    - id: black
-   repo: https://gitlab.com/pycqa/flake8
    rev: 3.8.4
    hooks:
    - id: flake8
-   repo: https://github.com/timothycrosley/isort
    rev: 5.7.0
    hooks:
    -   id: isort
-   repo: https://github.com/econchick/interrogate
    rev: 1.4.0  
    hooks:
    - id: interrogate
      args: [-vv, -i, --fail-under=80]
```

Para adicionar o pre-commit ao git hooks, digite:

```bash
$ pre-commit install
```

Resultado (output):

```bash
pre-commit installed at .git/hooks/pre-commit
```

### 7.3.8. Commit

Agora estamos prontos para dar o commit do novo código!

```bash
$ git commit -m 'add pre-commit examples'
```

E você deve ver algo como abaixo:

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

### 7.3.9. Pular verificação

Para evitar que o pré-commit verifique um determinado commit, adicione --no-verify ao git commit:

```bash
$ git commit -m 'add pre-commit examples' --no-verify
```
