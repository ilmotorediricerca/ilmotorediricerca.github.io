# Traduzione inglese e didascalie

Cosa c'è in questo pacchetto (da copiare nella radice del repository, sovrascrivendo i file esistenti):
- le 9 pagine italiane corrette (refusi, lingua della pagina, link vuoti, piè di pagina);
- le 9 pagine inglesi in `en/` (stessi nomi file, raggiungibili come `/en/`, `/en/oda`, ...);
- `assets/js/lightbox.js`, `assets/css/lightbox.css` e `assets/css/i18n.css`;
- questa cartella `_i18n/` con lo script che genera tutto.

## Didascalie
Apri `_i18n/didascalie.yaml`. Ogni foto ha tre campi:

    - file: 01-che_pesci_prendere.jpg   (non toccare, come `dir` e `thumbdir`)
      it: "didascalia in italiano"
      en: "caption in English"
      credit: "Nome Cognome"

Campi vuoti non mostrano niente. Il testo appare nell'ingrandimento (lightbox), con il credito dopo
un punto mediano: "Didascalia · © Nome". Per ora sono vuote tutte, tranne il credito delle foto di Giardino
Radicale (Yacine Benseddik), preso dal "Photo credits" scritto nella pagina.

Per rigenerare le pagine dopo aver modificato il file, dalla radice del repository:

    python3 _i18n/build_imr.py

(serve `pyyaml`: `pip install pyyaml`). Lo script parte sempre dagli originali in `_i18n/src/`, quindi si può rilanciare quante volte vuoi.

## Da rivedere
- Le traduzioni inglesi sono mie: vanno lette da te (in particolare i titoli tradotti, mostrati in corsivo sotto il titolo originale).
- `CORREZIONI.txt` elenca tutti i refusi corretti nelle pagine italiane.
