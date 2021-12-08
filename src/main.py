import os
import argparse
from recommendationSystem import RecommendationSystem as RS


# Paso de parámetros por línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="input file txt")
args = parser.parse_args()

# Recibimos documentos y comprobamos que existe
if (os.path.exists('./doc/' + args.file)):
  file = './doc/' + args.file
  A = RS(file)

  print(A.getNumOfDocuments())

  print(A.getDocumentArray(1))

  A.printTable()

else:
  print('File not Found')