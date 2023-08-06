EntPdf

===========

#### Um script Python que le e traduz arquivos PDF para texto e audio

## Instalaçao:

`pip install EntPdf`

## Uso:

`from EntPdf import main`

`pdf = main.EntPdf()`

## 0 ou 1 indica o que fazer, onde 0 ler uma pagina especifica e 1 a leitura do arquivo todo

`pdf.SayThis(nome_pdf (string), 0 ou 1 (int), numero da pagina (int))`

# Traduzir a pagina, informando numero da pagina e a lingua que deseja traduzir

`pdf.Translator(nome_pdf (string), pagina (int), lingua(string))`
