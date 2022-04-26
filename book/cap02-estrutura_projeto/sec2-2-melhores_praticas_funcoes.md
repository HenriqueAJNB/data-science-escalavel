[![View the code](https://img.shields.io/badge/GitHub-Visualizar_codigo-blue?logo=GitHub)](https://github.com/HenriqueAJNB/data-science-escalavel/tree/main/book)

<div style="text-align: justify">

## Boas práticas na escrita de funções

### Motivação

Você já olhou uma função que você mesmo escreveu há um mês e teve dificuldades de entender em 3 minutos? Se você já passou por isso, então este é o momento certo de refatorar seu código. Se sua função levar mais que 3 minutos para você mesmo entender o código, imagine quanto tempo demoraria para os seus colegas de trabalho.

Se você quer escrever códigos bons que possam ser reutilizados, então eles precisam necessariamente ser legíveis, fáceis de entender. Escrever códigos assim é extremamente importante para cientistas de dados que colaboram com outros membros de equipe em papéis diferentes.

Ao final, desejamos que uma função, não só em Python, mas em qualquer outra linguagem:
- seja pequena;
- faça uma coisa só;
- contenha código com mesmo nível de abstração;
- tenha menos do que 4 argumentos;
- não tenha código duplicado;
- use nomes descritivos.

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

A função `load_data` tenta baixar arquivos do Google Drive e extrair os dados. Mesmo que existam muitos comentários nesta função, é difícil entendê-la em menos de 3 minutos. Isso porque a função:
- é extremamente longa;
- faz mais do que uma coisa só;
- contém código com diferentes níveis de abstração;
- tem mais do que 3 argumentos;
- tem muita duplicação de código;
- não possui um nome mais descritivo.

Vamos mostrar como refatorar essa função na prática, seguindo os 6 pontos mencionados no começo do capítulo.

### Pequena

A função deve ser pequena porque é muito mais fácil de saber o que ela faz. Quão pequena? Na opinião da autora original do livro, Khuyen Tran, as funções raramente devem ter mais do que 20 linhas de código. Devem ser tão pequenas quanto o exemplo abaixo. As funções também não devem ter mais do que um ou dois níveis de indentação:

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

A função `download_zip_data_from_google_drive` somente faz <i>download</i> de um arquivo `.zip` do Google Drive e só! Nada mais além disso...

---
>**Comentário a parte do livro original:**
>
>A grande pergunta que fica aqui é: como saber quando a função faz mais de uma coisa? Um exercício bem simples, proposto pelo autor Robert C. Martin (famoso Uncle Bob) em seu livro Código Limpo é descrever o que a sua função faz em poucas palavras e ler o texto.
Se o texto se parecer com este: "Esta função faz isso **e depois** aquilo" é um forte indicativo de que ela faz mais de uma coisa. Os indicativos são: 
>- vírgulas presentes na descrição verbal ou escrita da função;
>- palavras ou expressões como `e`, `também`, `além disso`, `em seguida`;
>- código duplicado na função;
>- presença de instruções if-else na função com o seguinte comportamento: `se for isso, então faça assim, se for aquilo então faça assado`;

---

### Um único nível de abstração

O código da função `extract_texts_from_multiple_files` está em um nível diferente de abstração da função em si...

```python
import xml.etree.ElementTree as ET
from typing import List 

def extract_texts_from_multiple_files(path_to_file: str, files: list) -> List[str]:

    all_docs = []
    for file in files:
        list_of_text_in_one_file = [r.text for r in ET.parse(join(path_to_file, file_name)).getroot()[0]]
        text_in_one_file_as_string = ' '.join(t for t in list_of_text_in_one_file)
        all_docs.append(text_in_one_file_as_string)

    return all_docs
```

```{admonition} O que é nível de abstração?
:class: tip

A autora trouxe uma referência para responder a esta pergunta:

O nível de abstração é a quantidade de complexidade pela qual um sistema é visualizado ou programado. Quanto maior o nível, menos detalhes. Quanto mais baixo o nível, mais detalhes. — PCMag

Em outras palavras, quanto maior a complexidade, menor a abstração.
```

Baseado na definição acima, temos que:
- O nome da função em si `extract_texts_from_multiple_files` está em um alto nível de abstração (baixa complexidade, fácil de entender);
- Por outro lado, o trecho de código `list_of_text_in_one_file = [r.text for r in ET.parse(join(path_to_file, file_name)).getroot()[0]]` está em um nível baixo de abstração (alta complexidade, difícil de entender).

Para fazer com que o código na função esteja no mesmo nível de abstração, podemos colocar o código "de baixo nível" em outra função separada.

```python
import xml.etree.ElementTree as ET
from typing import List 

def extract_texts_from_multiple_files(path_to_file: str, files: list) -> List[str]:

    all_docs = []
    for file in files:
        text_in_one_file = extract_texts_from_each_file(path_to_file, file)
        all_docs.append(text_in_one_file)

    return all_docs
    
def extract_texts_from_each_file(path_to_file: str, file_name: list) -> str:
    
    list_of_text_in_one_file =[r.text for r in ET.parse(join(path_to_file, file_name)).getroot()[0]]
    text_in_one_file_as_string = ' '.join(t for t in list_of_text_in_one_file)
    
    return text_in_one_file_as_string
```

Agora temos o código da função - `extract_texts_from_each_file(path_to_file, file)` - e a função em si - `extract_texts_from_multiple_files` no mesmo nível de abstração.

### Código duplicado

O código a seguir está duplicado. O trecho que é usado para coletar dados de treino é bastante similar ao trecho usado para coletar dados de teste.

```python
import xml.etree.ElementTree as ET

t_train = []
for file in tweets_train_files:
    train_doc_1 =[r.text for r in ET.parse(join(path_train, file)).getroot()[0]]
    t_train.append(' '.join(t for t in train_doc_1))


t_test = []
for file in tweets_test_files:
    test_doc_1 =[r.text for r in ET.parse(join(path_test, file)).getroot()[0]]
    t_test.append(' '.join(t for t in test_doc_1))
```

Deve-se, de forma geral, evitar duplicações pelos seguintes motivos:
- É redundante;
- Se alteramos um trecho de código, precisamos alterar o trecho similar também. Podemos esquecer de alterar algum trecho, pois somos todos humanos, e acabamos introduzindo bugs em nosso código.

Podemos eliminar o código duplicado encapsulando-o em uma função.

```python
from typing import Tuple, List

def get_train_test_docs(path_train: str, path_test: str) -> Tuple[list, list]:
    tweets_train_files = get_files(path_train)
    tweets_test_files = get_files(path_test)

    t_train = extract_texts_from_multiple_files(path_train, tweets_train_files)
    t_test  = extract_texts_from_multiple_files(path_test, tweets_test_files)
    return t_train, t_test
    
def extract_texts_from_multiple_files(path_to_file: str, files: list) -> List[str]:

    all_docs = []
    for file in files:
        text_in_one_file = extract_texts_from_each_file(path_to_file, file)
        all_docs.append(text_in_one_file)

    return all_docs
```

### Nomes descritivos

```{admonition} Nomes descritivos
:class: tip

A autora trouxe uma definição do Robert C. Martin, também conhecido como "Tio Bob" (Uncle Bob, do inglês):

Um nome descritivo longo é melhor que um nome enigmático curto. Um nome descritivo longo é melhor que um comentário descritivo longo. — Código Limpo de Robert C. Martin

Inclusive recomendo altamente a leitura desta obra citada!
```

Outras pessoas conseguem entender o que a função `extract_texts_from_multiple_files` simplesmente lendo o nome da função.

Não tenham medo de escrever nomes longos. É melhor escrever nomes longos do que vagos. Se você tentar encurtar o nome da função para algo parecido com `get_texts`, seria difícil para as outras pessoas entenderem o que a função faz exatamente sem olhar o código dela.

Se o nome da sua função é extremamente longo, como `download_file_from_google_drive_and_extract_text_from_that_file`, é um forte sinal de que sua função está fazendo mais do que uma coisa só e deveria ser quebrada em funções menores.

### Ter menos que 4 argumentos

Uma função não deve ter mais do que 3 argumentos, pois pode ser um sinal de que ela faz mais do que uma única tarefa. Sem contar que é difícil testar uma função com mais do que 3 argumentos, pois a combinação entre eles começa a crescer exponencialmente.

Por exemplo, a função `load_data` tem 4 argumentos: `url`, `output_path`, `path_train`, and `path_test`. Portanto, tem-se uma leve sensação de que ela faz muitas coisas:
- Usa a `url` para fazer <i>download</i> do dado;
- Salva-o em `output_path`;
- Extrai os dados de `output_path` e os salva em `path_train` e `path_test`.

```{admonition} Dica
:class: tip

Se a função tem mais de 3 argumentos, considere torná-la uma classe!
```

Por exemplo, nós poderíamos dividir a função `load_data` em 3 outras funções diferentes:

```python
download_zip_data_from_google_drive(url, output_path)

unzip_data(output_path)

tweet_train, tweet_test = get_train_test_docs(path_train, path_test)
```

As três funções tem um objetivo único de extrair dados, podemos criar uma classe chamada `DataGetter`.

```python
import xml.etree.ElementTree as ET
import zipfile
from os import listdir
from os.path import isfile, join
from typing import List, Tuple

import gdown


def main():

    url = "https://drive.google.com/uc?id=1jI1cmxqnwsmC-vbl8dNY6b4aNBtBbKy3"
    output_path = "Twitter.zip"
    path_train = "Data/train/en"
    path_test = "Data/test/en"

    data_getter = DataGetter(url, output_path, path_train, path_test)

    tweet_train, tweet_test = data_getter.get_train_test_docs()


class DataGetter:
    def __init__(self, url: str, output_path: str, path_train: str, path_test: str):
        self.url = url
        self.output_path = output_path
        self.path_train = path_train
        self.path_test = path_test
        self.download_zip_data_from_google_drive()
        self.unzip_data()

    def download_zip_data_from_google_drive(self):

        gdown.download(self.url, self.output_path, quiet=False)

    def unzip_data(self):

        with zipfile.ZipFile(self.output_path, "r") as zip_ref:
            zip_ref.extractall(".")

    def get_train_test_docs(self) -> Tuple[list, list]:

        tweets_train_files = self.get_files(self.path_train)
        tweets_test_files = self.get_files(self.path_test)

        t_train = self.extract_texts_from_multiple_files(
            self.path_train, tweets_train_files
        )
        t_test = self.extract_texts_from_multiple_files(
            self.path_test, tweets_test_files
        )
        return t_train, t_test

    @staticmethod
    def get_files(path: str) -> List[str]:

        return [
            file
            for file in listdir(path)
            if isfile(join(path, file)) and file != "truth.txt"
        ]

    def extract_texts_from_multiple_files(
        self, path_to_file: str, files: list
    ) -> List[str]:

        all_docs = []
        for file in files:
            text_in_one_file = self.extract_texts_from_each_file(path_to_file, file)
            all_docs.append(text_in_one_file)

        return all_docs

    @staticmethod
    def extract_texts_from_each_file(path_to_file: str, file_name: list) -> str:

        list_of_text_in_one_file = [
            r.text for r in ET.parse(join(path_to_file, file_name)).getroot()[0]
        ]
        text_in_one_file_as_string = " ".join(t for t in list_of_text_in_one_file)

        return text_in_one_file_as_string


if __name__ == "__main__":
    main()
```

```{admonition} Nota
:class: note

No código acima a autora usou o decorador `staticmethod` para alguns métodos, pois eles não usam nenhum atributo ou método da classe. Ela também indicou [este site](https://realpython.com/instance-class-and-static-methods-demystified/) para buscar por mais informações. 
```

Como podemos observar, nenhuma das funções ou métodos acima, com exceção do construtor, tem mais do que 3 argumentos! E embora o código que usa o paradigma da programação orientada à objetos seja bem mais longo, ele é muito mais legível. Sabemos, também, o que cada trecho de código faz de forma bem específica.

### Como escrever funções como estas?

Não tente escrever o código perfeito de primeira. Escreva códigos complexos que você tem em mente. Conforme o seu código cresce, pergunte-se se as suas funções violam alguma das boas práticas mencionadas acima. Se sim, refatore-as, teste-as, e mova para próxima função.

### Conclusão

Você acabou de aprender as 6 melhores práticas para escrever funções mais legíveis e, ao mesmo tempo, testáveis. Sabendo que cada função faz uma única coisa, você perceberá que a escrita dos testes unitários de cada uma delas será mais fácil e será possível garantir que todos obtenham sucesso quando uma alteração for feita.

Se você não medir esforços para que seus colegas de equipe entendam seu código, eles ficaram eternamente felizes em reutilizá-los em outros projetos.

</div>
