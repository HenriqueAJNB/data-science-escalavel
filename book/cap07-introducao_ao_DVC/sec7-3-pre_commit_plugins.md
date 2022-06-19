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
pip instalar pré-commit
```

Legal! Agora vamos adicionar alguns plugins úteis ao nosso pipeline de pré-commit.

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