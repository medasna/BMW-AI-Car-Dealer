import sqlite3

connection = sqlite3.connect("cars.db")
cursor = connection.cursor()

# Create the cars table
cursor.execute("""
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER,
    price INTEGER,
    fuel TEXT,
    transmission TEXT,
    body_type TEXT,
    horsepower INTEGER,
    mileage INTEGER,
    seats INTEGER,
    available INTEGER
)
""")

# Clear the existing inventory
cursor.execute("DELETE FROM cars")

# BMW inventory
cars = [
    ("BMW", "1 Series", 2023, 28500, "Petrol", "Automatic", "Hatchback", 136, 18000, 5, 1),
    ("BMW", "1 Series", 2022, 24500, "Diesel", "Manual", "Hatchback", 116, 35000, 5, 1),
    ("BMW", "2 Series Gran Coupe", 2023, 33500, "Petrol", "Automatic", "Sedan", 178, 22000, 5, 1),
    ("BMW", "2 Series", 2021, 29500, "Diesel", "Automatic", "Coupe", 190, 41000, 4, 1),

    ("BMW", "3 Series", 2024, 42000, "Petrol", "Automatic", "Sedan", 184, 12000, 5, 1),
    ("BMW", "3 Series", 2022, 36500, "Diesel", "Automatic", "Sedan", 190, 38000, 5, 1),
    ("BMW", "3 Series Touring", 2023, 39500, "Diesel", "Automatic", "Wagon", 190, 25000, 5, 1),

    ("BMW", "4 Series Coupe", 2022, 45500, "Petrol", "Automatic", "Coupe", 184, 29000, 4, 1),
    ("BMW", "4 Series Gran Coupe", 2023, 44000, "Diesel", "Automatic", "Sedan", 190, 21000, 5, 1),

    ("BMW", "5 Series", 2023, 52000, "Diesel", "Automatic", "Sedan", 197, 18000, 5, 1),
    ("BMW", "5 Series", 2021, 39500, "Diesel", "Automatic", "Sedan", 190, 55000, 5, 1),
    ("BMW", "5 Series Touring", 2022, 43500, "Diesel", "Automatic", "Wagon", 190, 47000, 5, 1),

    ("BMW", "X1", 2024, 41500, "Petrol", "Automatic", "SUV", 170, 10000, 5, 1),
    ("BMW", "X1", 2022, 35000, "Diesel", "Automatic", "SUV", 150, 32000, 5, 1),
    ("BMW", "X1", 2021, 31000, "Petrol", "Manual", "SUV", 136, 48000, 5, 1),

    ("BMW", "X3", 2023, 48500, "Diesel", "Automatic", "SUV", 190, 24000, 5, 1),
    ("BMW", "X3", 2021, 39500, "Diesel", "Automatic", "SUV", 190, 52000, 5, 1),

    ("BMW", "X5", 2023, 68000, "Diesel", "Automatic", "SUV", 286, 18000, 5, 1),
    ("BMW", "X5", 2021, 55500, "Diesel", "Automatic", "SUV", 286, 61000, 5, 1),

    ("BMW", "X6", 2022, 62500, "Petrol", "Automatic", "SUV", 340, 35000, 5, 1),
    ("BMW", "X7", 2023, 79000, "Diesel", "Automatic", "SUV", 340, 22000, 7, 1),

    ("BMW", "Z4", 2022, 48500, "Petrol", "Automatic", "Convertible", 197, 19000, 2, 1),
    ("BMW", "M2", 2023, 72000, "Petrol", "Automatic", "Coupe", 460, 9000, 4, 1),
    ("BMW", "M3", 2022, 79500, "Petrol", "Automatic", "Sedan", 510, 16000, 5, 1),
]

cursor.executemany("""
INSERT INTO cars (
    brand, model, year, price, fuel, transmission,
    body_type, horsepower, mileage, seats, available
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", cars)

connection.commit()
connection.close()

print(f"BMW inventory created successfully! {len(cars)} cars added.")
