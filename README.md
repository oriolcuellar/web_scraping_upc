# web_scraping_upc

    descarga todos los examenes de una carrera UPC (bibliotecnica)
 
# acciones necesarias:

  todas las librerias y el geckodriver.exe sin comprimir deben estar en la carpeta donde se ejecuta el main.py
  
### Config

    - Necitas usuario y contraseña de upc
      en la variable pag_web introduce un string con la pagina web de la carrera
      ej:  "https://upcommons.upc.edu/handle/2117/134982"
      
### Geckodriver
    - descargar geckodriver (para linux, version linux) (para windows, version windows)
      https://github.com/mozilla/geckodriver/releases
     
### Librerias:

 contiene un zip con las librerias
 
    selenium
    urllib3
    requests
    mechanize
    webbrowser
    html5lib (falta en zip)
  
### Addon

    Se debe añadir un addon el firefox (selenium)
