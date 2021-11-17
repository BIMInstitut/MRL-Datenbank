import urllib.request # file downloads
import psycopg2 # db connection
import pandas as pd # data frames
import numpy as np # stuff
import time
import os
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

# Einlesen der Tabellenblätter eines Exceldokuments
def getDataFrameList(filePath, sheetNames):
    dfList = list()
    for sheetName in sheetNames:
        dataFrame = pd.read_excel(filePath, sheet_name = sheetName)
        dfList.append(dataFrame)
        # print(dataFrame.head())
    return dfList

#
def getDfItem(df, sourceName, row, key):
    try: # KeyError: '400' -> Keine Spalte mit dieser Bezeichnung vorhanden
        item = df.loc[row, key]
        return item
    except KeyError:
        print("ERROR: Sheet " + sourceName + " fehlt Spaltenbezeichnung " + key)

# Überzählige Leerzeichen, Umbrüche etc in String entfernen
def cleanStr(s):
    try:
        s = s.strip() # Leerzeichen, Tabs, Umbrüche am Anfang und Ende entfernen
        s = s.replace("  ", " ") # Doppelte Leerzeichen reduzieren
        s = s.replace("- \n", "") # Umbrüche im Wort entfernen
        s = s.replace("-\n", "") # Umbrüche im Wort entfernen
        s = s.replace("\n", "") # Verbleibende Umbrüche entfernen
    except AttributeError:
        pass
    return s

def online(host='http://example.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

'''
Eingangsdaten aus config.txt lesen
'''
# Config in Unterordner
dir = os.path.dirname(__file__)
i = dir.find("\MRL-DB-Setup")
dir = os.path.dirname(__file__)[:i] # Unterordner abschneiden
configFilePath = dir + '\config.txt'
# Config lesen
url = "" # local files unless url is specified
with open(configFilePath, encoding='utf8') as f:
    for line in f:
        #print(line)
        i = line.find("=")+1 # Startindex von Wert
        if "dbname=" in line:
            dbname = line[i:].strip()
            #print(dbname)
        elif "user=" in line:
            user = line[i:].strip()
            #print(user)
        elif "password=" in line:
            password = line[i:].strip()
            #print(password)
        elif "url=" in line:
            url = line[i:].strip()
            #print(url)
        else:
            continue
if dbname is None or user is None or password is None:
    configRead = False
    print("FEHLER! Config.txt konnte nicht gelesen werden.")
else:
    configRead = True
    print("Config.txt Datei gelesen.")

# Dateinamen für DB-Input-Tabellen
logFileName = "MRL-data_20210716_Anlage-3_LOG.xlsx" # Download von BIM-Institutsseite
loiFileName = "MRL-data_20200918-Anlage-3_LOI.xlsx" # Download von BIM-Institutsseite
dinFileName = "MRL-data_DIN276.csv" # Download von BIM-Institutsseite
ifcFileName = "MRL-data_IFC4.csv" # Download von BIM-Institutsseite
resFileName = "MRL-data_Verantwortlichkeit.csv" # Download von BIM-Institutsseite
logFilePath = url + logFileName # Download von BIM-Institutsseite
loiFilePath = url + loiFileName # Download von BIM-Institutsseite
dinFilePath = url + dinFileName # Download von BIM-Institutsseite
ifcFilePath = url + ifcFileName # Download von BIM-Institutsseite
resFilePath = url + resFileName # Download von BIM-Institutsseite
# LOKALER DATEIPFAD FÜR DATENBANK-RESET (NICHT ÄNDERN!)
sqlFileName = "MRL-DB_Setup.sql" # lokal vorhanden


print("Download und Verarbeitung der Datentabellen gestartet...")
allFilesOnline = online(logFilePath) and online(loiFilePath) and online(dinFilePath) and online(ifcFilePath) and online(resFilePath)
#allFilesOnline = True
if configRead and allFilesOnline:

    '''
    LoG einlesen und auswerten
    '''
    # Attribtutabellen (LoI) der einzelnen Typen/Kategorien
    logSheetNames = ["tabArbeitsbereich_export", "tabKategorie_export", "tabTyp_export"]
    logDataFrames = getDataFrameList(logFilePath, logSheetNames)
    print("LoG Sheets: " + str(len(logDataFrames)))

    # Erstellen der Liste von Kategorien und Typen
    # Liste der Arbeitsbereiche
    workAreas = list()
    df = logDataFrames[0]
    #print(df.head())
    for j in range(len(df)): # rows
        item = getDfItem(df, logSheetNames[0], j, "Bezeichnung")
        if item is None:
            continue
        value = cleanStr(item)
        workAreas.append(value)
    print("Arbeitsbereiche gelesen...")
    #print(workAreas)
    #print()
    # Liste der Kategorien
    dfNameKey = "Bezeichnung"
    dfKeys = ["Arbeitsbereich", "LoG100", "LoG200", "LoG300", "LoG400", "LoG500"]
    categories = {} # {Bezeichnung:{Arbeitsbereich:"", LoG100:"", ...}}
    df = logDataFrames[1]
    #print(df.head())
    for j in range(len(df)): # rows
        item = getDfItem(df, logSheetNames[1], j, dfNameKey)
        if item is None:
            continue
        nameValue = cleanStr(item)
        #print(dfKeys[0] + ": " + nameValue)
        categories[nameValue] = {}
        for key in dfKeys: # col names
            item = getDfItem(df, logSheetNames[1], j, key)
            if item is None:
                continue
            if key in {"Arbeitsbereich", "LoG100", "LoG200", "LoG300", "LoG400", "LoG500"} and (item == 0 or pd.isna(item)):
                value = ""
            else:
                value = cleanStr(item)
            #print(key + ": " + str(value))
            categories[nameValue][key] = value
    print("Kategorien gelesen...")
    #print(categories)
    #print()
    # Liste der Typen, DIN276-KGs und IFC-Entitäten
    dfNameKey = "Bezeichnung"
    dfKeys = ["Kategorie", "Klassifikation DIN", "Klassifikation IFC"]
    types = {} # {Bezeichnung:{Kategorie:"", DIN276:"", IFC:""}}
    df = logDataFrames[2]
    #print(df.head())
    for j in range(len(df)): # rows
        item = getDfItem(df, logSheetNames[2], j, dfNameKey)
        if item is None:
            continue
        nameValue = cleanStr(item)
        #print(dfKeys[0] + ": " + nameValue)
        types[nameValue] = {}
        for key in dfKeys: # col names
            item = getDfItem(df, logSheetNames[2], j, key)
            if item is None:
                continue
            if key in {"Kategorie", "Klassifikation IFC"} and item == 0:
                value = ""
            else:
                value = cleanStr(item)
            #print(key + ": " + str(value))
            types[nameValue][key] = value
    print("Typen gelesen...")
    #print(types)

    '''
    Vordefinierte Klassifikationstabellen (DIN276, IFC, OmniClass, Uniformat, Verantwortlichkeit) einlesen
    '''
    df = pd.read_csv(dinFilePath, sep=";", encoding="cp1252")
    dinList = list()
    for j in range(len(df)): # rows
        item1 = getDfItem(df, dinFileName, j, "kostengruppe")
        item2 = getDfItem(df, dinFileName, j, "bezeichnung")
        if item1 is None and item2 is None:
            continue
        name = cleanStr(item2)
        dinList.append((item1, name))
    print("DIN276-Kostengruppen gelesen...")
    #print(dinList)
    #print()

    df = pd.read_csv(ifcFilePath, sep=";", encoding="cp1252")
    ifcList = list()
    for j in range(len(df)): # rows
        item = getDfItem(df, ifcFileName, j, "Entities")
        if item is None:
            continue
        value = cleanStr(item)
        ifcList.append(value)
    print("IFC-Entitäten gelesen...")
    #print(ifcList)
    #print()

    df = pd.read_csv(resFilePath, sep=";", encoding="cp1252")
    responsibilities = list()
    for j in range(len(df)): # rows
        item1 = getDfItem(df, resFileName, j, "bezeichnung")
        item2 = getDfItem(df, resFileName, j, "erklaerung")
        if item1 is None:
            continue
        name = cleanStr(item1)
        desc = cleanStr(item2)
        responsibilities.append((name, desc))
    responsibilities.append(("", "keine Angabe"))
    print("Verantwortlichkeit gelesen...")
    #print(responsibilities)
    #print()

    '''
    LoI einlesen und auswerten
    '''
    # Attribtutabellen (LoI) der einzelnen Typen/Kategorien
    loiFile = pd.ExcelFile(loiFilePath)
    loiSheetNames = loiFile.sheet_names
    loiDataFrames = getDataFrameList(loiFile, loiSheetNames)
    print("LoI Sheets: " + str(len(loiDataFrames)))

    # Menge der Attribute aller Typen
    dfNameKey = "Bezeichnung"
    dfKeys = ["Format"] # Relevante Spaltennamen
    properties = {} # {Bezeichnung:{Format:""}}
    formats = list()
    for sheetName, df in zip(loiSheetNames, loiDataFrames): # DataFrames
        #print(df.head(3))
        for j in range(len(df)): # rows
            item = getDfItem(df, sheetName, j, dfNameKey)
            if item is None:
                continue
            nameValue = cleanStr(item)
            #print(dfKeys[0] + ": " + nameValue)
            properties[nameValue] = {}
            for key in dfKeys: # col names
                if key == "Format":
                    item = getDfItem(df, sheetName, j, key)
                    if item is None:
                        continue
                    if item == 0 or pd.isna(item):
                        value = ""
                    else:
                        value = cleanStr(item)
                    #print(key + ": " + str(value))
                    properties[nameValue][key] = value
                    if value not in formats:
                        formats.append(value)
    print("Attribute gelesen...")
    #print(properties)
    print("Formate gelesen...")
    #print(formats)

    # Erstellen der Kombinationsliste von Typen und Attributen
    dfNameKey = "Bezeichnung"
    dfKeys = ["Pset", "Format", "Einheit", "100", "200", "300", "400", "500", "IL", "IA"] # Relevante Spaltennamen
    tpMatching = list() # Kombinationsliste von Typen und Attributen
    psets = list()
    units = list()
    for sheetName, df in zip(loiSheetNames, loiDataFrames): # DataFrames
        #print(sheetName)
        #print(df.head(3))
        for j in range(len(df)): # rows
            item = getDfItem(df, sheetName, j, dfNameKey)
            if item is None:
                continue
            nameValue = cleanStr(item)
            #print(dfNameKey + ": " + nameValue)
            # Prüfe ob Match bereits enthalten ist und überspringe ggf.
            check = next((item for item in tpMatching if item["Typ"] == sheetName and item["Attribut"] == nameValue), None)
            if check is not None:
                continue
            match = {"Typ":sheetName, "Attribut": nameValue}
            for key in dfKeys: # col names
                item = getDfItem(df, sheetName, j, key)
                if item is None:
                    continue
                if item == 0 or pd.isna(item):
                    value = ""
                else:
                    value = cleanStr(item)
                #print(key + ": " + str(value))
                if key in {"100", "200", "300", "400"}:
                    if "loi_min" not in match and value == "x":
                        match["loi_min"] = key
                elif key == "500" and "loi_min" not in match:
                    match["loi_min"] = "500"
                else:
                    match[key] = value
                    if key == "Einheit" and value not in units:
                        units.append(value)
                    if key == "Pset" and value not in psets:
                        psets.append(value)
            tpMatching.append(match)
    print("Psets gelesen...")
    #print(psets)
    print("Einheiten gelesen...")
    #print(units)
    print("Matching zugeordnet...")
    #print(tpMatching)

    '''
    Aufgesplittete Typen (die aufgesplittet nur in der Typentabelle vorhanden sind) im Matching ergänzen.
    Der Eintrag mit den alten Typen im Matching wird anschließend gelöscht.
    '''
    # Aufsplittung von Typen mit gleichem Attributset auf mehrere
    typeMapping = {
        "Fundament":[
            "Streifenfundament",
            "Einzelfundament"
        ],
        "Bodenplatte":[
            "Bodenplatte",
            "Fundamentplatte",
            "Fundament",
            "Fundamentplattenversprung",
            "Bodenplattenversprung"
        ],
        "Wand Rohbau":[
            "Außenwand",
            "Innenwand",
            "Attika",
            "Brüstung"
        ],
        "Stütze":[
            "Innenstütze",
            "Außenstütze"
        ],
        "Decke":[
            "Geschossdecke",
            "Deckenversprung",
            "Balkon",
            "Rampe"
        ],
        "Träger":[
            "Unterzug",
            "Überzug"
        ],
        "Treppe":[
            "Treppenlauf",
            "Treppenpodest"
        ],
        "Dach":[
            "Flachdach",
            "Steildach",
            "Vordach",
            "Kuppel",
            "Gewölbe"
        ],
        "Durchbruch":[
            "Wanddurchbruch",
            "Deckendurchbruch",
            "Kernbohrung"
        ],
        "Tür, Tor":[
            "Außentür",
            "Außentor",
            "Innentür",
            "Innentor"
        ],
        "Treppe":[
            "Treppenlauf",
            "Treppenpodest"
        ],
        "Fenster":[
            "Außenfenster",
            "Innenfenster"
        ],
        "Dachfenster":[
            "Flachdachfenster",
            "Steildachfenster",
            "Flachdachfenster als Dachausstieg",
            "Steildachfenster als Dachausstieg"
        ],
        "Wand Ausbau":[
            "Trockenbauwand",
            "Vorsatzschale (Außenwand)",
            "Fliese (Außenwand)",
            "Wandbekleidung mit Unterkonstruktion (Außenwand)",
            "Vorsatzschale (Innenwand)",
            "Fliese (Innenwand)",
            "Wandbekleidung mit Unterkonstruktion (Innenwand)",
            "Systemtrennwand"
        ],
        "Bodenaufbau":[
            "Estrich (Gründungsbelag)",
            "Estrich (Deckenbelag)",
            "Hohlraumboden (Gründungsbelag)",
            "Hohlraumboden (Deckenbelag)",
            "Doppelboden (Gründungsbelag)",
            "Doppelboden (Deckenbelag)"
        ],
        "Dachaufbau":[
            "Dachbelag auf Steildach",
            "Flachdachaufbau begehbar",
            "Flachdachaufbau befahrbar",
            "Gründach"
        ],
        "Deckenbekleidung":[
            "Gipskartondecke (Decke)",
            "Alu-Paneeldecke (Decke)",
            "Akustikdecke (Decke)",
            "Rasterdecke (Decke)",
            "Blechkassettendecke (Decke)",
            "Mineralfaserdecke (Decke)",
            "Gipskartondecke (Dach)",
            "Alu-Paneeldecke (Dach)",
            "Akustikdecke (Dach)",
            "Rasterdecke (Dach)",
            "Blechkassettendecke (Dach)",
            "Mineralfaserdecke (Dach)"
        ],
        "Decken, sonstiges":[
            "Geländer (Decke)",
            "Handlauf (Decke)",
            "Boden-und Einschubtreppe (Decke)",
            "Leiter (Decke)",
            "Gitter (Decke)",
            "Rost (Decke)",
            "Schachtdeckel (Decke)",
            "Gitter (Außenwand)",
            "Handlauf (Außenwand)",
            "Gitter (Innenwand)",
            "Handlauf (Innenwand)",
            "Geländer (Dach)",
            "Handlauf (Dach)",
            "Boden-und Einschubtreppe (Dach)",
            "Leiter (Dach)",
            "Gitter (Dach)",
            "Rost (Dach)",
            "Schachtdeckel (Dach)"
        ],
        "Wandbekleidung außen":[
            "Fassadenbekleidung"
        ],
        "Elementierte Außenwand":[
            "Vorhangfassade"
        ]}


    # Rematching: Typ ersetzen in Matching
    for oldType in typeMapping:
        #print("Old Type: " + oldType)
        newMatchBuffer = list()
        oldMatchPile = list()
        for dict in tpMatching:
            #print("Check Type: " + dict["Typ"] + "...")
            #print(type(dict["Typ"]))
            if dict["Typ"] == oldType:
                match = dict
                #print("Match:")
                #print(match)
                # Neue Matchings auf Basis von altem Match erstellen
                for newType in typeMapping[oldType]:
                    newMatch = match.copy()
                    newMatch["Typ"] = newType
                    newMatchBuffer.append(newMatch)
                oldMatchPile.append(match)
        # Altes Match löschen
        for oldMatch in oldMatchPile:
            #print("Match wird gelöscht:")
            #print(oldMatch)
            tpMatching.remove(oldMatch)
        # Neue gesammelte Matches hinzufügen
        tpMatching += newMatchBuffer
    print("Matching nach Type-Mapping untergliedert...")
    print("Einlesen der Datentabellen erfolgreich.")
    print()

    '''
    Datenbankverbindung aufbauen und Tabellen initialisieren
    '''
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, host='localhost', password=password)
        print("Verbindung zur Datenbank aufgebaut.")
    except:
        print("Fehler: Konnte keine Verbindung zur Datenbank aufbauen!")

    cursor = conn.cursor()
    # Encoding prüfen (UTF8/Unicode)
    cursor.execute("SHOW SERVER_ENCODING;")
    encServer = cursor.fetchone()[0]
    print("Server Encoding: " + encServer)
    print("Client Encoding: " + conn.encoding)
    if encServer != conn.encoding:
        print("Warnung: Server und Client Encoding stimmen nicht überein!")

    # Datenbanktabellen löschen und neue leere Tabellen erstellen
    sqlFile = open(sqlFileName, "r")
    cursor.execute(sqlFile.read())
    conn.commit()
    print("SQL-Relationen erzeugt.")
    cursor.close()

    '''
    Tabellendaten einander zuordnen und in Datenbank übertragen
    '''
    cursor = conn.cursor()

    # Format
    for value in formats:
        insertion = value
        #print(insertion)
        cursor.execute("INSERT INTO Format (bezeichnung) VALUES (%s)", [insertion])
    # Attribut
    for i, name in enumerate(properties.keys()):
        #print(name)
        insertion = [
            i,
            name,
            properties[name]["Format"]
        ]
        #print(insertion)
        cursor.execute("INSERT INTO Attribut (id, bezeichnung, format) VALUES (%s, %s, %s)", insertion)
    # Arbeitsbereich
    for value in workAreas:
        insertion = value
        #print(insertion)
        cursor.execute("INSERT INTO Arbeitsbereich (bezeichnung) VALUES (%s)", [insertion])
    # Kategorie
    for i, name in enumerate(categories.keys()):
        insertion = [
            i,
            name,
            categories[name]["Arbeitsbereich"],
            categories[name]["LoG100"],
            categories[name]["LoG200"],
            categories[name]["LoG300"],
            categories[name]["LoG400"],
            categories[name]["LoG500"]
        ]
        #print(insertion)
        cursor.execute("INSERT INTO Kategorie (id, bezeichnung, arbeitsbereich, log100, log200, log300, log400, log500) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", insertion)

    # DIN276 Kostengruppen
    for tuple in dinList:
        insertion = tuple
        #print(insertion)
        cursor.execute("INSERT INTO KL_DIN276 (kostengruppe, bezeichnung) VALUES (%s, %s)", insertion)
    # IFC Entitäten
    for value in ifcList:
        insertion = value
        #print(insertion)
        cursor.execute("INSERT INTO KL_IFC (bezeichnung) VALUES (%s)", [insertion])
    # Typ
    for i, name in enumerate(types.keys()):
        insertion = [
            i,
            name,
            str(types[name]["Klassifikation DIN"]),
            types[name]["Klassifikation IFC"]
        ]
        search = types[name]["Kategorie"]
        i = list(categories.keys()).index(search)
        insertion.insert(2, i)
        #print(insertion)
        cursor.execute("INSERT INTO Typ (id, bezeichnung, kategorieId, klDin276, klIfc) VALUES (%s, %s, %s, %s, %s)", insertion)
    # Psets
    for value in psets:
        insertion = value
        #print(insertion)
        cursor.execute("INSERT INTO Pset (bezeichnung) VALUES (%s)", [insertion])
    # Einheiten
    for value in units:
        insertion = value
        #print(insertion)
        cursor.execute("INSERT INTO Einheit (bezeichnung) VALUES (%s)", [insertion])
    # Verantwortlichkeiten
    for tuple in responsibilities:
        insertion = tuple
        #print(insertion)
        cursor.execute("INSERT INTO Verantwortlichkeit (bezeichnung, erklaerung) VALUES (%s, %s)", insertion)
    # Matching Attribut/Typ
    for match in tpMatching:
        insertion = []
        #print(match)
        typId = list(types.keys()).index(match["Typ"])
        insertion.append(str(typId))
        propId = list(properties.keys()).index(match["Attribut"])
        insertion.append(str(propId))
        insertion.append(match["Pset"])
        insertion.append(str(match["loi_min"]))
        insertion.append(match["Einheit"])
        insertion.append(match["IL"])
        insertion.append(match["IA"])
        #print(insertion)
        cursor.execute("INSERT INTO Matching (typId, attributId, pset, loi_min, einheit, infoLieferung, infoAufnahme) VALUES (%s, %s, %s, %s, %s, %s, %s)", insertion)

    # Daten übergeben
    conn.commit()
    print("Daten in Datenbank übertragen.")

    # Verbindung zur Datenbank schließen
    cursor.close()
    conn.close()
    print("Datenbankverbindung geschlossen.")
    print("Datenbank wurde aktualisiert.")

elif not configRead:
    print("Datenbank wurde nicht aktualisiert.")
else:
    print("Dateien konnten nicht von Server abgerufen werden. Bitte überprüfen Sie Ihre Internetverbindung. Oder unsere...")
    print("Datenbank wurde nicht aktualisiert.")

print("Fenster schließt sich automatisch...")
time.sleep(10)
