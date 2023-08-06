# Coding Pirates Kuglebane controller

Controlleren kan modtage et (simpelt) serielt signal med en kommando - f.eks. fra en fra micro:bit.

Ud fra den modtagne kommando sender controlleren et request til [_kuglebane centralen_](https://github.com/Coding-Pirates-Viborg/kuglebane-central) og sender efterfølgende et svar tilbage til micro:bit'en.

Når controlleren starter op (se afsnit herunder) startes en tråd der poller _kuglebane centralen_ for at høre om der er kommet events til den kuglebane controlleren er tilknyttet.

- [Coding Pirates Kuglebane controller](#coding-pirates-kuglebane-controller)
  - [Kommandoer der kan sendes til controlleren](#kommandoer-der-kan-sendes-til-controlleren)
    - [Kommando: `init:<<bane_id>>`](#kommando-initbane_id)
    - [Kommando: `send:<<bane_id>>`](#kommando-sendbane_id)
    - [Kommando: `events`](#kommando-events)
    - [Kommando: `pop`](#kommando-pop)
    - [Kommando: `pop:<<event_id>>`](#kommando-popevent_id)
  - [Start kuglebane controlleren](#start-kuglebane-controlleren)
    - [Konfiguration af micro:bit og kuglebane-central](#konfiguration-af-microbit-og-kuglebane-central)
    - [Controller initialiseres ved opstart](#controller-initialiseres-ved-opstart)
  - [Micro:bit emulator](#microbit-emulator)
  - [Eksempelkode til micro:bit'en](#eksempelkode-til-microbiten)
  - [Finde den port micro:bit'en kommunikerer på](#finde-den-port-microbiten-kommunikerer-på)
    - [Linux (Pi)](#linux-pi)
      - [Installere screen på Ubuntu](#installere-screen-på-ubuntu)
    - [Mac](#mac)


## Kommandoer der kan sendes til controlleren

Hver gang en kommando modtages vil controlleren svare på formen:  `STATUS:KOMMANDO:SVAR`

Hvor: 

* STATUS = `OK` eller `ERROR`
* KOMMANDO = den kommando der er modtaget
* SVAR = for `OK` er dette svaret på kommandoen og for `ERROR` er dette noget yderligere fejlinformation

Svarene er uddybet herunder.

P.t. understøttes disse kommandoer:

---
### Kommando: `init:<<bane_id>>`

Initialisere controlleren til den kuglebane (med id=`bane_id`), som controlleren er tilknyttet.

* **Svar fra controller**: `OK:INIT:<<bane_id>>`


---
### Kommando: `send:<<bane_id>>`

Sender en `START` event til bane `<<bane_id>>`

* **Svar fra controller**: `OK:SEND:<<fra-bane_id>>:<<til-bane_id>>`


---
### Kommando: `events`

Henter alle events der er sendt til den kuglebane controlleren er tilnkyttet (dvs. kuglebanen man har angivet med `init` kommandoen)

* **Svar fra controller**: `OK:EVENTS-TRACK:<<bane_id>>:<<antal-events>>`
  * `bane_id` = den kuglebane controlleren er tilnkyttet (_dvs. det ID der er modtaget fra micro:bit'en med_ `init` _kommandoen_)
  * `antal_events` = antallet af beskeder der er modtaget til denne kuglebane

Beærk: i svaret ses bare antallet af events. Kig på konsollen for controlleren for at se hvilke events der er modtaget. 

For at afvikle den første (ældste) event sendes `pop` kommandoen.

For at afvikle en bestemt event sendes `pop:<<event_id>>` kommandoen


---
### Kommando: `pop`

Fjerner den ældste event fra _kuglebane centralen_ og sender kommando-id fra eventen til enheden (f.eks. en micro:bit) på den serielle port, så denne kan udføre kommandoen (f.eks. `START` for at starte en kugle) på kuglebanen den er tilnkyttet.

Desuden medsendes hvilken afdeling og kuglebane eventen blev afsendt fra.

* **Svar fra controller**: `OK:POP:<<fra_afdeling>>:<<fra-bane_id>>:<<kommando_id>>` 

  * EKSEMPEL: ældste besked er et `START` event afsendt fra afdeling `CPB` kuglebane nr. `2`:  `OK:POP:CPB:2:START`

* **Svar hvis der opstår en fejl:**: `ERROR:POP:<<eventuel fejlbesked>>`


---
### Kommando: `pop:<<event_id>>`

_ENDNU IKKE IMPLEMENTERET!_

Samme som `pop` men med et specifikt `<<event_id>>` i stedet for den ældste event. 

* **Svar fra controller**: `OK:POP:event_id:kommando_id` - f.eks. `OK:POP:6:START`

---

## Start kuglebane controlleren

Denne kan startes med `kb_controller.server.start()` 

F.eks.:

```python
>>> from kb_controller import controller
>>> controller.start()
```

eller fra et aktiveret `venv`:

```
  python venv/lib/python3.7/site-packages/kb_controller/controller.py
```

eller (hvis koden er klonet fra Github):

```text
  python src/kb_controller/controller.py
```

Controlleren forventer at der sidder en enhed på den serielle port - f.eks. en micro:bit (eller emulatoren - se herunder).

Hvis den angivne serielle port ikke er tilgængelig stopper controlleren med en fejl.


### Konfiguration af micro:bit og kuglebane-central
Første gang controlleren startes oprettes en `kbc-config.ini` konfigurationsfil, hvor port-angivelse til micro:bit'en, url'en til kuglebanecentralen og polling-intervallet til kuglebanecentralen angives. 

Der kan være forskllige konfigurationer, afhængigt af om micro:bit'en emuleres og om man bruger en lokal version af kuglebane-centralen eller ej. Dette styres med disse to flag i konfig-filen:

```
is_production = True eller False
is_emulator = True eller False
```

Tilret konfigurationsfilen, så den passer med hvilken seriel port micro:bit'en er forbundet til.

Se afsnittet længere ned [om at finde den port micro:bit'en sidder på](#finde-den-port-microbiten-kommunikerer-på)

Desuden kan man angive hvilket interval controlleren skal polle kuglebanecentralen med (dvs. hvor tit skal controlleren spørge centralen om der er kommen nye events). Intervallet angives i sekunder.

```
polling_interval=300
```


### Controller initialiseres ved opstart

Når controlleren starter sender den en "init" forespørgsel ud på det serielle interface og forventer et svar med `init:<<bane_id>>` (dette skal programmeres på den micro:bit, der er tilsluttet)

Herefter spyttes der en del info ud i konsollen, hvor man bla. kan se hvilken forening og kuglebane controlleren er konfigureret til og hvilke kuglebaner der er tilgængelige i kugelbane-caentralen, f.eks.:

```text
============================================================
Seriel forbindelse:
/dev/ttys006

============================================================
   M I C R O : B I T   S E R I A L   C O N T R O L L E R
============================================================
Kuglebane central: http://kuglebane.pythonanywhere.com/
Afdeling.........: CPV
Kuglebane........: 1
-----------------------------------------------------------

Tilgængelige kuglebaner:

  ---------------------------------
  CPV (EGEN AFDELING):
    1 - TEST Bane cpv
  ---------------------------------

  CPB:
    2 - TEST Bane cpb

  CPS:
    4 - TEST bane cps

-----------------------------------------------------------
```

## Micro:bit emulator

Med `ubit_emulator.start(<<track_id>>)` startes en simpel emulator, hvor man kan emulere de tekst kommandoer der sendes fra f.eks. en micro:bit der er forbundet serielt til controlleren.

Emulatoren defaulter til track-id=1. Dette skal sættes til det ID der passer med en kuglebane i den forening, controlleren er konfigureret til.

For at sætte emulatoren til at "lege" kugelbane 3, sættes `track_id=3` i start parameteren, f.eks:

```python
>>> from kb_controller import ubitemulator
>>> ubitemulator.start(3)
```

eller fra et aktiveret `venv`:

```
  python venv/lib/python3.7/site-packages/kb_controller/ubitemulator.py 3
```

eller (hvis koden er klonet fra Github):

```text
  python src/kb_controller/ubitemulator.py 3
```

Når emulatoren starter, skriver den hvilken seriel port den er startet på og hvilket track ID den er startet op med, f.eks.:

```text
=============================
     micro:bit emulator
=============================

Brug denne port på controlleren:
--------------------------------

/dev/ttys006

--------------------------------

micro:bit track-ID: 3

Venter på controller...

```

Og den venter nu på en `init` forespørgsel fra controlleren, som emulatoren svarer på. Herefter kan man sende en vilkårlig kommando til controlleren.

```
--------------------------------

micro:bit track-ID: 1

Venter på controller...
Controller forbundet.
Sender bane-ID "3" til controller
--> init:1

<-- OK:INIT:3
Emulator klar - skriv kommando og tryk <Enter>

Skriv kommando: 
```


## Eksempelkode til micro:bit'en

Et eksempel, hvor micro:bit'en kan modtage og sende kan ses i 

https://github.com/Coding-Pirates-Viborg/microbit-controller


## Finde den port micro:bit'en kommunikerer på

### Linux (Pi)

1. Plug in the micro:bit and open a new terminal window.
2. Typing dmesg | tail will shows you which /dev/ node the micro:bit was assigned (e.g. /dev/ttyACM0).
3. UBUNTU: dmesg | grep tty
4. Type sudo screen /dev/tty0 115200, replacing the number with the number you found in the previous step. You may need to install the screen program if you don't already have it.
5. To exit, press Ctrl-A then Ctrl-D.

Eks på tty for micro:bit’en: ttyACM0: USB ACM device

#### Installere screen på Ubuntu

- sudo apt install screen

### Mac

1. Plug in the micro:bit and open a new terminal window.
2. Type `ls /dev/cu.\*` to get a list of connected serial devices; one of them will look like /dev/cu.usbmodem1422 (the exact number depends on your computer).
3. Type `screen /dev/cu.usbmodem1422 115200`, replacing the 'usbmodem' number with the number you found in the previous step. This will open the micro:bit's serial output and show all messages received from the device.
4. To exit, press Ctrl-A then Ctrl-D.
