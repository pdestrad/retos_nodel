# Retos Nodel
## NOTA: Crear un virtual enviroment con requirements.txt adjuntado

## Reto 1
En el directorio "Reto1" esta el archivo de python (python3.7) en donde a través de pyquery hace queries a la pagina web para 
extaer la data. 
En el mismo directorio hay un archivo reto1.txt en donde esta escrita toda la información extraída en formato legible.
En este script también se reservo un espacio para guardar esta data en un spreadsheet para usarlo después en el Reto4.
Para ejecutar: python3.7 reto1.py

## Reto 2
El el directorio "Reto2" esta el archivo de python (python3.7) que lee el archivo tweet_page.html para extraer la data y presentarla
en formato legible a través del archivo reto2.txt
Para completar este ejercicio primero se necesita entrar al url del tweet y descargar el source code de la pagina web de Twitter, y guardar el archivo en el mismo directorio del script de python.
Para ejecutar: python3.7 reto2.py

## Reto 3
El el directorio "Reto3" esta el archivo de python (python3.7) que lee el archivo amazon.cvs para extraer la data y presentarla en formato legible a través del archivo reto3.txt
Para completar este ejercicio primero se necesita extraer el archivo .cvs con cualquier herramienta de scrapping, en este caso se utilizo la extensión de Google Chrome "Web Scraper". Una vez descargado el archivo .cvs guardar el archivo en el mismo directorio del script de python.
Para ejecutar: python3.7 reto3.py

## Reto 4
El el directorio "Reto3" esta el archivo de python (python3.7) que lee un spreadsheet elaborado en el script del Reto 1, con esta data el script escribe la información en la url: https://docs.google.com/spreadsheets/d/1dSBiCy_I7MCkJlON7A1dGEKuty5hTW_osH408fPv3uU/edit#gid=0
Donde la "Hoja 1" corresponde a la agrupación por Categoria, la "Hoja 2" corresponde a la agrupación por Ranking, y la hoja "Graficos" corresponde a una serie de gráficos.
Para ejecutar: python3.7 reto4.py

### Nota: Si se desea cambiar el spreadsheet de destino, asegurarse que este compartido al correo de credentials.json o que este sin restricciones para editar. Además, es necesario que el spreadsheet tenga 3 hojas o sheets, la primera llamada "Hoja 1", la segunda "Hoja 2" y la tercera "Graficos". Y por último, copiar el sheetId de "Hoja 2" y "Graficos" y pegarlos en la linea 10 y 11 (respectivamente) del script de python
