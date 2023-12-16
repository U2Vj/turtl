# TURTL (Vir**TU**al Netwo**R**k Securi**T**y **L**ab)
TURTL is an acronym for VirTUal NetwoRk SecuriTy Lab. TURTL is an innovative, virtual and expandable learning environment for IT security in computer networks. TURTL started as a "Fellowship für Innovationen in der digitalen Hochschullehre" (Digi-Fellow) project funded by the "Ministerium für Kultur und Wissenschaft NRW". TURTL was initiated by Prof. Dr. Gundula Dörries (deceased) and Prof. Dr. Holger Schmidt.

 ## Eine virtuelle und erweiterbare Lernumgebung für IT-Sicherheit in Rechnernetzen

Für die praxisorientierte Lehre in dem Themengebiet IT-Sicherheit in Rechnernetzen sollen Studierende sowohl eine Verteidiger-Sicht als auch eine Angreifer-Sicht einnehmen und mit "echten" Schwachstellen konfrontiert werden. Bisherige Ansätze fur eine entsprechende Umsetzung in der Lehre basieren entweder auf teurer und unflexibler Netzwerkinfrastruktur oder nutzen einseitige (nur Angreifer-Sicht) und praxisferne Simulationen. 

Ziel des vorgestellten Projektes ist die Realisierung der auf Virtualisierung grundenden Lernumgebung TURTL (Vir**TU**al Netwo**R**k Securi**T**y **L**ab) für das Themengebiet IT-Sicherheit in Rechnernetzen. TURTL soll handlungsorientiertes Lernen flexibel, ortsunabhängig und ohne größeren Vorbereitungs- und Betreuungsaufwand unterstützen. Die Virtualisierung ermöglicht dabei in praxisnaher Weise die Bereitstellung komplexer Infrastrukturen, wie sie für das Themengebiet typisch sind, und macht dadurch aufwändige Hardware und theorielastige Simulationen verzichtbar.

## Structure
This TURTL Prototyp uses [Django](https://www.djangoproject.com/) as a Backend and [Docker](https://www.docker.com/) for managing containers.  
[*Docker SDK for Python*](https://docker-py.readthedocs.io/en/stable/) is used to call the Docker API via Django.  
The structure looks like:   
Vue.js <--> Django <--> *Docker SDK for Python* <--> Docker API

## Implementation
Inside the [Frontend](frontend/) a [Websocket](https://developer.mozilla.org/de/docs/WebSockets) is created to the Django Backend. 
Inside Django the package [Django Channels](https://channels.readthedocs.io/en/latest/) is used to handle the incoming Websocket request. When the Frontend-Websocket connection is accepted another Websocket is opened via *Docker SDK for Python* to a Docker container.   
Both Websockets get chained, so the Frontend can send Command to the container and can recieve the output.
Via Django-Channels it's possible to add a Middleware for 
[Authentification via Websockets](https://channels.readthedocs.io/en/latest/topics/authentication.html).  
This can be usefull to ensure a user is authenticated to access a specific Docker container.  

The structure of the Websockets looks like:  
Vue.js <--> Websocket <--> Django Channels <--> Socket <-->Container  
Datei: ```shell/consumers.py```


## Development  
- [Backend Development Guide](./BackendDevelopmentGuide.md)
- [Frontend Development Guide](./frontend/FrontendDevelopmentGuide.md)
