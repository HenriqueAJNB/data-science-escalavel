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