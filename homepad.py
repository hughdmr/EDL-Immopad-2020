import json
import io
import os
import re

listRoom = ["Cabane jardin", "Garage", "Buanderie", "Cave", "Bureau", "Entrée", "Hall", "Séjour", "Cuisine",
            "Salle de bains", "WC", "Chambre avec dressing", "Chambre porte fenêtre", "Chambre", "Balcon",
            "Extérieur-jardin", "Local technique", "Dressing", "Nettoyage + divers", "Salle à manger",
            "EQUIPEMENTS GENERAUX", "Mezzanine", "Cage d'escalier", "Accueil", "Escalier"]
listElementT = ["vue générale", "Seuil", "Dallage", "façades", "Interphone", "Sol", "Radiateur", "Stores", "Plinthes",
                "Murs", "Plafond", "Point lumineux", "Porte", "Fenêtre", "Rebord de fenêtre", "Interrupteurs", "Prises",
                "prises", "Evier", "Lave-vaisselle", "Hotte aspirante", "Meubles", "plaques induction", "placard",
                "Armoires", "Plan de travail", "Robinetterie", "crédence", "Douche", "Lavabo", "wc", "Lampes",
                "robinet extérieur", "éléments de jardin", "chaudière gaz", "aspirateur", "étendage à linge",
                "Nettoyage général", "Détecteur de Fumée (DAAF)", "Baignoire", "Cuisinière", "congélateur", "Frigo",
                "Machine à laver", "Table de berger", "Sèche-linge", "Balustrade", "Four", "Ventilation",
                "frigo américain", "Velux", "Ancienne cheminee", "tablette", "lave-linge"]
listCaractéristics = ["Nature", "état", "Etat", "Description", "Nombre", "couleur", "Accessoires inclus", "photo", "x"]
listNature = ["métallique", "carrelage", "en bois", "bois", "peinture", "crépi", "crépis", "parquet bois",
              "lamelles PVC", "bois-métal double", "inox", "plâtre", "chrome", "PVC double", "verre", "douille",
              "dalles béton", "béton", "bois double", "aluminium", "chêne massif"]
listEtat = ["Bon", "d'usage", "satisfaisant", "Mauvais"]
repD = []

# photo345
##rajout du tiret --> erreur état
##Vue générale
##nb en dessous

listRoomNomenclature = []
listElementNomenclature = []
listNatureNomenclature = []
listDescriptionNomenclature = []

# Niveau de log :
# 1 - erreur
# 2 - lignes ignorées
# 3 - verbose
log = 0


class infos:
    def __init__(self, edl_etat_edl_lot_designation, edl_etat_edl_lot_adresse_ligne_1, edl_etat_edl_lot_ville,
                 edl_etat_edl_lot_code_postal, edl_etat_edl_lot_nb_room, edl_etat_edl_lot_lot_meuble,
                 edl_etat_edl_lot_num_etage, edl_etat_edl_lot_num_appart, edl_etat_edl_lot_surface_habitable):
        self.edl_etat_edl_lot_designation = edl_etat_edl_lot_designation
        self.edl_etat_etat = "edl_etat_etat_ferme"
        self.edl_etat_date_signature = ""
        self.edl_etat_edl_lot_adresse_ligne_1 = edl_etat_edl_lot_adresse_ligne_1
        self.edl_etat_edl_lot_adresse_ligne_2 = ""
        self.edl_etat_edl_lot_ville = edl_etat_edl_lot_ville
        self.edl_etat_edl_lot_code_postal = edl_etat_edl_lot_code_postal
        self.edl_etat_edl_lot_type_bien = edl_etat_edl_lot_designation
        self.edl_etat_edl_lot_nb_room = edl_etat_edl_lot_nb_room
        self.edl_etat_edl_lot_lot_meuble = edl_etat_edl_lot_lot_meuble
        self.edl_etat_edl_lot_num_etage = edl_etat_edl_lot_num_etage
        self.edl_etat_edl_lot_num_appart = edl_etat_edl_lot_num_appart
        self.edl_etat_edl_lot_description_logement = ""
        self.edl_etat_edl_lot_code_acces_immeuble = ""
        self.edl_etat_edl_lot_surface_habitable = edl_etat_edl_lot_surface_habitable
        self.edl_etat_nom_representant = ""
        self.edl_etat_email_representant = ""
        self.edl_etat_phone_representant = ""

    def jsonable(self):
        return self.__dict__


class occupants:
    def __init__(self, edl_etat_occupant_last_name, edl_etat_occupant_entry_date):
        self.edl_etat_occupant_last_name = edl_etat_occupant_last_name
        self.edl_etat_occupant_address_1 = ""
        self.edl_etat_occupant_address_2 = ""
        self.edl_etat_occupant_zip_code = ""
        self.edl_etat_occupant_city = ""
        self.edl_etat_occupant_telephone = ""
        self.edl_etat_occupant_mobile = ""
        self.edl_etat_occupant_email = ""
        self.edl_etat_occupant_entry_date = edl_etat_occupant_entry_date


    def jsonable(self):
        return self.__dict__


class Photo:
    def __init__(self, edl_photo_intitule, edl_photo_commentaire):
        self.edl_photo_intitule = edl_photo_intitule
        self.edl_photo_commentaire = edl_photo_commentaire
        self.edl_photo_data_uri = ""

    def jsonable(self):
        return self.__dict__


class Caracteristics:
    def __init__(self, edl_etat_element_intitule, edl_etat_element_valeur, edl_etat_element_observations):
        self.edl_etat_element_intitule = edl_etat_element_intitule
        self.edl_etat_element_type = 2
        self.edl_etat_element_valeur = edl_etat_element_valeur
        self.edl_etat_element_observations = edl_etat_element_observations

    def jsonable(self):
        return self.__dict__


class owners:
    def __init__(self, edl_etat_owner_last_name):
        self.edl_etat_owner_last_name = edl_etat_owner_last_name

    def jsonable(self):
        return self.__dict__

class Element:
    def __init__(self, edl_etat_element_intitule):
        self.edl_etat_element_intitule = edl_etat_element_intitule
        self.edl_etat_element_type = 1
        self.edl_etat_element_valeur = ""
        self.edl_etat_element_observations = ""
        self.elements = []
        self.photos = []

    def add_elements(self, elements):
        self.elements.append(elements)

    def add_photos(self, photos):
        self.photos.append(photos)

    def jsonable(self):
        return self.__dict__


class Room:
    def __init__(self, edl_etat_element_intitule):
        self.edl_etat_element_intitule = edl_etat_element_intitule
        self.edl_etat_element_type = 1
        self.edl_etat_element_valeur = ""
        self.edl_etat_element_observations = ""
        self.element = []

    def add_element(self, element):
        self.element.append(element)

    def jsonable(self):
        return self.__dict__


class Appart:
    def __init__(self):
        self.infos = []
        self.owners = []
        self.occupants = []
        self.room = []


    def add_occupants(self, occupants):
        self.occupants.append(occupants)

    def add_room(self, room):
        self.room.append(room)

    def add_infos(self, infos):
        self.infos.append(infos)

    def add_owners(self, owners):
        self.owners.append(owners)

    def jsonable(self):
        return self.__dict__


def ComplexHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()
    else:
        # raise TypeError 'Object of type %s with value of %s is not JSON serializable' % (type(Obj),repr(Obj))
        print('error')


def intermediaire(fichier, dossier_a_traiter):
    cnt = 0

    with io.open(dossier_a_traiter + "/" + fichier, mode="r", encoding="utf-8") as inoput:
        with io.open("./étape intermédiaire/intermédiaire0.txt", mode="w", encoding="utf-8") as output:
            # création d'une variable pour éviter de lire tout le fichier
            stop = 0
            for line in inoput:
                # trouver la ligne "Le locataire entrant se déclare" stop prend la valeur de cette ligne
                if line.find("Le locataire entrant se déclare") != -1:
                    stop += 1
                    break
                else:
                    stop += 1
                    output.write(line)

    with io.open("./étape intermédiaire/intermédiaire0.txt", mode="r", encoding="utf-8") as inoput:
        with io.open("./étape intermédiaire/intermédiaire.txt", mode="w", encoding="utf-8") as output:

            for line in inoput:
                cnt += 1
                # si le numéro de la ligne est < à "stop" on s'arrête
                if cnt > stop:
                    break

                # si "Les éléments suivants" apparait dans la ligne:
                if line.find('Les éléments suivants') != -1:
                    lineConcat = ""
                    lineConcat += line
                    # tant que la ligne != "retour à la ligne", tout mettre sur la même ligne
                    while line != "\n":
                        line = next(inoput)
                        lineConcat += line
                    # ecrire en sortie la ligne en remplacant les retour à la ligne par des espaces puis sauter 2 lignes
                    output.write(lineConcat.replace("\n", " ") + "\n" * 2)
                # sinon, ecrire la ligne sans lmodifications
                else:
                    output.write(line)

    with io.open("./étape intermédiaire/intermédiaire.txt", mode="r", encoding="utf-8") as input2:
        with io.open("./étape intermédiaire/intermédiaire1.txt", mode="w", encoding="utf-8") as output2:
            for line in input2:
                # pour chaque ligne, avec r = ((a1, b1), (a2, b2)...) remplace tous les a par b
                for r in (("Les éléments suivants ont été vérifiés et sont en état d'état d'usage :",
                           "Les éléments suivants ont été vérifiés et sont en état d'état d'usage :" + "\n" + " -"), (
                                  "Les éléments suivants ont été vérifiés et sont en bon état :",
                                  "\n" + "Les éléments suivants ont été vérifiés et sont en bon état :"), (
                                  "Les éléments suivants ont été vérifiés et sont en bon état :",
                                  "Les éléments suivants ont été vérifiés et sont en bon état :" + "\n" + " -"),
                          ("/", "\n" + " -")):
                    line = line.replace(*r)
                output2.write(line)

    cnt1 = 0
    # ajouter la mention "d'usage" avant chaque ligne dont les éléments sont "en état d'état d'usage"
    with io.open("./étape intermédiaire/intermédiaire1.txt", mode="r", encoding="utf-8") as inoput:
        with io.open("./étape intermédiaire/intermédiaire2.txt", mode="w", encoding="utf-8") as output:
            for line in inoput:
                cnt1 += 1
                if cnt1 > stop:
                    break

                if line.find("Les éléments suivants ont été vérifiés et sont en état d'état d'usage") != -1:
                    lineConcat1 = ""
                    lineConcat1 += line
                    while line.find("Les éléments suivants ont été vérifiés et sont en bon état :") == -1 \
                            and line != "\n":
                        line = next(inoput)
                        lineConcat1 += "d'usage"
                        lineConcat1 += line
                    output.write(lineConcat1)
                else:
                    output.write(line)

    cnt2 = 0
    # ajouter la mention "Bon" avant chaque ligne dont les éléments sont "en bon état"
    with io.open("./étape intermédiaire/intermédiaire2.txt", mode="r", encoding="utf-8") as inoput:
        with io.open("./étape intermédiaire/intermédiaire3.txt", mode="w", encoding="utf-8") as output:
            text = inoput.readline()

            for line in inoput:
                cnt2 += 1
                if cnt2 > stop:
                    break

                if line.find("Les éléments suivants ont été vérifiés et sont en bon état :") != -1:
                    lineConcat2 = ""
                    lineConcat2 += line
                    while line != "\n" and cnt < len(text):
                        cnt2 += 1
                        line = next(inoput)
                        if line != "\n":
                            lineConcat2 += "Bon"
                            lineConcat2 += line
                        else:
                            lineConcat2 = line
                    output.write(lineConcat2)
                else:
                    output.write(line)

    cnt4 = 0
    with io.open("./étape intermédiaire/intermédiaire3.txt", mode="r", encoding="utf-8") as inoput:
        with io.open("./étape intermédiaire/intermédiaire4.txt", mode="w", encoding="utf-8") as output:
            for line in inoput:
                cnt4 += 1
                if cnt4 > stop:
                    break

                if line.find('(s)') != -1:
                    output.write(line[:line.find('(s)')] + line[(line.find('(s)') + 3):])

                else:
                    output.write(line)

    cnt5 = 0
    with io.open("./étape intermédiaire/intermédiaire4.txt", mode="r", encoding="utf-8") as inoput:
        with io.open("./étape intermédiaire/intermédiaire5.txt", mode="w", encoding="utf-8") as output:
            for line in inoput:
                cnt5 += 1
                if cnt4 > stop:
                    break

                if line.find("Clés remises") != -1:
                    while line != "\n":
                        line = next(inoput)
                else:
                    output.write(line)

    cnt3 = 0
    with io.open("./étape intermédiaire/intermédiaire5.txt", mode="r", encoding="utf-8") as inoput:
        with io.open("./étape intermédiaire/intermédiaire6.txt", mode="w", encoding="utf-8") as output:
            for line in inoput:
                cnt3 += 1
                if cnt3 > stop:
                    break

                if line.find(
                        "Les éléments suivants ont été vérifiés et sont en état d'état d'usage") == -1 and line.find(
                    "Les éléments suivants ont été vérifiés et sont en bon état") == -1 and line.find(
                    "Le locataire entrant se déclare") == -1 and line.find(
                    "Etabli avec le logiciel homePad.com (Pro v 3.7.1)") == -1 and line.find(
                    "Cimm Immobilier Sallanches") == -1 and line.find(
                    "gestion@cimm-immobilier.fr") == -1 and line.find("Cimm Gestion") == -1:
                    output.write(line)
    return


def conversion_json(dossier_a_traiter):
    # supprimer les dossiers précédents
    for i in range(2):
        if i == 0:
            dossier = "./fichier json"
        else:
            dossier = "./étape intermédiaire"
        if len(dossier) > 0:
            for fichier in os.listdir(dossier):
                os.remove(dossier + "/" + fichier)

    i = 0
    for fichier in os.listdir(dossier_a_traiter):
        # print si on veut voir le nombre de fichier traité et le nom du fichier avec erreur si il y en a une
        print("on traite le fichier:", i)
        print(fichier)
        if fichier == ".DS_Store":
            i += 1
            continue
        intermediaire(fichier, dossier_a_traiter)
        number = str(fichier[0: 6])
        i += 1

        myAppart = Appart()
        meuble, nappart, surface = "", "", ""
        cprop, cSurf, cnapp = 0, 0, 0
        with io.open("./étape intermédiaire/intermédiaire6.txt", mode="r", encoding="utf-8") as fh:
            cnt = 0

            # pour toute les lignes du fichier
            for line in fh:
                cnt += 1
                foundLine = False
                truc = False

                if line[0] == '\n':
                    continue


                for findRoom in listRoom:
                    if findRoom in line:
                        # ajouter une pièce dans la classe myAppart
                        myAppart.add_room(Room(findRoom))
                        # ajouter la pièce dans la liste : "listRoomNomenclature"
                        listRoomNomenclature.append(findRoom)
                        if log >= 3:
                            print("#room " + findRoom)
                        currFindRoom = findRoom
                        foundLine = True
                    # si on a  trouvé, on sort de la deuxième boucle for
                    if foundLine:
                        break

                # Si on a trouvé on passe à la ligne suivante
                if foundLine:
                    continue

                ###############
                # Ligne élément : il s'agit d'un élément dans la liste de nomenclature
                # Ex : - 1x Stores (motorisés, volets roulants, lamelles PVC, couleur : marron):
                # On va chercher
                #   - le nombre d'éléments si affiché
                #   - l'état si affiché
                #   - les commentaires entre parenthèses (dont la couleur)
                ###############

                for findElement in listElementT:
                    if findElement in line:
                        if len(myAppart.room) != 0:
                            myAppart.room[-1].add_element(Element(findElement))
                            listElementNomenclature.append(findElement)
                        else:
                            if log > 2:
                                print("élément trouvé alors qu'il n'y a pas de room " + str(cnt) + ": " + line.strip(
                                    '\n'))
                            truc = True
                            break
                        if log >= 3:
                            print("#room " + currFindRoom + "#element " + findElement)
                        currFindElement = findElement
                        foundLine = True

                        # On a trouvé un élément, on regarde si il y a un état au début
                        # c = 0
                        listEtatElement = line.split(" ")
                        for findEtat in listEtat:
                            if findEtat == listEtatElement[0]:
                                # if len(listEtatElement)==1:
                                # c+=1
                                # else:
                                myAppart.room[-1].element[-1].add_elements(Caracteristics("Etat", findEtat, ""))
                                if log >= 3:
                                    print("#room " + currFindRoom + " element " + currFindElement + "#etat " + findEtat)

                        # On regarde le nombre d'éléments x sur la ligne
                        reNombreElement = re.compile('- \d+x')  # nombre entre "-" et "x"
                        listNombreElement = reNombreElement.findall(line)
                        # nombre = line.find('x ')-1
                        if listNombreElement:
                            reNombreElement = re.compile('\d+')
                            listNombreElement = reNombreElement.findall(listNombreElement[0])
                            myAppart.room[-1].element[-1].add_elements(
                                Caracteristics("Nombre", str(listNombreElement[0]), ""))
                            if log >= 3:
                                print("#room " + currFindRoom + " element " + currFindElement + "#nombre " +
                                      listNombreElement[
                                          0])

                        # Ensuite on regarde si il y a des parentheses de description à la fin de l'élément
                        if ('(') in line:
                            parenthese = line.split('(')[1].split(')')[0]
                            listInfoParenthese = parenthese.split(",")
                            # On parcourt les éléments
                            for infoParenthese in listInfoParenthese:
                                if log >= 3:
                                    print(
                                            "#room " + currFindRoom + " element " + currFindElement + " #parenthese " + infoParenthese)
                                foundParenthese = False

                                # on cherche la couleur dans la parenthese avec "couleur :"
                                if infoParenthese.find('couleur') != -1:
                                    myAppart.room[-1].element[-1].add_elements(
                                        Caracteristics("Couleur", (infoParenthese.split('couleur : '))[1].split(')')[0],
                                                       ""))
                                    if log >= 3:
                                        print(
                                                "#room " + currFindRoom + " element " + currFindElement + " parenthese #couleur "
                                                + (infoParenthese.split('couleur : '))[1].split(')')[0])
                                    foundParenthese = True
                                    break
                                if foundParenthese:
                                    continue

                                # on cherche la nature dans la parenthese à partir d'une liste de valeur
                                for findNature in listNature:
                                    if findNature == infoParenthese:
                                        listNatureNomenclature.append(findNature)
                                        myAppart.room[-1].element[-1].add_elements(
                                            Caracteristics("Nature", findNature, ""))
                                        if log >= 3:
                                            print(
                                                    "#room " + currFindRoom + " element " + currFindElement + " parenthese #nature " + infoParenthese)
                                        foundParenthese = True
                                        break
                                    if foundParenthese:
                                        continue

                                if infoParenthese.find('vue générale') != -1:
                                    myAppart.room[-1].element[-1].add_photos(
                                        Photo("Photo {}".format(str((line.split('photo '))[1].split(')')[0])),
                                              line[1:line.find("photo ") - 2]))
                                    if log >= 3:
                                        print(
                                                "#room " + currFindRoom + " element " + currFindElement + " parenthese #vue générale " + infoParenthese)
                                    foundParenthese = True
                                    break
                                if foundParenthese:
                                    continue

                                # si ce n'est ni la couleur, ni la nature, c'est une description
                                if not foundParenthese:
                                    listDescriptionNomenclature.append(infoParenthese)
                                    myAppart.room[-1].element[-1].add_elements(
                                        Caracteristics("Description", infoParenthese, ""))
                                    if log >= 3:
                                        print(
                                                "#room " + currFindRoom + " element " + currFindElement + " parenthese #description " + infoParenthese)
                                    foundParenthese = True

                if truc is True:
                    continue

                if not foundLine:

                    if myAppart.room and myAppart.room[-1].element:
                        # Vérifie si on a déjà trouvé un élément sinon pb

                        # Sur toutes les lignes on extrait les photos
                        if line.find('photo') != -1:
                            myAppart.room[-1].element[-1].add_photos(
                                Photo("Photo {}".format(str((line.split('photo '))[1].split(')')[0])),
                                      line[1:line.find("photo ") - 2]))
                            if log >= 3:
                                print("#room " + currFindRoom + " element " + currFindElement + "#photo " +
                                      (line.split('photo '))[1].split(')')[0])

                        ###############
                        # Pour Hugues :
                        #   X traiter le cas ou il y a plusieurs photo
                        #       Ex : - Marque(s) (photo 54, 55, 56)
                        #   X ajouter le reste de la ligne dans le commentaire de la photo : "edl_photo_commentaire": "Marque(s)",
                        #   X traiter le "vue générale" pour ajouter une photo à une pièce : "edl_photo_commentaire": "vue générale",
                        ###############

                        ###############
                        # ce n'est ni une room ni un élément, donc c'est un état
                        # Ex : - Bon état (photo 53)
                        ###############

                        d = 0
                        for findEtat in listEtat:
                            if findEtat in line:
                                if line == findEtat + "\n":
                                    d += 1
                                else:
                                    myAppart.room[-1].element[-1].add_elements(Caracteristics("Etat", findEtat, ""))
                                    if log >= 3:
                                        print(
                                                "#room " + currFindRoom + " element " + currFindElement + "#etat " + findEtat)
                                    foundLine = True
                                    breakpoint

                        if foundLine:
                            continue

                        ###############
                        # ce n'est ni une room ni un élément ni un état, c'est donc une description
                        # Ex :- Rebord de fenêtre (photo 53), peinture écaillée
                        ###############

                        if "- " in line:
                            description = line.strip("- ").replace(":,", ":")
                            rePhoto = re.compile('\(photo \d+\)')
                            description = rePhoto.sub("", description)

                            listDescriptionNomenclature.append(description)
                            myAppart.room[-1].element[-1].add_elements(Caracteristics("Description", description, ""))
                            if log >= 3:
                                print("#room " + currFindRoom + " element " + currFindElement + "#desc " + description)


                        # On regarde si c'est un numéro de page et on saute la ligne
                        elif re.compile('\d+\n').findall(line):
                            continue

                        else:
                            # Ce n'est pas une description : on doit traiter cette erreur
                            if log >= 1:
                                print("on a rien trouvé pour la ligne " + str(cnt) + ": " + line.strip('\n'))

                    elif myAppart.room and not myAppart.room[-1].element:
                        # Il n'y a pas d'élément
                        if log >= 1:
                            print("on a rien trouvé pour la ligne " + str(cnt) + ": " + line.strip('\n'))

                        ###############
                        # Hugues : traiter la vue générale ici XX
                        ###############


                    else:
                        # Il n'y a pas de room ni d'élément
                        if log >= 2:
                            print("on ignore la ligne " + str(cnt) + ": " + line.strip('\n'))

                # Pour ne pas traiter tout le fichier
                # if cnt > 200:
                #    break

        with io.open("./étape intermédiaire/intermédiaire6.txt", mode="r", encoding="utf-8") as fh:
            cnt = 0

            # pour toute les lignes du fichier
            for line in fh:
                cnt += 1

                if line[0] == '\n':
                    continue

                if "Etat des lieux" in line:
                    pas_assez_info = False
                    while line.find("Appartement") == -1 and line.find("Chalet") == -1 and \
                            line.find("Local commercial") == -1 and line.find("Duplex") == -1:
                        if line.find("Maison") != -1:
                            nbroom = ""
                            break
                        else:
                            line = next(fh)
                            cnt += 1
                    lignecoupe = line.split()
                    designation = lignecoupe[0]
                    if len(lignecoupe) > 2:
                        if lignecoupe[2] == "-":
                            nbroom = lignecoupe[1] + lignecoupe[2] + lignecoupe[3]
                        else:
                            nbroom = lignecoupe[1]
                        if lignecoupe[-1] != "pces":
                            if lignecoupe[-2] == "non":
                                meuble = 0
                            elif lignecoupe[-1] == "meublé(e)":
                                meuble = 1
                        else:
                            meuble = ""
                    else:
                        nbroom = ""
                    line = next(fh)
                    cnt += 1
                    adresse = line
                    line = next(fh)
                    cnt += 1
                    if line != '\n':
                        lignecoupe = line.split()
                        cpostal = lignecoupe[0]
                        lignecoupe.pop(0)
                        lignecoupe = "".join(lignecoupe)
                        ville = lignecoupe
                    else:
                        cpostal = ""
                        ville = ""

                if "Etage" in line:
                    ref = cnt
                    compteur = 0
                    while line != "\n":
                        compteur += 1
                        cnt += 1
                        line = next(fh)
                        if "Propriétaire" in line:
                            cprop = cnt
                        if "Surface" in line:
                            cSurf = cnt
                        if "N° d'appart" in line:
                            cnapp = cnt
                    with io.open("./étape intermédiaire/intermédiaire6.txt", mode="r", encoding="utf-8") as lire:
                        etage = lire.readlines()[ref + compteur]
                        etage = etage[:-1]
                    if cprop != 0:
                        with io.open("./étape intermédiaire/intermédiaire6.txt", mode="r", encoding="utf-8") as lire:
                            propriétaire = lire.readlines()[compteur + cprop]
                            propriétaire = propriétaire[:-1]
                    if cSurf != 0:
                        with io.open("./étape intermédiaire/intermédiaire6.txt", mode="r", encoding="utf-8") as lire:
                            surface = lire.readlines()[cSurf + compteur]
                            surface = surface[:-1]
                    if cnapp != 0:
                        with io.open("./étape intermédiaire/intermédiaire6.txt", mode="r", encoding="utf-8") as lire:
                            nappart = lire.readlines()[cnapp + compteur]
                            nappart = nappart[:-1]

        with io.open("./étape intermédiaire/intermédiaire0.txt", mode="r", encoding="utf-8") as fh:
            cnt = 0
            for line in fh:
                if line.find("Locataire entrant (Date d’entrée") == -1:
                    cnt += 1
                else:
                    line = line.split()
                    date = line[-3] + ' ' + line[-2] + ' ' + line[-1]
                    date = date[:-1]
                    cnt += 1
                    line = next(fh)
                    nom_locataire = line
                    nom_locataire = nom_locataire[:-1]
                    cnt += 1


        myAppart.add_infos(infos(designation, adresse, ville, cpostal, nbroom, meuble, etage, nappart, surface))
        myAppart.add_owners(owners(propriétaire))
        myAppart.add_occupants(occupants(nom_locataire, date))
        # convert to json string
        jsonStr = json.dumps(myAppart, default=ComplexHandler, indent=4)

        # jsonStr = ''.join(word.title() for word in jsonStr.split('_'))
        # print(jsonStr)  # SnakeCaseName

        fichier = open("./fichier json/" + number + ".json", "a")
        fichier.write(jsonStr)
        fichier.close()



    fichier = open("./fichier json/Nomenclature.txt", "a")
    fichier.write("listRoomNomenclature : \n" + "\n".join(set(listRoomNomenclature)) + '\n' + '\n')
    fichier.write("listElementNomenclature : \n" + "\n".join(set(listElementNomenclature)) + '\n' + '\n')
    fichier.write("listNatureNomenclature : \n" + "\n".join(set(listNatureNomenclature)) + '\n' + '\n')
    fichier.write("listDescriptionNomenclature : \n" + "\n".join(set(listDescriptionNomenclature)) + '\n' + '\n')
    fichier.close()
    return


conversion_json("document non traité")
