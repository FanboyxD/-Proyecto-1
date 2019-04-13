import csv

Userlist = []

def escritura(Userlist):

	with open("Usuarios_prueba.csv","a", newline = '') as doc_usuarioscsv:
		csv_data = csv.writer(doc_usuarioscsv)
		csv_data.writerows(Userlist)
	doc_usuarioscsv.close()

def lectura():
	doc = open("Usuarios_prueba.csv","r")
	documento = csv.reader(doc)
	for (nombre) in documento:
		print (nombre)
	doc.close()

def pro(mo,Userlist):
	Userlist = Userlist +[[mo]]
	escritura(Userlist)


pro("ahuevo",Userlist)

lectura()