import numpy as np
import math
from tabulate import tabulate
import re

# Clase que almacena los atributos y métodos necesarios de un sistema de recomendación
# siguiendo el modelo basado en el contenido
class RecommendationSystem:

  def __init__(self, file):
    self.num_of_documents = 0
    self.documentsArray = [] # Almacena en cada posición un documento

    self.readFile(file)

    self.table = [['Índice del Término', 'Término', 'TF', 'IDF', 'TF-IDF']]

  def readFile(self, file):
    f = open(file, "r")
  
    for linea in f:
      self.num_of_documents += 1
      self.documentsArray.append(self.cleanDocument(linea))
      # print(cleanDocument)

    f.close()
    

  def cleanDocument(self, linea):
    return re.sub(r'[^\w\s]', '', linea)

  def getDocumentArray(self, index):
    return self.documentsArray[index]

  # Proporciona salida en formato tabla
  def printTable(self):
    print(tabulate(self.table, headers='firstrow', tablefmt='grid', showindex=True))

  # Obtener el número de documentos de un fichero
  # Cada línea dentro del fichero hace referencia a un documento
  def getNumOfDocuments(self):
    return self.num_of_documents