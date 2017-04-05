from bs4 import BeautifulSoup
import requests

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
        dt = {
                'title': title,
                'sinopse': sinopse,
        }
        dd = book_data.find_all('dd')
        for i, data in enumerate(book_data.find_all('dt')):
                key = data.text.strip()
                dt[key] = dd[i].text.strip()
        return dt

for linha in open('codigoBarras.txt'):
  linha = linha.strip()
  print(linha)
  try:
      if linha[:1] != '#':
          whatever = get_book_info(linha)
          print(whatever['title'])
          print(whatever['sinopse'])
          print(whatever['ISBN:'])
          print(whatever['Dimensões:'])
  except AttributeError:
     pass
  except KeyError:
      pass



