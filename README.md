# Digitale Genusswand V1
#### in Gedenken an den heiligen Strichegott 😁😉

<br>
Das Projekt hilft zur Überwachung der von bösen Studenten und Mitarbeitern begangenen
Verfehlungen.

<br><br>

#### NUTZUNG
Das System bietet die Möglichkeit mehrere User anzulegen, jeder User kann eigene
Genusswände erstellen

<br>
Für die Nutzung muss ein Dockerimage mit der Dockerfile gebaut werden

```
    docker build -t genusswand .
```
Diese muss mit einem Port gestartet werden, intern hört der Server auf Port 8000,
über docker an das System ausgegeben wird ist aber egal, solange dieser in dem Container
auf 8000 gelinkt ist

```
    docker run -p 8000:8000 genusswand
```


<br>

#### Erweiterungen für geplante "DIGITALE GENUSSWAND V2"
Aktuell können Frontend-Seitig dem "bösen Mitarbeiter" nur Striche hinzugefügt und
entfernt werden, das Backend bietet allerdings bereits die Möglichkeit jedem Strich
einen Grund und einen Reporter (also dem, welchem die Verfehlung aufgefallen ist)
hinzuzufügen, ebenso wird jedem Strich auch ein Datum hinzugefügt, für V2 ist somit
folgendes geplant:
- Frontend aufgrund von Transparenz mit Informationen über einen Strich ausstatten
- Frontend stylisch stark überarbeiten, bin halt einfach scheiße in CSS
- REST-API Schnittstellen um besseres Fehler-Catching erweitern
