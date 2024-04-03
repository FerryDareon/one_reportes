def dataframe_one(tabla_interes="Importaciones", año_interes=2024, url=None):
    """
    Esta función extrae datos de un archivo Excel alojado en el sitio web de ONE (Oficina Nacional de Estadística) de la República Dominicana.
    Se requiere especificar el nombre de la tabla de interés y el año de interés para seleccionar los datos adecuados del archivo.

    Parámetros:
        - tabla_interes (str): El nombre de la tabla de interés. Por defecto es "Importaciones".
        - año_interes (int): El año de interés para seleccionar los datos adecuados. Por defecto es 2024.
        - url(str): URL del archivo a leer en formato xlsx. Si se proporciona, se ignora el nombre de la tabla y el año de interés,
          y se procederá a realizar una consulta del link en caso de que este contenga un documento en .xlsx
    Returns:
        Un diccionario de DataFrames con las hojas de Excel seleccionadas según los parámetros especificados.
    """

    import pandas as pd
    import numpy as np
    import requests
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    import time

    if url == None:  # Si no se proporciona una URL
            
        # Establecer la opción para mostrar el contenido completo de las columnas
        pd.set_option("display.max_colwidth", -1)

        # Configuración del navegador Chrome
        driveroptions = Options()
        driveroptions.add_argument("--headless=new")

        # Inicializar el navegador Chrome
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=driveroptions)
        driver.get('https://www.one.gob.do/datos-y-estadisticas/')

        # Esperar hasta que aparezca el enlace a las descargas
        wait = WebDriverWait(driver, timeout=5)
        wait.until(lambda a: driver.find_element(By.XPATH, "/html/body/div[7]/section/div/ul/li[2]/a").is_displayed())

        # Hacer clic en el enlace de descargas
        driver.find_element(By.XPATH, "/html/body/div[7]/section/div/ul/li[2]/a").click()

        # Esperar a que aparezcan las tablas de descargas
        wait.until(lambda a: len(driver.find_element(By.XPATH, "/html/body/div[7]/section/div/div[3]/div[2]/div/div[2]/div[2]/div/div").text.split('\n')) > 1)
        time.sleep(2)

        # Consultar las tablas de descargas disponibles
        position_dataset = []
        database_name = []
        for x in range(1, len(driver.find_element(By.XPATH, "/html/body/div[7]/section/div/div[3]/div[2]/div/div[2]/div[2]/div/div").text.split('\n')) + 1):
            database_name.append(driver.find_element(By.XPATH, f"/html/body/div[7]/section/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div[{x}]/header/div[2]").text)
            position_dataset.append(x)
        database_control = pd.DataFrame(data={'DB_code': position_dataset,
                                            'DB_name': database_name})

        try:
            # Filtrar la tabla de interés
            filter_search = database_control[database_control['DB_name'].str.contains(tabla_interes, case=False)]
            db_code = filter_search.iloc[0]['DB_code']

            # Hacer clic en la tabla de interés
            driver.find_element(By.XPATH, f"/html/body/div[7]/section/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div[{db_code}]/header/div[2]").click()
        except:
            print("Tablas Disponibles")
            table_list = ("Exportaciones", "Importaciones", "Perfil Empresas Exportadoras",
                        "Perfil Empresas Importadoras", "Registro de Oferta de Edificaciones (ROE)",
                        "Carga Marítima Internacional", "Contenedores en TEUS",
                        "Permisos de construcción del sector privado", "Finanzas de los gobiernos locales",
                        "Atmósfera y Clima", "Residuos sólidos")
            print(database_control[database_control["DB_name"].isin(table_list)])

        try:
            # Esperar a que aparezcan los archivos disponibles en la tabla de interés
            wait.until(lambda a: len(driver.find_elements(By.XPATH, f"/html/body/div[7]/section/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div[{db_code}]/div/div/div[2]/div/table/tbody/tr")) > 1)
            time.sleep(1)

            # Consultar los archivos disponibles del año de interés
            excel_position = []
            excel_files_name = []
            excel_href = []
            for x in range(1, len(driver.find_elements(By.XPATH,f"/html/body/div[7]/section/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div[{db_code}]/div/div/div[2]/div/table/tbody/tr"))+1):
                excel_files_name.append(
                    driver.find_element(By.XPATH,f"/html/body/div[7]/section/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div[{db_code}]/div/div/div[2]/div/table/tbody/tr[{x}]/td/a/div[2]/h5"
                                        ).text)
                excel_position.append(x)
                excel_href.append(driver.find_element(By.XPATH,f"/html/body/div[7]/section/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div[{db_code}]/div/div/div[2]/div/table/tbody/tr[{x}]/td/a"
                                                    ).get_attribute('href'))
            excel_document_control = pd.DataFrame(data={'excel_code':excel_position,
                                                'excel_name':excel_files_name,
                                                'excel_link':excel_href
                                                })
            excel_document_control['year'] = excel_document_control['excel_name'].str.extract('(\d+)')
            excel_document_control = excel_document_control[excel_document_control['excel_link'].str.endswith((".xlsx"))].copy()

            try:
                excel_filter_search = excel_document_control[excel_document_control['year'] == f'{año_interes}']
                if len(excel_filter_search) > 1:
                    print(excel_filter_search[["excel_code","excel_name"]])
                    excel_code=input("Selecciona el excel_code del archivo a consultar")
                    excel_db_code = excel_filter_search[excel_filter_search["excel_code"]==int(excel_code)].iloc[0]['excel_link']
                else:
                    excel_db_code = excel_filter_search.iloc[0]['excel_link']
                print("Generando el DataFrame")
                df = pd.read_excel(requests.get(f"{excel_db_code}").content,sheet_name=None)
            except:
                print("Archivos Disponibles en el Reporte de Interés")
                print(excel_document_control[["excel_code","excel_name"]])
                time.sleep(0.5)
                excel_code=input("Selecciona el excel_code del archivo a consultar")
                excel_db_code = excel_document_control[excel_document_control["excel_code"]==int(excel_code)].iloc[0]['excel_link']
                print("Generando el DataFrame")
                df = pd.read_excel(requests.get(f"{excel_db_code}").content,sheet_name=None)
            return df
        except:
            print("Tablas Disponibles")
            table_list = ("Exportaciones","Importaciones","Perfil Empresas Exportadoras",
                    "Perfil Empresas Importadoras","Registro de Oferta de Edificaciones (ROE)","Carga Marítima Internacional",
                    "Contenedores en TEUS","Permisos de construcción del sector privado","Finanzas de los gobiernos locales",
                    "Atmósfera y Clima","Residuos sólidos")
            print(database_control[database_control["DB_name"].isin(table_list)]["DB_name"])
        print("DataFrame Generado")
        driver.close()
    else:
        try:
            df = pd.read_excel(requests.get(f"{url}").content,sheet_name=None)
            return df
        except:
            print("La URL no contiene un documento en Excel")
