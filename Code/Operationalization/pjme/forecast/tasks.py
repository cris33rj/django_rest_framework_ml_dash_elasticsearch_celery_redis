from core.celery import app
import elasticsearch
import random
import json
import pandas as pd



INDEX_MAPPING = {
            "settings": {
                "number_of_shards": 3
            },
        "mappings": {
            "properties": {
                "date": {
                "type": "date"
                },
                "energy_type": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "flag": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "id": {
                "type": "long"
                },
                "pjme_mw": {
                "type": "float"
                },
                "zone": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
            }
        }
    }
}
}


INDEX_NAME = "pjme_energy_consumption"


@app.task()
def elk_insertion_single_registry(measurement_id):
    from forecast.models import Measurements

    import time
    print("Recebido, Processando...")
    time.sleep(2)    

    #measurement = User.objects.get(id=user_id)
    measurement = Measurements.objects.get(id=measurement_id)

    zones = ['pacific', 'mountain', 'central', 'eastern']
    zone = random.choice(zones)
    flags = ['green','yellow','red']
    flag_color = random.choice(flags)
    energy_types =  ['eletric','thermal','wind']
    energy_type = random.choice(energy_types)

    document = {
        "id": measurement.id,
        "date": measurement.date,
        "pjme_mw":measurement.PJME_MW,
        "zone":zone,
        "flag":flag_color,
        "energy_type":energy_type
    }

    client = elasticsearch.Elasticsearch('localhost:9200')

    exists = client.indices.exists(INDEX_NAME); 

    if exists == False:
    
        client.indices.create(INDEX_NAME, body=INDEX_MAPPING)

    
    client.index(index=INDEX_NAME, id=str(measurement.id), body=document)



@app.task()
def elk_insertion(date, PJME_MW):    
    print('#########date#######',date)
    print('#########date#######',PJME_MW)      

    client = elasticsearch.Elasticsearch('localhost:9200')
    client.indices.put_settings(index=INDEX_NAME, body={"index": {"refresh_interval": "-1"}})

    zones = ["pacific", "mountain", "central", "eastern"]
    zone = random.choice(zones)
    flags = ["green","yellow","red"]
    flag_color = random.choice(flags)
    energy_types =  ["eletric","thermal","wind"]
    energy_type = random.choice(energy_types)      
   
    document = {                    
            "date": date,
            "pjme_mw":PJME_MW,
            "zone":zone,
            "flag":flag_color,
            "energy_type":energy_type
        } 
    client.index(index=INDEX_NAME, body=document)

   # Restaurar a configuração padrão do Refresh
    client.indices.put_settings(index=INDEX_NAME, body={"index": {"refresh_interval": "2s"}})

   # Refresh e Flush
    client.indices.refresh(index=INDEX_NAME)
    client.indices.flush(index=INDEX_NAME)  