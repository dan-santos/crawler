from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import nltk
import re
import pymysql

<<<<<<< HEAD
=======

>>>>>>> 1b8378262e546af4af3ad2c3e35b35af1b766ba6
links = list() #onde ficarão armzazenados todos os links da busca em sites de notícias
titulos = list() #onde ficarão armazenados os títulos das notícias
relevancia = list() #onde ficará armazenada a relevancia da noticia

tweets = list() #onde ficarão armazenados todos os tweets dos dois candidatos

#Nas listas abaixo, ficarão armazenados apenas o conteúdo do tweet de cada candidato, para a análise mais perspicaz
#das temáticas mais abordadas poor cada um
tweetsJoaoDoria = list()
tweetsMarcioFranca = list()

pegarLinks()
indexarNoticias(links)
pegarTweets()
indexarTweet(tweets)
indexarTematicas(tweetsJoaoDoria, 1)
indexarTematicas(tweetsMarcioFranca, 2)
    
recuperarTweets()

def recuperarTweets():
    """
    Abre conexão com o MySQL e retorna o contéudo de todos os tweets dos dois candidatos
    Também calcula a média de interações por tweet que cada candidato obteve (resultados disponíveis nos arquivos de texto
    presentes neste mesmo respositório com o nome "Média de interações por tweet - Candidato")

    :return: void/nulo
    """
    #
    mediaEngajamentoJD = 0.0
    mediaEngajamentoMF = 0.0

    conexao = pymysql.connect(host='localhost', user='root', passwd='fsociety', db='eleicoes', use_unicode = True, charset = 'utf8mb4', autocommit = True)
    cursorUrl = conexao.cursor()
    cursorUrl.execute('select (Conteudo_Tweet) from tweets')
<<<<<<< HEAD
    resultados = cursorUrl.fetchall()
    tweets = list(resultados)
    
    mediaEngajamentoMF = 0
    mediaEngajamentoJD = 0
    
=======
    resultados = cursorUrl.fetchall() #captura todos os resultados retornados no select
    tweets = list(resultados) #transforma os resultados em composnentes e uma lista
        
>>>>>>> 1b8378262e546af4af3ad2c3e35b35af1b766ba6
    for i, tweet in enumerate(tweets):
        #As seguintes linhas (até o primeiro if) são responsáveis por capturar os números de respostas, retweets e curtidas
        #de cada tweet e tranformá-los em valores inteiros através do método formatar()

        respostas = tweet[0][tweet[0].index('Respostas: ')+11:tweet[0].index(' Retweets: ')]
        resp = formatar(respostas)
        retweets = tweet[0][tweet[0].index('Retweets: ')+10:tweet[0].index(' Curtidas: ')]
        retw = formatar(retweets)
        curtidas = tweet[0][tweet[0].index('Curtidas: ')+10:]
        curt = formatar(curtidas)
        
<<<<<<< HEAD
        if i <= 636:
            mediaAntigaJD = mediaEngajamentoJD
            mediaEngajamentoJD = ((resp+retw+curt) + mediaEngajamentoJD)
            arquivoJD = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento1.txt', 'r', encoding='UTF-8')
            conteudoJD = arquivoJD.readlines()
            conteudoJD.append(f'({resp+retw+curt} + {mediaAntigaJD}) = {mediaEngajamentoJD}\n')
            
            arquivoJD = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento1.txt', 'w', encoding='UTF-8')
            arquivoJD.writelines(conteudoJD)
            arquivoJD.close()
        else:
            mediaAntigaMF = mediaEngajamentoMF
            mediaEngajamentoMF = ((resp+retw+curt) + mediaEngajamentoMF)
            arquivoMF = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento2.txt', 'r', encoding='UTF-8')
            conteudoMF = arquivoMF.readlines()
            conteudoMF.append(f'({resp+retw+curt} + {mediaAntigaMF}) = {mediaEngajamentoMF}\n')
=======
        if i <= 636: # 0 <= i <= 636 -> Tweets do candidato João Dória
            mediaAntiga = mediaEngajamentoJD
            mediaEngajamentoJD = ((resp+retw+curt) + mediaEngajamentoJD)/2
            arquivo = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento1.txt', 'r', encoding='UTF-8')
            conteudo = arquivo.readlines()
            conteudo.append(f'({resp+retw+curt} + {mediaAntiga})/2 = {mediaEngajamentoJD}\n')
            
            arquivo = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento1.txt', 'w', encoding='UTF-8')
            arquivo.writelines(conteudo)
            arquivo.close()
        else: # i > 636 -> Tweets dos candidato Márcio França
            mediaAntiga = mediaEngajamentoMF
            mediaEngajamentoMF = ((resp+retw+curt) + mediaEngajamentoMF)/2
            arquivo = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento2.txt', 'r', encoding='UTF-8')
            conteudo = arquivo.readlines()
            conteudo.append(f'({resp+retw+curt} + {mediaAntiga})/2 = {mediaEngajamentoMF}\n')
>>>>>>> 1b8378262e546af4af3ad2c3e35b35af1b766ba6
            
            arquivoMF = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento2.txt', 'w', encoding='UTF-8')
            arquivoMF.writelines(conteudoMF)
            arquivoMF.close()
            
        
    arquivoJD = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento1.txt', 'r', encoding='UTF-8')
    conteudoJD = arquivoJD.readlines()
    conteudoJD.append(f'({mediaEngajamentoJD}/636) = {mediaEngajamentoJD/636}\n')
    arquivoJD = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento1.txt', 'w', encoding='UTF-8')
    arquivoJD.writelines(conteudoJD)
    arquivoJD.close()
    
    arquivoMF = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento2.txt', 'r', encoding='UTF-8')
    conteudoMF = arquivoMF.readlines()
    conteudoMF.append(f'({mediaEngajamentoMF}/1071) = {mediaEngajamentoMF/1071}\n')
    arquivoMF = open('C:/Users/danie/Documents/USP/IC/Crawler/Engajamento2.txt', 'w', encoding='UTF-8')
    arquivoMF.writelines(conteudoMF)
    arquivoMF.close()
            
    cursorUrl.close()
    conexao.close()
    
    
def formatar(texto):
    """
    Função responável por tranformar os valores contidos nas variáveis de retweet, curtidas e respostas em números inteiros
    :param texto: número em formato de string
    :return: número em formato de float (real)
    """
    texto = texto.strip()
    if texto == '':
        texto = '0'
    if 'mil' in texto:
        texto = texto.replace('mil','')
        texto = texto.replace(',','.')
        texto = texto.strip()
        texto = float(texto)
        txt = float(texto*1000)
        return txt
    else:    
        txt = float(texto)
        return txt
    
    

def pegarLinks():
    """
    Esse método possui a função de percorrer os sites do G1, Estadão, Folha de SP e O GLobo, respectivamente.
    Para cada site, a função pegará todos os links e títulos das notícias presentes em até as 5 primeiras páginas de
    resultados da busca (já configurada nos próprios links da lista "sites". O número de resultados de cada página não
    é padronizado, por se tratarem de empresas diferentes, então é natural obter mais links em um domínio do que em outro.
    Também vai ser armazenada a página na qual a notícia foi captura, para representar a relevância que a notícia tem em
    relação à pesquisa com os filtros aplicados.

    O intervalo de datas estabelecido é de 01/08/2018 até 01/11/2018
    As palavras chave mudam de acordo com o site por um princípio de expansão da obtenção de dados, no qual pode ser verificado
    na planilha "Crawler - Levantamento de dados" localizada no mesmo diretório que este código

    :return: void/nulo
    """
    sites = ['http://g1.globo.com/busca/?q=Fake+News+Intelig%C3%AAncia+Artificial+elei%C3%A7%C3%B5es+SP+2018+Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a&page=1&order=recent&from=2018-08-01T00%3A00%3A00-0300&to=2018-11-01T23%3A59%3A59-0300&species=not%C3%ADcias',
         'https://busca.estadao.com.br/?tipo_conteudo=Not%C3%ADcias&quando=01%2F08%2F2018-01%2F11%2F2018&q=Jo%C3%A3o%20D%C3%B3ria%20M%C3%A1rcio%20Fran%C3%A7a%20&editoria%5B%5D=Pol%C3%ADtica&editoria%5B%5D=Geral',
         'https://search.folha.uol.com.br/search?q=Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a+Fake+News+Elei%C3%A7%C3%B5es+SP+2018&periodo=personalizado&sd=01%2F08%2F2018&ed=01%2F11%2F2018&site=todos',
         'https://oglobo.globo.com/busca/?q=Jo%C3%A3o+D%C3%B3ria+M%C3%A1rcio+Fran%C3%A7a&species=not%C3%ADcias&page=1']

    #tags css dos botões de "próximo, ver mais, próxima página" ou semelhante
    botoes = ['.results__content:last-child > div > a', '.mais-itens:last-child > div > a', '.c-pagination__arrow:last-child > a', '.proximo']

    #tags css dos links das notícias
    tagLinks = ['.widget--info__text-container:last-child > a', '.link-title', '.c-headline__content:last-child > a', '.species-materia > .cor-produto']

    #tags dos títulos das notícias
    tagTitulos = ['.widget--info__title', '.third', '.c-headline__title', '.species-materia > .cor-produto']

    #Inicializando navegador
    opts = webdriver.ChromeOptions()
    opts.add_argument('start-maximized')
    opts.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=opts, executable_path='chromedriver.exe')
    
    for i in range(len(sites)): #Percorrera todos os quatro sites
        driver.get(sites[i]) #Acessando o site
        click = 0 #Variável que contará quantas vezes o botão de "Ver mais" ou semelhante foi clicado
        while click < 5: #Se existir, o botão "Ver mais" será clicado 4 vezes, contabilizando assim 5xNúmero de links padrão de cada site
            try:
                if i == 2: 
                    #O site da folha mostra apenas 25 por vez, dessa forma, a cada clique nesse site, temos que armazenar os links
                    for pags in driver.find_elements(By.CSS_SELECTOR, tagLinks[i]): #capturando links
                        links.append(pags.get_attribute('href'))
                        relevancia.append(click+1) #relevância é sempre o número da váriável click + 1
                    for titulo in driver.find_elements(By.CSS_SELECTOR, tagTitulos[i]): #capturando títulos
                        titulos.append(titulo.text)
                        
                elif i == 3: 
                    """
                    O site "O Globo" só mostra 10 resultados por vez, e, além disso, não possui filtro de busca com datas
                    Devido a isso, deveremos verificar se a notícia está no intervalo pretendido (01/08/2018 até 01/11/2018)
                    Ademais, mesmo após os resultados tendo esgotado-se, o botão de "próximo" continua sendo válido para clique,
                    fazendo o algoritmo capturar mais de uma vez os links da última página, por isso, antes de armazenar o link, 
                    devemos verificar se ele já não foi inserido (O conflito acontece na último página de resultados)
                    """
                    #definindo limite de datas
                    dataInicio = datetime.date(2018, 8, 1)
                    dataFim = datetime.date(2018, 11, 1)
                    dataNoticia = list()

                    #Localizando datas
                    for datas in driver.find_elements(By.CSS_SELECTOR, '.tempo-decorrido'):
                        data = datas.text.strip() #tirando possíveis espaços em branco
                        data = data[:10] #tirando hora e deixando só a data
                        data = datetime.date(int(data[6:]), int(data[3:5]), int(data[:2]))#Pegando texto e tranformando em data
                        if dataInicio <= data <= dataFim: #Definindo se a data de publicação da notícia é válida
                            dataNoticia.append(True)
                        else:
                            dataNoticia.append(False)
                    
                    j = 0 #contador
                    for pags in driver.find_elements(By.CSS_SELECTOR, tagLinks[i]): #evitando inserção das mesmas notícias
                        if pags.get_attribute('href') not in links and dataNoticia[j] == True: #se o link ainda não existe dentro da lista e a respectiva data é válida
                            links.append(pags.get_attribute('href'))
                            titulos.append(pags.text)
                            relevancia.append(click+1)
                        j += 1
                    
                #independente de qual site estamos trabalhando, a linha abaixo realiza o clique para a próxima página de resultados
                driver.execute_script('arguments[0].click();', WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, botoes[i])))) #Localizando botão de "ver mais"
                time.sleep(2) #Tempo se 2 seg de espera para evitar erros de carregamento da página
                click += 1 #incremento
                
            except: #Só cairá aqui se não existe mais botão de "Ver mais"
                break #Sai do while
        
        if i < 2: #Os veículos "Folha de SP" e "O globo" não precisam passar por aqui pois a captura dos dados já foi realizada no for anterior
            #Os sites "G1" e "Estadão" mostram todos os resultados, por isso deixamos para fazer a coleta de links abaixo
            for j, pags in enumerate(driver.find_elements(By.CSS_SELECTOR, tagLinks[i])): #Percorrerá todos os links para as notícias
                links.append(pags.get_attribute('href'))
                #Como não há como paginar, definimos a relevância da notícia de acordo com a sua posição dentro da página
                if i == 0: # G1
                    if j <= 15:
                        relevancia.append(1)
                    elif j <= 30:
                        relevancia.append(2)
                    elif j <= 45:
                        relevancia.append(3)
                    elif j <= 60:
                        relevancia.append(4)
                    else:
                        relevancia.append(5)
                else: # Estadão
                    if j <= 10:
                        relevancia.append(1)
                    elif j <= 20:
                        relevancia.append(2)
                    elif j <= 30:
                        relevancia.append(3)
                    elif j <= 40:
                        relevancia.append(4)
                    else:
                        relevancia.append(5)
                    
            for titulo in driver.find_elements(By.CSS_SELECTOR, tagTitulos[i]): 
                titulos.append(titulo.text)
    
    driver.close() # Ao acabar de pegar todos os links de todos os sites, o navegador fecha
    
    
def indexarNoticias(noticias):
    """
    Grava todas as notícias (link, título e relevância) no banco de dados
    :param noticias: list composta pelos links das notícias
    :return: void/nulo
    """
    conexao = pymysql.connect(host='localhost', user='root', passwd='fsociety', db='eleicoes', use_unicode = True, charset = 'utf8mb4', autocommit = True)
    cursorUrl = conexao.cursor()
    
    # As listas de links das noticias, titulos e relevancia possuem o mesmo tamanho
    print('INDEXANDO NOTÍCIAS')
    for i in range(len(noticias)):
        cursorUrl.execute('insert into noticias (Titulo_Noticia, Link_Noticia, Relevancia_Noticia)'
                          +' values (%s, %s, %s)', (titulos[i], links[i], relevancia[i]))
        
    cursorUrl.close()
    conexao.close()


def pegarTweets():
    """
    Essa função pega por completo o conteúdo textual feito pelos dois candidatos no intervalo de tempo já citado.
    Ela é capaz de identificar se o tweet é realmente um tweet direcionado a todos os seguidores, se
    é direcionado a outro User do Twitter como resposta ou é um retweet.

    Esse trecho do código está sujeito a não funcionar da maneira correta, pois por um bug do próprio Twitter,
    a rede social pode abrir a página com dois layouts diferentes, e a função só está preparada para receber um deles.

    Além disso, o layout no qual a função não se adapta também possui falhas na captura de tags, isto é, elementos
    iguais da página, por vezes, possuem tags css diferentes, o que impossibilita a captura de todos os tweets da
    forma correta.

    Após uma pesquisa, averiguou-se que no ano de 2019 o Twitter passou por uma
    mudança de layout, o que não justifica, mas elucida a possível origem do bug de dos layouts diferentes para o mesmo link.

    Como não é possível fazer de forma viável e suficientemente legível a captura de todos os dados pretendidos do tweet
    - data, categoria, conteúdo e engajamento - a função terá que percorrer todos os tweets um total de 3 vezes (data e
    categoria são obtidos no mesmo laço).
    :return: void/null
    """

    #links dos tweets já com os filtros de busca aplicados
    perfisTwitter = ['https://twitter.com/search?f=tweets&vertical=default&q=since%3A2018-08-01%20until%3A2018-11-01%20from%3Ajdoriajr&src=unkn',
         'https://twitter.com/search?f=tweets&vertical=default&q=since%3A2018-08-01%20until%3A2018-11-01%20from%3Amarciofrancagov&src=unkn']

    tagLinks = ['.content', #Tweet inteiro
            ' > div[class="js-tweet-text-container"] > p', #Conteúdo escrito do tweet
            '.js-actions'] #curtidas, retweets e repostas

    # Abrindo navegador
    opts = webdriver.ChromeOptions()
    opts.add_argument('start-maximized')
    opts.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=opts, executable_path='chromedriver.exe')

    # As seguintes variáveis serão utilizadas como referencial da posição de cada tweet para a iteração dos laços necessários
    posicaoTweet = 0
    posicaoEngajamento = 0

    # Percorrere o perfil dos dois candidatos
    for i in range(len(perfisTwitter)):
        driver.get(perfisTwitter[i]) # Pega o link de pesquisa avançada

        """ O proxímo laço é responsável por verificar se o crawler chegou ao fim da página
         Como os tweets vão sendo carregados conforme o scroll-down da pagina, o cálculo se dá pela seguinte lógica:
         Se a altura antes do crawler chegar no fim da página = altura da pag depois do crawler chegar ao fim da página, então,
         realmente o final da página chegou e podemos começar a capturar o conteúdo dos tweets """

        last_height = driver.execute_script('return document.body.scrollHeight')
        time.sleep(2) # Espera de dois segundos para certificar que todos os compontentes da página foram corretamente carregados
        while True:
            try:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3)
                new_height = driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height: 
                    #Se após o scroll a altura da página permanecer a mesma, é porque chegamos ao final
                    break
                last_height = new_height
            except:
                break
                
        print(f'PEGANDO TWEETS DO {i+1}º CANDIDATO...')
        for tweet in driver.find_elements(By.CSS_SELECTOR, tagLinks[0]): #pegar todos os tweets
            if i == 0: # João Dória
                if ' retweetou ' in tweet.text: #retweet
                    tweets.append(tweet.text[:10] + '(' + tweet.text[29:38] + '), em ' + tweet.text[39:56] + 
                                  ', em resposta à menção de ' + tweet.text[83:tweet.text.index('\n', 83)] + ', tweetou: ')
                elif 'Em resposta a' in tweet.text: #tweet de resposta
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
        
        print('ADICIONANDO CORPO PRINCIPAL DOS TWEETS...')
        #Adicionando o conteúdo do tweet
        for tweet in driver.find_elements(By.CSS_SELECTOR, tagLinks[0]+tagLinks[1]):
            tweets[posicaoTweet] += '\n\n\"' + tweet.text.strip() + '\"\n\n'
            posicaoTweet += 1
            if i == 0:
                tweetsJoaoDoria.append(tweet.text.strip())
            else:
                tweetsMarcioFranca.append(tweet.text.strip())
                
        print('ADICIONANDO ENGAJAMENTO AOS TWEETS...')
        #Adicionando o engajamento do tweet
        for tweet in driver.find_elements(By.CSS_SELECTOR, tagLinks[2]):
            texto = tweet.text.strip().replace('\n', '') #Tirando as quebras de linhas
            #Aprimorando a visualização dos dados recolhidos
            texto = texto.replace('Responder', 'Respostas: ') 
            texto = texto.replace('Retweetar', ' Retweets: ')
            texto = texto.replace('Curtir', ' Curtidas: ')
            tweets[posicaoEngajamento] += texto #Adicionando texto de engajamento ao resto do tweet
            posicaoEngajamento += 1  
            
        if i == 1: #Quando percorrer os dois perfis, o browser fecha
            driver.close()
            
            
def indexarTematicas(listaTweets, candidato):
    """
    Função responsável por chamar o indexador de palavras para cada tweet da lista anteriormente capturada

    :param listaTweets: list composta por apenas o conteúdo de todos os tweets dos candidatos (sem cabeçalho e interações)
    :param candidato: int que indica qual o ID do candidato
    1 - João Dória
    2 - Márcio França
    * A escolha do ID foi feita por ordem alfabética
    :return: void/nulo
    """
    for tweet in listaTweets:
        palavraIndexada(separaPalavras(tweet), candidato)
            
            
def separaPalavras(texto):
    """
    Pega o texto do tweet, separa as palavras, desconsidera as stopwords e retorna uma lista contendo todas as palavras
    que restaram.
    :param texto: string - Conteúdo do tweet
    :return: list - palavras que não são stopwords
    """
    stopWords = nltk.corpus.stopwords.words('portuguese')
    #StopWords que não estão listadas na lista acima:
    stopWordsNaoListadas = ['joão', 'dória', 'joao', 'doria', 'márcio', 'frança', 'marcio', 'franca', 'https', 'www', 'capital', 
                            'obrigado', 'paulo', 'pessoal', 'vamos', 'márciofrança40', 'onovogovernador40', 'acelerasp', 'mil',
                            'aquitempalavra40', 'vote45', 'doriagovernador', 'bolsodoria', 'joãodoria45', '40', 'paulo', 'equipemárciofrança',
                            'palavra', 'joãotrabalhador', 'fazer', 'vamos', 'ser', 'ter', 'têm', 'havia', 'último', 'boa', 'dia',
                            'acerca', 'agora', 'algumas', 'alguns', 'ali', 'ambos', 'antes', 'apontar', 'aqui', 'atrás', 'bem',
                            'bom', 'cada', 'caminho', 'cima', 'comprido', 'conhecido', 'corrente', 'debaixo', 'dentro', 'desde',
                            'ligado', 'deve', 'devem', 'deverá', 'diz', 'dizer', 'dois', 'dose', 'enquanto', 'então', 'importante',
                            'estar', 'estará', 'fará', 'faz', 'fazer', 'fazia', 'fez', 'fim', 'horas', 'iniciar', 'inicio', 'ir',
                            'irá', 'ista', 'iste', 'ligado', 'maioria', 'maiorias', 'muitos', 'nome', 'novo', 'onde', 'outro', 
                            'parte', 'pegar', 'pessoas', 'pode', 'poderá', 'podia', 'porque', 'povo', 'ir', 'oquê', 'qualquer',
                            'quieto', 'saber', 'ser', 'somente', 'têm', 'tal', 'tempo', 'tentar', 'tentaram', 'tente', 'tentei',
                            'todos', 'trabalhar', 'trabalho', 'umas', 'uns', 'usa', 'usar', 'valor', 'veja', 'ver', 'verdade', 'verdadeiro']
    
    stopWords += stopWordsNaoListadas[:]
    del(stopWordsNaoListadas)
    
    splitter = re.compile('\\W+') #Pega todas as paçavras que tenham a-zA-z0-9_
    listaPalavras = list()
    lista = [p for p in splitter.split(texto) if p != ''] #pegando todos os termos do tweet
    
    for palavra in lista: #Pegando palavras que não são stopwords e nem espaços em branco
        if palavra.lower() not in stopWords and len(palavra) > 1:
            listaPalavras.append(palavra.lower())
    return listaPalavras


def palavraIndexada(palavras, candidato):
    """
    Verifica se as palavras inseridas na lista já estão no banco de dados, se sim, faz um update no banco incrementando em
    +1 a quantidade que aquela determinada palavra aparece. Se não, faz um insert na nova palavra
    
    :param palavras: list - palavras dos tweets, já desconsiderando stopwords
    :param candidato: ID do candidato autor dos tweets que o algoritmo está analisando
    1 - João Dória
    2 - Márcio França
    * A escolha do ID foi feita por ordem alfabética
    :return: void/nulo
    """
    conexao = pymysql.connect(host='localhost', user='root', passwd='fsociety', db='eleicoes', use_unicode = True, charset = 'utf8mb4', autocommit = True)
    cursorUrl = conexao.cursor()
    
    for palavra in palavras:
        cursorUrl.execute(f'select (ID_Tematica) from tematicas where Nome_Tematica = %s and ID_Candidato = %s', (palavra, candidato))
        if cursorUrl.rowcount > 0: #se retornou algum resultado
            idPalavra = cursorUrl.fetchone()[0]
            cursorUrl.execute(f'select (Quantidade_Tematica) from tematicas where ID_Tematica = %s', idPalavra)
            qtd = 1 + cursorUrl.fetchone()[0] #fetchone()[0] = pega o primeiro reultado retornado
            print(f'ATUALIZEI A QTD DA PALAVRA "{palavra.strip()}" PARA {qtd}')
            cursorUrl.execute(f'update tematicas set Quantidade_Tematica = %s where ID_Tematica = %s', (qtd, idPalavra))
        else:
            cursorUrl.execute(f'insert into tematicas (ID_Candidato, Nome_Tematica, Quantidade_Tematica) values '+
                                                       '(%s, %s, %s)', (candidato, palavra.strip(), 1)) #FK do candidato, Nome, Quantidade
            print(f'GRAVEI A PALAVRA "{palavra.strip()}"')
        
    cursorUrl.close()
    conexao.close()  


def indexarTweet(tweets):
    """
    Grava todos os tweets inseridos na lista no banco de dados.
    A lista que deve ser passada para esse parâmetro deve ser a que possui a estrutura
    data - categoria do tweet - conteúdo - engajamento, pois eles serão lidos posteriormente,
    diferente das listas de tweets destinadas para cada candidato presentes no início do algoritmo,
    que possuem são utilizadas apenas para a análise e gravação das palavras/temáticas.

    :param tweets: list - Tweets que seguem a estrutura supracitada.
    :return: void/nulo
    """
    conexao = pymysql.connect(host='localhost', user='root', passwd='fsociety', db='eleicoes', use_unicode = True, charset = 'utf8mb4', autocommit = True)
    cursorUrl = conexao.cursor()

    for tweet in tweets:
        if tweet[0] == 'J': # Tweet do João Dória
            print('INDEXANDO TWEETS DE João Dória ...\n')
            cursorUrl.execute('insert into tweets (ID_Candidato, Conteudo_Tweet) values (%s, %s)', (1, tweet))
        else: # Tweet do Márcio França
            print('INDEXANDO TWEETS DE Márcio França ...\n')
            cursorUrl.execute('insert into tweets (ID_Candidato, Conteudo_Tweet) values (%s, %s)', (2, tweet))
            
    cursorUrl.close()
    conexao.close()