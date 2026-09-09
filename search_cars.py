import sqlite3


def search_cars(
    max_price=None,
    fuel=None,
    transmission=None,
    body_type=None
):
    connection = sqlite3.connect("cars.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = "SELECT * FROM cars WHERE available = 1"
    parameters = []

    if max_price:
        query += " AND price <= ?"
        parameters.append(max_price)

    if fuel:
        query += " AND LOWER(fuel) = LOWER(?)"
        parameters.append(fuel)

    if transmission:
        query += " AND LOWER(transmission) = LOWER(?)"
        parameters.append(transmission)

    if body_type:
        query += " AND LOWER(body_type) = LOWER(?)"
        parameters.append(body_type)

    query += " ORDER BY price ASC"

    cursor.execute(query, parameters)
    cars = cursor.fetchall()

    connection.close()

    return [dict(car) for car in cars]
