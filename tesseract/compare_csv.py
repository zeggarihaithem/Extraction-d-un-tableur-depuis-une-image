import csv
import sys

def LCS(X, Y):
    """
    Retourne la plus longue sous-sequence commune (LCS) entre ces deux chaînes X et Y

    #1:utiliser une matrice "L" de taille (len(X)+1) x (len(Y)+1) pour stocker les résultats intermédiaires,
    #2:initialiser la première ligne et la première colonne de la matrice L à 0 
    #3:L[i][j] représente la LCS de X[0:i] et Y[0:j]    
    #4:si les caractères dans X et Y sont égaux, incrémenter le nombre commun LCS et avancer
    #5:sinon, prendre le maximum de LCS jusqu'à présent en avançant dans X ou dans Y
    #6:reconstruire la chaîne LCS à partir de la matrice L
    #7:parcourir la matrice L de droite à gauche pour trouver les caractères LCS
    on initialise les indices i et j à la dernière case de la matrice L
    #8: Tant que i et j ne sont pas égaux à 0 :
    si les caractères de X et Y dans les positions i-1 et j-1 sont identiques :
    on ajoute le caractère correspondant dans la chaîne lcs.
    on décrémente i, j et index. 
    #9: Sinon, si la valeur de L dans la case en haut de la position actuelle est supérieure à celle dans la case à gauche :
    on décrémente i.Sinon :
    on décrémente j.
    on retourne la chaîne lcs en la concaténant à l'aide de la méthode join()
    """
    m = len(X)
    n = len(Y)
    
    L = [[None]*(n+1) for i in range(m+1)]  #1   
    for i in range(m+1): #2
        for j in range(n+1):
            if i == 0 or j == 0:     
                L[i][j] = 0 #3
            elif X[i-1] == Y[j-1]: #4
                L[i][j] = L[i-1][j-1] + 1
            else: #5
                L[i][j] = max(L[i-1][j], L[i][j-1])

    index = L[m][n] #6
    lcs = [""] * (index+1)
    lcs[index] = ""
       
    i = m #7
    j = n
    while i > 0 and j > 0:#8 
        if X[i-1] == Y[j-1]:      
            lcs[index-1] = X[i-1]
            i -= 1
            j -= 1
            index -= 1
        elif L[i-1][j] > L[i][j-1]: #9 
            i -= 1
        else:
            j -= 1

    return ''.join(lcs)


def print_diffs(cell1, cell2):
    cell1 = cell1.strip()
    cell2 = cell2.strip()

    # Comparer les cellules caractere par caractere et imprimer les differences
    for i in range(min(len(cell1), len(cell2))):
        if cell1[i] != cell2[i]:
            print("Difference trouvee au niveau du caractère {}: '{}' vs '{}'".format(i, cell1[i], cell2[i]))
    if len(cell1) != len(cell2):
        print("Ces cellules ont differentes longueurs: '{}' vs '{}'".format(cell1, cell2))

        
def compare_csv_files(filename1, filename2):
    # Lire les deux fichiers CSV et stocker ses contenus dans deux listes
    with open(filename1, 'r') as f1:
        csv_reader1 = csv.reader(f1)
        csv_data1 = [row for row in csv_reader1]

    with open(filename2, 'r') as f2:
        csv_reader2 = csv.reader(f2)
        csv_data2 = [row for row in csv_reader2]

    # Comparer le nombre de lignes/colonnes dans les deux fichiers CSV
    nb_lignes_colonnes1 = (len(csv_data1), len(csv_data1[0]) if csv_data1 else 0)
    nb_lignes_colonnes2 = (len(csv_data2), len(csv_data2[0]) if csv_data2 else 0)

    # Comparer le nombre de caractères dans les deux fichiers CSV après le trimming
    nb_caract1 = sum(len(cell.strip()) for row in csv_data1 for cell in row)
    nb_caract2 = sum(len(cell.strip()) for row in csv_data2 for cell in row)

    # Comparer le nombre de caractères alphanumeriques dans les deux fichiers CSV
    nb_alphabet_caract1 = sum(sum(1 for char in cell if char.isalpha()) for row in csv_data1 for cell in row)
    nb_digit_caract1 = sum(sum(1 for char in cell if char.isdigit()) for row in csv_data1 for cell in row)
    nb_alphabet_caract2 = sum(sum(1 for char in cell if char.isalpha()) for row in csv_data2 for cell in row)
    nb_digit_caract2 = sum(sum(1 for char in cell if char.isdigit()) for row in csv_data2 for cell in row)

    # Comparez chaque cellule des deux fichiers CSV à l'aide de LCS
    nb_differences = 0
    for i in range(nb_lignes_colonnes1[0]):
        for j in range(nb_lignes_colonnes1[1]):
            if i >= nb_lignes_colonnes2[0] or j >= nb_lignes_colonnes2[1]:
                print("Difference trouvee: cell ({},{}) se trouve pas dans l'un des deux fichiers ".format(i, j))
                nb_differences += 1
            else:
                lcs = LCS(csv_data1[i][j], csv_data2[i][j])
                if lcs != csv_data1[i][j] or lcs != csv_data2[i][j]:
                    print("Difference trouvee: cell ({},{}) a valeures differentes".format(i, j))
                    print_diffs(csv_data1[i][j], csv_data2[i][j])
                    nb_differences += 1

    # Print the number of differences found
    if nb_differences == 0:
        print("Les deux fichiers CSV sont identiques")
    else:
        print(" {} differences trouvees entre les deux fichiers CSV ".format(nb_differences))

    return nb_lignes_colonnes1, nb_lignes_colonnes2, nb_caract1, nb_caract2, nb_alphabet_caract1, nb_digit_caract1, nb_alphabet_caract2, nb_digit_caract2, nb_differences


def compare(file1, file2):
    # Get file names from command line arguments
    # if len(sys.argv) < 3:
    #     print("Veuillez fournir les noms des fichiers comme arguments de ligne de commande.")
    #     print("Usage: python compare_csv.py file1.csv file2.csv")
    #     sys.exit()

    # file1 = sys.argv[1]
    # file2 = sys.argv[2]
    
    nb_lignes_colonnes1, nb_lignes_colonnes2, nb_caract1, nb_caract2, nb_alphabet_caract1, nb_digit_caract1, nb_alphabet_caract2, nb_digit_caract2, nb_differences = compare_csv_files(file1, file2)

    print("Nombre de lignes/colonnes dans fichier 1: {}".format(nb_lignes_colonnes1))
    print("Nombre de lignes/colonnes dans fichier 2: {}".format(nb_lignes_colonnes2))
    print("Nombre de characteres dans fichier1 (after trimming): {}".format(nb_caract1))
    print("Nombre de characteres dans fichier2 (after trimming): {}".format(nb_caract2))
    print("Nombre d'alphabet (a-z) dans fichier1: {}".format(nb_alphabet_caract1))
    print("Nombre de caracteres numeriques (0-9) dans fichier1: {}".format(nb_digit_caract1))
    print("Nombre de alphabet characters (a-z) dans fichier2: {}".format(nb_alphabet_caract2))
    print("Nombre de caracteres numeriques (0-9) dans fichier2: {}".format(nb_digit_caract2))
    print("Nombre de cellules differentes entre fichier1 et fichier2: {}".format(nb_differences))

    # Extraire le nombre de lignes et de colonnes des tuples
    num_lines1, num_columns1 = nb_lignes_colonnes1
    num_lines2, num_columns2 = nb_lignes_colonnes2

    difference_factor = nb_differences / max((num_lines1 * num_columns1), (num_lines2 * num_columns2))

    print("Fichiers identiques à : {:.2f} %".format(100-difference_factor*100))

    return 100-difference_factor*100