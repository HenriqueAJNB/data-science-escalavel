[![View the code](https://img.shields.io/badge/GitHub-Visualizar_codigo-blue?logo=GitHub)](https://github.com/HenriqueAJNB/data-science-escalavel/tree/main/book)


## 7.1. Introdução ao DVC: Controle de Versionamento de Dados para Projetos de Aprendizado de Máquina

<div style="text-align: justify">

<!---figura "Photo by Franki Chamaki on Unsplash" -->

### 7.1.1. Motivação

Git é uma ferramenta poderosa para controle de versão. Ele permite que você vá e volte entre diferentes versões do seu código sem ter medo de perder o código que você alterou. Como cientista de dados, você pode não apenas querer controlar diferentes versões de seu código, mas também controlar diferentes versões de seus dados pelo mesmo motivo: você não quer perder os dados anteriores quando os dados são alterados.

Mas o Git não é ideal para controle de versão de banco de dados por dois motivos:

-É confuso comparar alterações em diferentes versões de dados com o Git. Eu lembro que preciso aceitar manualmente cerca de 100 linhas de dados que foram alteradas entre 2 commits quando utilizei git pull e foi uma dor de cabeça.

-Arquivos binários são geralmente grandes. Se você enviá-los ao seu repositório, seu tamanho se tornará ainda maior. Além disto pode ser que leve muito tempo para realizar o commit dos dados no Git.

Não seria bom se você pudesse armazenar seus dados em seu serviço de armazenamento favorito, tal como Amazon S3, Google Drive, Google Cloud Storage ou em sua própria máquina local, enquanto ainda fosse capaz de alternar entre diferentes versões dos dados? É aí que o DVC te dá uma mão.

### 7.1.2. O que é DVC?

DVC é um sistema para controle de versionamento de dados. É essencialmente como o Git, mas é utilizado para dados. Com o DVC, você pode manter as informações sobre diferentes versões de seus dados no Git enquanto armazena seus dados originais em outro lugar.

Melhor ainda, a sintaxe de DVC é similar à do Git! Se você já conhece o Git, aprender DVC é muito fácil.

Vamos ver como usar o DVC do exemplo. Utilizarei <a href='https://github.com/khuyentran1401/Machine-learning-pipeline'>meu repositório</a> como exemplo desta seção. Você pode acompanhar clonando o repositório.

Inicie instalando o pacote

```
pip install dvc
```

Encontre as instruções sobre mais formas de instalar o DVC <a href='https://dvc.org/doc/install'>aqui</a>.

### 7.1.3. Iniciar

Após a instalação do DVC, <b>em um projeto Git</b>, inicialize-o executando

```
git commit -m "Inicialize DVC"
```

Aqui está a estrutura do meu diretório de dados

```
data
├── processed
│   ├── test_text.txt
│   ├── train_label.txt
│   ├── train_text.txt
│   ├── val_label.txt
│   └── val_text.txt
└── raw
    ├── mex20_test_full.txt
    ├── mex20_train_labels.txt
    ├── mex20_train.txt
    ├── mex20_val_labels.txt
    └── mex20_val.txt
```

Para começar a rastrear um arquivo ou diretório, utilize

```
dvc add data
```

A informação do arquivo ou diretório adicionado será armazenada no arquivo .dvc arquivo nomeado data.dvc . Este é um pequeno arquivo de texto que armazena informações sobre como acessar os dados originais, e não são os dados originais em si.

Como o tamanho desse arquivo de texto é pequeno, ele pode ser versionado como um código-fonte com o Git.

Agora, basta realizar o commit do arquivo dvc como faria com o código-fonte. Certifique-se de adicionar dados ao .gitignore com antecedência para evitar o commit dos dados.

```
git add data.dvc
git commit -m "add data"
```

