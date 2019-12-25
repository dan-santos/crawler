from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http = urllib3.PoolManager()
links = [] #onde ficarão armzazenados todos os links 

pagsG1()

def pagsG1():
    conteudoPag = http.request('GET', 'http://g1.globo.com/busca/?q=Fake+News+Intelig%C3%AAncia+Artificial+elei%C3%A7%C3%B5es+SP+2018+Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a&page=1&order=recent&from=2018-08-01T00%3A00%3A00-0300&to=2018-11-01T23%3A59%3A59-0300&species=not%C3%ADcias') #tirei o link real pra facilitar a visualização
    
    sopa = BeautifulSoup(conteudoPag.data, 'lxml')
    linkBase = 'https://g1.globo.com/busca/'
    linkFiltros = '&order=recent&from=2018-08-01T00%3A00%3A00-0300&to=2018-11-01T23%3A59%3A59-0300&species=not%C3%ADcias'
    continua = True;
    paginasResultado = 1
    
    #Nesse laço, verificamos se a página tem o botão "ver mais", se tiver, ela irá até a página 5
    #se ela não tiver o botão em uma das páginas menores que 5, o laço também será interrompido
    #Laço para o G1
    while(continua and paginasResultado < 5):
        conteudo = str(sopa)
        #"load-more" é parte do texto que só a classe do botão "ver mais" tem
        if conteudo.find('load-more') != -1: #se tiver o botão de carregar mais
            linkVar = linkBase + sopa.find('a', class_='fundo-cor-produto pagination__load-more').get('href') + linkFiltros #link do botão
            conteudoPag = http.request('GET', linkVar) #pegando conteúdo da página apontada pelo botão
            sopa.append(BeautifulSoup(conteudoPag.data, 'lxml')) #adicionando novo conteúdo a sopa
            paginasResultado += 1 #incrementando contador
        else: #A Não possui botão
            continua = False
    
    #alocando todos os links válidos da sopa        
    pags = []
    
    for divs in sopa.find_all('div', class_='widget--info__text-container'): #Identificando os links
        pags.append(divs.find('a'))
        
    for link in pags:
        links.append('https:' + link.get('href'))



