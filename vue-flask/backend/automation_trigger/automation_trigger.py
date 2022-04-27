#### Irá buscar na DB da camara os dados e ver a condiçao presente na DB de automações.
#### Exemplo de JSON dos dados {"data": { "fluxo1" : 100, "fluxo2" : 60}}
#### Exemplo de JSON das automações:
# 
""" {"info": {"name":"automação1", "GPIO":2},
  "rules":{ "and" : [
  {">" : [
      {"var" : "fluxo1"}, 30]},
  {">" : [
      { "var" : "fluxo2" }, "50" ] }
] } """


#### Executa jsonLogic.apply(rules, data);
#### Retorna true ou false -> se true coloca pino x a 1