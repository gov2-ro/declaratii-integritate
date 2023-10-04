[declaratii.integritate.eu](https://declaratii.integritate.eu/) 

- [ ] get list of declaratii 
- [ ] download pdfs
- [ ] extract data from pdfs

PROMPT: 
start from today, each 4 days
02.10.2023 DD.MM.YYYY





### error: 
Căutarea &#238;ntoarce mai mult de 10 000 de rezultate. Vă rugăm să mai rafinați termenii de căutare
<form action="/index.html" enctype="application/x-www-form-urlencoded" id="errorForm" method="post" name="errorForm">

### no results
<table><tr><td><div class="ui-panel-content ui-widget-content" id="form:j_idt142_content"><h5>Nu s-au găsit rezultate</h5>


## sample curl, emulate with selenium

python emulate the following curl
instead of endDate_input=04.10.2023 use current date, 
instead of startDate_input=29.09.2023 use current date - 4 working days (skip weekends)
curl 'https://declaratii.integritate.eu/index.html' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-GB,en;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Content-type: application/x-www-form-urlencoded;charset=UTF-8' \
  -H 'Cookie: JSESSIONID=A462FCD7C5BD612529E850BFCF8F7BC9' \
  -H 'Faces-Request: partial/ajax' \
  -H 'Origin: https://declaratii.integritate.eu' \
  -H 'Referer: https://declaratii.integritate.eu/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-GPC: 1' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw 'form=form&ice.window=m2lnbnelb0&ice.view=vnvzv1alta1%3A0&form%3ANumePrenume_input=&form%3AautoComplete_input=&form%3AFnc_input=&form%3AstartDate_input=29.09.2023&form%3AendDate_input=04.10.2023&form%3AJudet_input=-1&form%3ALocalitate_input=-1&form%3ATip_input=-1&advancedAction=&javax.faces.ViewState=7509137171488588252%3A-1271403620584155180&javax.faces.ClientWindow=m2lnbnelb0&javax.faces.source=form%3AsubmitButtonAS&javax.faces.partial.execute=%40all&javax.faces.partial.render=%40all&ice.window=m2lnbnelb0&ice.view=vnvzv1alta1%3A0&ice.focus=form%3AsubmitButtonAS&form%3AsubmitButtonAS=caut%C4%83%3E&ice.event.target=form%3AsubmitButtonAS&ice.event.captured=form%3AsubmitButtonAS&ice.event.type=onclick&ice.event.alt=false&ice.event.ctrl=false&ice.event.shift=false&ice.event.meta=false&ice.event.x=943&ice.event.y=946&ice.event.left=true&ice.event.right=false&javax.faces.behavior.event=click&javax.faces.partial.event=click&javax.faces.partial.ajax=true' \
  --compressed