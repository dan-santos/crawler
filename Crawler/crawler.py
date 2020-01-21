from bs4 import BeautifulSoup
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import nltk
import re
import pymysql

#TODO: Retirar os dois pontos que aparecem depois dos números de engajamento do tweet
#TODO: Verificar se o tamanho da variável que armazenará o tweet é suficiente
#TODO: Gravar Tweets no banco de dados
#TODO: Saber se guardaremos as notícias no banco de dados ou a página html em uma página determinada

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http = urllib3.PoolManager()

#links = list() #onde ficarão armzazenados todos os links da busca em sites de notícias
tweets = list() #onde ficarão armazenados todos os tweets dos dois candidatos

#Nas listas abaixo, ficarão armazenados apenas o conteúdo do tweet de cada candidato, para a análise mais perspicaz
#das temáticas mais abordadas poor cada um
tweetsJoaoDoria = list()
tweetsMarcioFranca = list()

#pegarLinks() #Método que pegará todos os links de todos os sites            
pegarTweets() #Método que pegará todos os tweets (Essa lista servirá apenas para armazenarmos todos os tweets em BD)

#indexarTematicas(tweetsJoaoDoria, 1) #O número é a PK do candidato, pois precisamos contabilizar as temáticas por candidato
#indexarTematicas(tweetsMarcioFranca, 2)

def pegarLinks():
    #sites que o crawler irá buscar (e atributos importantes para a captura de informações)
    #Em todos os sites o período de busca será 01/08/18 até 01/11/18
    sites = ['http://g1.globo.com/busca/?q=Fake+News+Intelig%C3%AAncia+Artificial+elei%C3%A7%C3%B5es+SP+2018+Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a&page=1&order=recent&from=2018-08-01T00%3A00%3A00-0300&to=2018-11-01T23%3A59%3A59-0300&species=not%C3%ADcias',
         'https://busca.estadao.com.br/?tipo_conteudo=Not%C3%ADcias&quando=01%2F08%2F2018-01%2F11%2F2018&q=Jo%C3%A3o%20D%C3%B3ria%20M%C3%A1rcio%20Fran%C3%A7a%20&editoria%5B%5D=Pol%C3%ADtica&editoria%5B%5D=Geral',
         'https://search.folha.uol.com.br/search?q=Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a+Fake+News+Elei%C3%A7%C3%B5es+SP+2018&periodo=personalizado&sd=01%2F08%2F2018&ed=01%2F11%2F2018&site=todos',
         'https://oglobo.globo.com/busca/?q=Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a+Fake+News&species=not%C3%ADcias&page=1']
    botoes = ['.results__content:last-child > div > a', '.mais-itens:last-child > div > a', '.c-pagination__arrow:last-child > a', '.proximo']
    tagLinks = ['.widget--info__text-container:last-child > a', '.link-title', '.c-headline__content:last-child > a', '.species-materia > .cor-produto']
    #Inicializando navegador
    opts = webdriver.ChromeOptions()
    opts.add_argument('start-maximized')
    opts.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=opts, executable_path='chromedriver.exe')
    
    for i in range(len(sites)): #Percorrera todos os sites
        driver.get(sites[i]) #Acessando o site
        click = 0 #Variável que contará quantas vezes o botão de "Ver mais" ou semelhante foi clicado
        while click < 4: #Se existir, o botão "Ver mais" será clicado 4 vezes, contabilizando assim 5xNúmero de links padrão de cada site
            try:
                if i == 2: 
                    #O site da folha mostra apenas 25 por vez, dessa forma, a cada clique nesse site, temos que armazenar os links
                    for pags in driver.find_elements(By.CSS_SELECTOR, tagLinks[i]): 
                        links.append(pags.get_attribute('href'))
                elif i == 3: 
                    #O site o globo só mostra 10 resultados por vez, e, além disso, não pos possui filtro de busca com datas
                    # Graças a isso, deveremos verificar se a notícia está no intervalo pretendido.
                    # Ademais, mesmo após os resultados tendo se esgotado, o botão de próximo continua sendo válido para clique, por isso
                    # antes de armazenar o link, devemos verificar se ele já não foi inserido (O conflito acontece na último página de resultados)
                    dataInicio = datetime.date(2018, 8, 1)
                    dataFim = datetime.date(2018, 11, 1)
                    dataNoticia = list()
                    #Localizando datas
                    for datas in driver.find_elements(By.CSS_SELECTOR, '.tempo-decorrido'):
                        data = datas.text.strip() #tirando possíveis espaços em branco
                        data = data[:10] #tirando hora e deixando só a data
                        data = datetime.date(int(data[6:]), int(data[3:5]), int(data[:2]))#Pegando texto e tranformando em data
                        if dataInicio <= data <= dataFim: #Definindo se a data é válida
                            dataNoticia.append(True)
                        else:
                            dataNoticia.append(False)
                    
                    j = 0 #contador
                    for pags in driver.find_elements(By.CSS_SELECTOR, tagLinks[i]):
                        if pags.get_attribute('href') not in links and dataNoticia[j] == True: #se o link ainda não existe dentro da lista e a respectiva data é válida
                            links.append(pags.get_attribute('href'))
                        j += 1
                
                driver.execute_script('arguments[0].click();', WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, botoes[i]))))#Localizando botão de "ver mais"
                time.sleep(2) #Tempo se 2 seg de espera para evitar erros de carregamento da página
                click += 1 #incremento
                
            except: #Só cairá aqui se não existe mais botão de "Ver mais"
                break #Sai do while
        
        if i < 2: #O site da folha não precisa passar por aqui por já foi analizada no for anterior
            #Os sites G1 e Estadão mostram todos os resultados, por isso deixamos para fazer a coleta de links agora
            for pags in driver.find_elements(By.CSS_SELECTOR, tagLinks[i]): #Percorrerá todos os links para as notícias
                links.append(pags.get_attribute('href'))
    
    driver.close() # Ao acabar de pegar todos os links de todos os sites, o navegador fecha


def pegarTweets():
    perfisTwitter = ['https://twitter.com/search?f=tweets&vertical=default&q=since%3A2018-10-26%20until%3A2018-11-01%20from%3Ajdoriajr&src=unkn',
         'https://twitter.com/search?f=tweets&vertical=default&q=since%3A2018-10-26%20until%3A2018-11-01%20from%3Amarciofrancagov&src=unkn']

    tagLinks = ['.content', #Tweet inteiro
            ' > div[class="js-tweet-text-container"] > p', #Conteúdo escrito do tweet
            '.js-actions'] #curtidas, retweets e repostas
    opts = webdriver.ChromeOptions()
    opts.add_argument('start-maximized')
    opts.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=opts, executable_path='chromedriver.exe')
    posicaoTweet = 0
    posicaoEngajamento = 0
    
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
                
            
        for tweet in driver.find_elements(By.CSS_SELECTOR, tagLinks[0]): #pegar todos os tweets
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
        
        #Adicionando o conteúdo do tweet
        for tweet in driver.find_elements(By.CSS_SELECTOR, tagLinks[0]+tagLinks[1]):
            tweets[posicaoTweet] += '\n\n"' + tweet.text + '"\n\n'
            posicaoTweet += 1
            if i == 0:
                tweetsJoaoDoria.append(tweet.text)
            else:
                tweetsMarcioFranca.append(tweet.text)
                
        #Adicionando o engajamento do tweet
        for tweet in driver.find_elements(By.CSS_SELECTOR, tagLinks[2]):
            tweets[posicaoEngajamento] += tweet.text.strip().replace('\n', ': ')
            posicaoEngajamento += 1
           
            
        if i == 2:
            driver.close()
            
            
def indexarTematicas(listaTweets, candidato):
    for tweet in listaTweets:
        palavraIndexada(separaPalavras(tweet), candidato)
            
            
def separaPalavras(texto): #Vai pegar o texto dos tweets para contabilizar a quantidade de palavras mais repetidas por cada candidato
    stopWords = nltk.corpus.stopwords.words('portuguese')
    stopWordsNaoListadas = ['joão', 'dória', 'márcio', 'frança', 'é', 'https', 'www', 'obrigado', 'são', 'paulo', 'pessoal', 'vamos']
    stopWords.append(stopWordsNaoListadas[:])
    
    splitter = re.compile('\\W+') #Pega todas as paçavras que tenham a-zA-z0-9_
    listaPalavras = list()
    lista = [p for p in splitter.split(texto) if p != ''] #pegando todos os termos do tweet
    
    for palavra in lista: #Pegando palavras que não são stopwords e nem espaços em branco
        if palavra.lower() not in stopWords and len(palavra) > 1:
            listaPalavras.append(palavra.lower())
    return listaPalavras

                        
#verificando se a palavra existe no bd, se exitir, incrementa +1. senão, grava
def palavraIndexada(palavras, candidato):
    conexao = pymysql.connect(host='localhost', user='root', passwd='fsociety', db='eleicoes', use_unicode = True, charset = 'utf8mb4', autocommit = True)
    cursorUrl = conexao.cursor()
    
    for palavra in palavras:
        cursorUrl.execute(f'select (ID_Tematica) from tematicas where Nome_Tematica = "{palavra}" and ID_Candidato = {candidato}')
        if cursorUrl.rowcount > 0: #se retornou algum resultado
            idPalavra = cursorUrl.fetchone()[0]
            cursorUrl.execute(f'select (Quantidade_Tematica) from tematicas where ID_Tematica = {idPalavra}')
            qtd = 1 + cursorUrl.fetchone()[0] #fetchone()[0] = pega o primeiro reultado retornado
            print(f'ATUALIZEI A QTD DA PALAVRA "{palavra.strip()}" PARA {qtd}')
            cursorUrl.execute(f'update tematicas set Quantidade_Tematica = {qtd} where ID_Tematica = {idPalavra}')
        else:
            cursorUrl.execute(f'insert into tematicas (ID_Candidato, Nome_Tematica, Quantidade_Tematica) values ({candidato}, "{palavra.strip()}", {1})') #FK do candidato, Nome, Quantidade
        print(f'GRAVEI A PALAVRA "{palavra.strip()}"')
        
    cursorUrl.close()
    conexao.close()                