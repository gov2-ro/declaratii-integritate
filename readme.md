[declaratii.integritate.eu](https://declaratii.integritate.eu/) 

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


1 - open https://declaratii.integritate.eu/index.html

2 - click 'Căutare avansată' button (<a id="form:showAdvancedSearch">) found here: <div class="srch_switch"><a href="#" id="form:showAdvancedSearch">Căutare avansată</a><span></span></div>

3 - wait for <div id="form:advanced-search-panel"><table><tbody><tr><td><div id="form:advanced-search-panel_content"> to load

4 - input current date (ex: 03.10.2023) in this field, also change 'value' parameter accordingly  <input id="form:endDate_input" name="form:endDate_input" role="textbox" type="text" value="03.10.2023">
    input current date - 3 working days (ex: 29.09.2023) in  <input id="form:startDate_input" name="form:startDate_input" role="textbox" size="10" type="text" value="29.09.2023"> - also change 'value' attribute inside tag

5 - click on <input id="form:submitButtonAS"> inside <div class="advanced_srch_subm_right"><input class="button" id="form:submitButtonAS" name="form:submitButtonAS" type="submit" value="caută>"><span></span></div>

----

<div class="ui-datatable ui-widget" data-elementupdate="form:resultsTable" data-lastreordering="0" id="form:resultsTable" tabindex="0"><div><table><thead id="form:resultsTable_header"><tr><th class="ui-widget-header ui-col-0"><div class="ui-header-column ui-sortable-column clickable" id="form:resultsTable:nume"><span><span class="ui-header-text" id="form:resultsTable:nume_text">Nume Prenume</span></span>&nbsp;<span class="ui-header-right"><span class="ui-sortable-control" id="form:resultsTable:nume_sortControl"><span class="ui-sortable-column-icon"><a class="ui-icon ui-icon-triangle-1-n" id="form:resultsTable:nume_sortControl_up" onclick="ice.setFocus('form:resultsTable:nume_sortControl_up');" tabindex="0" style="opacity: 0.33;"></a><a class="ui-icon ui-icon-triangle-1-s" id="form:resultsTable:nume_sortControl_down" onclick="ice.setFocus('form:resultsTable:nume_sortControl_down');" tabindex="0" style="opacity: 0.33;"></a></span><span class="ui-sortable-column-order"></span></span></span></div></th><th class="ui-widget-header ui-col-1"><div class="ui-header-column ui-sortable-column clickable" id="form:resultsTable:institutie"><span><span class="ui-header-text" id="form:resultsTable:institutie_text">Institutie</span></span>&nbsp;<span class="ui-header-right"><span class="ui-sortable-control" id="form:resultsTable:institutie_sortControl"><span class="ui-sortable-column-icon"><a class="ui-icon ui-icon-triangle-1-n" id="form:resultsTable:institutie_sortControl_up" onclick="ice.setFocus('form:resultsTable:institutie_sortControl_up');" tabindex="0" style="opacity: 0.33;"></a><a class="ui-icon ui-icon-triangle-1-s" id="form:resultsTable:institutie_sortControl_down" onclick="ice.setFocus('form:resultsTable:institutie_sortControl_down');" tabindex="0" style="opacity: 0.33;"></a></span><span class="ui-sortable-column-order"></span></span></span></div></th><th class="ui-widget-header ui-col-2"><div class="ui-header-column ui-sortable-column clickable" id="form:resultsTable:functie"><span><span class="ui-header-text" id="form:resultsTable:functie_text">Functie</span></span>&nbsp;<span class="ui-header-right"><span class="ui-sortable-control" id="form:resultsTable:functie_sortControl"><span class="ui-sortable-column-icon"><a class="ui-icon ui-icon-triangle-1-n" id="form:resultsTable:functie_sortControl_up" onclick="ice.setFocus('form:resultsTable:functie_sortControl_up');" tabindex="0" style="opacity: 0.33;"></a><a class="ui-icon ui-icon-triangle-1-s" id="form:resultsTable:functie_sortControl_down" onclick="ice.setFocus('form:resultsTable:functie_sortControl_down');" tabindex="0" style="opacity: 0.33;"></a></span><span class="ui-sortable-column-order"></span></span></span></div></th><th class="ui-widget-header ui-col-3"><div class="ui-header-column ui-sortable-column clickable" id="form:resultsTable:localitate"><span><span class="ui-header-text" id="form:resultsTable:localitate_text">Localitate</span></span>&nbsp;<span class="ui-header-right"><span class="ui-sortable-control" id="form:resultsTable:localitate_sortControl"><span class="ui-sortable-column-icon"><a class="ui-icon ui-icon-triangle-1-n" id="form:resultsTable:localitate_sortControl_up" onclick="ice.setFocus('form:resultsTable:localitate_sortControl_up');" tabindex="0" style="opacity: 0.33;"></a><a class="ui-icon ui-icon-triangle-1-s" id="form:resultsTable:localitate_sortControl_down" onclick="ice.setFocus('form:resultsTable:localitate_sortControl_down');" tabindex="0" style="opacity: 0.33;"></a></span><span class="ui-sortable-column-order"></span></span></span></div></th><th class="ui-widget-header ui-col-4"><div class="ui-header-column ui-sortable-column clickable" id="form:resultsTable:judet"><span><span class="ui-header-text" id="form:resultsTable:judet_text">Judet</span></span>&nbsp;<span class="ui-header-right"><span class="ui-sortable-control" id="form:resultsTable:judet_sortControl"><span class="ui-sortable-column-icon"><a class="ui-icon ui-icon-triangle-1-n" id="form:resultsTable:judet_sortControl_up" onclick="ice.setFocus('form:resultsTable:judet_sortControl_up');" tabindex="0" style="opacity: 0.33;"></a><a class="ui-icon ui-icon-triangle-1-s" id="form:resultsTable:judet_sortControl_down" onclick="ice.setFocus('form:resultsTable:judet_sortControl_down');" tabindex="0" style="opacity: 0.33;"></a></span><span class="ui-sortable-column-order"></span></span></span></div></th><th class="ui-widget-header ui-col-5"><div class="ui-header-column ui-sortable-column clickable" id="form:resultsTable:dataCompletare"><span><span class="ui-header-text" id="form:resultsTable:dataCompletare_text">Data completare declaratie</span></span>&nbsp;<span class="ui-header-right"><span class="ui-sortable-control" id="form:resultsTable:dataCompletare_sortControl"><span class="ui-sortable-column-icon"><a class="ui-icon ui-icon-triangle-1-n" id="form:resultsTable:dataCompletare_sortControl_up" onclick="ice.setFocus('form:resultsTable:dataCompletare_sortControl_up');" tabindex="0" style="opacity: 0.33;"></a><a class="ui-icon ui-icon-triangle-1-s" id="form:resultsTable:dataCompletare_sortControl_down" onclick="ice.setFocus('form:resultsTable:dataCompletare_sortControl_down');" tabindex="0" style="opacity: 0.33;"></a></span><span class="ui-sortable-column-order"></span></span></span></div></th><th class="ui-widget-header ui-col-6"><div class="ui-header-column ui-sortable-column clickable" id="form:resultsTable:tipDeclaratie"><span><span class="ui-header-text" id="form:resultsTable:tipDeclaratie_text">Tip declaratie</span></span>&nbsp;<span class="ui-header-right"><span class="ui-sortable-control" id="form:resultsTable:tipDeclaratie_sortControl"><span class="ui-sortable-column-icon"><a class="ui-icon ui-icon-triangle-1-n" id="form:resultsTable:tipDeclaratie_sortControl_up" onclick="ice.setFocus('form:resultsTable:tipDeclaratie_sortControl_up');" tabindex="0" style="opacity: 0.33;"></a><a class="ui-icon ui-icon-triangle-1-s" id="form:resultsTable:tipDeclaratie_sortControl_down" onclick="ice.setFocus('form:resultsTable:tipDeclaratie_sortControl_down');" tabindex="0" style="opacity: 0.33;"></a></span><span class="ui-sortable-column-order"></span></span></span></div></th><th class="ui-widget-header ui-col-7"><div class="ui-header-column clickable" id="form:resultsTable:veziDeclaratie"><span><span class="ui-header-text" id="form:resultsTable:veziDeclaratie_text">Vezi declaratie</span></span></div></th><th class="ui-widget-header ui-col-8"><div class="ui-header-column clickable" id="form:resultsTable:shareDeclaratie"><span><span class="ui-header-text" id="form:resultsTable:shareDeclaratie_text">Distribuie</span></span></div></th></tr></thead><tbody class="ui-datatable-data ui-widget-content" id="form:resultsTable_body"><tr class=" ui-datatable-odd  " id="form:resultsTable_row_25" tabindex="0"><td class="null ui-col-0"><span id="form:resultsTable:25:numeCell">GRECU P PETRUȚA AURORA</span></td><td class="null ui-col-1"><span id="form:resultsTable:25:institutieCell">Liceul Tehnologic Energetic Dragomir Hurmuzescu Deva</span></td><td class="null ui-col-2"><span id="form:resultsTable:25:functieCell">Director adjunct</span></td><td class="null ui-col-3"><span id="form:resultsTable:25:localitateCell">Deva</span></td><td class="null ui-col-4"><span id="form:resultsTable:25:judetCell">Hunedoara</span></td><td class="null ui-col-5"><span id="form:resultsTable:25:dataCompletareCell">30.09.2023</span></td><td class="null ui-col-6"><span id="form:resultsTable:25:tipDeclaratieCell">Declaraţie de avere</span></td><td class="null ui-col-7">
<a href="/DownloadServlet?fileName=15080778_2787787_a.pdf&amp;uniqueIdentifier=NTNTARTLNE_15080778" target="_self">Vezi document</a></td><td class="null ui-col-8"><input alt="Distribuie" class="shareButton" id="form:resultsTable:25:shareBtn" name="form:resultsTable:25:shareBtn" onclick="ice.ace.ab({'source':'form:resultsTable:25:shareBtn','execute':'form:resultsTable:25:shareBtn','render':'shareDialog','event':'action'});;return false" type="submit" value="" data-hasqtip="form:resultsTable:25:_t154"><span id="form:resultsTable:25:_t154"></span></td></tr><tr class=" ui-datatable-even  " id="form:resultsTable_row_26" tabindex="0"><td class="null ui-col-0"><span id="form:resultsTable:26:numeCell">DAMIAN D IULIA</span></td><td class="null ui-col-1"><span id="form:resultsTable:26:institutieCell">Administratia Nationala Apele Romane - Cod Caen 3600, 3900, 4291, 6203, 7112, 7120, 7219, 8413, 8425, 8559</span></td><td class="null ui-col-2"><span id="form:resultsTable:26:functieCell">Șef birou</span></td><td class="null ui-col-3"><span id="form:resultsTable:26:localitateCell">Sectorul 1</span></td><td class="null ui-col-4"><span id="form:resultsTable:26:judetCell">Bucuresti</span></td><td class="null ui-col-5"><span id="form:resultsTable:26:dataCompletareCell">02.10.2023</span></td><td class="null ui-col-6"><span id="form:resultsTable:26:tipDeclaratieCell">Declaraţie de avere</span></td><td class="null ui-col-7">
<a href="/DownloadServlet?fileName=15070872_2787968_a.pdf&amp;uniqueIdentifier=NTNTARTLNE_15070872" target="_self">Vezi document</a></td><td class="null ui-col-8"><input alt="Distribuie" class="shareButton" id="form:resultsTable:26:shareBtn" name="form:resultsTable:26:shareBtn" onclick="ice.ace.ab({'source':'form:resultsTable:26:shareBtn','execute':'form:resultsTable:26:shareBtn','render':'shareDialog','event':'action'});;return false" type="submit" value="" data-hasqtip="form:resultsTable:26:_t154"><span id="form:resultsTable:26:_t154"></span></td></tr><tr class=" ui-datatable-even  " id="form:resultsTable_row_48" tabindex="0"><td class="null ui-col-0"><span id="form:resultsTable:48:numeCell">TEODORESCU Gh GEORGETA</span></td><td class="null ui-col-1"><span id="form:resultsTable:48:institutieCell">Inspectoratul Scolar Al Judetului Arges</span></td><td class="null ui-col-2"><span id="form:resultsTable:48:functieCell">Inspector scolar</span></td><td class="null ui-col-3"><span id="form:resultsTable:48:localitateCell">Pitesti</span></td><td class="null ui-col-4"><span id="form:resultsTable:48:judetCell">Arges</span></td><td class="null ui-col-5"><span id="form:resultsTable:48:dataCompletareCell">30.09.2023</span></td><td class="null ui-col-6"><span id="form:resultsTable:48:tipDeclaratieCell">Declaraţie de interese</span></td><td class="null ui-col-7">
<a href="/DownloadServlet?fileName=15080747_2787683_a.pdf&amp;uniqueIdentifier=NTNTARTLNE_15080747" target="_self">Vezi document</a></td><td class="null ui-col-8"><input alt="Distribuie" class="shareButton" id="form:resultsTable:48:shareBtn" name="form:resultsTable:48:shareBtn" onclick="ice.ace.ab({'source':'form:resultsTable:48:shareBtn','execute':'form:resultsTable:48:shareBtn','render':'shareDialog','event':'action'});;return false" type="submit" value="" data-hasqtip="form:resultsTable:48:_t154"><span id="form:resultsTable:48:_t154"></span></td></tr><tr class=" ui-datatable-odd  " id="form:resultsTable_row_49" tabindex="0"><td class="null ui-col-0"><span id="form:resultsTable:49:numeCell">Gorcitz V Lucica</span></td><td class="null ui-col-1"><span id="form:resultsTable:49:institutieCell">Directia Generala Regionala A Finantelor Publice Brasov</span></td><td class="null ui-col-2"><span id="form:resultsTable:49:functieCell">Inspector</span></td><td class="null ui-col-3"><span id="form:resultsTable:49:localitateCell">Targu Mures</span></td><td class="null ui-col-4"><span id="form:resultsTable:49:judetCell">Mures</span></td><td class="null ui-col-5"><span id="form:resultsTable:49:dataCompletareCell">02.10.2023</span></td><td class="null ui-col-6"><span id="form:resultsTable:49:tipDeclaratieCell">Declaraţie de avere</span></td><td class="null ui-col-7">
<a href="/DownloadServlet?fileName=15080746_2787919_a.pdf&amp;uniqueIdentifier=NTNTARTLNE_15080746" target="_self">Vezi document</a></td><td class="null ui-col-8"><input alt="Distribuie" class="shareButton" id="form:resultsTable:49:shareBtn" name="form:resultsTable:49:shareBtn" onclick="ice.ace.ab({'source':'form:resultsTable:49:shareBtn','execute':'form:resultsTable:49:shareBtn','render':'shareDialog','event':'action'});;return false" type="submit" value="" data-hasqtip="form:resultsTable:49:_t154"><span id="form:resultsTable:49:_t154"></span></td></tr></tbody></table></div><div class="ui-paginator ui-paginator-bottom ui-widget-header" id="form:resultsTable_paginatorbottom" style="width: 869px;"><span><a href="#" id="form:resultsTable_paginatorbottom_firstPageLink" class="ui-paginator-first ui-state-default ui-corner-all" onclick="ice.setFocus('form:resultsTable_paginatorbottom_firstPageLink');" onkeydown="var e = event || window.event; if (e.keyCode == 32 || e.keyCode == 13) { this.click();return false; }" tabindex="0" title="First" aria-label="First" style="vertical-align:middle;"><span class="ui-icon ui-icon-seek-first"></span></a> <a href="#" id="form:resultsTable_paginatorbottom_previousPageLink" class="ui-paginator-previous ui-state-default ui-corner-all" onclick="ice.setFocus('form:resultsTable_paginatorbottom_previousPageLink');" onkeydown="var e = event || window.event; if (e.keyCode == 32 || e.keyCode == 13) { this.click();return false; }" tabindex="0" title="Prev" aria-label="Prev" style="vertical-align:middle;"><span class="ui-icon ui-icon-triangle-1-w"></span></a> <span class="ui-paginator-pages"><a href="#" class="ui-paginator-page ui-state-default ui-corner-all" onclick="ice.setFocus('form:resultsTable_paginatorbottom_current_page');" onkeydown="var e = event || window.event; if (e.keyCode == 32 || e.keyCode == 13) { this.click();return false; }" tabindex="0">1</a><a href="#" onclick="this.focus();" class="ui-paginator-page ui-state-default ui-corner-all ui-paginator-current-page ui-state-active" style="cursor: default;" id="form:resultsTable_paginatorbottom_current_page" onkeydown="var e = event || window.event; if (e.keyCode == 32 || e.keyCode == 13) { this.click();return false; }" tabindex="0">2</a><a href="#" class="ui-paginator-page ui-state-default ui-corner-all" onclick="ice.setFocus('form:resultsTable_paginatorbottom_current_page');" onkeydown="var e = event || window.event; if (e.keyCode == 32 || e.keyCode == 13) { this.click();return false; }" tabindex="0">3</a><a href="#" class="ui-paginator-page ui-state-default ui-corner-all" onclick="ice.setFocus('form:resultsTable_paginatorbottom_current_page');" onkeydown="var e = event || window.event; if (e.keyCode == 32 || e.keyCode == 13) { this.click();return false; }" tabindex="0">4</a></span> <a href="#" id="form:resultsTable_paginatorbottom_nextPageLink" class="ui-paginator-next ui-state-default ui-corner-all" onclick="ice.setFocus('form:resultsTable_paginatorbottom_nextPageLink');" onkeydown="var e = event || window.event; if (e.keyCode == 32 || e.keyCode == 13) { this.click();return false; }" tabindex="0" title="Next" aria-label="Next" style="vertical-align:middle;"><span class="ui-icon ui-icon-triangle-1-e"></span></a> <a href="#" id="form:resultsTable_paginatorbottom_lastPageLink" class="ui-paginator-last ui-state-default ui-corner-all" onclick="ice.setFocus('form:resultsTable_paginatorbottom_lastPageLink');" onkeydown="var e = event || window.event; if (e.keyCode == 32 || e.keyCode == 13) { this.click();return false; }" tabindex="0" title="Last" aria-label="Last" style="vertical-align:middle;"><span class="ui-icon ui-icon-seek-end"></span></a></span></div><span id="form:resultsTable_setup"></span><span style="display:none;">false null [0, 1, 2, 3, 4, 5, 6, 7, 8]</span></div>

![search](docs/screenshots/ani-search.png)

![results](docs/screenshots/ani-results.png)


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