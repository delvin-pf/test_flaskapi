## test_flaskapi


### API para recebimento e processamento de Webhooks

WebService construido em Flask, usando base de dados MySQl e Peewee como
administrador de base de dados.

Consta de varios templates para login, cadastro e um dashboard de 
webhooks.

---

### Endpoints


- #### Pages 

**`/`** (Get, Post) - Template de login.

**`/cadastro`** (Get, Post) - Template de cadastro.

**`/home`** (Get, Post) - Dashboard de Webhooks. 


- #### API

`/api/webhooks` **(Post) - Envio dos webhooks**

`/api/webhooks` (Get) - Lista de Webhooks

`/api/users` (Post) - Cria um novo usuario

`/api/users/login` (Post) - Loga un usuario e retorna um JWT