# 🚀 Email Classifier API

API REST para classificação inteligente de emails usando GPT-3.5-turbo.

## 📋 Pré-requisitos

- Python 3.8+
- OpenAI API Key
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### 1. Clone o repositório (se ainda não fez)

```bash
git clone <seu-repositorio>
cd EMAIL-CLASSIFIER/backend
```

### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na pasta `backend/`:

```env
OPENAI_API_KEY=sk-seu-token-aqui
```

## ▶️ Como Executar

### Desenvolvimento

```bash
# Na pasta backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- **API**: http://localhost:8000
- **Documentação Interativa**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

### Produção

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 Documentação da API

### Endpoints Principais

#### `POST /api/v1/classify`
Classifica um email.

**Parâmetros:**
- `text` (string, opcional): Texto do email
- `file` (file, opcional): Arquivo PDF ou TXT

**Resposta:**
```json
{
  "categoria": "Produtivo",
  "confianca": 95,
  "razao": "Email contém solicitação clara de pagamento",
  "resposta_sugerida": "Olá! Vou processar o pagamento..."
}
```

#### `GET /health`
Verifica se a API está online.

#### `GET /api/docs`
Documentação interativa (Swagger UI).

## 🏗️ Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Configuração FastAPI
│   ├── routes.py            # Endpoints da API
│   ├── config.py            # Configurações e constantes
│   └── services/
│       ├── __init__.py
│       ├── ai_service.py    # Integração com OpenAI
│       └── file_service.py  # Processamento de arquivos
├── requirements.txt
├── .env
└── README.md
```

## 🔒 Segurança

- CORS configurado para origens específicas
- Validação de tamanho de arquivo (máx 10MB)
- Validação de tipos de arquivo (.txt, .pdf)
- Rate limiting (configurar se necessário)

## 🌐 Deploy

### Render.com

1. Conecte seu repositório ao Render
2. Configure as variáveis de ambiente:
   - `OPENAI_API_KEY`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Railway.app

1. Conecte seu repositório
2. Adicione a variável `OPENAI_API_KEY`
3. Railway detectará automaticamente o projeto Python

## 🐛 Troubleshooting

### Erro: "OPENAI_API_KEY não configurada"
- Verifique se o arquivo `.env` existe na pasta `backend/`
- Confirme que a chave está correta

### Erro: "Failed to fetch"
- Verifique se o backend está rodando
- Confirme a URL no frontend
- Verifique configurações de CORS

### Erro 500 ao classificar
- Verifique se a API Key da OpenAI é válida
- Confira os logs do servidor
- Teste a API usando `/api/docs`

## 📝 Licença

MIT

## 👨‍💻 Desenvolvedor

Júnior Ivan