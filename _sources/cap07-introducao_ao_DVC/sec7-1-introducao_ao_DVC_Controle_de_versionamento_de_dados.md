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

Vamos ver como usar o DVC do exemplo. Utilizarei [meu repositório](https://github.com/khuyentran1401/Machine-learning-pipeline) como exemplo desta seção. Você pode acompanhar clonando o repositório.

Inicie instalando o pacote

```bash
pip install dvc
```

Encontre as instruções sobre mais formas de instalar o DVC [aqui](https://dvc.org/doc/install).

### 7.1.3. Iniciar

Após a instalação do DVC, `em um projeto Git`, inicialize-o executando

```bash
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

```bash
dvc add data
```

A informação do arquivo ou diretório adicionado será armazenada no arquivo .dvc arquivo nomeado data.dvc . Este é um pequeno arquivo de texto que armazena informações sobre como acessar os dados originais, e não são os dados originais em si.

Como o tamanho desse arquivo de texto é pequeno, ele pode ser versionado como um código-fonte com o Git.

Agora, basta realizar o commit do arquivo dvc como faria com o código-fonte. Certifique-se de adicionar dados ao .gitignore com antecedência para evitar o commit dos dados.

```bash
git add data.dvc
git commit -m "add data"
```

### 7.1.4. Armazenando os dados remotamente


Legal! Agora nós criamos um arquivo para armazenar as informações sobre os dados originais. O próximo passo é descobrir onde armazenar os dados.

Assim como utilizamos `git add remote` para armazenar a URL do repositório remoto, também queremos utilizar `dvc remote add` para armazenar a localização do repositório remoto.

O DVC nos permite armazenar nossos dados no Google Drive, Amazon S3, Azure Blob Storage, Google Cloud Storage, Aliyun OSS, SSH, HDFS e HTTP. Como eu assumo que todo mundo tenha uma conta no Google Drive, vamos aprender como armazenar nossos dados no Google Drive.

Comece criando uma pasta no Google Drive

<!---figura do Google Drive-->


Depois de criarmos uma pasta, nosso link será algo assim [https://drive.google.com/drive/folders/1ynNBbT-4J0ida0eKYQqZZbC93juUUbVH](https://drive.google.com/drive/folders/1ynNBbT-4J0ida0eKYQqZZbC93juUUbVH)
Basta adicionar esse link ao DVC para armazenar a localização do repositório remoto

```bash
dvc remote add -d remote gdrive://1ynNBbT-4J0ida0eKYQqZZbC93juUUbVH
```

-d se refere a padrão (`default`). As informações sobre o armazenamento serão salvas em `.dvc/config`

```
[core]
remote = remote
['remote "remote"']
url = gdrive://1ynNBbT-4J0ida0eKYQqZZbC93juUUbVH
```

Agora basta confirmar o arquivo de configuração

```bash
git commit .dvc/config -m "Configurar armazenamento remoto"
```

E envie os dados para o Google Drive

```bash
push dvc
```

É isto! Agora todos os dados são enviados para o Google Drive. Verifique com `dvc remote add` para visualizar mais maneiras de armazenar seus dados em outros serviços de armazenamento.

Para enviar a mudança que fizemos até agora para nosso repositório remoto, digite

```bash
git push origin <branch>
```
### 7.1.5. Acesse os dados

Seus dados estão armazenados em algum lugar seguro. Mas agora você ou seus colegas de equipe querem acessar os dados, o que você ou seus colegas devem fazer?

É direto ao ponto. Basta usar `git pull` para puxar as mudanças no código como você normalmente faz. Agora você tem o arquivo .dvc em seu repositório local.

Para recuperar os dados, basta digitar

```bash
dvc pull
```

para extrair os dados do armazenamento remoto. É isto!

Se você estiver seguindo o tutorial e ainda tiver o repositório de dados em sua máquina local, exclua-o para ver como o dvc pull pode recuperar seus dados do repositório remoto.

### 7.1.6. Faça alterações

Para fazer alterações, utilize

```bash
dvc add data
git commit data.dvc -m 'Data updates'
dvc push
git push origin <branch>
```

É direto, não?

### 7.1.7. Alternar entre diferentes versões

O ponto principal de se utilizar o DVC é que podemos alternar entre diferentes versões de nossos dados. Então, como exatamente podemos fazer isso? Novamente, assim como alternamos entre diferentes versões de nosso código com o Git, use dvc checkout para alternar entre diferentes versões de nossos dados.

```bash
git checkout <...>
dvc checkout
```

Por exemplo, se quisermos mudar para a versão anterior dos dados, digite

```bash
git checkout HEAD^1 data.dvc
dvc checkout
```

Agora, quando os dados reverterem para a versão anterior, utilize

```bash
git commit data.dvc -m "reverter para a versão anterior"
```

para salvar as alterações.

Basicamente, mudamos para outra versão do nosso código com `git checkout. dvc checkout` restaura as versões correspondentes dos arquivos `.dvc` e diretórios `.dvc/cache` para a área de trabalho.

Bem legal não?

</div>
