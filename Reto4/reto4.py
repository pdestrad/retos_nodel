import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

##  Id de spreadsheets
data_id = "1K9Sz7aBS3eB7vUNxnupcuZTOFEeTb8xvVv1-LPQUpsU"
resultado_id = "1dSBiCy_I7MCkJlON7A1dGEKuty5hTW_osH408fPv3uU"

##  Id de sheets
ranking_sheet_id = 1421982431
graficos_sheet_id = 1207775974

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
service = build('sheets', 'v4', credentials=creds)


##############################################################
##                      POR CATERGORIAS
##############################################################
def separarPorCategoria():
    ##  Leyendo data spreadsheet
    result = service.spreadsheets().values().get(
        spreadsheetId=data_id, range="Hoja 1").execute()
    rows = result.get('values', [])

    ##  Separando por categorias y obtener el ranking para grafica
    categorias = {}
    ranking_categorias = {}
    for r in rows:
        categoria = r[1]
        ##  Para categorias
        if categoria in categorias:
            categorias[categoria].append(r)
        else:
            categorias[categoria] = [r]
            ranking_categorias[categoria] = {}


    ##  Creando array para escribir datos en spreadsheet 
    data = []
    for index, categoria in enumerate(categorias):
        data.append([categoria.capitalize()])
        data.append(["Posición","Título","Descripción","Ranking","Link Descarga"])
        for row in categorias[categoria]:
            del row[1]
            data.append(row)
            ranking = str(int(float(row[3])))
            if ranking in ranking_categorias[categoria]:
                ranking_categorias[categoria][ranking] += 1
            else:
                ranking_categorias[categoria][ranking] = 1
        data.append([])
        data.append([])
    body = {
        'values': data
    }
    ##  Escribiendo data en el spreadsheet
    result = service.spreadsheets().values().update(
        spreadsheetId=resultado_id, range="Hoja 1",
        valueInputOption="RAW", body=body).execute()

    ##  Escribiendo data para la grafica en el spreadsheet
    contador = 1
    for categoria in ranking_categorias:
        valores = [["Categoria: " + categoria.capitalize()],["Ranking", "Cantidad"]]
        ##  Creando rango dinamico
        rango = "Graficos!A" + str(contador) + ":B" + str(contador + len(ranking_categorias[categoria]) + 1)
        for ranking in ranking_categorias[categoria]:
            valores.append([str(ranking) + " Estrellas", ranking_categorias[categoria][ranking]])

        body = {
            'values': valores
        }
        result = service.spreadsheets().values().update(
        spreadsheetId=resultado_id, range=rango,
        valueInputOption="RAW", body=body).execute()

        cantidad_elementos_r = len(ranking_categorias[categoria])
        contador += cantidad_elementos_r + 20


    ##  Configurando estilo de spreadsheet Hoja 1
    requests = {
        "requests" : []
    }
    contador = 0
    for categoria in categorias:
        requests["requests"].append({
            "repeatCell" : {
                "range" : {
                    "sheetId" : 0,
                    "startRowIndex" : contador,
                    "endRowIndex" : contador + 2
                },
                "cell" : {
                    "userEnteredFormat" : {
                        "textFormat" : {
                            "bold" : True,
                            "fontSize": 14,
                        },
                        "horizontalAlignment" : "CENTER"
                    }
                },
                "fields": "userEnteredFormat(textFormat,horizontalAlignment)"
            }
        })
        requests["requests"].append({
            "mergeCells": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex" : contador,
                    "endRowIndex" : contador + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 5
                },
                "mergeType": "MERGE_ALL"
            }
        })
        requests["requests"].append({
            "repeatCell" : {
                "range" : {
                    "sheetId" : 0,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell" : {
                    "userEnteredFormat" : {
                        "horizontalAlignment" : "CENTER"
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })
        requests["requests"].append({
            "repeatCell" : {
                "range" : {
                    "sheetId" : 0,
                    "startColumnIndex": 3,
                    "endColumnIndex": 4
                },
                "cell" : {
                    "userEnteredFormat" : {
                        "horizontalAlignment" : "CENTER"
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })
        requests["requests"].append({
            "repeatCell" : {
                "range" : {
                    "sheetId" : 0,
                    "startRowIndex" : contador + 2,
                    "endRowIndex" : contador + len(categorias[categoria]) + 2
                },
                "cell" : {
                    "userEnteredFormat" : {
                        "verticalAlignment" : "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(verticalAlignment)"
            }
        })
        requests["requests"].append({
            "repeatCell" : {
                "range" : {
                    "sheetId" : 0,
                    "startRowIndex" : contador + 2,
                    "endRowIndex" : contador + len(categorias[categoria]) + 2,
                    "startColumnIndex" : 2,
                    "endColumnIndex" : 3
                },
                "cell" : {
                    "userEnteredFormat" : {
                        "wrapStrategy" : "LEGACY_WRAP"
                    }
                },
                "fields": "userEnteredFormat(wrapStrategy)"
            }
        })
        requests["requests"].append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": 0,
                    "dimension": "COLUMNS",
                    "startIndex": 1,
                    "endIndex": 3
                },
                "properties": {
                    "pixelSize": 350
                },
                "fields": "pixelSize"
            }
        })
        requests["requests"].append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": 0,
                    "dimension": "COLUMNS",
                    "startIndex": 4,
                    "endIndex": 5
                },
                "properties": {
                    "pixelSize": 250
                },
                "fields": "pixelSize"
            }
        })
        requests["requests"].append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": 0,
                    "dimension": "ROWS",
                    "startIndex": contador + 2,
                    "endIndex": contador + len(categorias[categoria]) + 2
                },
                "properties": {
                    "pixelSize": 90
                },
                "fields": "pixelSize"
            }
        })
        contador += len(categorias[categoria]) + 4
    service.spreadsheets().batchUpdate(spreadsheetId=resultado_id, body=requests).execute()

    ##  Configurando estilo de spreadsheet Graficos
    requests = {
        "requests" : []
    }
    contador = 0
    for categoria in categorias:
        requests["requests"].append({
            "repeatCell" : {
                "range" : {
                    "sheetId" : graficos_sheet_id,
                    "startRowIndex" : contador,
                    "endRowIndex" : contador + 2
                },
                "cell" : {
                    "userEnteredFormat" : {
                        "textFormat" : {
                            "bold" : True,
                            "fontSize": 14,
                        },
                        "horizontalAlignment" : "CENTER"
                    }
                },
                "fields": "userEnteredFormat(textFormat,horizontalAlignment)"
            }
        })
        requests["requests"].append({
            "mergeCells": {
                "range": {
                    "sheetId" : graficos_sheet_id,
                    "startRowIndex" : contador,
                    "endRowIndex" : contador + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2
                },
                "mergeType": "MERGE_ALL"
            }
        })
        requests["requests"].append({
            "repeatCell" : {
                "range" : {
                    "sheetId" : graficos_sheet_id,
                    "startRowIndex" : contador + 2,
                    "endRowIndex" : contador + 2 + len(ranking_categorias[categoria])
                },
                "cell" : {
                    "userEnteredFormat" : {
                        "horizontalAlignment" : "CENTER"
                    }
                },
                "fields": "userEnteredFormat(textFormat,horizontalAlignment)"
            }
        })
        requests["requests"].append({
            "addChart": {
                "chart": {
                    "spec": {
                        "title": "Rankings de Categoria: " + categoria.capitalize(),
                        "pieChart": {
                            "legendPosition": "RIGHT_LEGEND",
                            "threeDimensional": True,
                            "domain": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": graficos_sheet_id,
                                            "startRowIndex": contador + 2,
                                            "endRowIndex": contador + len(ranking_categorias[categoria]) + 2,
                                            "startColumnIndex": 0,
                                            "endColumnIndex": 1
                                        }
                                    ]
                                }
                            },
                            "series": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": graficos_sheet_id,
                                            "startRowIndex": contador + 2,
                                            "endRowIndex": contador + len(ranking_categorias[categoria]) + 2,
                                            "startColumnIndex": 1,
                                            "endColumnIndex": 2
                                        }
                                    ]
                                }
                            },
                        }
                    },
                    "position": {
                        "overlayPosition": {
                            "anchorCell": {
                                "sheetId": graficos_sheet_id,
                                "rowIndex": contador + 1,
                                "columnIndex": 4
                            }
                        }
                    }
                }
            }
        })
        contador += len(ranking_categorias[categoria]) + 20
    service.spreadsheets().batchUpdate(spreadsheetId=resultado_id, body=requests).execute()

##############################################################
##                      POR CATERGORIAS
##############################################################
def separarPorRanking():
    ##  Leyendo data spreadsheet
    result = service.spreadsheets().values().get(
        spreadsheetId=data_id, range="Hoja 1").execute()
    rows = result.get('values', [])

    ##  Separando por categorias y obtener el ranking para grafica
    rankings = {}
    for r in rows:
        ranking = r[4]
        ##  Para rankings
        if ranking in rankings:
            rankings[ranking].append(r)
        else:
            rankings[ranking] = [r]

    ##  Creando array para escribir datos en spreadsheet 
    data = []
    for ranking in rankings:
        data.append([str(ranking) + " de 10 Estrellas"])
        data.append(["Categoria","Título","Descripción","Link Descarga"])
        for row in rankings[ranking]:
            del row[0]
            del row[3]
            data.append([row[0], row[1], row[2], row[3]])
        data.append([])
        data.append([])
    body = {
        'values': data
    }
    ##  Escribiendo data en el spreadsheet
    result = service.spreadsheets().values().update(
        spreadsheetId=resultado_id, range="Hoja 2",
        valueInputOption="RAW", body=body).execute()

    ##  Configurando estilo de spreadsheet
    requests = {
        "requests" : []
    }
    contador = 0
    for ranking in rankings:
        requests["requests"].append({
            "repeatCell" : {
                "range" : {
                    "sheetId" : ranking_sheet_id,
                    "startRowIndex" : contador,
                    "endRowIndex" : contador + 2
                },
                "cell" : {
                    "userEnteredFormat" : {
                        "textFormat" : {
                            "bold" : True,
                            "fontSize": 14,
                        },
                        "horizontalAlignment" : "CENTER"
                    }
                },
                "fields": "userEnteredFormat(textFormat,horizontalAlignment)"
            }
        })
        requests["requests"].append({
            "repeatCell" : {
                "range" : {
                    "sheetId" : ranking_sheet_id,
                    "startRowIndex" : contador + 2,
                    "endRowIndex" : contador + len(rankings[ranking]) + 2
                },
                "cell" : {
                    "userEnteredFormat" : {
                        "verticalAlignment" : "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(verticalAlignment)"
            }
        })
        requests["requests"].append({
            "repeatCell" : {
                "range" : {
                    "sheetId" : ranking_sheet_id,
                    "startRowIndex" : contador + 2,
                    "endRowIndex" : contador + len(rankings[ranking]) + 2,
                    "startColumnIndex" : 2,
                    "endColumnIndex" : 3
                },
                "cell" : {
                    "userEnteredFormat" : {
                        "wrapStrategy" : "LEGACY_WRAP"
                    }
                },
                "fields": "userEnteredFormat(wrapStrategy)"
            }
        })
        requests["requests"].append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": ranking_sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 1,
                    "endIndex": 4
                },
                "properties": {
                    "pixelSize": 350
                },
                "fields": "pixelSize"
            }
        })
        requests["requests"].append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": ranking_sheet_id,
                    "dimension": "ROWS",
                    "startIndex": contador + 2,
                    "endIndex": contador + len(rankings[ranking]) + 2
                },
                "properties": {
                    "pixelSize": 90
                },
                "fields": "pixelSize"
            }
        })
        requests["requests"].append({
            "mergeCells": {
                "range": {
                    "sheetId": ranking_sheet_id,
                    "startRowIndex" : contador,
                    "endRowIndex" : contador + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 4
                },
                "mergeType": "MERGE_ALL"
            }
        })

        contador += len(rankings[ranking]) + 4
    service.spreadsheets().batchUpdate(spreadsheetId=resultado_id, body=requests).execute()

separarPorCategoria()
separarPorRanking()


