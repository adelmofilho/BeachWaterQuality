from os import makedirs
from os.path import exists
from pdfquery import PDFQuery
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime


def write_boletim_xml(file, input_dir="data/raw", output_dir="data/processed"):
    
    if not exists(input_dir):
        raise Exception("Input directory does not exist")
    
    if not exists(output_dir):
        makedirs(output_dir)  
    
    boletim_name = file.split(".")[0]
    boletim_path = f"{input_dir}/{file}"
    
    xml_name = f"{boletim_name}.xml"
    xml_path = f"{output_dir}/{xml_name}"
    
    pdf = PDFQuery(boletim_path)
    pdf.load()
    pdf.tree.write(xml_path, pretty_print=True)


def extract_table(file, input_dir="data/processed", output_dir="data/tabular"):
    
    if not exists(input_dir):
        raise Exception("Input directory does not exist")
    
    if not exists(output_dir):
        makedirs(output_dir)  
    
    content = []
    target = ["Própria", "Imprópria", "Indisponível"]
    xml_path = f"{input_dir}/{file}"

    with open(xml_path, "r") as f:
        content = f.readlines()

    content = "".join(content)
    bs_content = bs(content, "lxml")
    a = [text.text.strip() for text in bs_content.find_all("ltrect")]

    lista = list()
    for opts in range(len(a)):
        if a[opts] in target:
            lista.append([a[opts-2], a[opts-1], a[opts]])       

    if lista:
        df = pd.DataFrame(lista, columns =['ponto', 'local', 'categoria']) 

        id_campanha = file.split(".")[0].split("_")[1]
        df["campanha"] = id_campanha

        metadados = bs_content.find("lttextboxhorizontal").text

        boletim_number = metadados.split(" / ")[0].split(":")[2].strip()
        df["boletim"] = boletim_number

        data = metadados.split(" / ")[1].split(":")[1].strip()
        date_object = datetime.strptime(data, '%d/%m/%Y').date()
        df["data"] = date_object.strftime("%Y-%m-%d")

        regex = df.ponto.str.split(r'(\s-\s\b)(?!.*\1)', n=1, expand= True)
        codigos = regex[2].str.strip().str.split(" ", expand=True)
        codigos.columns = ["cod_regiao", "cod_ponto", "cod_monitor"]
        
        nome_ponto = regex[0]
        df["nome_ponto"] = nome_ponto

        df = pd.concat([df, codigos], axis=1)

        boletim_name = file.split(".")[0]

        csv_path = f"{output_dir}/{boletim_name}.csv"
        df.to_csv(csv_path,index=False)