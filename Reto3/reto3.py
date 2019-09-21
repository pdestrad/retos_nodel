import csv

f = open("reto3.txt", "w+")
##	Obteniendo cantidad de reviews
with open('amazon.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    cantidad_reviews = sum(1 for filas in readCSV)
    f.write("-- {} REVIEWS -- \n\n\n".format(cantidad_reviews))

##	Escribiendo cada review
with open('amazon.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    ignorar_primera_linea = True
    for fila in readCSV:
    	if ignorar_primera_linea:
    		ignorar_primera_linea = False
    	else:
    		f.write("{} - {} ({})\n{}\n\n".format(fila[2],fila[3],fila[6],fila[5]))
    		f.write("--------------------------------------\n")
   	
f.close()