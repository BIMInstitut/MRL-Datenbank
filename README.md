# MRL-Datenbank
Notwendige Software: PostgreSQL 13, Phyton 3.9.2, Python Module gem. Ziffer 2.b.

 1. Einrichtung Datenbank-Umgebung
  a. Download der PostgreSQL-Datenbankumgebung Version 13.1
  b. Installation mit Standardeinstellungen inkl. des beiliegenden Datenbankmanagement-systems pgAdmin. Wählen Sie wenn aufgefordert ein Passwort für das Datenbanksys-tem, das Sie   später verwenden (siehe Hinweis). Wählen Sie am Ende der Installation die Option Launch Stack Builder ab.
  Hinweis: Bitte verwenden Sie keine persönlichen Passwörter. Das Passwort wird später in eine unverschlüsselte Textdatei eingegeben und gespeichert und ist somit nicht si-cher.     Die Textdatei enthält bereits das vordefinierte Passwort „1234“, welches Sie än-dern können.
2. Einrichtung Python-Umgebung
  a. Damit Python-Skripte ausgeführt werden können, wird die Python Laufzeitumgebung benötigt. Das Python Setup2 kann größtenteils mit den Standardeinstellungen installiert        werden, jedoch mit der Zusatzoption „Add Python to PATH“. Die Installation von zu-sätzlich erforderlichen Modulen erfolgt über die Konsole. Die folgende Anleitung gilt nur für Windows-Betriebssysteme. Ausführung wie folgt an Beispiel mit Modul pandas:
    1. Windows Konsole aufrufen mit [Win]+[R], Textfeld "cmd" -> [Enter]
    2. In der Konsole eingeben: python -m pip install pandas und mit [Enter] bestäti-gen
  b. Es gibt mehrere erforderliche Module, die für die Verwendung der Python Skripte in-stalliert werden müssen. Hierfür muss Schritt 2 des Beispiels oben für alle benötigten  Module wiederholt werden, wobei der Begriff pandas jeweils durch die folgenden Na-men ausgetauscht wird. Die notwendigen Module für die die Datenbankanwendung sind: psycopg2,lxml, openpyxl, XlsxWriter, Requests, flask.
3. Skripte: Aktualisierung der Datenbank und Start Datenbank-App
  a. Entpacken Sie die Zip-Datei MRL-DB-Prototyp.zip, falls noch nicht geschehen.
  b. Tragen Sie das während dem Datenbank Setup (siehe oben) gewählte Passwort in die Da-tei config.txt ein und falls Sie eine neue Datenbank erstellt haben (im Normalfall nicht   erforderlich) den Namen der Datenbank und den Nutzernamen. Speichern und schließen Sie die Datei.
  c. Führen Sie die Datei MRL-DB.bat aus. Es öffnen sich zwei Konsolenfenster
    1. Datenbank aktualisieren, schließt sich kurz darauf
    2. Serverinstanz, muss geöffnet bleiben, solange die Webseite verwendet wird
  und anschließend ein Browserfenster mit dem Webservice in dem die Datenbank abgefragt werden kann. Bedienung siehe Endbericht.


PostgreSQL downloadbar über https://www.postgresql.org/download/
<br/>Python downloadbar über https://www.python.org/downloads/
