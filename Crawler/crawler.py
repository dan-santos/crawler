from bs4 import BeautifulSoup
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http = urllib3.PoolManager()

links = list() #onde ficarão armzazenados todos os links da busca em sites de notícias
tweets = list() #onde ficarão armazenados todos os tweets dos dois candidatos

#sites que o crawler irá buscar (e atributos importantes para a captura de informações)
#Em todos os sites o período de busca será 01/08/18 até 01/11/18
sites = ['http://g1.globo.com/busca/?q=Fake+News+Intelig%C3%AAncia+Artificial+elei%C3%A7%C3%B5es+SP+2018+Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a&page=1&order=recent&from=2018-08-01T00%3A00%3A00-0300&to=2018-11-01T23%3A59%3A59-0300&species=not%C3%ADcias',
         'https://busca.estadao.com.br/?tipo_conteudo=Not%C3%ADcias&quando=01%2F08%2F2018-01%2F11%2F2018&q=Jo%C3%A3o%20D%C3%B3ria%20M%C3%A1rcio%20Fran%C3%A7a%20Fake%20News%20&editoria%5B%5D=Pol%C3%ADtica&editoria%5B%5D=Geral',
         'https://search.folha.uol.com.br/search?q=Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a+Fake+News+Elei%C3%A7%C3%B5es+SP+2018&periodo=personalizado&sd=01%2F08%2F2018&ed=01%2F11%2F2018&site=todos']
botoes = ['.results__content:last-child > div > a', '.mais-itens:last-child > div > a', '.c-pagination__arrow:last-child > a']
tagLinks = ['.widget--info__text-container:last-child > a', '.link-title', '.c-headline__content:last-child > a']

#pegarLinks(sites, botoes, tagLinks) #Método que pegará todos os links de todos os sites

#tiramos os links inicialmente alocados na lista para usá-las novamente procurando os tweets
sites.clear()
tagLinks.clear()
sites = ['https://twitter.com/search?f=tweets&vertical=default&q=since%3A2018-08-01%20until%3A2018-11-01%20from%3Ajdoriajr&src=unkn',
         'https://twitter.com/search?f=tweets&vertical=default&q=since%3A2018-08-01%20until%3A2018-11-01%20from%3Amarciofrancagov&src=unkn']

tagLinks = ['.content', #Tweet inteiro
            ' > div[class="js-tweet-text-container"] > p'] #Conteúdo escrito do tweet
            
pegarTweets(sites, tagLinks)

def pegarLinks(site, botao, tagLink):
    #Inicializando navegador
    opts = webdriver.ChromeOptions()
    opts.add_argument('start-maximized')
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
                
                driver.execute_script('arguments[0].click();', WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, botao[i]))))#Localizando botão de "ver mais"
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


def pegarTweets(perfisTwitter, tagLink):
    opts = webdriver.ChromeOptions()
    opts.add_argument('start-maximized')
    opts.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=opts, executable_path='chromedriver.exe')
    posicaoTweet = 0
    
    for i in range(len(perfisTwitter)): #Percorrera o perfil dos dois candidatos
        driver.get(perfisTwitter[i]) #`Pega o link de pesquisa avançada
        last_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            try:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(1)
                new_height = driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height: 
                    #Se após o scroll a altura da página permanecer a mesma, é porque chegamos ao final
                    #pois o Twitter carrega novos resultados quando a tela chega no fim da página
                    break
                last_height = new_height
            except:
                break
                
            
        for tweet in driver.find_elements(By.CSS_SELECTOR, tagLink[0]): #pegar todos os tweets
            if i == 0: #Marcio França
                if ' retweetou ' in tweet.text: #retweet
                    tweets.append(tweet.text[:10] + '(' + tweet.text[29:38] + '), em ' + tweet.text[39:56] + 
                                  ', em resposta à menção de ' + tweet.text[83:tweet.text.index('\n', 83)] + ', tweetou: ')
                elif 'Em resposta a' in tweet.text: #twwet de resposta
                    tweets.append(tweet.text[:10] + '(' + tweet.text[29:38] + '), em ' + tweet.text[39:56] + 
                                  ', tweetou em resposta a ' + tweet.text[tweet.text.index('@', 38):tweet.text.index('\n', 77)] + ': ')
                else: #tweet normal
                    tweets.append(tweet.text[:10] + '(' + tweet.text[29:38] + '), em ' + tweet.text[39:56] + ', tweetou: ')
            else:
                if ' retweetou ' in tweet.text: #retweet
                    tweets.append(tweet.text[:13] + '(' + tweet.text[32:48] + '), em ' + tweet.text[49:66] +
                                  ', tweetou em resposta à menção de ' + tweet.text[93:tweet.text.index('\n', 93)] + ', tweetou: ')
                elif 'Em resposta a' in tweet.text: #Tweet de resposta. Temos que guardar também o user da pessoa que está sendo respondida
                    tweets.append(tweet.text[:13] + '(' + tweet.text[32:48] + '), em ' + tweet.text[49:66] + 
                                  ', tweetou em resposta a ' + tweet.text[tweet.text.index('@', 48):tweet.text.index('\n', 87)] + ': ') #pegando @ do perfil que o candidato está respondendo
                else:
                    tweets.append(tweet.text[:13] + '(' + tweet.text[32:48] + '), em ' + tweet.text[49:66] + ', tweetou: ')
                
        
        for tweet in driver.find_elements(By.CSS_SELECTOR, tagLink[0]+tagLink[1]):
            tweets[posicaoTweet] += tweet.text
            posicaoTweet += 1
            
            
        if i == 1:
            driver.close()
                