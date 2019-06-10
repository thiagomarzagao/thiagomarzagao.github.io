---
comments: true
layout: post
title: how much is your apartment worth? (part 2)
---

So, Brazilian banks are using predictive models to do property valuation but they are [doing it wrong](http://thiagomarzagao.com/2019/06/08/property-valuation/). It's time for us data folks to step in and cause some disruption.

<iframe src="https://giphy.com/embed/lQJIEmMzyr8OhoTA9t" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/lQJIEmMzyr8OhoTA9t"></a></p>

**our hypothetical property**

Let's assume that we want to find the market value of an apartment in Brasília. It's 120m<sup>2</sup>, it's in the Noroeste sector (Brasília is a planned city, so it has sectors instead of neighborhoods), it has three bedrooms, three bathrooms, and two parking spots. The condo fee is R$ 580/month and the property tax is R$ 745/month.

**getting data**

It's 2019, so there's no need to go knocking on doors asking people how much they paid for their apartments, how many bedrooms they have, etc. We can simply scrape online listing sites like [ZAP](https://www.zapimoveis.com.br/), [wimoveis](https://www.wimoveis.com.br/), or [Viva Real](https://www.vivareal.com.br/). Any of the three would do (and scraping all three of them would be best). Here I'll scrape wimoveis for the simple reason that it is the easiest one to scrape.

Granted, that just gives us asking prices, not transaction prices. But the alternative is to go knocking on doors asking people about their apartments. (Unless of course you are a bank and you have tons of mortgage data.)

Here's the (Python) code I wrote to scrape the result pages:

{% highlight python %}
import time
import requests

destination = '/Volumes/UNTITLED/wimoveis/paginas/'
base_url = 'https://www.wimoveis.com.br/'
num_pages = 1557 # number of results pages
for i in range(1, num_pages):
    print('page', i)
    query_url = base_url + 'apartamentos-venda-distrito-federal-goias-pagina-{}.html'.format(i)
    response = requests.get(query_url)
    if response.status_code == 200:
        # save source code of the page 
        with open(destination + 'pagina_{}.html'.format(i), mode = 'w') as f:
            f.write(response.text)
            time.sleep(2)
{% endhighlight %}

Every page of results contains up to 20 listings. But it only has summary information for each listing. The full data is in each listing's own URL. So we need to get the URL of every listing from every page. I use [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for that:

{% highlight python %}
import os
from bs4 import BeautifulSoup

hrefs = []
path = '/Volumes/UNTITLED/wimoveis/paginas/'
for fname in os.listdir(path):
    print(fname)
    if ('.html' in fname) and ('._' not in fname):
        with open(path + fname, mode = 'r') as f:
            html = f.read()
            soup = BeautifulSoup(html)
            h4 = soup.find_all('h4', class_ = 'aviso-data-title')
            href = [e.find('a')['href'] for e in h4]
            hrefs += href

print(len(hrefs))
df = pd.DataFrame(hrefs)
df.to_csv('hrefs.csv', index = False)
{% endhighlight %}

Now we're finally ready to scrape the listings themselves, with all the data we need (price, m<sup>2</sup>, pictures, etc).

{% highlight python %}
import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

basepath = '/Volumes/UNTITLED/wimoveis/anuncios/'
hrefs = pd.read_csv('hrefs.csv') # get URLs
hrefs = set(hrefs['href']) # remove duplicate URLs
for i, href in enumerate(hrefs):

    # get ID of the listing
    id_anuncio = re.findall(r'[0-9]{1,20}\.html', href)[0].replace('.html', '')

    # if listing has been downloaded before, ignore
    path = basepath + id_anuncio + '/'
    if os.path.exists(path):
        continue

    # get the source code of the listing;
    # doesn't always work on the first try, so
    # wait for 60s and try again if necessary;
    # looks like this risks infinite loops, but
    # somehow that didn't happen
    url = 'https://www.wimoveis.com.br' + href    
    while True:
        try:
            response = requests.get(url)
            break
        except:
            print('error; waiting')
            time.sleep(60)

    # if it worked, move on
    if response.status_code == 200:
        print(i, path)
        os.mkdir(path) # create destination directory
        html = response.text # get source code

        # save source code to file
        with open(path + 'anuncio_' + str(i) + '.html', mode = 'w') as f:
            f.write(html)

        # now the time-consuming part: getting the
        # pictures of the listing
        pic_path = path + 'pics/'
        os.mkdir(pic_path) # create destination directory

        # find URLs of the pictures
        soup = BeautifulSoup(html)
        figures = soup.find_all('figure', class_ = 'slide-content')
        links = [e.find('img')['data-flickity-lazyload'] for e in figures]

        # try downloading each picture
        for n, link in enumerate(links):
            while True:
                try:
                    response = requests.get(link, stream = True)
                    break
                except:
                    print('conn error; waiting')
                    time.sleep(60)

            # if it worked, save picture to file
            if response.status_code == 200:
                with open(pic_path + str(n) + '.jpg', mode = 'wb') as f:
                    for chunk in response:
                        f.write(chunk)
{% endhighlight %}

This will take a couple of days to run, because of all the pictures you're downloading.

<iframe src="https://giphy.com/embed/jBK8OrYIO1yTe" width="480" height="384" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/waiting-charlie-chaplin-work-problems-jBK8OrYIO1yTe"></a></p>

In the end we'll have over 15k samples. That's up from the current 25-250 samples that real estate appraisers are using.

**parsing data**

Ok, what we have now is a huge mess of HTML and JPG files. The data we need is all buried in those files. We need to extract it.

For now I'll ignore the JPG files and only use the HTML files.

{% highlight python %}
import os
import pandas as pd
from bs4 import BeautifulSoup

dados = []
basepath = '/Volumes/UNTITLED/wimoveis/anuncios/'
for i, anuncio_id in enumerate(os.listdir(basepath)):

    # Dropbox creates an annoying hidden folder,
    # let's ignore it
    if '.' in anuncio_id: 
        continue

    anuncio_path = basepath + anuncio_id + '/'
    for fname in os.listdir(anuncio_path):
        if '.html' in fname:
            print(i, fname)

            # empty dict to store the listing data
            dados_anuncio = {}

            # read source code of the listing
            with open(anuncio_path + fname, mode = 'r') as f:
                source = f.read()

            # soupify source code
            soup = BeautifulSoup(source, 'lxml')

            # get ID of the listing
            dados_anuncio['anuncio_id'] = anuncio_id

            # get title of the listing
            title = soup.find('h2', class_ = 'title-type-sup')
            if title:
                title = title.text.strip()
            try:
                title2 = soup.find_all('div', class_ = 'section-title')[1]
            except:
                continue
            if title2:
                title2 = title2.text.strip()
            dados_anuncio['titulo'] = title
            dados_anuncio['titulo_compl'] = title2

            # get location of the property
            local = soup.find('h2', class_ = 'title-location')
            if local:
                local = local.text.strip()
            local2 = soup.find('div', class_ = 'section-location')
            if local2:
                local2 = local2.text.strip()
            dados_anuncio['local'] = local
            dados_anuncio['local_compl'] = local2

            # get asking price (and rent price, if available)
            price_block = soup.find('div', class_ = 'block-price-container')
            try:
                price_list = price_block.find_all('div', class_ = 'block-price block-row')
            except:
                continue
            for e in price_list:
                operation = e.find('div', class_ = 'price-operation').text.strip()
                price = e.find('div', class_ = 'price-items').text.strip()
                dados_anuncio[operation] = price

            # get condo fee and property tax
            expense_list = price_block.find_all('div', class_ = 'block-expensas block-row')
            for e in expense_list:
                full_text = e.text.strip()
                idx = full_text.index('R$')
                expense = full_text[:idx]
                price = full_text[idx:]
                dados_anuncio[expense] = price

            # get ID of the seller
            anunciante = soup.find('h3', class_ = 'publisher-subtitle').text.strip()
            dados_anuncio['anunciante'] = anunciante

            # get text description of the property
            descricao = soup.find('div', {'id': 'verDatosDescripcion'}).text.strip()
            dados_anuncio['descricao'] = descricao

            # get structured features of the property
            # (those that have accompanying icons)
            features_block = soup.find('ul', class_ = 'section-icon-features')
            lis = features_block.find_all('li', class_ = 'icon-feature')
            for e in lis:
                label = e.find('span').text.strip()
                value = e.find('b').text.strip()
                dados_anuncio[label] = value

            # get other features of the property
            # (those that do not have accompanying icons)
            areas = soup.find_all('ul', class_ = 'section-bullets')
            for area in areas:
                lis = area.find_all('li')
                for e in lis:
                    if e.find('b'):
                        area_feature_label = e.find('h4').text.strip()
                        area_feature_value = e.find('b').text.strip()
                        dados_anuncio[area_feature_label] = area_feature_value
                    else:
                        area_feature = e.string
                        dados_anuncio[area_feature] = '1'

            # clean sobre garbagem from the data
            for key in dados_anuncio.keys():
                v = dados_anuncio[key]
                if v:
                    v = v.replace('\n', ' ')
                    v = v.replace('\r', ' ')
                    v = v.replace('\t', ' ')
                    while '  ' in v:
                        v = v.replace('  ', ' ')
                    dados_anuncio[key] = v.strip()

            # append row of data
            dados.append(dados_anuncio)

# save everything as a CSV file
df = pd.DataFrame.from_dict(dados)
df.to_csv('listings_data.csv', index = False)
{% endhighlight %}

Hooray, now we've put all the (non-image) data in a CSV file with proper column names and everything.

**throwing data away**

Now that we have all that data it's time to throw some of it away.

You see, people are lazy. When they list their properties on wimoveis they don't bother to tick all the boxes - "pool", "playground", "A/C", etc. Whatever they consider relevant they'll write down in the text field (often with lots of adjectives and exclamation marks). The result is that our CSV file is mostly empty: most of its cells are missing data. This varies according to the feature we're talking about. But the vast majority of the features have simply too many missing data points to be useful. So let's clean up a bit.

{% highlight python %}
import numpy as np
import pandas as pd

# column names to load (and their new names)
colnames = {
    'anuncio_id': 'anuncio_id',
    'Venda': 'preco_total',
    'titulo': 'titulo',
    'titulo_compl': 'titulo_compl',
    'local': 'local',
    'local_compl': 'local_compl',
    'Área útil': 'area_util',
    'Vagas': 'vagas',
    'descricao': 'descricao',
    'Andares': 'andares',
    'Banheiros': 'banheiros',
    'Brinquedoteca': 'brinquedoteca',
    'Churrasqueira': 'churrasqueira',
    'Condomínio ': 'condominio',
    'Elevador': 'elevador',
    'IPTU ': 'iptu',
    'Piscina': 'piscina',
    'Circuito de TV': 'tv',
    'Fitness/Sala de Ginástica': 'academia',
    'Idade do imóvel': 'idade',
    'Playground': 'playground',
    'Portaria 24 horas': 'portaria',
    'Quartos': 'quartos',
    'Salão de Jogos': 'jogos',
    'Salão de festas': 'festas',
    'Sauna': 'sauna',
    'Suítes': 'suites',
    }

# load data
df = pd.read_csv('listings_data.csv', usecols = colnames)

# rename columns
old_names = list(df.columns)
new_names = [colnames[k] for k in old_names]
df.columns = new_names

# merge location columns
df['local'] = df['local'].fillna('')
df['local_compl'] = df['local_compl'].fillna('')
df['local'] = df['local'] + ' ' + df['local_compl']
del df['local_compl']

# clean up location
def fix_local(v):
    v_new = v.replace('\n', ' ')
    v_new = v_new.replace('\r', ' ')
    v_new = v_new.replace('\t', ' ')
    while '  ' in v_new:
        v_new = v_new.replace('  ', ' ')
    v_new = v_new.strip()
    return v_new

df['local'] = df['local'].map(lambda x: fix_local(x))

# drop sample if no location
df = df[df['local'] != '']

# drop sample if no price or m2
df = df.dropna(axis = 0, how = 'any', subset = ['preco_total', 'area_util'])

# merge title columns
df['titulo'] = df['titulo'].fillna('')
df['titulo'] = df['titulo_compl'].fillna('')
df['titulo'] = df['titulo'] + ' ' + df['titulo_compl']
del df['titulo_compl']

# transform some float variables into int
for var in ['vagas', 'andares', 'banheiros', 'quartos', 'suites']:
    df[var] = df[var].fillna(0)
    df[var] = df[var].map(lambda x: int(x))

df['idade'] = df['idade'].map(lambda x: int(x) if str(x).isdigit() else 0)

# convert money columns from str to float
def fix_money_value(v):
    try:
        v_new = v.replace('R$', '')
        v_new = v_new.replace('.', '')
        v_new = v_new.replace(' ', '')
        v_new = float(v_new)
        return v_new
    except:
        return None

for var in ['preco_total', 'iptu', 'condominio']:
    df[var] = df[var].map(lambda x: fix_money_value(x))

# convert m2 from string to float
def fix_area_value(v):
    v_new = v.replace('m2', '').replace('m²', '')
    v_new = v_new.replace('.', '')
    v_new = float(v_new)
    return v_new

df['area_util'] = df['area_util'].map(lambda x: fix_area_value(x))

# drop absurd values
df = df[df['preco_total'] > 1000]
df = df[df['area_util'] > 1]

# recode location
satelites = [
    'Gama',
    'Taguatinga',
    'Brazlândia',
    'Sobradinho',
    'Planaltina',
    'Paranoá',
    'Núcleo Bandeirante',
    'Ceilândia',
    'Guará',
    'Cruzeiro',
    'Samambaia',
    'Santa Maria',
    'São Sebastião',
    'Recanto das Emas',
    'Lago Sul',
    'Riacho Fundo',
    'Lago Norte',
    'Candangolândia',
    'Águas Claras',
    'Sudoeste',
    'Octogonal',
    'Varjão',
    'Park Way',
    'SCIA',
    'Jardim Botânico',
    'Itapoã',
    'SIA',
    'Vicente Pires',
    'Fercal'
    ]

def get_local(v):
    splitted = v.split(',')
    setor = splitted[-2].strip()
    cidade = splitted[-1].strip()
    if cidade == 'Brasília':
        return setor
    elif cidade in satelites:
        return cidade
    else:
        return 'Goiás'

df['endereco'] = df['local'].map(lambda x: get_local(x))

# handle some features where missing actually means "doesnt have it"
for var in ['churrasqueira', 'brinquedoteca', 'tv', 'piscina', 'playground', 'sauna', 'academia', 'portaria', 'jogos', 'festas']:
    df[var] = df[var].fillna(0)

# reorder and rename columns and save to CSV
df = df[['anuncio_id', 'preco_total', 'area_util', 'endereco', 'vagas', 'banheiros', 'quartos', 'churrasqueira', 'idade', 'brinquedoteca', 'tv', 'piscina', 'playground', 'sauna', 'academia', 'portaria', 'jogos', 'festas', 'suites', 'titulo', 'local', 'descricao', 'iptu', 'condominio', 'andares']]
df.columns = ['anuncio_id', 'preco_total', 'area_util', 'local', 'vagas', 'banheiros', 'quartos', 'churrasqueira', 'idade', 'brinquedoteca', 'tv', 'piscina', 'playground', 'sauna', 'academia', 'portaria', 'jogos', 'festas', 'suites', 'titulo', 'endereco', 'descricao', 'iptu', 'condominio', 'andares']
df.to_csv('wimoveis.csv', index = False, encoding = 'utf-8')
{% endhighlight %}

There! Now we have a clean, usable dataset.

**train the model**

I tried a few different algorithms to estimate the properties' asking prices: linear regression, SVM, random forest, boosted trees, neural networks. For each of these algorithms (except linear regression) I tweaked the corresponding parameters a bunch of times (and for neural networks I tried lots of different architectures). The clear winner was boosted trees (which won't be so surprising to Kaggle competitors).

Just a quick note: we discarded lots of features in the previous step because of missing data. Here we'll add some of them back. People don't always tick the "barbecue" box when filling out their listings, but they usually mention it in the text field. So the code below scans the text field looking for certain words.

{% highlight python %}
import math
import numpy as np
import pandas as pd
from unicodedata import normalize
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_predict

# set seed
random_state = 42

# load data
df = pd.read_csv('wimoveis.csv')
 
# keep only certain features
df = df[[
    'preco_total', # asking price
    'area_util', # m2
    'local', # location
    'iptu', # property tax
    'condominio', # condo fee
    'quartos', # num of bedrooms
    'suites', # num of suites
    'banheiros', # num of bathrooms
    'vagas', # num of parking spots 
    'titulo', # title of the listing
    'endereco', # address of the listing
    'descricao' # description of the listing
    ]]

# apartment we want to appraise
x_new = pd.DataFrame({
    'preco_total': [1.0], # just so we can drop it later
    'area_util': [120], 
    'local': ['Noroeste'],
    'iptu': [745],
    'condominio': [580],
    'quartos': [3],
    'suites': [3],
    'banheiros': [2],
    'vagas': [2],
    'titulo': '',
    'endereco': '',
    'descricao': '',
    })

# don't worry, we'll drop this before
# training the model
df = df.append(x_new)

# impute median values for missing condo fees and property tax
for var in ['iptu', 'condominio']:
    median = df[df[var] > 0][var].median()
    df[var] = df[var].fillna(median)

# drop outliers
df = df[df['area_util'] < 50000]
df = df[df['preco_total'] < 70000000]
df = df[df['condominio'] < 1500000]
df = df[df['iptu'] < 20000]
df = df[df['vagas'] < 10]

# take the log of all quantitative variables
for var in ['preco_total', 'area_util', 'iptu', 'condominio']:
    df[var] = df[var].map(lambda x: math.log(x))

# merge text columns (title + location + address + description)
# (this will let us extract some features later)
df['fulltext'] = df['local'] + ' ' + df['titulo'] + ' ' + df['endereco'] + ' ' + df['descricao']

# is it Caldas Novas? (that's a city in the state of Goiás)
def is_caldas(s):
    if 'caldas novas' in s.lower():
        return 1
    return 0
df['caldas'] = df['fulltext'].map(lambda x: is_caldas(str(x)))

# Goiania? (that's the capital of the state of Goiás)
def is_goiania(s):
    if ('goiania' in s.lower()) or ('goiânia' in s.lower()):
        return 1
    return 0
df['goiania'] = df['fulltext'].map(lambda x: is_goiania(str(x)))

# barbecue?
def has_grill(s):
    if 'churrasqueira' in s.lower():
        return 1
    return 0
df['churrasqueira'] = df['fulltext'].map(lambda x: has_grill(str(x)))

# pool?
def has_pool(s):
    if 'piscina' in s.lower():
        return 1
    return 0
df['piscina'] = df['fulltext'].map(lambda x: has_pool(str(x)))

# playground?
def has_playground(s):
    if ('playground' in s.lower()) or ('brinquedoteca' in s.lower()):
        return 1
    return 0
df['playground'] = df['fulltext'].map(lambda x: has_playground(str(x)))

# sauna?
def has_sauna(s):
    if 'sauna' in s.lower():
        return 1
    return 0
df['sauna'] = df['fulltext'].map(lambda x: has_sauna(str(x)))

# A/C?
def has_ac(s):
    if 'ar condicionado' in s.lower():
        return 1
    return 0
df['ar'] = df['fulltext'].map(lambda x: has_ac(str(x)))

# unobstructed view?
def has_view(s):
    if 'vista livre' in s.lower():
        return 1
    return 0
df['vista'] = df['fulltext'].map(lambda x: has_view(str(x)))

# high floor?
def is_high(s):
    if 'andar alto' in s.lower():
        return 1
    return 0
df['alto'] = df['fulltext'].map(lambda x: is_high(str(x)))

# faces sunrise?
def is_sunrise(s):
    if 'nascente' in s.lower():
        return 1
    return 0
df['nascente'] = df['fulltext'].map(lambda x: is_sunrise(str(x)))

# porcelain tiles?
def porcelanato(s):
    if 'porcelanato' in s.lower():
        return 1
    return 0
df['porcelanato'] = df['fulltext'].map(lambda x: porcelanato(str(x)))

# accepts mortgage?
def mortgage_ok(s):
    if 'aceita financiamento' in s.lower():
        return 1
    return 0
df['financiamento'] = df['fulltext'].map(lambda x: mortgage_ok(str(x)))

# renovated?
def is_renovated(s):
    if ('reformado' in s.lower()) or ('reformada' in s.lower()):
        return 1
    return 0
df['reformado'] = df['fulltext'].map(lambda x: is_renovated(str(x)))

# cabinets?
def has_cabinets(s):
    if ('armarios' in s.lower()) or ('armários' in s.lower()):
        return 1
    return 0
df['armarios'] = df['fulltext'].map(lambda x: has_cabinets(str(x)))

# private garage?
def has_parking(s):
    if 'garagem' in s.lower():
        return 1
    return 0
df['garagem'] = df['fulltext'].map(lambda x: has_parking(str(x)))

# recode location
# (to standardize spellings and do some aggregation)
new_locals = {
    'Asa Sul': 'asa_sul',
    'Asa Norte': 'asa_norte',
    'Goiás': 'goias',
    'Águas Claras': 'aguas_claras',
    'Taguatinga': 'taguatinga',
    'Guará': 'guara',
    'Sudoeste': 'sudoeste',
    'Noroeste': 'noroeste',
    'Lago Norte': 'lago_norte',
    'Samambaia': 'samambaia',
    'Ceilândia': 'ceilandia',
    'Centro': 'outros', # melhorar isso aqui depois (tem de tudo)
    'Setor De Industrias': 'asa_sul', # eh quase tudo SIG
    'Sobradinho': 'sobradinho',
    'Núcleo Bandeirante': 'bandeirante',
    'Riacho Fundo': 'riacho',
    'Vicente Pires': 'vicente',
    'Park Sul': 'parksul',
    'Recanto das Emas': 'recanto',
    'Lago Sul': 'lago_sul',
    'Gama': 'gama',
    'Setor De Industria Graficas': 'asa_sul',
    'Setor Habitacional Jardim Botânico': 'outros',
    'Octogonal': 'octogonal',
    'Planaltina': 'planaltina',
    'Cruzeiro': 'cruzeiro',
    'Santa Maria': 'santamaria',
    'São Sebastião': 'saosebastiao',
    'Setor Da Industria E Abastecimento': 'outros',
    'Zona Industrial': 'outros',
    'Paranoá': 'paranoa',
    'Setor De Autarquias Sul': 'asa_sul',
    'Setor Comercial Sul': 'asa_sul',
    'Setor Bancario Sul': 'asa_sul',
    'Setores Complementares': 'outros',
    'Park Way': 'parkway',
    'Candangolândia': 'candangolandia',
    'Setor De Radio E Televisao Sul': 'asa_sul',
    'Taquari': 'outros',
    'Setor Hoteleiro Sul': 'asa_sul',
    'Setor de Múltiplas Atividades Sul': 'outros',
    'Setor de Armazenagem e Abastecimento Norte': 'outros',
    'Setor Hospitalar Local Sul': 'asa_sul',
    'Zona Civico-administrativa': 'asa_sul',
    'Setor de Grandes Áreas Norte': 'asa_norte',
    'Setor De Clubes Esportivos Norte': 'lago_norte',
    'Setor De Clubes Esportivos Sul': 'lago_sul',
    'Zona Rural': 'outros',
    'Setor De Diversoes Norte': 'asa_norte',
    'Superquadra Sudoeste': 'sudoeste',
    'Setor de Mansões Dom Bosco': 'outros',
    'Setor Bancario Norte': 'asa_norte',
    'Setor Comercial Norte': 'asa_norte',
    'Setor De Oficinas Norte': 'asa_norte',
    'Setor Hoteleiro Norte': 'asa_norte',
    'Setor de Hotéis e Turismo Norte': 'asa_norte',
    'Quadra Mista Sudoeste': 'sudoeste',
    'Superquadra Noroeste': 'noroeste',
    'Setor Habitacional Jardins Mangueiral': 'outros',
    'Setor Habitacional Jardins Mangueiral': 'outros',
    'Vila Planalto': 'outros',
    'Alphaville': 'outros',
    'Granja Do Torto': 'outros',
    'Comércio Local Noroeste': 'noroeste',
    'Superquadra Sul': 'asa_sul',
    'Setor Terminal Norte': 'asa_norte',
    'Setor Terminal Sul': 'asa_sul',
    'Centro Comercial Noroeste': 'noroeste',
    'Setor de Grandes Áreas Norte': 'asa_norte',
    'Mansões do Lago': 'outros',
    'Setor de Garagens e Concessionárias de Veículos': 'outros',
    'Setor Comercial Local Residencial Norte': 'asa_norte',
    'Centro de Atividades': 'lago_norte',
    'Setor de Habitações Individuais Norte': 'lago_norte',
    'Superquadra Norte': 'asa_norte',
    'Centro Comercial Sudoeste': 'sudoeste',
    }
df['local'] = df['local'].map(lambda x: new_locals[x])
#print(df['local'].value_counts())

# dummify location
locais = pd.get_dummies(df['local'], prefix = 'local', drop_first = True)
for col in locais.columns:
    df[col] = locais[col]
del df['local']

# if city is Brasília, get more location details
def detail_location(s):
    locations = {

        # industras graficas
        ' sig ': 'sig',
        'graficas': 'sig',
        'setor de industrias': 'sig',

        # industria e abastecimento
        ' sia ': 'sia',
        'setor de industria e abastecimento': 'sia',

        # armazenagem e abastecimento norte
        ' saan': 'saan',
        'setor de armazenagem e abastecimento norte': 'saan',

        # armazenagem e abastecimento sul
        ' saas': 'saas',
        'setor de armazenagem e abastecimento sul': 'saas',

        # autarquias norte
        ' san ': 'san',
        'setor de autarquias norte': 'san',

        # autarquias sul
        ' sas ': 'sas',
        'setor de autarquias sul': 'sas',

        # comercial norte
        ' cln ': 'cln',
        ' scln ': 'cln',
        'comercial local norte': 'cln',
        'comercio local norte': 'cln',
        ' scn ': 'scn',
        'setor comercial norte': 'scn',
        ' sdn ': 'sdn',
        'setor de diversoes norte': 'sdn',

        # comercial sul
        ' cls ': 'cls',
        ' scls ': 'cls',
        'comercial local sul': 'cls',
        'comercio local sul': 'cls',
        ' scs ': 'scs',
        'setor comercial sul': 'scs',
        ' sds ': 'sds',
        'setor de diversoes sul': 'sds',

        # comercial noroeste
        ' clnw ': 'clnw',

        # comercial sudoeste
        ' clsw ': 'clsw',

        # bancario norte
        ' sbn ': 'sbn',
        'setor bancario norte': 'sbn',

        # bancario sul
        ' sbs ': 'sbs',
        'setor bancario sul': 'sbs',

        # grandes areas norte
        ' sgan ': 'sgan',
        'setor de grandes areas norte': 'sgan',

        # grandes areas sul
        ' sgas ': 'sgas',
        'setor de grandes areas sul': 'sgas',

        # hoteleiro norte
        ' shn ': 'shn',
        ' shtn ': 'shn',
        'setor hoteleiro norte': 'shn',
        'setor de hoteis e turismo norte': 'shn',

        # hoteleiro sul
        ' shs ': 'shs',
        ' shts ': 'shts',
        'setor hoteleiro sul': 'shs',
        'setor de hoteis e turismo sul': 'shs',

        # hospitalar norte
        ' shln ': 'shln',
        'setor hospitalar local norte': 'shln',

        # hospitalar sul
        ' shls ': 'shls',
        'setor hospitalar local sul': 'shls',

        # radio e tv norte
        ' srtvn ': 'srtvn',
        'setor de radio norte': 'srtvn',

        # radio e tv sul
        ' srtvs ': 'srtvs',
        'setor de radio sul': 'srtvs',

        # oficinas
        ' sof ': 'sof',
        'setor de oficina': 'sof',

        # seuperquadras
        'sqn': 'sqn',
        'super quadra norte': 'sqn',
        'superquadra norte': 'sqn',
        'sqs': 'sqs',
        'super quadra sul': 'sqs',
        'superquadra sul': 'sqs',
        'sqsw': 'sqsw',
        'super quadra sudoeste': 'sqsw',
        'superquadra sudoeste': 'sqsw',
        'sqnw': 'sqnw',
        'super quadra noroeste': 'sqnw',
        'superquadra noroeste': 'sqnw',

        'qmsw': 'qmsw',
        'quadra mista sudoeste': 'qmsw',
        'qrsw': 'qrsw',
    }
    s = normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')
    s = s.lower()
    for key in locations.keys():
        if key in s:
            return locations[key]
    return 'outros'

df['local_det'] = df['fulltext'].map(lambda x: detail_location(str(x)))

# dummify location details (for when city=Brasília)
locais = pd.get_dummies(df['local_det'], prefix = 'local_det', drop_first = True)
for col in locais.columns:
    df[col] = locais[col]
del df['local_det']

# drop text columns
del df['fulltext']
del df['titulo']
del df['endereco']
del df['descricao']

# drop row that contains the property we want to appraise
x_new = df[df['preco_total'] == 0]
del x_new['preco_total']
x_new = x_new.values
df = df[df['preco_total'] > 0]

# split X and Y
y = df['preco_total'].values
del df['preco_total']
X = df.values

# shuffle sample order
X, y = shuffle(X, y, random_state = random_state)

# instantiate model
model = GradientBoostingRegressor(loss = 'quantile', alpha = 0.5, n_estimators = 1000, random_state = random_state)

# train model
yhat = cross_val_predict(model, X, y, cv = 10)

# put estimated prices back in R$
yhat_reais = np.exp(yhat)

# put observed prices back in R$
y_reais = np.exp(y)

# compute errors
erros = yhat_reais - y_reais

# compute median absolute error
erro_absoluto_mediano = np.median(np.absolute(erros))
print('erro absoluto mediano:', erro_absoluto_mediano)

# compute proportional error (error / asking price)
erros_relativos = erros / y_reais
erro_relativo_mediano = np.median(np.absolute(erros_relativos))
erro_relativo_medio = np.mean(np.absolute(erros_relativos))
print('erro relativo mediano:', erro_relativo_mediano)
print('erro relativo medio:', erro_relativo_medio)
{% endhighlight %}

This gives me a median absolute error of R$ 46k. In proportional terms (i.e., error / asking price) we have a median absolute error of 10% and a mean absolute error of 23%. Which is line with previous work (see [here](https://sci-hub.tw/https://www.sciencedirect.com/science/article/pii/S0957417414007325)), where the mean absolute error is 25%-30%, and [here](https://www.pyimagesearch.com/2019/02/04/keras-multiple-inputs-and-mixed-data/), where the mean absolute error is 22%.)

We're not capturing everything here. Say, maybe the property is next door to a police station or to a church or to a loud bar. Maybe there was a murder in the premises. Etc etc. My point is not that these estimates should be final. My point is simply that these estimates are probably closer to the truth than the ones being produced today by professional appraisers all over Brazil.

**appraise!**

Alright then, time to appraise our Noroeste apartment. Just append the following lines to the previous code block and run it.

{% highlight python %}
# train models for lower bound, point estimate, and upper bound
model_lower = GradientBoostingRegressor(loss = 'quantile', alpha = 0.25, n_estimators = 1000, random_state = random_state)
model_mid = GradientBoostingRegressor(loss = 'quantile', alpha = 0.5, n_estimators = 1000, random_state = random_state)
model_upper = GradientBoostingRegressor(loss = 'quantile', alpha = 0.75, n_estimators = 1000, random_state = random_state)
model_lower.fit(X, y)
model_mid.fit(X, y)
model_upper.fit(X, y)

# appraise
yhat_lower = model_lower.predict(x_new)
yhat_mid = model_mid.predict(x_new)
yhat_upper = model_upper.predict(x_new)
print(np.exp(yhat_lower), np.exp(yhat_mid), np.exp(yhat_upper))
{% endhighlight %}

And voilà, we have our point estimate: R$ 978k (That's about US$ 254k).

We also have a prediction interval with lower and upper bounds: [788k, 1060k]. To produce this interval I used something similar to quantile regression. The lower bound is an estimate of the 25th percentile of the distribution. The upper bound is an estimate of the 75th percentile. The point estimate is an estimate of the 50th percentile (i.e., the median). As we have three different models, the lower and upper bounds are not centered around the point estimate (we actually have three point estimates). More details [here](https://towardsdatascience.com/how-to-generate-prediction-intervals-with-scikit-learn-and-python-ab3899f992ed).

**text**

Here I'm scanning the property descriptions for words like "A/C", "barbecue", etc, and featurizing them as dummies. But you can use the texts themselves in the model. Just insert the following code between the line where you shuffle the samples and the line where you instantiate the model:

{% highlight python %}
# little function to make corpus
def make_corpus(df):
    for row in df.iterrows():
        yield str(row[1]['fulltext'])

# vetorize corpus and create TFIDF matrix
vectorizer = TfidfVectorizer(strip_accents = 'unicode', lowercase = True, ngram_range = (1, 2))
tfidf = vectorizer.fit_transform(make_corpus(df))

# reduce dimensions (i.e., extract topics)
svd = TruncatedSVD(n_components = 400)
topics = svd.fit_transform(tfidf)

# add topics to the dataframe
for n in range(0, topics.shape[1]):
    df[str(n)] = topics[:,n]

# rescale topics to make them compatible with the m2 scale
scaler = MinMaxScaler(feature_range = (df['area_util'].min(), df['area_util'].max()))
for col in df.columns:
    if col.isdigit():
        df[col] = scaler.fit_transform(df[col].values.reshape(-1, 1))
{% endhighlight %}

The TFIDF matrix is too big - we end up with more columns than samples. So we don't use it directly, we use LSA to reduce the TFIDF matrix to a documentsXtopics matrix of 400 topics.

This improves the performance of the model a bit. But it's ultimately nonsensical: when you're appraising a new property you could keep tweaking the text until you get the price you want. So I did this just to inspect which topic vectors would be more relevant (see [here](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html#sklearn.ensemble.GradientBoostingRegressor.feature_importances_)), and then which words had more weight in these topics. This helped me decide which words to look for in the text fields (sauna, pool, etc).

**images**

I'm still figuring out the best way to use the pictures. I tried using the metadata first: number of pictures, height and width of the pictures, etc. That didn't improve the model. (I know, shocking. But I like to try the simple things first.)

I also checked whether the dominant colors help us predict the price. To do that I clustered the pixels of every picture of the property. Each pixel is defined by three values: R, G, B, each of which can vary from 0 to 255 and represents the intensity of each of the three primary colors (red, green, and blue). So the pixels exist in the same tridimensional space and therefore we can cluster them. The centroid of each cluster is a dominant color.

Ideally we'd use DBSCAN for this, as the clusters may have widely different sizes and shapes and we don't even know a priori how many clusters each picture has. But DBSCAN just takes forever to run. So I used k-means instead. I used the elbow technique to find the ideal number of clusters and it turns out that for most images that number was two or three.

That was a massive waste of time. K-means is faster but it still took almost a week to run. And in the end those centroids didn't improve the model one bit.

A friend who knows a lot more about images than I do suggested that I try something [along these lines](https://www.pyimagesearch.com/2019/02/04/keras-multiple-inputs-and-mixed-data/). I.e., having a branched neural network where I can input both structured features (m<sup>2</sup>, location, etc) and image features. So that's what I'm trying right now. It's tricky though because the number of pictures varies across samples, the pictures are of different sizes, and the pictures aren't standardized in any way (some listings have five pictures of the kitchen and none of the bedrooms, others have no pictures of kitchen, etc).

The same friend also suggested that I use some pre-trained neural network capable of identifying objects like "window", "A/C unit", and so on, and then use the identified objects as features. That's the next item on my to-do list.

All that said, the truth is that I'm not sure the images will be useful in the end. It's like with the texts: you could keep taking new pictures of the property until you get the "right" price. I think that's harder to do with pictures than with texts, but who knows. I need to think more about it. Suggestions are welcome.

**"someone must be doing it already!"**

You bet. ZAP [is doing it](https://www.zapimoveis.com.br/quanto-vale/). Which makes sense: they have tons of data, so why not use it? In fact just last month they [announced](http://www.tibahia.com/tecnologia_informacao/conteudo_unico.aspx?c=SERVICOS&fb=B_FULL&hb=B_CENTRA&bl=LAT1&r=SERVICOS&nid=52998) the next step: they'll start buying property themselves, picking the ones that their model suggests are underpriced.

In the US Zillow [is doing it](https://www.zillow.com/zestimate/). I bet that there are plenty of similar initiatives all over the world.

So I'm not proposing anything new here. Which makes it hard to understand why the heck Brazilian banks are not doing it yet. They have billions at stake.

**incentives matter**

I know better than to second guess the choices of people with skin in the game. But 70% of all mortgages in Brazil are concentrated in a state-owned bank - Caixa Econômica Federal (CEF). And when the state is involved the incentives are different. It's not about delivering results but about broadening your mandate, blame-shifting, and securing resources. (If you want to have an idea of how government works, watch HBO's Chernobyl.)

So it's not a market failure that we have here, but by and large a state failure. CEF's bureaucrats do not get punished for using the wrong tool to do property valuation. In a state-owned company there is a lot of noise between your actions and your punishments/rewards. Which helps explain CEF's long history of incompetence and [corruption](http://agenciabrasil.ebc.com.br/justica/noticia/2018-10/mpf-oferece-4-denuncias-por-fraude-de-r-3-bi-na-caixa-e-no-fgts).

<iframe src="https://giphy.com/embed/LMWUPwA8LMQiLQHseo" width="480" height="274" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/LMWUPwA8LMQiLQHseo"></a></p>

Not to mention that an entire ecosystem has evolved around the status quo. You see, to be contracted by CEF as an appraiser you need to be certified by the Federal Council of Realtors (yes, that exists). There's an exam for that and there are schools that charge good money to help prepare you for that exam. So, there are lots of people who benefit from the current system, which makes it harder to change.

**so long**

I guess this is it. I hope this post has inspired you to roll up your sleeves and do your own valuations from now on.

Happy appraisals!