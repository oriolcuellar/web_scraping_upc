from selenium import webdriver

import time
import random
import os

import urllib3
import requests


#importación de libreria para utilizar el motor de navegación web (descargar)
import mechanize
import webbrowser


#datos.....................................................................................................
usuario=""
contraseña=""
pag_web="https://upcommons.upc.edu/handle/2117/134982"
carrera="INFORMATICA"

#datos.....................................................................................................
#manejo de documentos no descargados
errores=""
cont_errores=0
#manejo directorios
ruta=os.path.dirname(os.path.abspath(__file__))
try:
    print("creando carpetas")
    os.mkdir(carrera)
except:
    print ("ya estaban creadas")
ruta=ruta+"/"+carrera

#abrir ventana
print("abriendo pag web")
driver = webdriver.Firefox( )
driver.get(pag_web)

#crear tabla de assiganturas
tabla=driver.find_elements_by_tag_name("tr")
print(len(tabla), "assignaturas")
links=[]
assignaturas=[]
for casilla in tabla:#creamos tabla de links assignaturas y nombres de assiganuras
    text=casilla.find_element_by_tag_name("a").get_attribute("href")
    links.append(text)
    text=casilla.find_element_by_tag_name("a").text
    text=text.replace("/", "-")
    assignaturas.append(text)
i=""
contador_as=0
for i in links:#recorro asignaturas
    print("\n", contador_as+1, "/", len(assignaturas), "assignaturas")
    print("ASSIGNATURA: ",assignaturas[contador_as] )#manejo contador
    try:
        os.mkdir(ruta+"/"+assignaturas[contador_as])
    except:
        print("")
    fichero=""
    fichero=assignaturas[contador_as]
    contador_as=contador_as+1

    driver.get(i)#ventana va a la assignatura
    tabla=driver.find_element_by_id("aspect_discovery_SimpleSearch_div_search-results")
    cerca=tabla.find_elements_by_tag_name("h4")
    tabla=[este.find_element_by_tag_name("a") for este in cerca]#creamos tabla de assignaturas (links)

    examenes_nombre=[]#tabla de nombres de examen (para crear carpetas)
    for examen_nombre in tabla:
        text=examen_nombre.text
        text=text.replace("/","-")
        text=text.replace(":","")
        text=text.replace("?","")
        text=text.replace("¿","")
        examenes_nombre.append(text)
    tabla=[examen.get_attribute("href") for examen in tabla]

    print (len(tabla), "examenes")
    contador_ex=0
    for examen in tabla:#recorro examenes
        print(examenes_nombre[contador_ex])#manejo contador
        contador_ex=contador_ex+1
        
        driver.get(examen)#ventana va a pagina del examen
        error=False
        try: #clicamos en abrir examen
            driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/div/div[1]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/a").click()
        except: #repito (por si no ha cargado pagina)
            driver.sleep(3)
            try:
                driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/div/div[1]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/a").click()
            except:
                error=True
        if error==False:    
            #entra si ha podido entrar a el examen
            if driver.current_url=="https://sso.upc.edu/CAS/login?service=https://upcommons.upc.edu/cas-login": #inicia sesion si nos manda a pag de iniciar sesion
                driver.find_element_by_id("formulario1").find_element_by_id("edit-name").send_keys(usuario)
                driver.find_element_by_id("formulario1").find_element_by_id("edit-pass").send_keys(contraseña)
                driver.find_element_by_id("formulario1").find_element_by_id("submit_ok").click()
            url=driver.current_url
            try:#hacemos inicio de sesion antes de descargar
                try:#a veces no hay que iniciar sesion
                    #conexion y validacion
                    browser = mechanize.Browser() 
                    browser.set_handle_robots(False)   
                    browser.open("https://sso.upc.edu/CAS/login?service=https://upcommons.upc.edu/cas-login")
                    #iniciar sesion
                    browser.select_form(name="formulario1") 
                    browser["adAS_username"] = usuario
                    browser["adAS_password"] = contraseña
                    #Ejecución del código y envío de la información 
                    response = browser.submit()
                except:
                    error=False
                #descarga del archivo
                browser.retrieve(url,ruta+"/"+fichero+"/"+examenes_nombre[contador_ex-1]+".pdf")[0]
            except:
                print( "no puedo descargar "+str(cont_errores))
                errores=errores+"\n"+"assignatura: "+ fichero+"\n"+"examen: "+examenes_nombre[contador_ex-1]
                cont_errores=cont_errores+1
        else:
            print( "no puedo descargar ",cont_errores)
            errores=errores+"\n"+"assignatura: "+ fichero+"\n"+"examen: "+examenes_nombre[contador_ex-1]
            cont_errores=cont_errores+1
texto="\n"+"ESTOS SON LOS ERRORES "+str(cont_errores)+"\n"+errores
documento=open(ruta+"/ERRORES.txt", "w")
documento.write(texto)
documento.close()
