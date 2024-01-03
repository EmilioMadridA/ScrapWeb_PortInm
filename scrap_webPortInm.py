import requests
import numpy as np
from bs4 import BeautifulSoup
import re
import pandas as pd
import seaborn as sns
import plotly.express as px

url = 'https://www.portalinmobiliario.com/venta/casa/san-fernando-bernardo-ohiggins'
response = requests.get(url)
soup = BeautifulSoup(response.content)

pages = np.arange(1,40*42,42).tolist() # Recopila información del total de páginas

def transform_html_to_data(soup):
    apartments_data = soup.find_all(class_='ui-search-layout__item')
    apartments = []
    for aparment in apartments_data:
        price = aparment.find('span',class_='andes-money-amount__fraction').text
        price = int(price.replace('.',''))
        address = aparment.find(class_='ui-search-item__group__element ui-search-item__location-label').text
        space_information = aparment.find(class_='ui-search-card-attributes ui-search-item__group__element ui-search-item__attributes-grid').text
        if space_information:
            size = re.search('(\d+) m', space_information)
            if size:
                size = int(size.group(1))
            rooms = re.search('(\d+) dormitorio', space_information)
            if rooms:
                rooms = int(rooms.group(1))
        data = {'price (CLP)':price, 'rooms':rooms, 'size (m2)':size, 'address': address}
        apartments.append(data)
    return apartments

apartments_list = []
for page in pages:
    url = 'https://www.portalinmobiliario.com/venta/casa/san-fernando-bernardo-ohiggins/_Desde_'+str(page)+'_NoIdex_True'
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    apartments_list += transform_html_to_data(soup)

print(apartments_list[3])

len(apartments_list)

apartments_list

df = pd.DataFrame(apartments_list)
df.head()

df.shape

# Limpieza de Datos
# Partimos limpiando aquellos que no entregan a lo menos 1 de los 4 datos solicitados

df.isna().sum()

df.dropna(inplace=True) # Elimina los que no cumplen requisitos
df.shape

'''condition = df['price (CLP)'] < 2500000 # Selecciona la condicion, en este caso, arriendo menores a 2.500.000
df = df[condition]
df.shape'''

'''condition = df['price (CLP)'] > 1000 # Selecciona la condicion, en este caso, arriendo mayores a 1.000 (Permite eliminar aquellos que estan en UF)
df = df[condition]'''

'''condition = df['rooms'] < 5 # Selecciona la condicion, en este caso, aquellos deptos con menos de 5 dormitorios
df = df[condition]'''

# Visualizacion de datos

fig = px.scatter(df, x='size (m2)', y='price (CLP)', size="rooms", title="Precio vs Tamaño")
fig.show()

sns.countplot(x='rooms', data=df)
sns.set(rc={'figure.figsize':(15,6)})

sns.catplot(x='rooms', y='price (CLP)', data=df, kind='box')

sns.regplot(x='size (m2)', y='price (CLP)', data=df)
sns.set(rc={'figure.figsize':(15,6)})

'''condition = df['size (m2)'] < 100
df_max_size_200 = df[condition]'''

#sns.regplot(x='size (m2)', y='price (CLP)', data = df_max_size_200, color ='green')

df.to_excel('./SnFdo.xlsx')
