[declaratii.integritate.eu](https://declaratii.integritate.eu/) scraper

- `declaratii-integritate.py `- fetches html rows and csvs (Exporta resultate)
- `consolidate_dl_csvs.py` - consolidates dowloaded (Exporta resultate) csvs
- `consolidate-all.py` - consolidates Exported csv w parsed html rows

## Roadmap

big pages wo pagination?
count page turns
max 10k
go for bucuresti, bucuresti si un fel de declaratie
then difference per judet, log errors

- [x] get data from result table
- [x] follow pagination
- [x] loop dates
- [x] log errors
- [ ] log results & meta/ count results
- [x] prevent overwrite (update untill found)
- [ ] scrape from today to the latest logged day
- [ ] split into functions
- [ ] update missing values
    - [ ] break query in parts - date, tip declaratie, judet
- [x] download csvs
  - [ ] rename to target date

- [ ] consolidate declaratii din tabel
- [x] consolidate downloaded csvs
    - [x] remove duplicates
- [x] compare results - between downloaded csvs and scraped table pages / rows 
- [ ] download pdfs
- [ ] parse pdfs

----

### Initial approach

open page
click advanced

    loop (while start_date < earliest_date)
        add dates 
        see if max 10000 - if so previou day log err
        see if none - if so previous range log err

        if resultsTable

        read table (function)
        check if next
            append table
            advance next

        write to csv
        advance days


1. open [declaratii.integritate.eu](https://declaratii.integritate.eu/index.html) 
2. click _'Căutare avansată'_ button (`<a id="form:showAdvancedSearch">`) found here: `<div class="srch_switch"><a href="#" id="form:showAdvancedSearch">Căutare avansată</a><span></span></div>`
3. wait for `<div id="form:advanced-search-panel"> ... <div id="form:advanced-search-panel_content">` to load
4. input current date (ex: 03.10.2023) in this field, also change 'value' parameter accordingly  `<input id="form:endDate_input" name="form:endDate_input" role="textbox" type="text" value="03.10.2023">` 
    input current date - 3 working days (ex: 29.09.2023) in  `<input id="form:startDate_input" name="form:startDate_input" role="textbox" size="10" type="text" value="29.09.2023">` - also change 'value' attribute inside tag
5. click on `<input id="form:submitButtonAS">` inside `<div class="advanced_srch_subm_right"><input class="button" id="form:submitButtonAS" name="form:submitButtonAS" type="submit" value="caută>"><span></span></div>`

<table><thead><tr><th><div>Nume Prenume&nbsp;</div></th><th><div>Institutie&nbsp;</div></th><th><div>Functie&nbsp;</div></th><th><div>Localitate&nbsp;</div></th><th><div>Judet&nbsp;</div></th><th><div>Data completare declaratie&nbsp;</div></th><th><div>Tip declaratie&nbsp;</div></th></tr></thead><tbody><tr><td>GRECU P PETRUȚA AURORA</td><td>Liceul Tehnologic Energetic Dragomir Hurmuzescu Deva</td><td>Director adjunct</td><td>Deva</td><td>Hunedoara</td><td>30.09.2023</td><td>Declaraţie de avere</td></tr><tr><td>DAMIAN D IULIA</td><td>Administratia Nationala Apele Romane - Cod Caen 3600, 3900, 4291, 6203, 7112, 7120, 7219, 8413, 8425, 8559</td><td>Șef birou</td><td>Sectorul 1</td><td>Bucuresti</td><td>02.10.2023</td><td>Declaraţie de avere</td></tr><tr><td>TEODORESCU Gh GEORGETA</td><td>Inspectoratul Scolar Al Judetului Arges</td><td>Inspector scolar</td><td>Pitesti</td><td>Arges</td><td>30.09.2023</td><td>Declaraţie de interese</td></tr><tr><td>Gorcitz V Lucica</td><td>Directia Generala Regionala A Finantelor Publice Brasov</td><td>Inspector</td><td>Targu Mures</td><td>Mures</td><td>02.10.2023</td><td>Declaraţie de avere</td></tr></tbody></table>

-----

## SQL

#### Consolidate CSVs (downloaded and scraped from table)

    SELECT
        COALESCE(d.NumePrenume, t.NumePrenume) AS NumePrenume,
        COALESCE(d.Institutie, t.Institutie) AS Institutie,
        COALESCE(d.Datacompletaredeclaratie, t.Datacompletaredeclaratie) AS Datacompletaredeclaratie,
        COALESCE(d.Tipdeclaratie, t.Tipdeclaratie) AS Tipdeclaratie,
        d.Functie_x,
        d.Localitate_x,
        d.Judet_x,
        d.Functie_y,
        d.Localitate_y,
        d.Judet_y,
        d.Vezideclaratie AS Vezideclaratie_d,
        d."Vezideclaratie.1" AS Vezideclaratie1_d,
        t.Functie AS Functie_t,
        t.Localitate AS Localitate_t,
        t.Judet AS Judet_t,
        t.Vezideclaratie AS Vezideclaratie_t,
        t."Vezideclaratie2" AS Vezideclaratie2_t,
        COALESCE(d.page, t.page) AS page,
        COALESCE(d.rezultate, t.rezultate) AS rezultate,
        COALESCE(d.start_date, t.start_date) AS start_date,
        COALESCE(d.end_date, t.end_date) AS end_date,
        CASE 
            WHEN d.NumePrenume IS NOT NULL AND t.NumePrenume IS NOT NULL THEN 'both'
            WHEN d.NumePrenume IS NOT NULL THEN 'dlcsv'
            ELSE 'tblz'
        END AS merged_status
    FROM dlcsv d
    LEFT JOIN tblz t ON d.NumePrenume = t.NumePrenume
                    AND d.Institutie = t.Institutie
                    AND d.Datacompletaredeclaratie = t.Datacompletaredeclaratie
    UNION ALL
    SELECT
        COALESCE(t.NumePrenume, d.NumePrenume),
        COALESCE(t.Institutie, d.Institutie),
        COALESCE(t.Datacompletaredeclaratie, d.Datacompletaredeclaratie),
        COALESCE(t.Tipdeclaratie, d.Tipdeclaratie),
        d.Functie_x,
        d.Localitate_x,
        d.Judet_x,
        d.Functie_y,
        d.Localitate_y,
        d.Judet_y,
        d.Vezideclaratie,
        d."Vezideclaratie.1",
        t.Functie,
        t.Localitate,
        t.Judet,
        t.Vezideclaratie,
        t."Vezideclaratie2",
        COALESCE(t.page, d.page),
        COALESCE(t.rezultate, d.rezultate),
        COALESCE(t.start_date, d.start_date),
        COALESCE(t.end_date, d.end_date),
        CASE 
            WHEN t.NumePrenume IS NOT NULL AND d.NumePrenume IS NULL THEN 'tblz'
            ELSE 'dlcsv'
        END AS merged_status
    FROM tblz t
    LEFT JOIN dlcsv d ON t.NumePrenume = d.NumePrenume
                    AND t.Institutie = d.Institutie
                    AND t.Datacompletaredeclaratie = d.Datacompletaredeclaratie
    WHERE d.NumePrenume IS NULL;

#### stats

    CREATE VIEW stats1 AS
        SELECT 
        SUBSTR(Datacompletaredeclaratie, 7, 4) AS year,
        SUBSTR(Datacompletaredeclaratie, 4, 2) AS month,
        Institutie,
        COALESCE(Localitate_x, Localitate_t) AS localitate,
        COALESCE(Judet_x, Judet_y, Judet_t) AS judet,
        COUNT(*) AS count
    FROM match_all
    WHERE Institutie IS NOT NULL
    AND Datacompletaredeclaratie IS NOT NULL
    GROUP BY year,
        month,
        Institutie,
        localitate,
        judet
    HAVING count > 0;