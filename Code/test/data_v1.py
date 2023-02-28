import sys
sys.path.append("/home/kylis/Desktop/Patrick__Barrera_and_Collins/Code/")
from PSD_PRJ import MetadataET
import Kkit
import pdf2doi
import json
from tqdm import tqdm

pdf2doi.config.set('verbose',False)

errors = {}

for i in tqdm(Kkit.klistdir("/home/kylis/Desktop/Paper/Papers")):
    try:
        info = MetadataET.extract_information(i)
        Kkit.store("/home/kylis/Desktop/data_v1/%s.json"%i.split("/")[-1], json.dumps(info, indent=4, ensure_ascii=False), "utf-8")
    except Exception as e:
        errors[i] = e

print(errors)
