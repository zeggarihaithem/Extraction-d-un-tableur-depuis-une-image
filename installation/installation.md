# Installation

## Installation Tesseract ocr
Pour installer tesseract OCR sur ubuntu, il faut d'abord installer le paquet `tesseract-ocr` et ensuite installer le paquet `libtesseract-dev` qui contient les headers pour le développement.

```bash
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

Puis les librairies suivantes si elles ne sont pas déjà installées :
```bash
sudo apt-get install g++ # or clang++ (presumably)
sudo apt-get install autoconf automake libtool
sudo apt-get install pkg-config
sudo apt-get install libpng-dev
sudo apt-get install libjpeg8-dev
sudo apt-get install libtiff5-dev
sudo apt-get install zlib1g-dev
```

Et enfin les outils d'entraînement :
```bash
sudo apt-get install libicu-dev
sudo apt-get install libpango1.0-dev
sudo apt-get install libcairo2-dev
```

Il faut aussi installer `Leptonica` qui est une librairie pour le traitement d'image :
```bash
sudo apt-get install libleptonica-dev
```

Pour faciliter l'installation, nous avons créé un script à exécuter qui installe toutes les librairies