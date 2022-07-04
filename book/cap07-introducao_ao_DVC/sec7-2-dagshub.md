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

### 7.2.4. Rastreie Experimentos

Bibliotecas como MLFlow permitem que cientistas de dados acompanhem seus experimentos junto com modelos e parâmetros. No entanto, eles não rastreiam o código.

Não seria legal se você pudesse salvar o código, modelos, parâmetros, dados de um experimento?

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Isso pode ser feito facilmente com o DagsHub. O DagsHub permite que você registre seus experimentos com o registrador DagsHub ou MLFlow. Seus experimentos na guia "Experiment" devem ter a aparência abaixo:

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

É uma boa prática usar o MLFlow para experimentar diferentes parâmetros rapidamente sem comprometer seu código. Depois de encontrar os experimentos com bons resultados, você pode usar o registrador do DagsHub para salvar os resultados em formatos abertos (metric.csv, param.yaml) e encapsulá-los com o código, modelo e dados que os produziram.

Vamos aprender como registrar seu experimento com cada um desses métodos.

#### 7.2.4.1. Registre seus experimentos com MLFlow

O [MLflow](https://www.mlflow.org/) é uma plataforma de código aberto que permite rastrear e comparar experimentos. Para instalar o MLflow, digite:

```bash
pip install mlflow
```

No código abaixo, utilizo o MLFlow para registrar métricas e parâmetros.

```bash
import mlflow
```

```Python
with mlflow.start_run():
  
  # código para treinar o modelo
  ...
  
  #parâmetros de registro
  mlflow.log_params({"model_class": type(model).__name__})
  mlflow.log_params({"model": model.get_params()})
  
  # código para avaliar o modelo
  ...
  
  # métricas de registro
  mlflow.log_metrics(
          {
              "k_melhor": k_melhor,
              "score_best": cotovelo.elbow_score_,
          }
      )
```

Também defino o URI de rastreamento para ser o URL encontrado em MLflow Tracking remote:

`mlflow.set_tracking_uri("https://dagshub.com/khuyentran1401/dagshub-demo.mlflow")`

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->


É isso! Agora, toda vez que você executar seu código, os parâmetros e métricas de cada experimento serão exibidos na guia Experimentos do seu repositório DagsHub:

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Ser capaz de registrar seus experimentos MLflow em um servidor remoto como o DagsHub em vez de um banco de dados local permitirá que seus colegas de equipe tenham acesso aos seus experimentos no navegador.

#### 7.2.4.2. Registre os seus Experimentos com DagsHub Logger

Depois de encontrar um bom experimento e estiver pronto para registrar o código, os dados e as saídas (outputs) desse experimento, basta alternar o MLFlow para o DagsHub logger.

Para usar o DagsHub logger, comece instalando o DagsHub:

```bash
pip install dagshub
```

Registrar seus experimentos com o DagsHub logger é muito similar a registrar com o MLFlow:

```Python
from dagshub import DAGsHubLogger

# intialize DagsHub logger
logger = DAGsHubLogger

# log parameters
logger.log_hyperparams({"model_class": type(model).__name__})
logger.log_hyperparams({"model": model.get_params()})

# log metrics
logger.log_metrics(
        {
            "k_best": k_best,
            "score_best": elbow.elbow_score_,
        }
    )
```

Depois de executar seu código, o DagsHub criará automaticamente dois `metrics.csv` e `params.yml` em seu diretório de trabalho:

```
.
├── metrics.csv
└── params.yml
```

Adicione todas as alterações à área de teste, confirme e envie essas alterações para o GitHub:

```bash
git add .
git commit -m 'experiment 1'
git push origin master
```

Agora, o novo experimento será registrado com o Git na guia Experiment.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

#### 7.2.4.3. Utilize tanto MLflow quanto DagsHub Logger ao mesmo tempo

Embora seja útil alternar entre o MLflow e DagsHub logger, achei inconveniente reescrever meu código toda vez que quero alternar para outro registrador.

Minha solução foi criar uma classe `BaseLogger` cujos métodos são `log_metrics` e `log_params`. Cada método utilizará tanto o MLflow logger quanto o DagsHub logger.

```Python
import mlflow
from dagshub import DAGsHubLogger

class BaseLogger:
    def __init__(self):
        self.logger = DAGsHubLogger()

    def log_metrics(self, metrics: dict):
        mlflow.log_metrics(metrics)
        self.logger.log_metrics(metrics)

    def log_params(self, params: dict):
        mlflow.log_params(params)
        self.logger.log_hyperparams(params)
```

Com `BaseLogger`, posso usar dois loggers ao mesmo tempo em uma linha de código.

```Python
import mlflow
from logger import BaseLogger

logger = BaseLogger()

with mlflow.start_run():
  
  # log parameters
  logger.log_params({"model_class": type(model).__name__})
  logger.log_params({"model": model.get_params()})
  
  # log metrics
  logger.log_metrics(
          {
              "k_best": k_best,
              "score_best": elbow.elbow_score_,
          }
      )
```

### 7.2.5. Compare entre experiementos MLflow

Para comparar entre dois ou mais experimentos, marque as caixas dos experimentos que deseja comparar e clique em Comparar (Compare).

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Você deve ver as comparações de todos os experimentos como abaixo:

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

DagsHub também cria automaticamente gráficos como gráficos de coordenadas paralelas e gráficos de barras para que você possa observar as relações entre os parâmetros e as saídas.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

### 7.2.6. Compare entre experimentos Git

Para comparar a diferença de arquivos entre dois experimentos do Git, copie seus IDs de confirmação na guia Experimentos (Experiments):

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Em seguida, cole cada ID de confirmação em cada ramificação na guia Arquivos (Files):

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Os arquivos que são diferentes entre os dois commits serão destacados em amarelo.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Para ver a diferença, clique nos arquivos. Como as informações ausentes são destacadas em vermelho e as informações adicionais são destacadas em verde, podemos ver claramente a diferença entre os dois commits.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Melhor ainda, o DagsHub fornece uma interface agradável para comparar dois notebooks Jupyter.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Como os cientistas de dados trabalham muito com o Jupyter Notebook, é útil poder comparar as saídas de dois notebooks.

### 7.2.7. Dica Bonus: Criar um pipeline DVC

Às vezes, você pode querer que outras pessoas entendam o fluxo de trabalho do seu projeto (ou seja, como as saídas de um script são usadas para outro script). O DagsHub permite que você crie a visualização do seu fluxo de trabalho de dados por meio do pipeline DVC.

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Para criar um pipeline DVC, comece criando um arquivo `dvc.yaml`. No código abaixo, divido meu fluxo de trabalho em 3 estágios: `process_data`, `segment` e `analyze`. Para cada uma das etapas,

- `cmd` especifica o comando para executar a etapa
- `deps` especifica as dependências da etapa
- `outs` especifica as saídas da etapa
- `metrics` especifica as métricas da etapa

```Yaml
stages:
  process_data:
    cmd: python src/process_data.py
    deps:
    - config/main.yaml
    - data/raw
    - params.yml
    - src/main.py
    - src/process_data.py
    outs:
    - data/intermediate:
        persist: true
  segment:
    cmd: python src/segment.py
    deps:
    - config/main.yaml
    - data/intermediate
    - params.yml
    - src/main.py
    - src/segment.py
    outs:
    - data/final:
        persist: true
    - image:
        persist: true
    - model/cluster.pkl:
        persist: true
    metrics:
    - metrics.csv:
        persist: true
  analyze:
    cmd: python src/run_notebook.py
    deps:
    - notebook/analyze_data.ipynb
    - data/final
```

Todos os arquivos listados como saídas (`outs`) de dunder são armazenados em cache, o que é semelhante ao que acontece quando você usa `dvc add`. É por isso que você não precisa mais usar `dvc add` com esses arquivos.

Agora você pode reproduzir todo o pipeline especificado em `dvc.yaml` executando:

`dvc repro`

Outputs:

```Python
Running stage 'process_data':
> python src/process_data.py
Updating lock file 'dvc.lock'                                                                                                                                                                          
Running stage 'segment':
> python src/segment.py
Updating lock file 'dvc.lock'                                                                                                                                                            
Running stage 'analyze':
> python src/run_notebook.py
Updating lock file 'dvc.lock'
```

Agora, outros poderão reproduzir seus resultados executando o comando dvc repro. Quão conveniente é isso?

Em seguida, execute `dvc push` para enviar todos os arquivos rastreados pelo DVC para o DagsHub. Use `git add` e `git commit` para enviar as alterações no código e nos dados para o GitHub.

Se você for ao seu repositório no DagsHub, deverá ver um bom gráfico interativo de todo o pipeline no DagsHub!

<!-- imagem - ![alt text](./images/image-tbd.png "Title") -->

Você pode obter mais detalhes sobre um nó no gráfico clicando nesse nó. Agora, outras pessoas podem entender seu fluxo de trabalho de dados simplesmente acessando seu repositório no DagsHub.
