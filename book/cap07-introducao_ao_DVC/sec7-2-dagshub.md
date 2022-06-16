## 7.2. DagsHub: um Suplemento de Github para Cientistas de Dados e Engenheiros de Aprendizado de Máquina

### 7.2.1. Motivação

Como um cientista de dados, você pode querer versionar seu código, modelo, dados, parâmetros e métricas para que possa reproduzir um determinado experimento.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

O GitHub é uma ótima plataforma para controle de versão do seu código, mas não é ideal para versionar seus dados, modelo e métricas por dois motivos:

- O GitHub tem um limite de arquivos de 100 MB, portanto, o upload de um arquivo binário médio pode facilmente exceder esse limite.
- É confuso comparar a mudança em diferentes versões de dados com o GitHub. Eu costumava aceitar manualmente mais de 100 alterações nos dados depois de usar o `git pull`, e era uma dor de cabeça.

[DVC](https://khuyentran1401.github.io/reproducible-data-science/version_control/dvc.html) (Data Version Control) é uma ferramenta ideal para versionar seus dados binários. No entanto, você não pode visualizar os arquivos rastreados pelo DVC no GitHub.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Não seria bom se houvesse uma plataforma semelhante ao GitHub, mas mais otimizada para Cientistas de Dados e Engenheiros de Aprendizado de Máquina? É aí que o DagsHub é útil.

### 7.2.2. O que é DagsHub?

O [DagsHub](https://dagshub.com/) é uma plataforma para cientistas de dados e engenheiros de aprendizado de máquina criarem versões de seus dados, modelos, experimentos e códigos.

O DagsHub permite que você crie um novo repositório em sua plataforma ou se conecte a um repositório no GitHub.

Se quiser criar um novo repositório no DagsHub, clique em Novo Repositório (New Repository):

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Se você já possui um repositório no GitHub e deseja migrar seu repositório para o DagsHub, clique em Migrar um Repositório (Migrate A Repo):

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Se você deseja gerenciar seu repositório por meio do GitHub e do DagsHub, clique em Conectar um Repositório (Connect A Repo):

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

A interface do seu novo repositório no DagsHub deve se parecer bastante com a interface do GitHub com a adição de algumas abas como Experiments, Data, Models, Notebooks, DVC e Git.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Você pode conferir o repositório acima [aqui](https://dagshub.com/khuyentran1401/dagshub-demo). Vamos explorar algumas funcionalidades do DagsHub.

### 7.2.3. Versione o seu Dado e Código

Suponha que você tenha uma cópia local do seu repositório GitHub em sua máquina, utilizaremos DVC para versionar seus dados binários.

Comece com a instalação do DVC:

```bash
pip instalar dvc
```

Normalmente, ao usar o DVC, você precisa usar um armazenamento externo como Google Drive, Amazon S3, Azure Blob Storage, Google Cloud Storage, etc. No entanto, com o DagsHub, você pode armazenar seus dados diretamente na plataforma.

Para fazer upload de seus dados para o DagsHub, comece obtendo o link DVC no botão Remote:

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Em seguida, defina esse link como armazenamento remoto do DVC:

```bash
dvc remote add origin https://dagshub.com/khuyentran1401/dagshub-demo.dvc
```

Adicionar autenticação:

```bash
dvc remote modify origin --local auth basicdvc remote modify origin --local user DAGSHUB_USERNAMEdvc remote modify origin --local password DAGSHUB_PASSWORD
```

Em seguida, adicione os dados binários que queremos armazenar no DagsHub. Por exemplo, para adicionar o diretório data/raw , eu executo:

```bash
dvc add data/raw
```

Este comando criará um novo arquivo .dvc. Esses são pequenos arquivos de texto que armazenam informações sobre como acessar os dados originais, mas não os dados originais em si.

```
data
├── raw
│   └── marketing_campaign.csv
└── raw.dvc
```

Envie esses arquivos para o armazenamento do DagsHub:

```bash
push dvc
```

Agora podemos adicionar alterações nos dados e no código e, em seguida, confirmar e enviar sua alteração para o GitHub:

```bash
git add .
```

```bash
git commit -m 'push data and code'
```

```bash
git push origin master
```

Se você estiver usando o GitHub e o DagsHub ao mesmo tempo, você só precisa enviar seus arquivos para o GitHub. O DagsHub será sincronizado automaticamente com o GitHub!

Observação: se o DagsHub não sincronizar, clique no ícone Atualizar sob o título do repositório:

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Se você está familiarizado com o DVC, não há nada de novo aqui. No entanto, a mágica acontece quando você visita seu repositório no DagsHub.

No GitHub, você pode ver seus arquivos `.dvc`, mas não os dados em si. Isso ocorre porque os dados reais são armazenados em outro lugar:

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

No DagsHub, você pode ver tanto os arquivos `.dvc` quanto os próprios dados, pois os dados são armazenados no DagsHub!

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Isso é bastante conveniente, pois posso analisar o código e os dados em uma mesma plataforma.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->
