# web_scraping_upc
descarga todos los examenes de una carrera

acciones necesarias:

descargar geckodriver (para linux, version linux) (para windows, version windows)
https://github.com/mozilla/geckodriver/releases
necitas usuario y contraseña de upc
en la variable pag_web introduce un string con la pagina web de la carrera
ej:  "https://upcommons.upc.edu/handle/2117/134982"
todas las librerias y el geckodriver.exe sin comprimir deben estar en la carpeta donde se ejecuta el main.py

escrito en python
librerias:
  selenium
  urllib3
  requests
  mechanize
  webbrowser
  
contiene un zip con las librerias
quiza debe añadir un addon el firefox (selenium)
