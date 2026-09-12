import sqlite3

# Connect to your existing database
connection = sqlite3.connect("cars.db")
cursor = connection.cursor()

# Public BMW images from Wikimedia Commons
IMAGE_URLS = {
    "1 Series": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_1_Series.jpg",
    "2 Series Gran Coupe": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_2_Series_Gran_Coupe_IMG001.jpg",
    "2 Series": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_2_SERIES_COUPE_%28G42%29_China_%282%29.jpg",
    "3 Series": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_3_Series_%28G20%29.jpg",
    "3 Series Touring": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_3_Series_touring_%2842258706764%29.jpg",
    "4 Series Coupe": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_4-Series_Coup%C3%A9_%28G22%29_420i_%282021%29_%2852915569315%29.jpg",
    "4 Series Gran Coupe": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_4_SERIES_GRAN_COUPE_%28G22%29_China_%284%29.jpg",
    "5 Series": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_5_Series_G30_black_%282%29.jpg",
    "5 Series Touring": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_5_series_Touring_%284051833058%29.jpg",
    "X1": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_X1_%28U11%29_%E2%80%93_f_15122024.jpg",
    "X3": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_X3_%28G01%29_%2824062344414%29.jpg",
    "X5": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_X5_G05_black_%281%29.jpg",
    "X6": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_X6_.jpg",
    "X7": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_X7.jpg",
    "Z4": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_Z4_g29.jpg",
    "M2": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_M2_%28G87%29.jpg",
    "M3": "https://commons.wikimedia.org/wiki/Special:Redirect/file/BMW_M3_%28G80%2C_2022%29_%2852227837026%29.jpg",
}

# Update existing cars ONLY
updated = 0

for model, image_url in IMAGE_URLS.items():
    cursor.execute(
        """
        UPDATE cars
        SET image_url = ?
        WHERE model = ?
        """,
        (image_url, model)
    )

    updated += cursor.rowcount

connection.commit()
connection.close()

print(f"Done! Added image URLs to {updated} cars.")