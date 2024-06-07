# CostWise
## Requisitos:
- Python

### Crie um arquivo chamado .env
 Dentro dele adicione as variaveis necessarias, o arquivo .env.example é uma base para o .env, utilize ele se acha necessario.

 O Arquivo de config do Flask preencher algumas dessas variaveis como default se não forem adicionadas.

 ## Crie um venv 
## Crie um venv
Para criar um ambiente virtual (venv) no Python, siga os seguintes passos:

1. Execute o seguinte comando para criar o ambiente virtual:

    ```
    python -m venv nome_do_venv
    ```

    Substitua `nome_do_venv` pelo nome que deseja dar ao seu ambiente virtual.

2. Após a execução do comando, um novo diretório com o nome do ambiente virtual será criado no diretório do seu projeto.

3. Ative o ambiente virtual executando o comando apropriado para o seu sistema operacional:

    - No Windows:

      ```
      nome_do_venv\Scripts\activate
      ```

    - No macOS/Linux:

      ```
      source nome_do_venv/bin/activate
      ```

    Após ativar o ambiente virtual, você verá o nome do ambiente virtual no prompt de comando.

### Instale as dependências
 Agora você pode instalar as dependências do seu projeto dentro do ambiente virtual usando o `pip` ou `pipenv`.

    ```
    pip install -r requirements.txt
    ```

### Iniciar o servidor
Com seu ambiente virtual configurado e pronto para ser usado. Você pode executar o seu projeto dentro do ambiente virtual.

Para da inicio ao servidor do Flask rode o comando abaixo:

```
flask --app src run
```

Se você deseja executar o servidor em modo de depuração, basta adicionar a opção `--debug` no final do comando de inicialização do Flask:

```bash
flask --app src run --debug
```

Quando abri o servidor você sera redirecionado para o endpoint /docs, nele todos os endpoints estão documentados e podem se executados.

Rode o comando abaixo se deseja executar os testes desse projeto:
```
pytest
```