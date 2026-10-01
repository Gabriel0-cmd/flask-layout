# flask-layout

## Executar

Instale a dependência e inicie a aplicação:

```bash
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000`. O banco `dados.db` e os registros de demonstração são criados automaticamente na primeira requisição.

## Área restrita

As páginas **Boletim** e **Anotações** exigem login. Para testar, use:

- Usuário: `gabriel`
- Senha: `estudo123`

A senha é armazenada no SQLite como hash, e as páginas consultam seus dados no banco. Para escolher as credenciais da conta inicial, configure `DEMO_USERNAME` e `DEMO_PASSWORD` antes da primeira requisição a um banco novo. Em ambientes de produção, configure também `FLASK_SECRET_KEY` com um valor secreto e exclusivo.