from bs4 import BeautifulSoup
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http = urllib3.PoolManager()
links = [] #onde ficarão armzazenados todos os links da busca

opts = webdriver.ChromeOptions()
opts.add_argument("start-maximized")
opts.add_argument('disable-infobars')
path = 'C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python37\\chromedriver.exe'
driver = webdriver.Chrome(options=opts, executable_path=path)

#pagsG1()
pagsEstadao()

def pagsG1():
    #link de pesquisa no site do G1, já com os filtros ativados
    conteudoPag = http.request('GET', 'http://g1.globo.com/busca/?q=Fake+News+Intelig%C3%AAncia+Artificial'+
                               '+elei%C3%A7%C3%B5es+SP+2018+Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a&page=1&'+
                               'order=recent&from=2018-08-01T00%3A00%3A00-0300&to=2018-11-01T23%3A59%3A59-0300&species=not%C3%ADcias')
    
    sopa = BeautifulSoup(conteudoPag.data, 'lxml')
    linkBase = 'https://g1.globo.com/busca/'
    #Precisamos do link de filtros pois após carregar novos resultados, a página carrega sem os filtros de busca
    linkFiltros = '&order=recent&from=2018-08-01T00%3A00%3A00-0300&to=2018-11-01T23%3A59%3A59-0300&species=not%C3%ADcias'
    continua = True; #Ficará falso quando não houver botão "Ver mais"
    paginasResultado = 0 #Armazena quantas vezes o botão "Ver mais" foi clicado
    
    #Nesse laço, verificamos se a página tem o botão "ver mais", se tiver, ela irá até a página 5
    #se ela não tiver o botão em uma das páginas menores que 5, o laço também será interrompido
    #Laço para o G1
    while(continua and paginasResultado < 4):
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
    for divs in sopa.find_all('div', class_='widget--info__text-container'): #Identificando os links
        links.append('https:' + divs.find('a').get('href'))
        

def pagsEstadao():    
    driver.get('https://busca.estadao.com.br/?tipo_conteudo=Not%C3%ADcias&quando=01%2F08%2F2018-01%2F11%2F2018&q=Jo%C3%A3o%20D%C3%B3ria')
    
    for i in range(4):
        try:
            #"btn-mais" é a classe do botão que quero clicar
            driver.execute_script("arguments[0].click();", WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-mais'))))
            time.sleep(5)
        except:
            break
        
    for pags in driver.find_elements(By.CLASS_NAME, 'link-title'): #Identificando os links
        links.append(pags.get_attribute('href'))
    driver.quit() #fecha a página depois de pegar os links

