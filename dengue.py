#importa bibliotecas de media, mediana e http requests
from statistics import median, mean
import requests

#função para deixar a impressão das respostas bonitinha
def resposta(numero, texto):
    verde = "\033[0;32m"
    branco = "\033[0;0m"
    print(30*"===" + f"{verde}\nQUESTÃO {numero}{branco}: " + texto )

#função que imprime resultados de media ou mediana para cada regiao
def regioesCalculo(MedianOrMean):
    print(f"""Norte: {MedianOrMean([caso.casos_confirmados for caso in norte_reg]):,.2f} casos
Nordeste: {MedianOrMean([caso.casos_confirmados for caso in nordeste_reg]):,.2f} casos
Centro Oeste: {MedianOrMean([caso.casos_confirmados for caso in centro_reg]):,.2f} casos
Sudeste: {MedianOrMean([caso.casos_confirmados for caso in sudeste_reg]):,.2f} casos
Sul: {MedianOrMean([caso.casos_confirmados for caso in sul_reg]):,.2f} casos""")
    
#consome api do ibge para definir regioes do brasil com seus respectivos estados
link_regioes = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/"

norte = [estado['nome'] for estado in requests.get(f"{link_regioes}1/estados").json()]
nordeste = [estado['nome'] for estado in requests.get(f"{link_regioes}2/estados").json()]
centro_oeste = [estado['nome'] for estado in requests.get(f"{link_regioes}5/estados").json()]
sudeste = [estado['nome'] for estado in requests.get(f"{link_regioes}3/estados").json()]
sul = [estado['nome'] for estado in requests.get(f"{link_regioes}4/estados").json()]

#define a classe DengueRegistros e os atributos para o método construtor
class DengueRegistros:
    def __init__(self, estado, ano, casos_confirmados, obitos, taxa_incidencia):
        self.estado = estado
        self.ano = int(ano)
        self.casos_confirmados = int(casos_confirmados)
        self.obitos = int(obitos)
        self.taxa_incidencia = float(taxa_incidencia)

dengue_total = []

with open("dengue.csv", "r") as arquivo:
    dengue_lista = arquivo.readlines() #transforma O dataset em uma lista
    cabecalho = dengue_lista[0].strip("\n").split(";") #cabecario será a primeira linha
    for item in dengue_lista[1:]: 
        linhas = item.strip("\n").split(";") #linhas será a segunda linha em diante
        dengue_dicionario = dict(zip(cabecalho, linhas)) #une cabecario e linhas
        dengue_total.append(DengueRegistros( #instancía o dicionário
            estado = dengue_dicionario['Estado'],
            ano = dengue_dicionario['Ano'],
            casos_confirmados = dengue_dicionario['CasosConfirmados'],
            obitos = dengue_dicionario['Obitos'],
            taxa_incidencia = dengue_dicionario['TaxaIncidencia']))

#filtra instancias dentro de dengue_total para cada regiao
norte_reg = list(filter(lambda registro: registro.estado in norte, dengue_total))
nordeste_reg = list(filter(lambda registro: registro.estado in nordeste, dengue_total)) 
centro_reg = list(filter(lambda registro: registro.estado in centro_oeste, dengue_total)) 
sudeste_reg = list(filter(lambda registro: registro.estado in sudeste, dengue_total)) 
sul_reg = list(filter(lambda registro: registro.estado in sul, dengue_total)) 

maior_obito = max(dengue_total, key=lambda registro: registro.obitos)
media_caso = mean([caso.casos_confirmados for caso in norte_reg])
mediana_caso = median([caso.casos_confirmados for caso in dengue_total if caso.ano == 2021])
mediana_estado_taxa = median([caso.taxa_incidencia for caso in dengue_total])
mediana_estado_obito = median([caso.obitos for caso in dengue_total])

resposta(1, f"O estado com maior número de óbitos é {maior_obito.estado} com o total de {maior_obito.obitos} registros")
resposta(2, f"A média de casos por região é:\n"); regioesCalculo(mean)
resposta(3, f"A mediana de casos confirmados para o ano de 2021 é {mediana_caso}")
resposta(4, f"A mediana de taxa de incidencia dos estados em 2021 é {mediana_estado_taxa}")
resposta(5, f"A mediana de óbitos por dengue dos estados em 2021 é {mediana_estado_obito}")
resposta(6, f"A mediana de casos por região é:\n"); regioesCalculo(median)
