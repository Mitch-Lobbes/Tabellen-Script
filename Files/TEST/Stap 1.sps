* Encoding: UTF-8.
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* DEEL 1. LOCATIES EN ALGEMENE INSTELLINGEN.
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* Geef de locatie van de projectmap.
FILE HANDLE MAP /NAME=
'C:\Users\mlobbes\Documents\Tabellen Script\Files\TEST'.

* Geef de naam van het SPSS databestand (format MWM2 Research Platform).
FILE HANDLE DATA /NAME=
'MAP\4 Dataverwerking\1 Ruwe data\Ruwe_data.sav'.

* Instellingen worden uitgelezen en een kopie van het databestand wordt geopend.
OMS /SELECT TABLES 
/IF COMMANDS=['CROSSTABS'] SUBTYPES=['Case Processing Summary'] 
/DESTINATION VIEWER=NO.
SET TLOOK = "C:\Users\mlobbes\Documents\Tabellen Uitdraaien Stappenplan\MWM2Look_V2.stt".
SET CTEMPLATE 'C:\Users\mlobbes\Documents\Tabellen Uitdraaien Stappenplan\MWM2Grafiek.sgt'.
SET CACHE 5.
SET PRINTBACK = OFF.
GET FILE = DATA.
DATASET NAME Origineel.
DATASET COPY Kopie.
DATASET ACTIVATE Kopie.
DATASET CLOSE Origineel.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* DEEL 2. VOORBEREIDING.
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
*Achtergrondvariabelen worden door SPSS als stringvariabele opgeslagen. Hierdoor kunnen deze niet in tabellen worden verwerkt. 
* Met onderstaande syntax kunnen variabelen uit een databestand worden omgezet naar numerieke variabelen. Er zijn twee manieren, afhankelijk of het getallen (bijv. leeftijd) of letters (bijv. geslacht) betreft.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * Manier 1* * * * * * * * * * * * * * * * * * * * ** * * * * * * *
*Voor strings die uit getallen bestaan zoals leeftijd. Verschilt met manier 2 op (SYSMIS=-99) ipv (MISSING=SYSMIS).

* nieuwe string variabele aanmaken - vullen met oude data - omzetten naar nominaal.
 * STRING COPY_D## (A2500).
 * COMPUTE COPY_D## = D##.
 * ALTER TYPE COPY_D## (F8.0).
 * EXECUTE.

* * variabele hercoderen en categorieën indelen.
 * RECODE COPY_D## (SYSMIS=-99) (1 THRU 17=1) (18 thru 24=2) (25 thru 34=3) (35 thru 44=4) (45 thru 54=5) (55 thru 64=6) (65 thru HI=7) INTO D##_REC.
 * VARIABLE LABELS D##_REC 'Leeftijd'.
 * FORMATS D##_REC (F8.0).
 * EXECUTE.

 * VALUE LABELS D##_REC
  1 'Jonger dan 18'
  2 '18 t/m 24 jaar'
  3 '25 t/m 34 jaar'
  4 '35 t/m 44 jaar'
  5 '45 t/m 54 jaar'
  6 '55 t/m 64 jaar'
  7 '65+'.
 * EXECUTE.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * Manier 2* * * * * * * * * * * * * * * * * * * * ** * * * * * * *
* Voor strings die letters bevatten. Gebruikt (MISSING=SYSMIS) ipv (SYSMIS=-99).

*String omzetten naar numeriek met CONVERT.
 * RECODE D## (missing=SYSMIS) (CONVERT) ('M'=1) ('V'=2) INTO D##_REC.
 * VARIABLE LABELS D##_REC 'Geslacht'.
 * VARIABLE LEVEL D##_REC (NOMINAL).
 * FORMATS D##_REC (F8.0).
 * EXECUTE.

 * VALUE LABELS D##_REC
1 'Man'
2 'Vrouw'.
 * EXECUTE.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* NOMINAAL.

* Geef de lijst met nominale variabelen (NV).
DEFINE NV () 
V1
V2
V14_1
!ENDDEFINE.

* Deel eventueel de categorieën van nominale variabelen opnieuw in.
 * RECODE V## (1 thru 2=1) (3 thru 5=2) (6 thru 7=3).
 * VALUE LABELS V##
  1 'Type A'
  2 'Type B'
  3 'Type C'.
 * EXECUTE.

* System missings (-99) worden omgezet naar user missings (99), daarna wordt het label toegevoegd.
RECODE NV (-99=99) (MISSING=99).
MISSING VALUES NV (99).
ADD VALUE LABELS NV 99 '(geen antwoord gegeven)'.
EXECUTE.

* Geef eventuele aanvullende missing values aan die je wel in de tabellen wilt tonen.
 * MISSING VALUES V## (99, ##).

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* 5-PUNTS BEOORDELINGSSCHAAL.
*Deze regels syntax kunnen eveneens gekopieerd en aangepas worden wanneer er schalen zijn met meer of minder beoordelingspunten.

* Geef de lijst met 5-punts beoordelingsschaal variabelen (SV_5).
DEFINE SV_5 () 
V3
V11_1
V11_2
V11_3
V12_1
V12_2
V12_3
!ENDDEFINE.

RECODE SV_5 (SYSMIS=-99).
ADD VALUE LABELS SV_5 -99 '(geen antwoord gegeven)'.
EXECUTE.

* Individuele 5-punts variabelen eventueel omcoderen. Denk eraan dat je ook de value labels mee aanpast bij omcoderen.
 * RECODE V## (1=5) (2=4) (3=3) (4=2) (5=1).
 * EXECUTE.
 * VALUE LABELS V##  
  5 'zeer tevreden' 
  4 'tevreden' 
  3 'neutraal' 
  2 'ontevreden' 
  1 'zeer ontevreden'.
 * EXECUTE.

* Indien de 'weet niet' niet mee hoeft te worden geteld in het totaal, draai dan onderstaande syntax. Als je ook het label 'weet niet' wilt verwijderen, draai dan de value labels opnieuw.
 * RECODE  SV_5 (6=SYSMIS).
 * EXECUTE.

* Dit zijn de lijst (SV_5) variabelen met de extenties '_Score', '_Top2', '_Bot2' en '_POMP' Gebruik hiervoor het Excel bestand 'Schaalvariabelen samenstellen' in de map.
DEFINE Score_5 () 
V3_Score
V11_1_Score
V11_2_Score
V11_3_Score
V12_1_Score
V12_2_Score
V12_3_Score
!ENDDEFINE.

DEFINE Top2_5 () 
V3_top2
V11_1_top2
V11_2_top2
V11_3_top2
V12_1_top2
V12_2_top2
V12_3_top2
!ENDDEFINE.

DEFINE Bot2_5 () 
V3_bot2
V11_1_bot2
V11_2_bot2
V11_3_bot2
V12_1_bot2
V12_2_bot2
V12_3_bot2
!ENDDEFINE.

*POMP hoeft niet ingevuld te worden, dit geeft een specifieke statische eenheid weer, de 'Percentage Of Maximum Potential'.

* De lijst 5-punts variabelen wordt getransformeerd. 
* Let goed op of de hoogste en laagste waarde kloppen.
RECODE SV_5 (1=1) (2=2) (3=3) (4=4) (5=5) (6=6) INTO Score_5.
RECODE SV_5 (6, 3 thru 5=0) (1 thru 2=100) INTO Top2_5.
RECODE SV_5 (4 thru 5=100) (6, 1 thru 3=0) INTO Bot2_5.
EXECUTE.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* MEERKEUZEVRAGEN.

*meerkeuze sets worden tegenwoordig standaard aangemaakt in het labelbestand.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* RAPPORTCIJFER.

* Geef de lijst met rapportcijfer variabelen (RCi).
COMPUTE RC1 = V5.
EXECUTE.

DEFINE RC () 
RC1
!ENDDEFINE.

* Variabele properties van de rapportcijfervragen worden overgenomen.
APPLY DICTIONARY FROM * /SOURCE VARIABLES = V5 /TARGET VARIABLES = RC1 /NEWVARS.

RECODE RC (-99=99) (MISSING=99).
MISSING VALUES RC (99).
ADD VALUE LABELS RC 99 '(geen antwoord gegeven)'.
EXECUTE.

* Individuele rapportcijfer variabelen eventueel omcoderen. Pas ook de value labels aan.
 * RECODE RC## (1=10) (2=9) (3=8) (4=7) (5=6) (6=5) (7=4) (8=3) (9=2) (10=1).
 * EXECUTE.
 * VALUE LABELS RC 
  10 '10' 
  9 '9' 
  8 '8' 
  7 '7' 
  6 '6' 
  5 '5'
  4 '4'
  3 '3'
  2 '2'
  1 '1 '
  -99 '(geen antwoord gegeven)' 
 * EXECUTE.

* Indien de 'weet niet' niet mee hoeft te worden geteld in het totaal, draai dan onderstaande syntax. Als je ook het label 'weet niet' wilt verwijderen, draai dan de value labels opnieuw.
 * RECODE RC## (11=SYSMIS).
 * EXECUTE.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* NPS.

* Geef lijst met NPS variabelen (NPSi).
COMPUTE NPS1 = V4.
EXECUTE.

DEFINE NPS () 
NPS1
!ENDDEFINE.

* De variabele properties van de NPS vragen worden overgenomen.
APPLY DICTIONARY FROM * /SOURCE VARIABLES = V4 /TARGET VARIABLES = NPS1 /NEWVARS.
 * APPLY DICTIONARY FROM * /SOURCE VARIABLES = V## /TARGET VARIABLES = NPS2 /NEWVARS.

RECODE NPS (-99=99) (MISSING=99).
MISSING VALUES NPS (99).
ADD VALUE LABELS NPS 99 '(geen antwoord gegeven)'.
EXECUTE.

* Individuele NPS variabelen eventueel hercoderen.
 * RECODE NPS## (0=10) (1=9) (2=8) (3=7) (4=6) (5=5) (6=4) (7=3) (8=2) (9=1) (10=0).
 * EXECUTE.
 * RECODE NPS## (1=0) (2=1) (3=2) (4=3) (5=4) (6=5) (7=6) (8=7) (9=8) (10=9) (11=10).
 * EXECUTE.

 * VALUE LABELS NPS## 
  10 '10 (zeer waarschijnlijk)'
  9 '9'
  8 '8' 
  7 '7' 
  6 '6' 
  5 '5' 
  4 '4'
  3 '3'
  2 '2'
  1 '1'
  0 '0 (zeer onwaarschijnlijk)'
  -99 '(geen antwoord gegeven)' 
 * EXECUTE.

* Indien de 'weet niet' niet mee hoeft te worden geteld in het totaal, draai dan onderstaande syntax.  Als je ook het label 'weet niet' wilt verwijderen, draai dan de value labels opnieuw.
 * RECODE NPS## (11=SYSMIS).
 * EXECUTE.


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* OPEN.

* Geef de lijst met open variabelen (OV).
DEFINE OV () 
OPEN2_5
OPEN7_5
OPEN8_5
!ENDDEFINE.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * 
*GEMIDDELDES (zonder iets anders).

DEFINE GEM ()
V5
V9
V10
V13_1
V13_2
V13_3
V14_1
!ENDDEFINE.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* KRUISVARIABELEN.

* Definieer de lijst met kruisvariabelen (KVi).
* Default wordt in de Custom Tables uitgesplitst naar 3 kruisvariabelen (KV1, KV2 en KV3). Aanvullende variabelen (KV4, KV5, etc.) kunnen hier worden ingevoerd.

COMPUTE KV1 = V1.
COMPUTE KV2 = V2.
EXECUTE.

DEFINE KV () 
KV1
KV2
!ENDDEFINE.

* In de Custom Tables syntax wordt default de volgende string gebruikt: 'KV1 [C] + KV2 [C] + KV3 [C]' .

* Wanneer er meer (of minder) kruisvariabelen zijn kan deze string in de syntax eenvoudig worden vervangen.
* Dit kan via Find and Replace.Bijvoorbeeld: Find: 'KV1 [C] + KV2 [C] + KV3 [C]' - Replace: 'KV1 [C] + KV2 [C] + KV3 [C] + KV4 [C]' .

* Variabele properties van de kruisvariabelen worden overgenomen.
APPLY DICTIONARY FROM * /SOURCE VARIABLES = V1 /TARGET VARIABLES = KV1 /NEWVARS.
APPLY DICTIONARY FROM * /SOURCE VARIABLES = V2 /TARGET VARIABLES = KV2 /NEWVARS.

*Pas de labels van de kruisvariabelen aan.
VARIABLE LABELS KV1 'V1'.
VARIABLE LABELS KV2 'V2'.
EXECUTE.


* Deel eventueel de categorieën van de kruisvariabelen eventueel opnieuw in.
 * RECODE KV2 (1=1) (2 thru 3=2) (4 thru 5=3) (MISSING=SYSMIS).
 * VALUE LABELS KV2
  1 '25 jaar of jonger'
  2 '26 t/m 55 jaar'
  3 '56 jaar of ouder'.
 * EXECUTE.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* TOTAAL.

* Variabele Totaal wordt aangemaakt, voor het weergeven van de 'overall' kolom vooraan in de tabellen. Hier hoef je niks te veranderen.
COMPUTE Totaal = 1.
VARIABLE LABELS Totaal ' '.
VARIABLE LEVEL Totaal (NOMINAL).
FORMATS Totaal (F8.0).
VALUE LABELS Totaal 1 'Totaal'.
EXECUTE.
OUTPUT CLOSE *.
