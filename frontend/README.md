# 🎨 Email Classifier Frontend

Interface web moderna para o sistema de classificação inteligente de emails.

## 📋 Características

- ✅ Interface responsiva (mobile-first)
- ✅ Drag & drop de arquivos
- ✅ Validação em tempo real
- ✅ Feedback visual claro
- ✅ Tema moderno com gradientes
- ✅ Animações suaves

## 🔧 Configuração

### 1. Ajustar URL da API

Edite o arquivo `index.html` na linha 190:

```javascript
const API_CONFIG = {
    development: 'http://localhost:8000/api/v1',
    production: 'https://seu-backend.onrender.com/api/v1'
};
```

**Substitua** `seu-backend.onrender.com` pela URL real do seu backend em produção.

## ▶️ Como Executar

### Opção 1: Servidor Python Simples

```bash
# Na pasta frontend/
python -m http.server 8080
```

Acesse: http://localhost:8080

### Opção 2: Live Server (VS Code)

1. Instale a extensão "Live Server"
2. Clique com botão direito em `index.html`
3. Selecione "Open with Live Server"

### Opção 3: Servir com Node.js

```bash
npx serve .
```

## 🌐 Deploy

### Render

1. No Dashboard, clique em New + > Static Site.
2. Conecte seu repositório GitHub.
3. Nas configurações, preencha:
    3.1 Build Command: (Deixe em branco)
    3.2 Publish Directory: frontend
5. Clique em Create Static Site.

## 📱 Funcionalidades

### Upload de Arquivos
- Formatos suportados: `.txt`, `.pdf`
- Tamanho máximo: 10MB
- Drag & drop habilitado

### Análise de Texto
- Limite: 5.000 caracteres
- Contador em tempo real
- Validação de conteúdo mínimo

### Resultados
- Categoria visual (cores dinâmicas)
- Barra de confiança animada
- Explicação detalhada
- Resposta sugerida copiável

## 🎨 Customização

### Cores

O sistema usa Tailwind CSS. As cores principais são:

- **Primária**: Azul (`blue-600`)
- **Sucesso**: Verde (`green-600`)
- **Alerta**: Laranja (`orange-600`)
- **Erro**: Vermelho (`red-600`)

```

## 🔗 Estrutura de Arquivos

```
frontend/
├── index.html          # Aplicação completa (SPA)
├── assets/             # (opcional) Para organizar melhor
│   ├── css/
│   ├── js/
│   └── images/
└── README.md
```

## 🐛 Troubleshooting

### Frontend não conecta ao backend
1. Verifique se o backend está rodando
2. Confirme a URL da API no código
3. Abra o console do navegador (F12)
4. Verifique erros de CORS

### Arquivo não carrega
- Verifique o formato (.txt ou .pdf)
- Confirme se o tamanho é menor que 10MB
- Teste com um arquivo de texto simples primeiro

## 📝 Compatibilidade

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 📄 Licença

MIT

## 👨‍💻 Desenvolvedor

Júnior Ivan
