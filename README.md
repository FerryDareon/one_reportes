# one_reportes

Una función para realizar consultas de las Bases de Datos en descargas de la ONE (Oficina Nacional de Estadística) de la República Dominicana.

```python 
import pandas as pd
import numpy as np
from one_report import dataframe_one

# Observar el contenido de la función dataframe_one 
print(dataframe_one.__doc__)
```

Esta función extrae datos de un archivo Excel alojado en el sitio web de la ONE de la República Dominicana. Se requiere especificar el nombre de la tabla de interés y el año de interés para seleccionar los datos adecuados del archivo.

**Parámetros:**
- `tabla_interes` (str): El nombre de la tabla de interés. Por defecto es "Importaciones".
- `año_interes` (int): El año de interés para seleccionar los datos adecuados. Por defecto es 2024.
- `url` (str): URL del archivo a leer en formato xlsx. Si se proporciona, se ignora el nombre de la tabla y el año de interés.

**Returns:**
Un diccionario de DataFrames con las hojas de Excel seleccionadas según los parámetros especificados.

Estaríamos obteniendo un DataFrame compuesto por el Excel completo del archivo `.xlsx` consultado.

Con la función `.keys()` tendríamos una visualización de los nombres de las Hojas o Sheets del archivo leído. Y si se desea consultar o utilizar una hoja específica se deberá hacerlo como si de una columna de un DataFrame se tratara, obteniendo el DataFrame correspondiente.

```python
df = dataframe_one("Importaciones", 2023)
df.keys()
```
> Output: dict_keys(['IMP_2023_WEB'])

De esta forma, estaríamos guardando la información que se encuentra en el archivo exportado de `.xlsx` para su manipulación y uso.

```python
importaciones_2023 = df["IMP_2023_WEB"]
importaciones_2023.head()
```

Este archivo es útil para aquellos que necesiten realizar consultas específicas a las bases de datos de la ONE de forma sencilla y eficiente.
