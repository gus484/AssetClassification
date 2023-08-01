# AssetClassification

Dieses Python-Skript ermittelt das Klumpen-Risiko verschiedener ETFs und vergleicht diese miteinander.
Dafür werden die Positionen aus den Anbieter-Dokumenten gewonnen.
Des Weiteren wird die Regionalverteilung für jeden ETF ermittelt und nach einer Vorlage gruppiert.
Die Ergebnisse werden als Report (Website) generiert. Das Skript kann entweder mittels der Kommandozeile verwendet
werden oder über die GUI.

This Python script determines the cluster risk of different ETFs and compares them with each other.
For this, the positions are obtained from the issuers documents.
Furthermore, the regional distribution for each ETF is determined and grouped according to a template.
The results are generated as a report (website)
The script can be used either by command line or via the GUI.

#### Kommandozeilenparameter / command line parameters

* "-id", "--idirectory" - input directory
* "-od", "--odirectory" - output path for html report
* "-is", "--isin" - whitespace separated list of interested ISINs
* "-gpo", "--gpo_desc" - path to region mapping json file

#### Unterstütze Anbieter / supported issuers

* Vanguard
* iShares
* VanEck

#### Funktionsumfang / functions

* Darstellung des Klumpen-Risikos / representation of the cluster risk
* Darstellung der regionalen Verteilung / representation of the regional distribution
    * konfigurierbar per json-Datei / configurable via json-file
* Filtern von Cash-Positionen / filtering cash positions

#### Einschränkungen / limitations

* Die Anbieter-Dokumente müssen selbst geholt werden / no automatic download of holding sheets
* Die Unternehmen werden anhand ihres Namens zusammengefasst / holdings are grouped by their names

#### Pläne / further plans

* :white_check_mark: ~~Report-Sprachauswahl via GUI / change report language via GUI~~
* Fortschrittsanzeige und Logging in der GUI / GUI displays the progress and log messages
* Unterstützung weiterer Anbieter / support for other issuers
* automatischer Download / automatic download
* :wrench: Anbindung an Portfolio Performance / link to Portfolio Performance
* Branchen-Auswertung / Sector evaluation

#### Verwendete Bibliotheken / used libs

* [chart.js](https://www.chartjs.org/)