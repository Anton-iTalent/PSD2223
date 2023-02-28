import sys

sys.path.append("/Users/anton/Documents/HPCDS/PSD/Patrick__Barrera_and_Collins/Code")
from PSD_PRJ import MetadataET
from PSD_PRJ import DBoperation
import pdf2doi
import os
from tqdm import tqdm


def listdir_full(path, with_prefix=True):
    if with_prefix:
        return [os.path.join(path, i) for i in os.listdir(path)]
    else:
        return os.listdir(path)


pdf2doi.config.set('verbose', False)

errors = {}
db = DBoperation.DB("root", "18170620626Xad", "PSD")
for i in tqdm(listdir_full("/Users/anton/Documents/HPCDS/PSD/Patrick__Barrera_and_Collins/papers/Papers")):
    try:
        info = MetadataET.extract_information(i)
        # Kkit.store("/home/kylis/Desktop/data_v1/%s.json"%i.split("/")[-1], json.dumps(info, indent=4, ensure_ascii=False), "utf-8")
        db.update_by_info_dict(info)
    except Exception as e:
        errors[i] = e
        print(i, e)

print(errors)
