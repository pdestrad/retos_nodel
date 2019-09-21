from pyquery import PyQuery as pq
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import urllib.parse
import gspread

pagina = 1
url = "https://www.cinecalidad.to"
categorias = ["/peliculas/4k-ultra-hd","/genero-peliculas/accion","/genero-peliculas/infantil","/genero-peliculas/comedia","/genero-peliculas/terror","/genero-peliculas/ciencia-ficcion","/genero-peliculas/aventura","/genero-peliculas/suspenso","/genero-peliculas/romance","/genero-peliculas/fantasia"]
peliculas = []

##  Retorna parametro para ordenar lista
def getParam(elem):
    return elem[2]

##  Retorna el link de descarga segun el servicio
def getLink(data, key, titulo):
    codigo = ""
    titulo = urllib.parse.quote(titulo, safe="")
    if data:
        data = data.split(" ")
        data_int = []
        for d in data:
            data_int.append(int(d) - 2)
        codigo += "".join(map(chr, data_int))       
    else:
        return None

    video_urls = {
        "OnlineUpToBox" : "https://uptobox.com/" + codigo,
        "OnlineYourUpload" : "https://www.yourupload.com/watch/" + codigo,
        "TheVideoMe" : "https://thevideo.me/" + codigo,
        "Vevio" : "https://vev.io/" + codigo,
        "OnlineFilesCDN" : "https://filescdn.com/" + codigo,
        "OnlineGD" : "/protect/gdredirect.php?l=" + codigo,
        "OnlineUsersCloud" : "https://userscloud.com/" + codigo,
        "OnlineUsersFiles" : "https://usersfiles.com/" + codigo,
        "OnlineOkRu" : "https://ok.ru/video/" + codigo,
        "OnlineOpenload" : "https://openload.co/f/" + codigo,
        "OnlineStreamango" : "https://streamango.com/f/" + codigo,
        "OnlineRapidVideo" : "https://www.rapidvideo.com/v/" + codigo,
        "OnlineMega" : "https://mega.nz/#!" + codigo,
        "UploadedTo" : "http://uploaded.net/file/" + codigo,
        "TurboBit" : "https://turbobit.net/" + codigo + ".html",
        "1fichier" : "https://1fichier.com/?" + codigo + "&af=2942360",
        "OnlineFembed" : "https://www.fembeder.com/f/" + codigo,
        "OnlineVerystream" : "https://verystream.com/stream/" + codigo,
        "OnlineGounlimited" : "https://gounlimited.to/" + codigo,
        "OnlineClipwatching" : "https://clipwatching.com/" + codigo,
        "OnlineVidcloud" : "https://vidcloud.co/v/" + codigo,
        "OnlineVidoza" : "https://vidoza.net/" + codigo + ".html",
        "OnlineNetu" : "https://netu.tv/watch_video.php?v=" + codigo,
        "Mega" : "https://www.cinecalidad.to/protect/v.php?i=" + codigo + "&title=" + titulo,
        "MediaFire" : "https://www.cinecalidad.to/protect/v.php?i=" + codigo + "&title=" + titulo
    }
    return video_urls.get(key,None)

##  Obtener informacion de la pagina y almacenarna en una lista
for index, categoria in enumerate(categorias):
    print("CATEGORIA: " + categoria)
    pagina = 1
    paquete = []
    while(True):
        try:
            d = pq(url=url + categoria + "/page/" + str(pagina))
            peliculas_por_pagina = d(".home_post_cont")
            hilos = list()
            divs = []
            i = 0
            for div in peliculas_por_pagina:
                ##  Creando objeto div pyquery 
                div_obj = pq(div)

                ##  Obteniendo objeto 'a' e 'img' donde esta la referencia al link de la pelicula
                a = pq(div_obj("a"))
                referencia_pelicula = a.attr("href")
                d_ = pq(url=referencia_pelicula)

                ## Verificando si la pelicula tiene ranking
                ranking = d_("#imdb-box > a") ## Objeto pyquery
                ranking = pq(ranking).html() ## String
                if ranking:
                    ranking = ranking.split("/")[0]

                if ranking:
                    ##  Objeto pyquery
                    titulo = d_(".single_left > h1")
                    descripcion = d_("table tr td p")
                    link = d_("#panel_descarga .link")

                    ## Strings
                    titulo = pq(titulo).html()
                    link = getLink(pq(link).attr("data"), pq(link).attr("service"), titulo)

                    ##  Parseando links en descripcion
                    a = pq(pq(descripcion)[0])("a")
                    descripcion = pq(pq(descripcion)[0]).html()
                    for i in a:
                        descripcion = descripcion.replace(pq(i).outerHtml(), "@" + pq(i).html())
                    ##  Quitando caracteres indeseados
                    descripcion = descripcion.replace("<br/>", "")
                    descripcion = descripcion.replace("@", "")

                    paquete.append([titulo, descripcion, ranking, link])   
        except Exception as e:
            break
        finally: 
            pagina += 1

    peliculas.append(paquete)


##  Ordenando la lista con el top50 y escribiendola en texto leible 
peliculas_array_spreadsheet = []
f= open("reto1.txt","w+")
for i in range(0,len(peliculas)):
    top = peliculas[i][:50]
    top_ordenado = sorted(top, reverse=True, key=getParam)
    categoria = categorias[i].split("/")[-1]
    f.write("***    %s    ****\n" % categoria)
    for index, p in enumerate(top_ordenado):
        ##  Guardando datos en array para escritura en spreadsheet
        peliculas_array_spreadsheet.append([index+1,categoria,p[0],p[1],p[2],p[3]])
        f.write('#{}\nTitulo: {}\nDesc: {}\nRank: {}\nLink: {}\n\n'.format(index+1,p[0],p[1],p[2],p[3]))
    f.write("\n\n\n")
f.close()


##  Guardando data en spreadsheet para el reto 4
data_id = "1K9Sz7aBS3eB7vUNxnupcuZTOFEeTb8xvVv1-LPQUpsU"
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
service = build('sheets', 'v4', credentials=creds)

body = {
    'values': peliculas_array_spreadsheet
}
result = service.spreadsheets().values().update(
    spreadsheetId=data_id, range="Hoja 1",
    valueInputOption="RAW", body=body).execute()
print('{0} cells updated.'.format(result.get('updatedCells')))















