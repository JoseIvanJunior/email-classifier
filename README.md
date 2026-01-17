# 📁 Estrutura Completa do Projeto - Email Classifier

## 🏗️ Arquitetura

O projeto foi seguindo as melhores práticas de desenvolvimento:

```
EMAIL-CLASSIFIER/
│
├── backend/                        # API REST (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # ⚙️ Configuração FastAPI + CORS
│   │   ├── routes.py              # 🛣️ Endpoints da API
│   │   ├── config.py              # 🔧 Configurações e OpenAI client
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py     # 🤖 Lógica de IA (GPT-3.5)
│   │   │   └── file_service.py   # 📄 Extração de texto (PDF/TXT)
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── json_utils.py     # 🔍 Parse seguro de JSON
│   ├── .env                       # 🔐 Variáveis de ambiente
│   ├── .gitignore
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                       # Interface Web (HTML puro)
│   ├── index.html                 # 🎨 SPA completa
│   ├── assets/                    # (opcional)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── README.md
│
└── README.md                      # 📖 Documentação geral
```

## 🔄 Fluxo de Comunicação

```
┌─────────────────┐          HTTP/CORS          ┌─────────────────┐
│                 │ ───────────────────────────>│                 │
│   FRONTEND      │     POST /api/v1/classify   │    BACKEND      │
│  (HTML + JS)    │                             │   (FastAPI)     │
│                 │<─────────────────────────── │                 │
│  localhost:8080 │          JSON Response      │  localhost:8000 │
└─────────────────┘                             └─────────────────┘
                                                        │
                                                        │ API Call
                                                        ▼
                                                 ┌──────────────┐
                                                 │   OpenAI     │
                                                 │  GPT-3.5     │
                                                 └──────────────┘
```

### ✅ Estrutura
- Frontend independente
- Backend só retorna JSON
- CORS configurado corretamente
- Deploy separado e flexível
- Documentação automática (Swagger)

## 📝 Checklist de Migração

### Backend

- [x] Prefixo `/api/v1` nas rotas
- [x] Configurar CORS com origens permitidas
- [x] Adicionar modelos Pydantic para documentação
- [x] Implementar health check robusto
- [x] Melhorar logs e tratamento de erros
- [x] Documentação Swagger automática

### Frontend

- [x] Configurar API_BASE_URL dinâmica
- [x] Implementar verificação de saúde da API
- [x] Melhorar feedback de erros
- [x] Adicionar logs no console para debug

## 🔧 Como Usar

### 1️⃣ Configurar Backend

```bash
cd backend
pip install -r requirements.txt

# Executar
uvicorn app.main:app --reload
```

### 2️⃣ Configurar Frontend

```bash
cd frontend

# Editar index.html linha 190
- [x] Ajustar API_CONFIG.production com URL real

# Servir localmente
python -m http.server 8080

```

### 3️⃣ Testar

1. Acesse http://localhost:8080
2. Teste enviando um email de exemplo
3. Verifique logs no console (F12)

## 🌐 Deploy em Produção

### Backend (Render.com)

```yaml
# render.yaml
services:
  - type: web
    name: email-classifier-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
```

### Frontend (Vercel)

```bash
cd frontend
vercel --prod
```

Depois do deploy:
1. Copie a URL do backend do Render
2. Atualize `API_CONFIG.production` no frontend
3. Redeploy o frontend

## 🔐 Segurança

### Backend
- ✅ CORS configurado com whitelist
- ✅ Validação de entrada (Pydantic)
- ✅ Limite de tamanho de arquivo
- ✅ Tipos de arquivo restritos
- ✅ API Key em variável de ambiente
- [] Considere adicionar rate limiting

### Frontend
- ✅ Validação client-side
- ✅ Sanitização de entrada
- ✅ Timeouts em requisições
- ✅ Tratamento de erros robusto

## 📊 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Info da API |
| GET | `/health` | Health check |
| GET | `/api/docs` | Swagger UI |
| POST | `/api/v1/classify` | Classificar email |

## 🎯 Benefícios da Arquitetura

1. **Escalabilidade**: Backend e frontend podem escalar independentemente
2. **Manutenção**: Código mais organizado e fácil de manter
3. **Deploy**: Flexibilidade para usar diferentes providers
4. **Desenvolvimento**: Times podem trabalhar paralelamente
5. **Testes**: Mais fácil testar cada parte isoladamente
6. **Documentação**: Swagger gerado automaticamente
7. **Profissionalismo**: Arquitetura padrão da indústria

## 🐛 Debug

### Ver logs do backend
```bash
# Backend mostrará logs detalhados
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     📨 Nova requisição de classificação recebida
```

### Ver logs do frontend
```bash
# Abra o console do navegador (F12)
# Logs úteis:
✅ API está online
📤 Enviando para: http://localhost:8000/api/v1/classify
📥 Status: 200
✅ Resposta: {...}
```

## 📚 Próximos Passos

- [ ] Adicionar autenticação (JWT)
- [ ] Implementar rate limiting
- [ ] Adicionar testes unitários
- [ ] Configurar CI/CD
- [ ] Adicionar cache (Redis)
- [ ] Métricas e monitoring
- [ ] Suporte a múltiplos idiomas
- [ ] Histórico de classificações

## 👨‍💻 Desenvolvedor

**Júnior Ivan**  

---

**Licença**: MIT