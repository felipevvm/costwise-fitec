# costwise-fitec

## Inicializar a Aplicação

### Instale Python

### Instale o virtual env
```
pip install virtualenv
```

### Crie um virtualenv

#### Na pasta do projeto rode o comando
```
python -m venv venv
```

#### Ative o virtual env com o comando
```
venv/Scripts/activate
```

#### Instale as dependecias com o comando
```
pip install -r requirements.txt
```

### Inicialize o server
```
flask --app src run
```
#### Comando para inicializar no modo debug
```
flask --app src run --debug
```

### Documentation on the endpoint "/docs"