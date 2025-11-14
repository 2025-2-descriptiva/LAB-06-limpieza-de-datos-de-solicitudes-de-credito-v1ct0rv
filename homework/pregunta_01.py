"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import os
from datetime import datetime

import pandas as pd


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)

    # Eliminar filas con valores nulos ANTES de normalizar
    df = df.dropna()

    # Normalizar todas las columnas de texto a minúsculas y eliminar espacios
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip().str.lower()

    # Limpiar monto_del_credito - remover solo $ y comas, mantener punto decimal
    df["monto_del_credito"] = (
        df["monto_del_credito"].str.replace(r"[\$,]", "", regex=True).str.strip()
    )
    df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"], errors="coerce")

    # Normalizar barrio - mantener sufijos especiales como "._" diferenciados
    df["barrio"] = df["barrio"].str.replace(r"[-_.]", " ", regex=True)
    df["barrio"] = df["barrio"].str.replace(r"\s+", " ", regex=True).str.strip()
    df["barrio"] = df["barrio"].replace(
        {
            "bel¿n": "belén",
            "antonio nari¿o": "antonio nariño",
        }
    )

    # Normalizar idea_negocio - unificar separadores comunes
    df["idea_negocio"] = df["idea_negocio"].str.replace(r"[-_.]", " ", regex=True)
    df["idea_negocio"] = (
        df["idea_negocio"].str.replace(r"\s+", " ", regex=True).str.strip()
    )

    # Normalizar línea_credito - reemplazar caracteres especiales por espacios
    df["línea_credito"] = df["línea_credito"].str.replace("[-_.]", " ", regex=True)
    df["línea_credito"] = (
        df["línea_credito"].str.replace(r"\s+", " ", regex=True).str.strip()
    )

    # Convertir estrato a entero
    df["estrato"] = pd.to_numeric(df["estrato"], errors="coerce").astype("Int64")

    # Convertir comuna_ciudadano a entero
    df["comuna_ciudadano"] = pd.to_numeric(
        df["comuna_ciudadano"], errors="coerce"
    ).astype("Int64")

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(normalize_date)

    # Eliminar filas duplicadas
    df = df.drop_duplicates()

    # Crear files/output directory si no existe
    os.makedirs("files/output", exist_ok=True)

    # Guardar el resultado
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)


def normalize_date(value: str) -> str:
    value = str(value).strip()
    if "/" in value:
        parts = value.split("/")
        try:
            if len(parts[0]) == 4:
                parsed = datetime.strptime(value, "%Y/%m/%d")
            else:
                parsed = datetime.strptime(value, "%d/%m/%Y")
            return parsed.strftime("%d/%m/%Y")
        except ValueError:
            return value
    return value
