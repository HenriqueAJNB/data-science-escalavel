[![View the code](https://img.shields.io/badge/GitHub-Visualizar_codigo-blue?logo=GitHub)](https://github.com/HenriqueAJNB/data-science-escalavel/tree/main/book)

<div style="text-align: justify">

## Boas práticas na escrita de funções

### Motivação

Você já olhou uma função que você mesmo escrever há um mês atrás e teve dificuldades de entender em 3 minutos? Se você já passou por isso, então este é o momento certo de refatorar seu código. Se sua função levar mais que 3 minutos para você mesmo entender o código, imagine quanto tempo demoraria para os seus colegas de trabalho.

Se você quer escrever códigos bons que possam ser reutilizados, então eles precisam necessariamente ser legíveis, fáceis de entender. Escrever códigos assim é extremamente importante para cientistas de dados que colaboram com outros membros de equipe em papéis diferentes.

Ao final, desejamos que as funções, não só em Python, mas em qualquer outra linguagem:
- seja pequena
- faça uma coisa só
- contenha código com mesmo nível de abstração
- ter menos do que 4 argumentos
- não tenha código duplicado
- use nomes descritivos

Essas boas práticas acima tornarão as funções mais fáceis de ler e de depurar para encontrar erros.

Nesta seção, vamos discutir como usar essas 6 práticas para melhorar o código das nossas funções.

### Vamos lá

Vamos começar olhando para a função `load_data` abaixo:

```python
"""
Este trecho de código faz download dos arquivos no Google Drive e extrai os dados de treino e teste.
Autora do código: Khuyen Tran
Autor da tradução: Henrique Branco
"""
import xml.etree.ElementTree as ET
import zipfile
from os import listdir
from os.path import isfile, join

import gdown


def main():

    load_data(
        url="https://drive.google.com/uc?id=...",
        output="Twitter.zip",
        path_train="Data/train/en",
        path_test="Data/test/en",
    )


def load_data(url: str, output: str, path_train: str, path_test: str):

    # Faz download do Google Drive
    output = "Twitter.zip"
    gdown.download(url, output, quiet=False)

    # Unzipa o arquivo
    with zipfile.ZipFile(output, "r") as zip_ref:
        zip_ref.extractall(".")

    # Obtém os arquivos de treino e teste
    tweets_train_files = [
        file
        for file in listdir(path_train)
        if isfile(join(path_train, file)) and file != "truth.txt"
    ]
    tweets_test_files = [
        file
        for file in listdir(path_test)
        if isfile(join(path_test, file)) and file != "truth.txt"
    ]

    # Extrai o texto de cada um dos arquivos
    t_train = []
    for file in tweets_train_files:
        train_doc_1 = [r.text for r in ET.parse(join(path_train, file)).getroot()[0]]
        t_train.append(" ".join(t for t in train_doc_1))

    t_test = []
    for file in tweets_test_files:
        test_doc_1 = [r.text for r in ET.parse(join(path_test, file)).getroot()[0]]
        t_test.append(" ".join(t for t in test_doc_1))

    return t_train, t_test


if __name__ == "__main__":
    main()
```

A função `load_data` tenta baixar arquivos do Google Drive e extrair os dados. Mesmo que exista muitos comentários nesta função, é difícil entendê-la em menos de 3 minutos. Isso porque a função:
- é extremamente longa
- faz mais do que uma coisa só
- contém código com diferentes níveis de abstração
- tem mais do que 3 argumentos
- tem muita duplicação de código
- não possui um nome mais descritivo

Vamos mostrar como refatorar essa função na prática, seguindo os 6 pontos mencionados no começo do capítulo.

### Pequena

A função deve ser pequena porque é muito mais fácil de saber o que ela faz. Quão pequena? Na opinião da autora original do livro, Khuyen Tran, as funções raramente devem ter mais do que 20 linhas de código. Devem ser tão pequenas quanto o exemplo abaixo. As funções também não devem ter mais do que um ou dois níveis de identação:

```python
import zipfile

def unzip_data(output: str):
  
    with zipfile.ZipFile(output, 'r') as zip_ref:
        zip_ref.extractall('.')
```

### Fazer uma coisa só

Uma função deve fazer uma única coisa, e não várias. A função `load_data` tenta fazer download dos dados, unzipá-los, ler os nomes dos arquivos que contém dados de treino e teste, e extrair texto de cada um deles.

Por este motivo, ela deveria ser quebrada em várias funções menores, como mostrado abaixo:

```python
download_zip_data_from_google_drive(url, output_path)

unzip_data(output_path)

tweet_train, tweet_test = get_train_test_docs(path_train, path_test)
```

E cada função deve fazer uma coisa só, de forma bem específica:

```python
import gdown

def download_zip_data_from_google_drive(url: str, output_path: str):
    
    gdown.download(url, output_path, quiet=False) 
```

A função `download_zip_data_from_google_drive` somente faz download de um arquivo `.zip` do Google Drive e só! Nada mais além disso...

---
**Comentário a parte do livro original:**

A grande pergunta que fica aqui é: como saber quando a função faz mais de uma coisa? Um exercício bem simples, proposto pelo autor Robert C. Martin (famoso Uncle Bob) em seu livro Código Limpo é descrever o que a sua função faz em poucas palavras e ler o texto.
Se o texto se parecer com este: "Esta função faz isso **e depois** aquilo" é um forte indicativo de que ela faz mais de uma coisa. Os indicativos são: 
- vírgula presentes na descrição verbal ou escrita da função;
- palavras ou expressões como `e`, `também`, `além disso`, `em seguida`;
- código duplicado dentro da função;
- presença de instruções if-else dentro da função com o seguinte comportamento: `se for isso, então faça assim, se for aquilo então faça assado`;

---

</div>
