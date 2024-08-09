from services import database as db
from Controller.models.Cliente import Cliente

def create_cliente(cliente):
    db.cursor.execute('INSERT INTO clients (first_name, last_name, DNI, email, age, sex, date_created) '
                      'VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                      (cliente.first_name, cliente.last_name, cliente.DNI, cliente.email, cliente.age, cliente.sex, cliente.date_created))

def read_clientes():
    db.cursor.execute('SELECT * FROM clients')
    clienteList = []
    for row in db.cursor.fetchall():
        clienteList.append(Cliente(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    return clienteList

def delete_cliente(id):
    db.cursor.execute('DELETE FROM clients WHERE id = %s', (id,))

def update_cliente(cliente):
    db.cursor.execute('UPDATE clients SET first_name = %s, last_name = %s, DNI = %s, email = %s, age = %s, sex = %s, date_created = %s WHERE id = %s', 
                      (cliente.first_name, cliente.last_name, cliente.DNI, cliente.email, cliente.age, cliente.sex, cliente.date_created, cliente.id))

def select_cliente_by_id(id):
    db.cursor.execute('SELECT * FROM clients WHERE id = %s', (id,))
    result = db.cursor.fetchone()
    if result:
        return Cliente(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
    return None
