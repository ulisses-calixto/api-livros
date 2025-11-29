# API de Livros

API de gerenciamento de livros desenvolvida com FastAPI e Supabase.

## 🚀 Como rodar o projeto localmente

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente no arquivo `.env`:
```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-chave-anon-public
TABLE_LIVROS=livros
```

3. Inicie o servidor:
```bash
uvicorn main:app --reload --port 8000
```

A API estará disponível em `http://localhost:8000`

## 📚 Documentação da API

Acesse a documentação em: `http://localhost:8000/docs`

## 🌐 Como hospedar no Render

### Pré-requisitos
- Conta no [Render](https://render.com) (gratuita)
- Conta no [Supabase](https://supabase.com) com projeto criado
- Repositório Git (GitHub, GitLab ou Bitbucket)

### Passo a Passo

#### 1. Preparar o repositório

Certifique-se de que seu repositório contém os seguintes arquivos:
- `main.py` (código da aplicação)
- `requirements.txt` (dependências)
- `sql/livros.sql` (script SQL para criar a tabela)
- `collection/livros_api.postman_collection.json` (coleção Postman)
- Arquivo `.env` **não deve estar no repositório** (use apenas localmente)

#### 2. Configurar o Supabase

1. Acesse [https://supabase.com](https://supabase.com) e crie um projeto
2. Vá em **SQL Editor** e execute o script `sql/livros.sql`
3. Desabilite o `Confirm email` nas **Configurações do Projeto** em **Authentication** e salve
4. Copie suas credenciais em **Settings** → **API**:
   - `Project URL` = SUPABASE_URL
   - `anon public key` = SUPABASE_ANON_KEY

#### 3. Criar Web Service no Render

1. Acesse [https://dashboard.render.com](https://dashboard.render.com)
2. Clique em **"New +"** e selecione **"Web Service"**
3. Conecte seu repositório Git (autorize o acesso se necessário)
4. Selecione o repositório do projeto

#### 4. Configurar o Web Service

Preencha as seguintes informações:

- **Name**: `livros-api` (ou nome de sua preferência)
- **Region**: Escolha a região mais próxima (ex: `Oregon (US West)`)
- **Branch**: `main` (ou sua branch principal)
- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

#### 5. Configurar Variáveis de Ambiente

Na seção **Environment Variables**, adicione as seguintes variáveis:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | Sua URL do Supabase (ex: `https://xxxxx.supabase.co`) |
| `SUPABASE_ANON_KEY` | Sua chave anônima do Supabase |
| `TABLE_LIVROS` | `livros` (nome da tabela) |

**Como obter as credenciais do Supabase:**
1. Acesse seu projeto no [Supabase](https://app.supabase.com)
2. Vá em **Settings** → **API**
3. Copie a **URL** e a **anon/public key**

#### 6. Selecionar o Plano

- Escolha o plano **Free** para começar
- Clique em **"Create Web Service"**

#### 7. Aguardar o Deploy

- O Render irá automaticamente:
  1. Clonar seu repositório
  2. Instalar as dependências
  3. Iniciar a aplicação
- Acompanhe os logs em tempo real
- O primeiro deploy pode levar alguns minutos

#### 8. Acessar sua API

Após o deploy bem-sucedido:
- Sua API estará disponível em: `https://livros-api.onrender.com` (substitua pelo seu link)
- Acesse a documentação interativa em: `https://livros-api.onrender.com/docs`

### ⚙️ Configurações Adicionais

#### Auto-Deploy
Por padrão, o Render faz deploy automático quando você faz push para a branch configurada. Para desabilitar:
1. Vá em **Settings** do seu Web Service
2. Desative **"Auto-Deploy"**

#### Domínio Personalizado
1. Vá em **Settings** → **Custom Domain**
2. Adicione seu domínio
3. Configure os registros DNS conforme as instruções

#### Monitoramento
- Acesse a aba **"Logs"** para ver logs em tempo real
- Acesse a aba **"Metrics"** para ver uso de CPU e memória

### 🔧 Solução de Problemas

#### Erro: "Application failed to start"
- Verifique se o comando de start está correto: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Confirme que todas as variáveis de ambiente estão configuradas

#### Erro: "RuntimeError: Configure SUPABASE_URL e SUPABASE_ANON_KEY"
- Verifique se as variáveis de ambiente `SUPABASE_URL` e `SUPABASE_ANON_KEY` estão configuradas corretamente no Render

#### Erro 401: "Token não fornecido ou inválido"
- Certifique-se de que está enviando o header `Authorization: Bearer {seu_token}` nas requisições
- Faça login novamente para obter um token válido

#### Erro 404: "Livro não encontrado"
- Verifique se o ID do livro existe e pertence ao usuário autenticado
- Lembre-se: cada usuário só pode ver seus próprios livros (RLS habilitado)

#### Aplicação fica "suspensa" no plano gratuito
- O plano gratuito do Render suspende a aplicação após 15 minutos de inatividade
- A primeira requisição após a suspensão pode levar ~30 segundos para "acordar" o serviço

### 📝 Notas Importantes

- O plano gratuito do Render tem **750 horas/mês** de uso
- A aplicação pode ficar lenta após períodos de inatividade (cold start)
- Para produção, considere usar um plano pago para melhor performance
- **Row Level Security (RLS)** está habilitado: cada usuário vê apenas seus próprios livros

### 🔄 Atualizações

Para atualizar sua aplicação:
1. Faça commit e push das alterações no repositório
2. O Render detectará automaticamente e iniciará um novo deploy
3. Acompanhe o progresso na aba **"Events"**

## 🧪 Testando com Postman

1. Importe a coleção `collection/livros_api.postman_collection.json` no Postman
2. Execute as requisições na ordem:
   - **Registrar Usuário** - Crie uma conta
   - **Login** - Obtenha o token de acesso (salvo automaticamente)
   - **Criar Livro** - Adicione livros à sua biblioteca
   - **Listar Livros** - Veja todos os seus livros
   - **Buscar por ID** - Encontre um livro específico
   - **Atualizar Livro** - Edite informações
   - **Deletar Livro** - Remove um livro

## 📍 Endpoints

### Autenticação de Usuário
- `POST /auth/registrar` - Registrar novo usuário
- `POST /auth/login` - Fazer login
- `POST /auth/logout` - Fazer logout

### Livros (autenticação necessária)
- `GET /livros` - Listar todos os livros (com paginação e busca)
- `GET /livros/{id}` - Buscar livro por ID
- `POST /livros` - Criar novo livro
- `PUT /livros/{id}` - Atualizar livro
- `DELETE /livros/{id}` - Deletar livro

## 🔒 Segurança

- Autenticação via JWT (Supabase Auth)
- Row Level Security (RLS) presente
- Cada usuário acessa apenas seus próprios dados
- Senhas hash pelo Supabase

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Supabase** - Backend as a Service (PostgreSQL + Authentication)
- **Pydantic** - Validação de dados
- **httpx** - Cliente HTTP assíncrono
- **Uvicorn** - Servidor local ASGI
