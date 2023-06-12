from PIL import Image, ImageDraw, ImageFont
import csv
import random

# Définir les paramètres de l'image et du tableau
pays = ["France", "Cuba",  "Egypte", "Canada" ,  "Brézil" , "USA","Chili","Japan"]
image_width = 600
image_height = 600
img_size = (600, 600)
table_rows = 5
table_cols = 5
cell_width = int(image_width / table_cols)
cell_height = int(image_height / table_rows)

# Définir les polices à utiliser pour chaque tableau
fonts = [
    "fonts/Arial.ttf",
    "fonts/Verdana.ttf",
    "fonts/Times New Roman.ttf",
    "fonts/Courier New.ttf",
    "fonts/Calibri.ttf",
    "fonts/Garlicha.ttf",
    "fonts/Georgia.ttf",
    "fonts/Manuela.otf",
    "fonts/Rough Anthem Italic.ttf",
    "fonts/Rough Anthem.ttf",
    "fonts/Space Crusaders.ttf"
]

# Boucle sur les 5 tableaux à générer
for i in range(20):
    # Créer une nouvelle image vide
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Sélectionner une police aléatoire pour ce tableau
    font = ImageFont.truetype(random.choice(fonts), size=24)

    # Générer les données du tableau et les dessiner sur l'image
    table_data = []
    for row in range(table_rows):
        row_data = []
        for col in range(table_cols):
            cell_data = random.choice(pays)
            row_data.append(cell_data)
            draw.text((col * cell_width+20, row * cell_height+20), cell_data, font=font, fill="black")
        table_data.append(row_data)



    # Enregistrer l'image au format JPG
    image.save(f"table_{i+1}.jpg")

    # Enregistrer les données du tableau dans un fichier CSV
    with open(f"table_{i+1}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(table_data)
