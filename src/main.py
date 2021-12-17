import os
import argparse
from recommendationSystem import RecommendationSystem as RS

# Paso de parámetros por línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="input file txt")
parser.add_argument("numofdocument", default=0, type=int, help="input number of documents")
args = parser.parse_args()

# Recibimos documentos y comprobamos que existe
if (os.path.exists('./doc/' + args.file)):
  file = './doc/' + args.file
  A = RS(file)

  # Seleccionamos la tabla a observar
  print("\n------------------------ Documento " + str(args.numofdocument) + " --------------------------\n")
  A.printTable(args.numofdocument)

  print("\n------------------------ Matriz similitud coseno entre documentos --------------------------\n")
  A.printSimTable()
  
else:
  print('File not Found')