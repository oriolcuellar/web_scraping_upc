from selenium import webdriver

import time
import random
import os

import urllib3
import requests
import html5lib

#importación de libreria para utilizar el motor de navegación web (descargar)
import mechanize
import webbrowser
def datos():
    #datos.....................................................................................................
    global usuario
    usuario=""
    global contraseña
    contraseña=""
    global pag_web
    pag_web="https://upcommons.upc.edu/handle/2117/134992"  #donde estan las assignaturas
    global carrera
    carrera="FIB" #nombre de la carpeta

def variables():
    global link_as
    link_as=""
    global contador_as 
    contador_as=0

def carpetas():
    #manejo de documentos no descargados
    global errores
    errores=""
    global cont_errores
    cont_errores=0
    #manejo directorios
    global ruta
    ruta=os.path.dirname(os.path.abspath(__file__))
    try:
        print("creando carpetas")
        os.mkdir(carrera)
    except:
        print ("ya estaban creadas")
    ruta=ruta+"/"+carrera
    print("abriendo pag web")
    global start
    start=time.time()


def busca_asignaturas():
    #crear tabla de assiganturas
    global tabla
    tabla=driver.find_elements_by_tag_name("tr")
    print(len(tabla), "assignaturas")
    global links
    links=[]
    global assignaturas
    assignaturas=[]
    for casilla in tabla:#creamos tabla de links assignaturas y nombres de assiganuras
        text=casilla.find_element_by_tag_name("a").get_attribute("href")
        links.append(text)
        text=casilla.find_element_by_tag_name("a").text
        text=text.replace("/", "-")
        assignaturas.append(text)


def busca_examenes():
    global contador_as
    global driver
    print("\n", contador_as +1 , "/", len(assignaturas), "assignaturas")
    print("ASSIGNATURA: ",assignaturas[contador_as] )#manejo contador
    ruta_as=os.path.dirname(os.path.abspath(__file__))
    ruta_as=ruta_as+"/"+carrera+"/"+assignaturas[contador_as]
    if os.path.isdir(ruta_as): 
        print("ASSIGNATURA: ",assignaturas[contador_as], " ya estaba descargada" )#manejo ya descargados
        contador_as=contador_as+1
        return False
    os.mkdir(ruta+"/"+assignaturas[contador_as])
    global fichero
    fichero=""
    fichero=assignaturas[contador_as]
    contador_as=contador_as+1
    driver.get(link_as)#ventana va a la assignatura
    global tabla
    try:
        tabla=driver.find_element_by_id("aspect_discovery_SimpleSearch_div_search-results")
    except:
        time.sleep(2)
        tabla=driver.find_element_by_id("aspect_discovery_SimpleSearch_div_search-results")
    cerca=tabla.find_elements_by_tag_name("h4")
    tabla=[este.find_element_by_tag_name("a") for este in cerca]#creamos tabla de assignaturas (links)
    global examenes_nombre
    examenes_nombre=[]#tabla de nombres de examen (para crear carpetas)
    for examen_nombre in tabla:
        text=examen_nombre.text
        text=text.replace("/","-")
        text=text.replace(":","")
        text=text.replace("?","")
        text=text.replace("¿","")
        text=text.replace("*","")
        examenes_nombre.append(text)
    tabla=[examen.get_attribute("href") for examen in tabla]
    print (len(tabla), "examenes")
    global contador_ex
    contador_ex=0
    return True
def preparar():
        global driver
        global contador_ex
        global examenes_nombre
        global fecha
        driver.get(examen)#ventana va a pagina del examen
        contador_ex=contador_ex+1
        intento=0
        while intento<3:
            try:
                fecha0=driver.find_element_by_class_name("simple-item-view-date")
                fecha0=fecha0.text
                fecha=""
                do=False
                for letra in fecha0:
                    if letra=="2":
                        do=True
                    if do==True:
                        fecha=fecha+letra
                fecha=fecha.replace("/","-")
                intento=3
            except:
                intento=intento+1
                time.sleep(1)
        print(examenes_nombre[contador_ex-1]+fecha)#manejo contador
def descargamos():
        global fecha
        global driver  
        global errores
        global cont_errores      
        error=False
        try: #clicamos en abrir examen
            driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/div/div[1]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/a").click()
        except: #repito (por si no ha cargado pagina)
            time.sleep(3)
            try:
                driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/div/div[1]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/a").click()
            except:
                try:
                    time.sleep(2)
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
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
                browser.retrieve(url,ruta+"/"+fichero+"/"+examenes_nombre[contador_ex-1]+fecha+" "+str(contador_ex-1)+".pdf")[0]
            except:
                print( "no puedo descargar "+str(cont_errores))
                errores=errores+"\n"+"assignatura: "+ fichero+"\n"+"examen: "+examenes_nombre[contador_ex-1]
                cont_errores=cont_errores+1
        else:
            print( "no puedo descargar ",cont_errores)
            errores=errores+"\n"+"assignatura: "+ fichero+"\n"+"examen: "+examenes_nombre[contador_ex-1]+fecha+" "+str(contador_ex-1)
            cont_errores=cont_errores+1

def cerrar():
    global start
    global cont_errores
    global errores
    global texto
    global ruta
    global driver
    finish=time.time()
    texto="\n"+"tiempo total: "+str((finish-start)/60)+" minutos "+"\n"+"ESTOS SON LOS ERRORES "+str(cont_errores)+"\n"+errores
    documento=open(ruta+"/ERRORES.txt", "w")
    documento.write(texto)
    documento.close()
    driver.close()

# MAIN ...............................................................................
variables()
datos()
carpetas()


driver = webdriver.Firefox()
driver.get(pag_web)

busca_asignaturas()

for link_as in links:#recorro asignaturas
    descargo=busca_examenes()
    if descargo:
        for examen in tabla:#recorro examenes       
            preparar()
            descargamos()

cerrar()

# MAIN ...............................................................................
