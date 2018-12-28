import mysql.connector

mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database = "tv"
        )
db = mydb.cursor()
db.execute("INSERT INTO `tv`.`classify` (`value`,`pid`) VALUES ('q','1'),('q','1')")
print(db.rowcount)
mydb.commit()
