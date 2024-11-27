import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# lista empleados
employees = [
    {'id': 1, 'name': 'Alessandro'},
    {'id': 2, 'name': 'Manel'},
    {'id': 3, 'name': 'Diego'}
    ]

# ID para el siguiente empleado
nextEmployeeId = 4


# Función auxiliar para obtener un empleado por su ID
def get_employee(id):
    return next((e for e in employees if e['id'] == id), None)

# Función para validar los empleados
def employee_is_valid(employee):
    return 'name' in employee

# Ruta para obtener todos los empleados (GET)
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

# Ruta para obtener un empleado por su ID (GET)
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id:int):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404
    return jsonify(employee)

# Ruta para crear un nuevo empleado (POST)
@app.route('/employees', methods=['POST'])
def create_employes():
    global nextEmployeeId
    employee = json.loads(request.data)
    
    if not employee_is_valid(employee):
        return jsonify({'error': 'Invalid employee properties.'}), 400
    
    employee['id'] = nextEmployeeId
    nextEmployeeId += 1
    
    employees.append(employee)
    return '', 201, {'location': f'/employees/{employee["id"]}'}

# ruta para actualizar en empleado por ID (PUT)
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id:int):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404
    
    updated_employee = json.loads(request.data)
    
    if not employee_is_valid(updated_employee):
        return jsonify({'error': 'Invalid employee properties.'}), 400
    
    employee.update(updated_employee)
    return jsonify(employee)

# Ruta para eliminar un empleado por su ID (DELETE)
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id: int):
    global employees  # Declarar que estamos trabajando con la variable global
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404

    # Filtrar y eliminar el empleado con el ID especificado
    employees = [e for e in employees if e['id'] != id]
    return jsonify(employee), 200


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(port=5000)