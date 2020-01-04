from bs4 import BeautifulSoup
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http = urllib3.PoolManager()

#onde ficarão armzazenados todos os links da busca
links = [] 

#sites que o crawler irá buscar (e atributos importantes para a captura de informações)
#Em todos os sites o período de busca será 01/08/18 até 01/11/18
sites = ['http://g1.globo.com/busca/?q=Fake+News+Intelig%C3%AAncia+Artificial+elei%C3%A7%C3%B5es+SP+2018+Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a&page=1&order=recent&from=2018-08-01T00%3A00%3A00-0300&to=2018-11-01T23%3A59%3A59-0300&species=not%C3%ADcias',
         'https://busca.estadao.com.br/?tipo_conteudo=Not%C3%ADcias&quando=01%2F08%2F2018-01%2F11%2F2018&q=Jo%C3%A3o%20D%C3%B3ria%20M%C3%A1rcio%20Fran%C3%A7a%20Fake%20News%20&editoria%5B%5D=Pol%C3%ADtica&editoria%5B%5D=Geral',
         'https://search.folha.uol.com.br/search?q=Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a+Fake+News+Elei%C3%A7%C3%B5es+SP+2018&periodo=personalizado&sd=01%2F08%2F2018&ed=01%2F11%2F2018&site=todos']
botoes = ['.results__content:last-child > div > a', '.mais-itens:last-child > div > a', '.c-pagination__arrow:last-child > a']
tagLinks = ['.widget--info__text-container:last-child > a', '.link-title', '.c-headline__content:last-child > a']

pegarLinks(sites, botoes, tagLinks) #Método que pegará todos os links de todos os sites

def pegarLinks(site, botao, tagLink):
    #Inicializando navegador
    opts = webdriver.ChromeOptions()
    opts.add_argument("start-maximized")
    opts.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=opts, executable_path='chromedriver.exe')
    
    for i in range(len(site)): #Percorrera todos os sites
        driver.get(site[i]) #Acessando o site
        click = 0 #Variável que contará quantas vezes o botão de "Ver mais" ou semelhante foi clicado
        while click < 4: #Se existir, o botão "Ver mais" será clicado 4 vezes, contabilizando assim 5xNúmero de links padrão de cada site
            try:
                if i == 2: #O site da folha mostra apenas 25 por vez, dessa forma, a cada clique nesse site, temos que armazenar os links
                    for pags in driver.find_elements(By.CSS_SELECTOR, tagLink[i]): 
                        links.append(pags.get_attribute('href'))
                
                driver.execute_script("arguments[0].click();", WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, botao[i]))))#Localizando botão de "ver mais"
                time.sleep(2) #Tempo se 2 seg de espera para evitar erros de carregamento da página
                click += 1 #incremento
            except: #Só cairá aqui se não existe mais botão de "Ver mais"
                break #Sai do while
        
        if i != 2: #O site da folha não precisa passar por aqui por já foi analizada no for anterior
            #Os sites G1 e Estadão mostram todos os resultados, por isso deixamos para fazer a coleta de links agora
            for pags in driver.find_elements(By.CSS_SELECTOR, tagLink[i]): #Percorrerá todos os links para as notícias
                if('https:' in pags.get_attribute('href')):
                    links.append(pags.get_attribute('href'))
                else: # Links do G1 não possuem o 'https:' no início, por isso adicionamos antes do link esse trecho
                    links.append('https:' + pags.get_attribute('href'))
    
    driver.close() # Ao acabar de pegar todos os links de todos os sites, o navegador fecha


