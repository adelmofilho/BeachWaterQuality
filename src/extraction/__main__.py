import os
from tqdm import tqdm
from .tabulizer import write_boletim_xml, extract_table

for arquivo in tqdm(os.listdir("data/raw")):
    write_boletim_xml(arquivo)

for xml in tqdm(os.listdir("data/processed")):
    print(xml)
    extract_table(xml)
