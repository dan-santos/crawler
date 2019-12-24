from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http = urllib3.PoolManager()

conteudoPag = http.request('GET', 'link') #tirei o link real pra facilitar a visualização

sopa = BeautifulSoup(conteudoPag.data, 'lxml')
linkBase = 'https://g1.globo.com/busca/#'

continua = True;
paginasResultado = 1

#Nesse laço, verificamos se a página tem o botão "ver mais", se tiver, ela irá até a página 5
#se ela não tiver o botão em uma das páginas menores que 5, o laço também será interrompido
#Laço para o G1
while(continua and paginasResultado <= 5):
    conteudo = str(sopa)
    #"load-more" é parte do texto que só a classe do botão "ver mais" tem
    if conteudo.find('load-more') != -1: #se tiver o botão de carregar mais
        linkVar = str(sopa.find('a', class_='fundo-cor-produto pagination__load-more').get('href')) #link do botão
        conteudoPag = http.request('GET', linkBase+linkVar) #pegando conteúdo da página apontada pelo botão
        sopa.append(BeautifulSoup(conteudoPag.data, 'lxml')) #adicionando novo conteúdo a sopa
        paginasResultado += 1 #incrementando contador
    else: #A Não possui botão
        continua = False

#alocando todos os links válidos da sopa        
pags = []
links = []
for divs in sopa.find_all('div', class_='widget--info__text-container'): #Identificando os links
    pags.append(divs.find('a'))
    
for link in pags:
    links.append(link.get('href'))

for tags in sopa(['script', 'style']): #comandos js/tags do css
    tags.decompose() #remover todo o conteúdo da tag
    
conteudo = ' '.join(sopa.stripped_strings)



