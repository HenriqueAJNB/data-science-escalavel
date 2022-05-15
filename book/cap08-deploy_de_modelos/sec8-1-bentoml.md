## BentoML: Crie um serviço de ML para previsão em minutos

### O que é BentoML

[BentoML](https://github.com/bentoml/BentoML) é uma biblioteca de código aberto Python que permite aos usuários criar um modelo de machine learning para previsão em minutos, o que ajuda a preencher a lacuna entre ciência de dados e DevOps.

Para usar a versão do BentoML que será usada nesta seção, digite:

```bash
pip install bentoml==1.0.0a4
```

Para entender como BentoML funciona, ele será usando para servir um modelo que segmenta novos clientes baseado em suas personalidades.

### Processando dados

Primeiro deverá ser baixado o [Customer Personality Analysis](https://www.kaggle.com/imakash3011/customer-personality-analysis) dataset do Kaggle. Depois, os dados serão processados.

Já que será usado `StandardScaler` e `PCA` para processar os novos dados depois, estes transformers do scikit-learn serão salvos em arquivos pickles na pasta `processors`

```python
import pandas as pd 

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pickle

# Scale
scaler = StandardScaler()
scaler.fit(df)
df = pd.DataFrame(scaler.transform(df), columns=df.columns)

# Reduce dimension
pca = PCA(n_components=3)
pca.fit(df)
pca_df = pd.DataFrame(pca.transform(df), columns=["col1", "col2", "col3"])

# Save processors
pickle.dump(scaler, open("processors/scaler.pkl", "wb"))
pickle.dump(scaler, open("processors/PCA.pkl", "wb"))
```

### Salvando Modelos

Depois, será treinado o modelo `KMeans` no dataset processado e o modelo será salvo no repositório de modelo local do BentoML.

```python
from sklearn.cluster import KMeans
import bentoml.sklearn

pca_df = ...

model = KMeans(n_clusters=4)
model.fit(pca_df)

bentoml.sklearn.save("customer_segmentation_kmeans", model)
```

Depois de rodar o código acima, o código será salvo na pasta `~/bentoml/models/`. Todos os modelos salvos podem ser listados rodando o código a seguir: 

```bash
$ bentoml models list
```

Saída:

```bash
Tag                                            Module           Path                                                                       Size       Creation Time       
customer_segmentation_kmeans:o2ztyneoqsnwswyg  bentoml.sklearn  /home/khuyen/bentoml/models/customer_segmentation_kmeans/o2ztyneoqsnwswyg  10.08 KiB  2022-02-15 17:26:51
```

O modelos são versionados com uma tag específica. Se outro modelo for salvo com o memso nome, será atribuída uma tag diferente:

```bash
$ bentoml models list
```

```bash
Tag                                            Module           Path                                                                       Size       Creation Time       
customer_segmentation_kmeans:ye5eeaeoscnwswyg  bentoml.sklearn  /home/khuyen/bentoml/models/customer_segmentation_kmeans/ye5eeaeoscnwswyg  10.08 KiB  2022-02-15 18:54:50
customer_segmentation_kmeans:o2ztyneoqsnwswyg  bentoml.sklearn  /home/khuyen/bentoml/models/customer_segmentation_kmeans/o2ztyneoqsnwswyg  10.08 KiB  2022-02-15 17:26:51
```

Isso é bom já que o versionamento permite retornar a um modelo anterior se houver necessidade.

### Criando Serviços

Agora que o modelo está pronto, será criado um serviço com o último modelo de segmentação de clientes em `bentoml_app_pandas.py`:

```python
import bentoml
import bentoml.sklearn
from bentoml.io import NumpyNdarray, PandasDataFrame

import pickle
import numpy as np
import pandas as pd

# Load model
classifier = bentoml.sklearn.load_runner("customer_segmentation_kmeans:latest")

# Create service with the model
service = bentoml.Service("customer_segmentation_kmeans", runners=[classifier])
```

Após definido o serviço, ele pode ser usado para criar uma função de API:

```python
# Create an API function
@service.api(input=PandasDataFrame(), output=NumpyNdarray())
def predict(df: pd.DataFrame) -> np.ndarray:

    # Process data
    scaler = pickle.load(open("processors/scaler.pkl", "rb"))

    scaled_df = pd.DataFrame(scaler.transform(df), columns=df.columns)

    pca = pickle.load(open("processors/PCA.pkl", "rb"))
    processed = pd.DataFrame(
        pca.transform(scaled_df), columns=["col1", "col2", "col3"]
    )

    # Predict
    result = classifier.run(processed)
    return np.array(result)
```

O decorator `@service.api` declara que a função `predict` é uma API, em que o input é um `PandasDataFrame` e o output é um `NumpyNdarray`.

Agora o serviço será testado em modo debug rodando `bentoml serve`. Como `bentoml_app_pandas.py` está na pasta `src`, será rodado:

```bash
$ bentoml serve src/bentoml_app_pandas.py:service --reload
```

Saída:

```bash
[01:52:13 PM] INFO     Starting development BentoServer from "src/bentoml_app_pandas.py:service"                                                                              
[01:52:17 PM] INFO     Service imported from source: bentoml.Service(name="customer_segmentation_kmeans", import_str="src.bentoml_app_pandas:service",                        
                       working_dir="/home/khuyen/customer_segmentation")                                                                                                      
[01:52:17 PM] INFO     Will watch for changes in these directories: ['/home/khuyen/customer_segmentation']                                                       config.py:342
              INFO     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)                                                                           config.py:564
              INFO     Started reloader process [605974] using statreload                                                                                     basereload.py:56
[01:52:21 PM] INFO     Started server process [606151]                                                                                                            server.py:75
              INFO     Waiting for application startup.                                                                                                               on.py:45
              INFO     Application startup complete.  
```

Agora é possível interagir com a API acessando [http://127.0.0.1:5000](http://127.0.0.1:5000/) and clicando no botão "Try it out"

![](https://miro.medium.com/max/700/1*1gsFwFoaCc7RqTPWwtcNjg.png)

Insira os seguintes valores:

```python
[{"Income": 58138, "Recency": 58, "NumWebVisitsMonth": 2, "Complain": 0,"age": 64,"total_purchases": 25,"enrollment_years": 10,"family_size": 1}]
```

... em Request Body, que deve responder com o valor `1`. Isso significa que o modelo prevê que o cliente com essas características pertence ao cluster 1.

![](https://miro.medium.com/max/700/1*yoa7BCkJjjr9IuwUzW85-Q.gif)

### Criando Modelo de Dados com pydantic

Para ter certeza que os usuários inserirão os valores com os tipos corretos de dados na API, pode ser usado pydantic para criar um modelo de dados customizado:

```python
from bentoml.io import JSON, NumpyNdarray
from pydantic import BaseModel

# Code to create service
...

# Create customer model
class Customer(BaseModel):

    Income: float = 58138
    Recency: int = 58
    NumWebVisitsMonth: int = 7
    Complain: int = 0
    age: int = 64
    total_purchases: int = 25
    enrollment_years: int = 10
    family_size: int = 1

# Create an API function
@service.api(input=JSON(pydantic_model=Customer), output=NumpyNdarray())
def predict(customer: Customer) -> np.ndarray:

    df = pd.DataFrame(customer.dict(), index=[0])

    # Code to process and predict data
    ...
```

Agora os valores padrão poderão ser vistos em Request body.

![](https://miro.medium.com/max/662/1*6eQdlONSzafIOcT6r9kSAQ.png)

### Build Bentos

Depois de ter certeza de que tudo está em ordem, serão colocados o modelo, o serviço e as dependência em um bento.

![](https://miro.medium.com/max/700/1*Q_gi8bLO6NmSXKY-x5D9jg.png)

Para construir bentos, começe criando um arquivo nomeado `bentofile.yaml` no diretório do projeto:

```yaml
service: "src/bentoml_app.py:service"
include:
 - "src/bentoml_app.py"
python:
  packages:
  - numpy==1.20.3
  - pandas==1.3.4
  - scikit-learn==1.0.2
  - pydantic==1.9.0
```

Detalhes sobre o arquivo acima:

-   A seção `include` diz ao BentoML quais arquivos incluir em um bento. Neste arquivo, será incluído `bentoml_app.py` e todos os processadores salvos anteriormente.
-   A seção `python` dia ao BentoML quais pacotes Python que o serviço possui dependência.

Agora está pronto para criar bentos!

```bash
$ bentoml build
```

![](https://miro.medium.com/max/675/1*VxXEGqpddQDN_KGF3zNrcA.png)

O Bentos construído será salvo no diretório `~/bentoml/bentos/<model-name>/<tag>`. Os arquivos no diretório deverão ser similares ao esquema abaixo:

```bash
.
├── apis
│   └── openapi.yaml
├── bento.yaml
├── env
│   ├── conda
│   ├── docker
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   └── init.sh
│   └── python
│       ├── requirements.lock.txt
│       ├── requirements.txt
│       └── version.txt
├── models
│   └── customer_segmentation_kmeans
│       ├── latest
│       └── qb6awgeoswnwswyg
│           ├── model.yaml
│           └── saved_model.pkl
├── README.md
└── src
    ├── processors
    │   ├── PCA.pkl
    │   └── scaler.pkl
    └── src
        ├── bentoml_app.py
        └── streamlit_app.py
```

Muito legal! Foi criado uma pasta com modelo, serviço, preocessadores, requerimentos Python e um Dockerfile em poucas linhas de código!

### Deploy to Heroku

Com o Bentos construído, ele pode ser conteinerizado como uma [imagem Docker](https://docs.bentoml.org/en/latest/concepts/containerize_bentos.html#containerize-bentos-page) ou feito deploy para o Heroku. Aqui será criado um link público para a API, portanto será feito deploy para o Heroku Container Registry.

Faça a instalação do [Heroku](https://www.heroku.com/), então faça login em uma conta Heroku por meio da linha de comando:

```bash
$ heroku login
```

Faça login no Heroku Container Registry:

```bash
$ heroku container:login
```

Crie um app Heroku:

```bash
$ APP_NAME=bentoml-her0ku-$(date +%s | base64 | tr '[:upper:]' '[:lower:]' | tr -dc _a-z-0-9)heroku create $APP_NAME
```

Agora, vá para o diretório do docker no último Bentos construído. Para ver os diretórios onde estão os Bentos, rode:

```bash
$ bentoml list -o json
```

```json
[
  {
    "tag": "customer_segmentation_kmeans:4xidjrepjonwswyg",
    "service": "src.bentoml_app:service",
    "path": "/home/khuyen/bentoml/bentos/customer_segmentation_kmeans/4xidjrepjonwswyg",
    "size": "29.13 KiB",
    "creation_time": "2022-02-16 17:15:01"
  }
]
```

Como último Bentos está em ~/bentoml/bentos/customer_segmentation_kmeans/4xidjrepjonwswyg , deverá ser rodado:

```bash
cd ~/bentoml/bentos/customer_segmentation_kmeans/4xidjrepjonwswyg/env/docker
```

Coloque o Bentos em um container e faça um push para o Heroku app criado acima:

```bash
$ heroku container:push web --app $APP_NAME  --context-path=../..
```

Lance o app:

```bash
$ heroku container:release web --app $APP_NAME
```

O novo app agora deverá estar listado no [Heroku dashboard](https://dashboard.heroku.com/apps):

![](https://miro.medium.com/max/458/1*5az3H_dnTtChHoM_GMh0FQ.png)

Clicando no nome do app e após clicando em "Open app", o app será aberto:

![](https://miro.medium.com/max/442/1*I4egOGqVIEMCV6kXHMj_DA.png)

O link público do serviço de API deste app é [https://bentoml-her0ku-mty0ndg3mza0ngo.herokuapp.com](https://bentoml-her0ku-mty0ndg3mza0ngo.herokuapp.com/).

![](https://miro.medium.com/max/623/1*D-SgFdF7yQKpHJCI5vtWSw.png)

Com um link público, amostras de dados podem ser usadas para realizar solicitações de previsões:

```python
import requests

prediction = requests.post(
    "https://bentoml-her0ku-mty0ndg3mza0ngo.herokuapp.com/predict",
    headers={"content-type": "application/json"},
    data='{"Income": 58138, "Recency": 58, "NumWebVisitsMonth": 2, "Complain": 0,"age": 64,"total_purchases": 25,"enrollment_years": 10,"family_size": 1}',
).text

print(prediction)
```

```bash
2
```

E é isso! Agora este link pode ser enviado aos outros membros do time para que eles construam um web app a partir de um modelo de machine learning. **Nenhuma instalação e configuração** são necessárias para usar o modelo de machine learning. Bem legal, né?

A próxima seção ensinará como criar uma interface simples usando Streamlit.

### Construindo uma UI para o Serviço Usando Streamlit

Para que os gerentes ou stakeholders experimentem o modelo, é interessante construir uma UI simples para o modelo usando [Streamlit](https://streamlit.io/).


No arquivo `streamlit_app.py`, os inputs dos usuários são utilizados para realizar requerimentos de previsões.

```python
import json
import math

import requests
import streamlit as st

st.title("Customer Segmentation Web App")

# ---------------------------------------------------------------------------- #
# Get inputs from user
data = {}

data["Income"] = st.number_input(
    "Income",
    min_value=0,
    step=500,
    value=58138,
    help="Customer's yearly household income",
)
data["Recency"] = st.number_input(
    "Recency",
    min_value=0,
    value=58,
    help="Number of days since customer's last purchase",
)
data["NumWebVisitsMonth"] = st.number_input(
    "NumWebVisitsMonth",
    min_value=0,
    value=7,
    help="Number of visits to companyâ€™s website in the last month",
)
data["Complain"] = st.number_input(
    "Complain",
    min_value=0,
    value=7,
    help="1 if the customer complained in the last 2 years, 0 otherwise",
)
data["age"] = st.number_input(
    "age",
    min_value=0,
    value=64,
    help="Customer's age",
)
data["total_purchases"] = st.number_input(
    "total_purchases",
    min_value=0,
    value=25,
    help="Total number of purchases through website, catalogue, or store",
)
data["enrollment_years"] = st.number_input(
    "enrollment_years",
    min_value=0,
    value=10,
    help="Number of years a client has enrolled with a company",
)
data["family_size"] = st.number_input(
    "family_size",
    min_value=0,
    value=1,
    help="Total number of members in a customer's family",
)

# ---------------------------------------------------------------------------- #
# Make prediction
if st.button("Get the cluster of this customer"):
    if not any(math.isnan(v) for v in data.values()):
        data_json = json.dumps(data)

        prediction = requests.post(
            "https://bentoml-her0ku-mty0ndg3mza0ngo.herokuapp.com/predict",
            headers={"content-type": "application/json"},
            data=data_json,
        ).text
        st.write(f"This customer belongs to the cluster {prediction}")
```

Executando the app Streamlit:

```bash
$ streamlit run src/streamlit_app.py
```

E então acessando [http://localhost:8501](http://localhost:8501/), poderá ser visto um web app como abaixo.

![](https://miro.medium.com/max/662/1*N_d36Qnw-sISy8qH3_v9iw.gif)

O app agora está mais intuitivo para interagir.
