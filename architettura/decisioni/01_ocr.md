# Soluzioni OCR — Confronto Architetturale Software

> **Contesto:** Valutazione di soluzioni OCR per uno strumento di studio automatizzato che acquisisce documenti delle lezioni, li unisce agli appunti e genera note strutturate tramite AI. Valutato su 7 dimensioni architetturali.

---

## Soluzioni Valutate

| # | Soluzione | Descrizione |
|---|-----------|-------------|
| 1 | **Google Cloud Vision API** | OCR cloud generico, alta accuratezza, API completa |
| 2 | **Adobe Acrobat OCR** | Strumento desktop manuale, alta accuratezza, nessuna automazione |
| 3 | **Tesseract + Claude API** ⭐ *Consigliato* | OCR open-source + strutturazione AI, pipeline completamente locale |
| 4 | **Microsoft Azure AI Vision** | OCR cloud enterprise, ottima scrittura a mano, API completa |
| 5 | **Mathpix** | Specializzato per matematica/equazioni, output LaTeX |

---

## 1. Accuratezza e Qualità

| Dimensione | Google Cloud Vision | Adobe Acrobat | Tesseract + Claude | Azure AI Vision | Mathpix |
|------------|--------------------|--------------|--------------------|-----------------|---------|
| OCR testo stampato | ★★★★★ | ★★★★★ | ★★★★ | ★★★★★ | ★★★★ |
| Scrittura a mano | ★★★★ | ★★★ | ★★★ (+ correzione Claude) | ★★★★★ | ★ |
| Matematica / equazioni | ★★ | ★★ | ★★★ (Claude interpreta) | ★★ | ★★★★★ output LaTeX |
| Scansioni di bassa qualità | ★★★★ | ★★★ | ★★★ | ★★★★ | ★★★ |
| Post-elaborazione / correzione | Nessuna | Modifica manuale | ✅ Gestita da Claude | Nessuna | Nessuna |

**Note:**
- Azure vince sul riconoscimento della scrittura a mano — scelta migliore se gli appunti sono scritti a mano
- Mathpix è l'unica soluzione con output LaTeX nativo — essenziale per corsi STEM con equazioni
- L'accuratezza di Tesseract cala su scansioni degradate; Claude può compensare molti errori di estrazione

---

## 2. Integrazione e Automazione

| Dimensione | Google Cloud Vision | Adobe Acrobat | Tesseract + Claude | Azure AI Vision | Mathpix |
|------------|--------------------|--------------|--------------------|-----------------|---------|
| Disponibilità API | ✅ REST + SDK | ❌ Nessuna API | ✅ CLI + libreria Python | ✅ REST + SDK | ✅ REST API |
| Elaborazione batch | ✅ Batch asincrono nativo | ❌ Solo manuale | ✅ Loop scriptabile | ✅ Batch asincrono nativo | ⚠️ Rate-limited |
| Integrazione pipeline / CI-CD | ✅ Completa | ❌ Non automatizzabile | ✅ Script locale o cloud | ✅ Completa | ⚠️ Solo API, no hook |
| Supporto webhook / eventi | ✅ Integrazione Pub/Sub | ❌ Nessuno | ⚠️ Sviluppo custom | ✅ Azure Event Grid | ❌ Nessuno |
| Formati di output | JSON (bounding box) | PDF, DOCX, TXT | Testo semplice → qualsiasi | JSON (bounding box) | LaTeX, Markdown, HTML |
| Output note strutturate | ❌ Richiede passaggio extra | ❌ Richiede passaggio extra | ✅ Claude gestisce in pipeline | ❌ Richiede passaggio extra | ❌ Richiede passaggio extra |

**Note:**
- Adobe è escluso per qualsiasi workflow automatizzato — nessuna API, completamente manuale
- Tesseract + Claude è l'unica soluzione che gestisce OCR **e** generazione di note strutturate in un unico passaggio di pipeline
- GCP e Azure richiedono un livello AI separato per produrre note strutturate

---

## 3. Scalabilità e Performance

| Dimensione | Google Cloud Vision | Adobe Acrobat | Tesseract + Claude | Azure AI Vision | Mathpix |
|------------|--------------------|--------------|--------------------|-----------------|---------|
| Throughput | Molto alto | File singolo, manuale | Medio (CPU locale) | Molto alto | Rate-limited |
| Latenza per pagina | ~0.5–1s | ~3–10s (manuale) | ~1–3s (locale) | ~0.5–1s | ~1–2s |
| Scale-to-zero | ✅ Pay-per-use | ❌ Abbonamento fisso | ✅ Locale = sempre gratuito | ✅ Pay-per-use | ⚠️ Minimo mensile |
| Scaling orizzontale | ✅ Gestito da GCP | ❌ Nessuno | ⚠️ Manuale (worker pool) | ✅ Gestito da Azure | ❌ Cap concorrenza API |

**Note:**
- Per un caso d'uso studentesco (~50–200 pagine/settimana), il throughput non è un collo di bottiglia — latenza e costo per lezione contano di più
- L'elaborazione locale di Tesseract (~1–3s/pagina) è più che adeguata per batch di una singola lezione
- Le API cloud diventano rilevanti solo se lo strumento viene scalato in seguito a una piattaforma multi-utente

---

## 4. Sicurezza e Conformità

| Dimensione | Google Cloud Vision | Adobe Acrobat | Tesseract + Claude | Azure AI Vision | Mathpix |
|------------|--------------------|--------------|--------------------|-----------------|---------|
| Residenza dei dati | Region GCP | Cloud Adobe | ✅ Locale — nessun upload | Region Azure | Solo server USA |
| I dati lasciano il dispositivo? | ❌ Sì, verso GCP | ❌ Sì, verso Adobe | ✅ No (Tesseract locale) | ❌ Sì, verso Azure | ❌ Sì, verso Mathpix |
| Conformità GDPR / FERPA | ⚠️ Con accordo DPA | ⚠️ Con accordo DPA | ✅ Pienamente conforme (locale) | ⚠️ Con accordo DPA | ❌ Limitata, nessun DPA |
| Modello di autenticazione | OAuth2 / service account | Adobe ID / SSO | API key (Anthropic) | Azure AD / Entra | Solo API key |

**Note:**
- **FERPA** (USA) e **GDPR** (UE) regolano i dati accademici degli studenti — qualsiasi upload su cloud richiede un Data Processing Agreement (DPA) firmato
- Tesseract gira localmente; i documenti non lasciano mai il dispositivo, rendendolo l'opzione più sicura per impostazione predefinita
- Mathpix non ha un DPA pubblicato — un rischio di conformità in ambienti accademici regolamentati
- Nota: la chiamata API a Claude per la strutturazione invia il testo estratto ad Anthropic; valutare se accettabile secondo le policy del proprio istituto

---

## 5. Modello di Costo

| Dimensione | Google Cloud Vision | Adobe Acrobat | Tesseract + Claude | Azure AI Vision | Mathpix |
|------------|--------------------|--------------|--------------------|-----------------|---------|
| Modello di pricing | Per pagina, pay-as-go | Abbonamento mensile | OCR gratuito + token API | Per pagina, pay-as-go | Abbonamento mensile |
| Costo a ~50 pagine/settimana | ~$0.10–0.20/sett | ~$5–20/mese fisso | ~$0.05–0.15/sett | ~$0.08–0.15/sett | ~$10/mese fisso |
| Piano gratuito | 1.000 unità/mese | Nessuno | Illimitato (OCR locale) | 5.000 transazioni/mese | 100 richieste/mese |
| Prevedibilità del costo | ⚠️ Variabile | ✅ Fisso | ✅ Molto basso / prevedibile | ⚠️ Variabile | ✅ Fisso |

**Note:**
- A ~50 pagine/settimana (2.500 pagine/anno), Tesseract + Claude API è l'opzione più economica con il costo più prevedibile
- Gli abbonamenti Adobe e Mathpix costano più di quanto giustifichi l'utilizzo a scala studentesca
- I piani gratuiti di GCP e Azure coprono probabilmente l'utilizzo leggero interamente — validi per uso occasionale

---

## 6. Affidabilità e Operatività

| Dimensione | Google Cloud Vision | Adobe Acrobat | Tesseract + Claude | Azure AI Vision | Mathpix |
|------------|--------------------|--------------|--------------------|-----------------|---------|
| SLA / uptime | 99.9% (SLA GCP) | Nessun SLA | Locale = 100%; API variabile | 99.9% (SLA Azure) | Nessun SLA pubblicato |
| Rischio vendor lock-in | ❌ Alto (API GCP) | ❌ Alto (Adobe) | ✅ Basso — OCR open source | ❌ Alto (API Azure) | ❌ Alto (proprietario) |
| Funzionamento offline | ❌ No | ⚠️ Solo app desktop | ✅ Sì (Tesseract locale) | ❌ No | ❌ No |
| Osservabilità / logging | ✅ Cloud Logging integrato | ❌ Nessuno | ⚠️ Custom (log su file) | ✅ Azure Monitor | ❌ Nessuno |

**Note:**
- La capacità offline di Tesseract è preziosa in aule con connettività scarsa
- GCP e Azure offrono la migliore osservabilità out-of-the-box — rilevante se lo strumento servirà più utenti in futuro
- Il vendor lock-in è il principale rischio architetturale a lungo termine: GCP, Azure, Adobe e Mathpix richiedono tutti una riscrittura significativa per essere sostituiti

---

## 7. Manutenibilità ed Estensibilità

| Dimensione | Google Cloud Vision | Adobe Acrobat | Tesseract + Claude | Azure AI Vision | Mathpix |
|------------|--------------------|--------------|--------------------|-----------------|---------|
| Supporto lingue | 100+ lingue | 40+ lingue | 100+ (Tesseract) + Claude | 100+ lingue | Solo inglese + matematica |
| Fine-tuning personalizzato | ❌ Non disponibile | ❌ Non disponibile | ✅ Tesseract addestrabile; Claude personalizzabile via prompt | ⚠️ Solo piano Enterprise | ❌ Non disponibile |
| Self-hostable | ❌ No | ❌ No | ✅ Sì (Tesseract) | ❌ No (solo opzione container) | ❌ No |
| Community / OSS | ⚠️ Grande, supportata da Google | ❌ Proprietario | ✅ Grande OSS + Anthropic | ⚠️ Grande, supportata da Microsoft | ❌ Piccola, proprietaria |

**Note:**
- La personalizzazione via prompt di Claude permette di adattare la struttura delle note per corso (es. stile di intestazione diverso per giurisprudenza vs. ingegneria) senza modifiche al codice
- Tesseract può essere addestrato su font personalizzati o stili di scrittura specifici se necessario
- Tutte le soluzioni cloud richiedono migrazione delle versioni API nel tempo; Tesseract open-source è stabile e sotto il proprio controllo

---

## Scorecard Architetturale Complessiva

| Soluzione | Accuratezza | Integrazione | Scalabilità | Sicurezza | Costo | Affidabilità | Manutenibilità | **Totale** |
|-----------|-------------|--------------|-------------|-----------|-------|--------------|----------------|------------|
| Google Cloud Vision | ★★★★★ | ★★★★ | ★★★★★ | ★★★ | ★★★★ | ★★★★ | ★★★ | ★★★★ |
| Adobe Acrobat | ★★★★★ | ★ | ★ | ★★★ | ★★ | ★★ | ★★ | ★★ |
| **Tesseract + Claude** ⭐ | ★★★★ | ★★★★★ | ★★★ | ★★★★★ | ★★★★★ | ★★★★ | ★★★★★ | **★★★★★** |
| Azure AI Vision | ★★★★★ | ★★★★ | ★★★★★ | ★★★ | ★★★★ | ★★★★ | ★★★ | ★★★★ |
| Mathpix | ★★★★ | ★★★ | ★★ | ★★ | ★★ | ★★ | ★★ | ★★★ |

---

## Sintesi Decisionale

### ✅ Consigliato: Tesseract + Claude API

Vince su ogni dimensione che conta per uno strumento di automazione per singolo utente, una lezione alla volta:

- **Nessun costo ricorrente** — Tesseract è gratuito; Claude API addebita solo ciò che si usa
- **Privacy by default** — i documenti rimangono locali; nessun DPA istituzionale richiesto
- **Pipeline end-to-end** — OCR e strutturazione AI delle note avvengono nello stesso script
- **Zero vendor lock-in** — sostituire il modello AI o il motore OCR in modo indipendente
- **Funziona offline** — Tesseract gira senza internet; solo il passaggio di strutturazione con Claude richiede connessione

### Quando considerare alternative

| Scenario | Scelta migliore |
|----------|-----------------|
| Appunti prevalentemente scritti a mano | Azure AI Vision (migliore accuratezza scrittura a mano) |
| Corsi STEM con molte equazioni | Mathpix (output LaTeX nativo) |
| Scalare a piattaforma multi-utente in futuro | Google Cloud Vision o Azure (infrastruttura gestita, SLA) |
| Uso manuale occasionale, senza programmazione | Adobe Acrobat (interfaccia semplice, nessuna configurazione) |

---

*Generato per valutazione architetturale software — pipeline OCR per strumento di studio studentesco*