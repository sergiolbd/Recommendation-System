import math
from tabulate import tabulate
import re

# Clase que almacena los atributos y métodos necesarios de un sistema de recomendación
# siguiendo el modelo basado en el contenido
class RecommendationSystem:

  def __init__(self, file):
    self.num_of_documents = 0
    self.documentsArray = [] # Almacena en cada posición un documento
    self.normalizedTF = [] # TF normalizado
    self.tableFinal = [] # Tabla Indice, termino, TF, IDF, TF-IDF
    self.simTable = [] # Matrix de similitud de documentos

    self.readFile(file)

    # Calcular tabla para cada documento
    for i in range(self.num_of_documents):
      self.table = [['Índice del Término', 'Término', 'TF', 'IDF', 'TF-IDF']]
      tablei = self.modelContent(i)
      self.setTable(tablei)

    self.setnormalizerTF()
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
      self.table.append([j, self.documentsArray[i][j], tf, idf, tf*idf])

    return self.table

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
    idf = round(math.log10(N/dfx), 2)

    return idf

  # Configurar valores de la tabla
  def setTable(self, tablei):
    self.tableFinal.append(tablei)

  # Setear tablero 
  def setSimTable(self):
    docs = []
    for i in range(self.num_of_documents+1):
      if i == 0: 
        docs.append("docs")
      else:
        docs.append("doc" + str(i))

    self.simTable.append(docs)

    for j in range(self.num_of_documents):
      docs = []
      for i in range(self.num_of_documents+1):
        if i == 0:
          docs.append("doc" + str(j+1))
        else:
          # Por cada pareja de documentos obtener si similitud
          docs.append(self.calculateSimCos(i-1, j))

      self.simTable.append(docs)

  # Mostrar tabla similitud por pantalla
  def printSimTable(self):
    print(tabulate(self.simTable, headers='firstrow', tablefmt='grid'))

  def calculateSimCos(self, indexA, indexB):
    # Calcular la similitud entre dos documentos
    # Obtener los dos documentos
    A = self.documentsArray[indexA]
    B = self.documentsArray[indexB]

    # Obtener los términos comunes a ambos documentos
    commonTerms = list(set(A) & set(B))
    
    # Obtener los tf normalizados para los terminos comunes
    normalizedTFA = []
    normalizedTFB = []
    for termN in self.normalizedTF[indexA]:
      for commonTerm in commonTerms:
        if termN[0] == commonTerm:
          normalizedTFA.append(termN[1])

    for termN in self.normalizedTF[indexB]:
      for commonTerm in commonTerms:
        if termN[0] == commonTerm:
          normalizedTFB.append(termN[1])
 
    # Calcular la similitud coseno entre ambos
    simCos = 0
    for i in range(len(normalizedTFA)):
      simCos += normalizedTFA[i] * normalizedTFB[i]

    return round(simCos, 3)

  # Normalizar el TF de cada término
  def setnormalizerTF(self):
    # Recorrer cada una de las tablas
    for i in self.tableFinal:
      pair_term_tf = []
      pow_tf = []
      # Recorrer cada fila de la tabla
      for j in i:
        # Ignoramos la cabecera de cada tabla
        if j != ['Índice del Término', 'Término', 'TF', 'IDF', 'TF-IDF']:
          pow_tf.append(pow(j[2], 2))

      normalized = math.sqrt(sum(pow_tf))
  
      for j in i: 
        if j != ['Índice del Término', 'Término', 'TF', 'IDF', 'TF-IDF']:
          normalized_tf = float(j[2] / normalized)
          pair_term_tf.append([j[1], normalized_tf, 3])

      self.normalizedTF.append(pair_term_tf)

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
    # Eliminar dobles espacios
    linea = re.sub(r'  ', '', linea)
    # Convertirmos el string a un array usando como delimitador el espacio
    arrayLinea = linea.split(" ")
    # Eliminados cadenas vacias y saltos de línea de nuestro array
    arrayLinea = list(filter(('').__ne__, arrayLinea))
    arrayLinea = list(filter(('\n').__ne__, arrayLinea))
    return arrayLinea

  # Obtener un determinado documento
  def getDocumentArray(self, index):
    return self.documentsArray[index]

  # Proporciona salida en formato tabla
  def printTable(self, i):
    print(tabulate(self.tableFinal[i], headers='firstrow', tablefmt='grid'))

  # Obtener el número de documentos de un fichero
  # Cada línea dentro del fichero hace referencia a un documento
  def getNumOfDocuments(self):
    return self.num_of_documents