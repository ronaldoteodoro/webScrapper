#!/usr/bin/python

import re
import pymssql

ESTADO_INICIAL = 0
ESTADO_LENDO_TITULO = 1
ESTADO_LENDO_DIMENSOES = 2
ESTADO_LENDO_ISBN = 3
ESTADO_LENDO_TEMA = 4
ESTADO_FINAL = 5

estado = ESTADO_LENDO_TITULO
re_dimensoes = re.compile('([0-9]+,?[0-9]+)\scm x ([0-9]+,?[0-9]+)\scm\s\|\s([0-9]+)\sp[áa]ginas')

titulo = ''
dimensoes = (0, 0)
paginas = 0
tema = ''

conn = pymssql.connect(server='srvSAP',user='sa', password='senhasa@1234', database='FastCommerce')
cursor = conn.cursor()

for linha in open('he.txt'):
  linha = linha.strip()

  if estado == ESTADO_INICIAL:
    titulo = ''
    dimensoes = (0, 0)
    paginas = 0
    tema = ''

    estado = ESTADO_LENDO_TITULO

  if estado == ESTADO_LENDO_TITULO:
    if re_dimensoes.match(linha):
      estado = ESTADO_LENDO_DIMENSOES
    else:
      titulo = (titulo + ' ' + linha).strip()

  if estado == ESTADO_LENDO_TEMA:
    if linha.startswith("Tema: "):
      tema = [t.strip() for t in linha[6:].split(',')]
    estado = ESTADO_FINAL

  if estado == ESTADO_LENDO_ISBN:
    isbn = linha.strip()
    isbn = linha.replace("-","")
    estado = ESTADO_LENDO_TEMA

  if estado == ESTADO_LENDO_DIMENSOES:
    alt, larg, pag = re_dimensoes.findall(linha)[0]
    dimensoes = (float(alt.replace(",", ".")), float(larg.replace(",", ".")))
    paginas = int(pag)
    estado = ESTADO_LENDO_ISBN

  if estado == ESTADO_FINAL:
    print("Titulo: %s\n"
          "Dimensões: altura %f, largura %f\n"
          "Páginas: %d\n"
          "ISBN: %s\n"
          "Tema: %s\n" % (titulo, dimensoes[0], dimensoes[1], paginas, isbn, tema))
    titulo = "'" + titulo + "'"
    tema = "'" + ",".join(tema) + "'"
    sql = "INSERT INTO dbo.catalogoCiranda(isbn,titulo,altura,largura,paginas,tema) VALUES (%s,%s,%f,%f,%d,%s)" % (isbn,titulo, dimensoes[0], dimensoes[1], paginas,tema)
    print (sql)
    cursor.execute(sql)

    estado = ESTADO_INICIAL
conn.commit()
conn.close()
