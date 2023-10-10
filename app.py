import mysql.connector

# Устанавливаем соединение с базой данных
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Danil2002',
    database='mydatabase'
)

# Функция для выполнения SQL-запроса и вывода результатов
def execute_and_print_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    for row in results:
        print(row)

# Примеры запросов:

# 1. Вывести все машины и их водителей:
query1 = '''
    SELECT Cars.CarName, Drivers.DriverName
    FROM Cars
    JOIN CarDriverRelationship ON Cars.CarID = CarDriverRelationship.CarID
    JOIN Drivers ON CarDriverRelationship.DriverID = Drivers.DriverID
'''
print("Машины и их водители:")
execute_and_print_query(query1)

# 2. Вывести всех водителей и машины, которыми они управляют:
query2 = '''
    SELECT Drivers.DriverName, Cars.CarName
    FROM Drivers
    JOIN CarDriverRelationship ON Drivers.DriverID = CarDriverRelationship.DriverID
    JOIN Cars ON CarDriverRelationship.CarID = Cars.CarID
'''
print("\nВодители и машины, которыми они управляют:")
execute_and_print_query(query2)

# 3. Вывести машины и количество водителей для каждой машины:
query3 = '''
    SELECT Cars.CarName, COUNT(Drivers.DriverID) AS NumberOfDrivers
    FROM Cars
    LEFT JOIN CarDriverRelationship ON Cars.CarID = CarDriverRelationship.CarID
    LEFT JOIN Drivers ON CarDriverRelationship.DriverID = Drivers.DriverID
    GROUP BY Cars.CarName
'''
print("\nМашины и количество водителей:")
execute_and_print_query(query3)

# Закрываем соединение с базой данных
conn.close()