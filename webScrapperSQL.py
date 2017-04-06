from bs4 import BeautifulSoup
import requests
import wget
import pyodbc

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=srvFLEX;DATABASE=FCDEV;UID=sa;PWD=senhasa@1234')
cursor = cnxn.cursor()

def get_book_info(barcode):
        headers = {
                'User-agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
        }
        response = requests.get('https://www.cirandacultural.com.br/busca/{0}'.format(barcode))
        search_html = response.text
        soup = BeautifulSoup(search_html, 'html.parser')
        product_listing = soup.find(class_="listItems")
        product_link = product_listing.find('a').attrs['href']
        response = requests.get('https://www.cirandacultural.com.br{0}'.format(product_link), headers=headers)
        book_html = response.text
        soup = BeautifulSoup(book_html, 'html.parser')
        title = soup.find(class_='product-master-title').text.strip()
        sinopse = soup.find(id='collapseOne').find(class_='panel-body').text.strip()
        book_data = soup.find(id='bookData')
        imgPath = soup.find(id='product-media').find(class_='img-responsive')

        dt = {
                'title': title,
                'sinopse': sinopse,
                'imgPath' : 'https://www.cirandacultural.com.br{0}'.format(imgPath.attrs.get('src'))
        }
        dt['imgPath'] = dt['imgPath'].replace('false','true')
        dd = book_data.find_all('dd')
        for i, data in enumerate(book_data.find_all('dt')):
                key = str( data.text.strip() )
                key = key.replace(':','')
                dt[key] = dd[i].text.strip()
        return dt

cursor.execute("Select CodBarrasProd from dbo.Produtos")
rows = cursor.fetchall()
atual = 1

for row in rows:
    try:
            whatever = get_book_info(row.CodBarrasProd)
            filename = whatever['Código de barras'] + '.jpg'
            url = whatever['imgPath']
            img = wget.download(url,out="c:\\imgCiranda\\" + filename)
            peso = whatever['Peso'].split(' ')
            whatever['Peso'] = peso[0]
            print('Atualizando produto: ' + str(atual))
            print(int(whatever['Código de barras']))
            cursor.execute("UPDATE dbo.produtos SET NomeProd = ? , Peso  = ? , DescrLonga = ?"
                           " WHERE CodBarrasProd = ?",
                           whatever['title'], int(whatever['Peso']), whatever['sinopse'],
                           int(whatever['Código de barras']))
            cnxn.commit()
            atual = atual + 1
    except AttributeError as attribExp :
        attribExp.__traceback__
        pass
    except KeyError as keyErrorExp:
        keyErrorExp.__traceback__
        pass




