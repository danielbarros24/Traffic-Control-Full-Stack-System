#### Iterar por cada automação e verificar se enable e a data estão ON. Se sim -> verificar as variáveis. Se não -> avança
#### Buscar na DB da camara os dados e ver a condiçao presente na DB de automações.
#### Construir JSON dos dados: {"data": { "fluxo1" : 100, "fluxo2" : 60}}
#### Executa jsonLogic.apply(rules, data);
#### Retorna true ou false -> se true coloca pino x a 1


from tinydb import TinyDB, Query

# DATABASE
db_camera = TinyDB('../database/camera_data.json')
db_auth = TinyDB('../database/auth.json')
db_auto = TinyDB('../database/automations.json')
db_general = TinyDB('../database/general_info.json')

query = Query()


