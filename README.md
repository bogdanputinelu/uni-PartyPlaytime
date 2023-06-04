# PartyPlaytime

<img align="right" src="https://mir-s3-cdn-cf.behance.net/project_modules/disp/8aafd6121516019.60c7cf2e396a4.gif"> </img>

Aplicatia PartyPlaytime este o aplicatie destinata distractiei pentru grupuri de prieteni. Utilizatorul poate juca mai multe mini-game-uri cu grupurile de prieteni. In cazul in care nu are un grup de prieteni cu care sa se joace, utilizatorul poate opta pentru jocuri single player, avand posibilitatea de a juca cu un bot. 

**‘Word Rush’** este un joc de societate ce necesita cel putin doua echipe a cate doi jucatori. Pe ecran va aparea o expresie sau un cuvant care trebuie mimat, desenat sau descris de un membru al echipei. Ceilalti coechipieri trebuie sa ghiceasca cuvantul. Daca acestia il ghicesc, primesc un punct. Prima echipa care ajunge la X puncte castiga.  

**‘Headspin’** este un joc de societate ce necesita cel putin doua echipe a cate doi jucatori. Fiecare jucator al echipei se va afla pe rand in spatele calculatorului. Jucatorul are la dispozitie mai multe cuvinte pe care trebuie sa ghiceasca cu ajutorul coechipierului. Castiga echipa care a strans cele mai multe puncte.

**‘Board Blitz’** este un joc de societate ce necesita 2, 3, sau 4 persoane. Fiecare jucator are 4 pioni, iar scopul sau este sa isi duca pionii in zona de finish. Pionii avanseaza in functie de numarul indicat pe zar. Primul jucator care are toti pionii in zona de finish castiga. 

**‘Tic Tac Toe’** este un joc clasic ce necesita doua persoane. Pe ecran va aparea un tabel cu trei linii si trei coloane. Fiecare jucator marcheaza pe rand cate o casuta cu X si 0, iar primul jucator care reușește să marcheze 3 căsute adiacente pe orizontală, verticală sau diagonală caștigă jocul. In cazul in care este un singur utilizator, acesta o sa joace cu un bot.


## Membrii echipei 
- **[Putinelu Bogdan](https://github.com/bogdanputinelu)**
- **[Nicolae Mihaila](https://github.com/MihailaNicolae)**
- **[Enescu Irina ](https://github.com/irinaenescu2002)**

## User Stories 

1.	Ca utilizator, as dori o aplicatie cu diverse jocuri de societate.
2.	Ca utilizator, as dori sa imi pot crea un cont in aplicatie. 
3.	Ca utilizator, as dori sa am posibilitatea de a edita contul meu. 
4.	Ca utilizator, as dori sa imi pot seta un nickname. 
5.	Ca utilizator, as dori sa pot juca un joc in mod single player cu ajutorul unui bot. 
6.	Ca utilizator, as dori un set de instructiuni pentru fiecare joc.
7.	Ca utilizator, as dori sa pot juca jocuri in echipa.
8.	Ca utilizator, as dori sa salvez diverse setari ale jocurilor de grup in contul meu.
9.	Ca jucator, as dori ca jocurile din aplicatie sa imi indice de la inceput numarul minim de jucatori.
10.	Ca jucator, as dori sa setez numarul de runde in urma carora sa se castige un joc.
11.	Ca jucator, as dori sa setez cate puncte trebuie acumulate pentru a castiga un joc.
12.	Ca jucator, as dori sa pot adauga optiuni personalizate in jocuri.
13.	Ca jucator, as dori sa pot seta numarul de jucatori pentru jocurile de grup.
14.	Ca jucator, sa dori sa vad clasamentul la finalul jocului.
15.	Ca jucator, as dori sa vad modificari pe tabla de joc in timp real.
16.	Ca jucator, as dori sa primesc o atentionare in momentul in care parasesc jocul din greseala. 


## Backlog 
Backlog-ul proiectului a fost realizat cu ajutorul aplicatiei [Trello](https://trello.com/create-first-team) si se regaseste [aici](https://github.com/bogdanputinelu/uni-PartyPlaytime/tree/main/trelloBacklog). Imaginea reprezinta un stadiu al dezvoltarii software a proiectului. Fiecare joc a avut o lista de functionalitati ce trebuie implementate. Acestea au fost marcate pe parcurs cu etichete de tipul ‘Done’, ‘In progress’, ‘To do’ sau ‘Unsure’ pentru o gestionare mai buna a activitatii.

![image](https://github.com/bogdanputinelu/uni-PartyPlaytime/assets/93870739/90a3169c-193b-49a9-b78d-0d9510e8a6e2)

## Workflow Diagram 

Diagrama Workflow a aplicatiei se gaseste [aici](https://github.com/bogdanputinelu/uni-PartyPlaytime/tree/main/diagrameWorkflow). Aceasta contine cinci componente (Main, Word Rush, Headspin, Board Blitz si Tic Tac Toe) impartite conform functionalitatilor aplicatiei. Structurarea lor clara permite o buna intelegere a pasilor de implementare. 

![image](https://github.com/bogdanputinelu/uni-PartyPlaytime/assets/93870739/45eafa9f-7e17-4ccf-87a8-e9571437d99b)


## Source control cu git

Sincronizarea codului a fost realizata cu ajutorul Git. Am creat mai multe branch-uri (una pentru fiecare membru al echipei). Pe parcurs, am dat pull request-uri pentru a aduce pe main functionalitatile implementate de fiecare si am dat merge la branch-uri. Asa cum se observa, am avut mai mult de 10 commit-uri. 

## Code standards 

Am respectat un set de reguli și convenții pentru a scrie codul sursă într-un mod coerent și ușor de citit, în conformitate cu standardele industriei. Acest lucru facilitează înțelegerea codului și reduce erorile.
- Am folosit denumiri descriptive pentru variabile, funcții și clase. Am folosit snake_case pentru variabile și funcții (exemplu: alien_is_pressed) și PascalCase pentru denumirea claselor (exemplu: GameCardBehaviour).
- Am folosit identarea consistenta pentru a structura codul (patru spatii pe fiecare nivel).
- Am limitat lungimea liniilor de cod la aproximativ 79-80 de caractere pentru a asigura o vizualizare adecvată pe majoritatea ecranelor.
- Am urmat setul de recomandari de stil PEP 8 (Python Enhancement Proposal 8). 

![image](https://github.com/bogdanputinelu/uni-PartyPlaytime/assets/93870739/bc201f03-28e1-4622-af95-14df3cd35acc)

## Tool AI - ChatGPT 

Am folosit ChatGPT pentru urmatoarele: 
- furnizarea listei de cuvinte pentru jocuri 
- rezolvarea unor erori 
- generarea unor bucati de cod (aceste bucati de cod nu au fost integrate in program exact asa cum au fost generate de ChatGPT, ci au fost modificate - ele au reprezentat doar un punct de plecare)

![image](https://github.com/bogdanputinelu/uni-PartyPlaytime/assets/93870739/46709e9f-8a7f-4b73-9e58-7c584dfc4518)

## Comentarii  

Comentariile din cod sunt utilizate pentru a adăuga explicații și clarificări cu privire la modul în care funcționează sau ar trebui să funcționeze anumite functii. 
- Am adaugat comentarii in cod doar acolo unde sunt necesare si relevante, evitand redundanta si aglomerarea codului. Nu a fost nevoie de foarte multe comentarii deoarece denumirile variabilelor si functiilor sunt sugestive.
- Am respectat stilul, formatarea si identarea corespunzatoare a comentariilor adaugate pentru a le face usor de citit si de urmarit. 
- Am folosit comentariile pentru a comunica intre membrii echipei, punand in evidenta observatii sau sugestii utile pentru bucatile de cod ce se aseamana foarte mult. 

![image](https://github.com/bogdanputinelu/uni-PartyPlaytime/assets/93870739/f59213d2-980c-4e02-9785-e0a7c50e9685)

## Raportare bug si rezolvare cu pull request 
[Nicolae](https://github.com/MihailaNicolae) a raportat un bug in cadrul functionalitatii unui joc (jocurile anterioare afectau valorile pass & points in jocurile urmatoare), iar [Irina ](https://github.com/irinaenescu2002) l-a rezolvat cu pull request. 

![image](https://github.com/bogdanputinelu/uni-PartyPlaytime/assets/93870739/5e2db323-c01f-4477-ba54-c62d00f130ac)

## Teste automate 
- Functia care verifica daca avem un castigator 
- Functia care prezice urmatoarea mutare a bot-ului pe dificultatea hard 
- Functia care testeaza daca un pion are in fata un blocaj 
- Functia care verifica ce pioni pot fi mutati 

![image](https://github.com/bogdanputinelu/uni-PartyPlaytime/assets/93870739/9d8a6de7-6641-46a5-b5d4-b17b997db3e7)

## Code refactoring 
Urmatoarea bucata de cod face parte din functia ce animeaza miscarea pionilor pe table jocului BoardBlitz si se regaseste in acest [commit](https://github.com/bogdanputinelu/uni-PartyPlaytime/commit/400c11eddfbcfe87ca1eb3fdab773e24bc063485).

![image](https://github.com/bogdanputinelu/uni-PartyPlaytime/assets/93870739/c0791403-3722-4895-a9cb-4d1e93b293f4)

Acesta a fost refactorizat, fiind eliminate mai multe bucati de cod redundante. Noul cod este unul concis si usor de inteles si se regaseste in acest [commit](https://github.com/bogdanputinelu/uni-PartyPlaytime/commit/76caf9849976275f1c8eecde845d963031f5356d).

![image](https://github.com/bogdanputinelu/uni-PartyPlaytime/assets/93870739/fe9b8c50-ab7e-43e1-848c-3e79276ef291)

## Documentatie
O prezentare mai detaliata a proiectului se regaseste in folderul [documentation](https://github.com/bogdanputinelu/uni-PartyPlaytime/tree/main/documentation). 






