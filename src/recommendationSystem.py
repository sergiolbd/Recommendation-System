import numpy as np
import math
from tabulate import tabulate
from collections import OrderedDict
import re

# Clase que almacena los atributos y métodos necesarios de un sistema de recomendación
# siguiendo el modelo basado en el contenido
class RecommendationSystem:

  def __init__(self, file):
    self.num_of_documents = 0
    self.documentsArray = [] # Almacena en cada posición un documento

    self.readFile(file)

    self.table = [['Índice del Término', 'Término', 'TF', 'IDF', 'TF-IDF']]

    self.simTable = []
    self.setSimTable()

  # Leer el fichero txt pasado por parámetros
  def readFile(self, file):
    f = open(file, "r")
  
    for linea in f:
      self.num_of_documents += 1
      self.documentsArray.append(self.cleanDocument(linea))

    f.close()
    
  # Método para calcular los distintos parámetros de un término
  # i --> indice del documento a obtener la tabla
  def modelContent(self, i): 

    duplicate = []

    for j in range(len(self.documentsArray[i])):
      # Eliminar las palabras duplicadas de la tabla
      flag = False
      for k in range(len(duplicate)):
        if self.documentsArray[i][j] == duplicate[k]:
          flag = True

      if flag:
        continue

      # Calcular TF(x,y)
      tf = 0
      tf = self.calculateTF(self.documentsArray[i], self.documentsArray[i][j])
      # Si el tf > 1 significa que la palabra esta duplicada
      if tf > 1:
        duplicate.append(self.documentsArray[i][j])

      # Calcular IDF(x)
      idf = self.calculateIDF(self.documentsArray[i][j])
    
      # Introducir cálculos en la tabla
      self.setTable(j, self.documentsArray[i][j], tf, idf, tf*idf)


  # Método que recibe un array (document), y debe devolver un array con el número de ocurrencias de cada término
  def calculateTF(self, document, term):
    return document.count(term)

  # Método para calcular IDF
  def calculateIDF(self, term):
    N = self.getNumOfDocuments()
    # dfx = Número de documentos que contienen x
    dfx = 0
    for i in range(N):
      if term in self.documentsArray[i]:
        dfx += 1
    # Frecuencia inversa calculada IDF
    idf = 0
    idf = round(math.log(N/dfx), 2)

    return idf


  # Configurar valores de la tabla
  def setTable(self, index, term, tf, idf, tfidf):
      self.table.append([index, term, tf, idf, tfidf])

  # Setear tablero inicial
  def setSimTable(self):
    docs = []
    for i in range(self.num_of_documents):
      docs.append("doc" + str(i))

    self.simTable.append(docs)

    for j in range(self.num_of_documents):
      docs = []
      for i in range(self.num_of_documents):
        if i == 0:
          docs.append("doc" + str(j))
        else:
          docs.append(0)

      self.simTable.append(docs)

  # Mostrar tabla similitud por pantalla
  def printSimTable(self):
    print(tabulate(self.simTable, headers='firstrow', tablefmt='grid'))


  # Formatear los documentos
  def cleanDocument(self, linea):
    # Eliminar signos de puntación
    linea = re.sub(r'[^\w\s]', '', linea)
    # Convertir todo el texto a mayúscula
    linea = linea.lower()
    # Eliminar los números
    linea = re.sub(r'[0-9]+', '', linea)
    # Eliminar los \n
    linea = re.sub(r'\n', '', linea)
    # Convertirmos el string a un array usando como delimitador el espacio
    arrayLinea = linea.split(" ")
    # Eliminamos el último elemento ('\n')
    if arrayLinea[-1] == "\n":
      arrayLinea.pop()
    return arrayLinea

  # Obtener un determinado documento
  def getDocumentArray(self, index):
    return self.documentsArray[index]

  # Proporciona salida en formato tabla
  def printTable(self):
    print(tabulate(self.table, headers='firstrow', tablefmt='grid'))

  # Obtener el número de documentos de un fichero
  # Cada línea dentro del fichero hace referencia a un documento
  def getNumOfDocuments(self):
    return self.num_of_documents