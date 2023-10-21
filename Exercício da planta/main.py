import mysql.connector
conexao = mysql.connector.connect(host="localhost", user="root", password="159159", database="exercicio_planta")

if conexao.is_connected:
    print("Conectado!")

cursor = conexao.cursor()

json = open("logger.json", "r")

content = json.read()

dados = []
bruto = ""
virgula = 0

for i in range(len(content)):
    if content[i] == ",":
        virgula += 1

    if virgula != 5:
        bruto += content[i]
    else:  
        iD = ""
        datetime = ""
        hum = ""
        ledDiff = ""
        lux = ""
        temp = ""

        aspas = 0
        for j in range(len(bruto)):
            if bruto[j] == '"':
                aspas = aspas + 1
            if aspas <= 2:
                iD += bruto[j]
            elif aspas <= 6 and aspas > 4:
                datetime += bruto[j]
            elif aspas <= 10 and aspas > 8:
                hum += bruto[j]
            elif aspas <= 14 and aspas > 12:
                ledDiff += bruto[j]
            elif aspas <= 18 and aspas > 16:
                lux += bruto[j]
            elif aspas <= 22 and aspas > 20:
                temp += bruto[j]

        iD = iD.replace('"', "").replace('-', "").replace(":", "").replace("{", "")
        datetime = datetime.replace('"', "").replace(",", "")
        hum = hum.replace('"', "").replace(",", "")
        ledDiff = ledDiff.replace('"', "").replace(",", "")
        lux = lux.replace('"', "").replace(",", "")
        temp = temp.replace('"', "").replace("}", "").replace(",", "")
        
        dados.append((iD, datetime, hum, ledDiff, lux, temp))
        virgula = 0
        bruto = ""

print(dados)

insert = "INSERT INTO dados (iD, datetim, hum, ledDiff, lux, temp) VALUES (%s, %s, %s, %s, %s, %s)"

try:
    cursor.executemany(insert, dados)
    conexao.commit()

except mysql.connector.Error as err:
    conexao.rollback()
    print(err)

conexao.close()
cursor.close()