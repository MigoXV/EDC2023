import json

config={
    'fs':8e6,
    'nSamples':8000
}

with open('config.json','w',encoding='UTF-8') as f:
    f.write(json.dumps(config))
    
with open('config.json','r',encoding='utf-8') as f:
    result=json.loads(f.read())

for i in result:
    print(i,result[i])