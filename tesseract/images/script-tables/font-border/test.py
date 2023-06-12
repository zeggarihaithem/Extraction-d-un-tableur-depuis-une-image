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
cell_width = int((image_width-20) / table_cols)
cell_height = int((image_height-20) / table_rows)

# Définir les polices à utiliser pour chaque tableau
fonts = [
    "fonts/Arial.ttf",
    "fonts/Verdana.ttf",
    "fonts/Times New Roman.ttf",
    "fonts/Courier New.ttf",
    "fonts/Calibri.ttf",
    "fonts/Georgia.ttf"
]

# Boucle sur les 5 tableaux à générer
for i in range(20):
    # Créer une nouvelle image vide
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Sélectionner une police aléatoire pour ce tableau
    font = ImageFont.truetype(random.choice(fonts), 20)

    # Générer les données du tableau et les dessiner sur l'image
    draw.line([(10, 10), (10, img_size[1]-10)], fill=(0, 0, 0))
    draw.line([(10, 10), (img_size[0]-10, 10)], fill=(0, 0, 0))
    draw.line([(img_size[0]-10, 10), (img_size[0]-10, img_size[1]-10)], fill=(0, 0, 0))
    draw.line([(10, img_size[1]-10), (img_size[0]-10, img_size[1]-10)], fill=(0, 0, 0))
    table_data = []
    for row in range(table_rows):
        row_data = []
        x = row * cell_width
        if x > 10:
            draw.line([(x, 10), (x, img_size[1]-10)], fill=(0, 0, 0))
        for col in range(table_cols):
            y = row * cell_height
            if y > 10:
                draw.line([(10, y), (img_size[0]-10, y)], fill=(0, 0, 0))
            cell_data = random.choice(pays)
            text_width, text_height = draw.textsize(text=cell_data, font=font)
            row_data.append(cell_data)
            draw.text((col * cell_width+int(text_width/8)+15, row * cell_height+int(text_height/6)+15), cell_data, font=font, fill="black")

        table_data.append(row_data)



    # Enregistrer l'image au format JPG comme table_01, table_02, ..., table_10, ...
    image.save("table_{:02d}.jpg".format(i+1))

    # Enregistrer les données du tableau dans un fichier CSV
    with open("table_{:02d}.csv".format(i+1), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(table_data)
