const CONFIG = {
    // CONFIGURAÇÃO DA API
    API: {
        development: 'http://localhost:8000/api/v1',
        production: 'https://seu-backend.onrender.com/api/v1'
    },

    // LIMITES E VALIDAÇÕES
    LIMITS: {
        maxFileSize: 10 * 1024 * 1024,
        maxTextLength: 5000,
        minTextLength: 10,  
        charWarningThreshold: 4500
    },

    // TEMPOS E DELAYS
    TIMING: {
        errorAutoHide: 10000,
        healthCheckInterval: 30000,
        progressBarAnimation: 100
    },

    // TEXTOS E MENSAGENS
    MESSAGES: {
        errors: {
            noInput: 'Por favor, digite um texto ou envie um arquivo.',
            textTooShort: 'O texto é muito curto. Digite pelo menos 10 caracteres.',
            fileTooLarge: 'Arquivo muito grande. Máximo: 10MB',
            networkError: 'Não foi possível conectar ao servidor.\n\n Verifique se o backend está rodando.\n\n Dica: Execute "uvicorn app.main:app --reload" na pasta backend/',
            serverError: 'Erro interno do servidor. Verifique a chave da API OpenAI.',
            invalidData: 'Dados inválidos.',
            incompleteResponse: 'Resposta da API incompleta',
            unknown: 'Erro desconhecido. Tente novamente.'
        },
        success: {
            copied: 'Resposta copiada para a área de transferência!',
            apiOnline: 'API está online'
        },
        loading: {
            processing: 'Processando...',
            classifying: 'Consultando Inteligência Artificial...'
        }
    },

    // CONFIGURAÇÕES DE CONFIANÇA (CORES)
    CONFIDENCE: {
        high: {
            threshold: 80,
            color: 'bg-green-600'
        },
        medium: {
            threshold: 50,
            color: 'bg-blue-600'
        },
        low: {
            threshold: 0,
            color: 'bg-orange-600'
        }
    },

    // CATEGORIAS E SUAS CORES
    CATEGORIES: {
        Produtivo: {
            bg: 'bg-green-100',
            text: 'text-green-700',
            border: 'border-green-200'
        },
        Improdutivo: {
            bg: 'bg-orange-100',
            text: 'text-orange-700',
            border: 'border-orange-200'
        },
        Erro: {
            bg: 'bg-red-100',
            text: 'text-red-700',
            border: 'border-red-200'
        }
    },

    // VERSÃO DA APLICAÇÃO
    VERSION: '1.0.0',
    AUTHOR: 'Júnior Ivan'
};

// DETECÇÃO AUTOMÁTICA DE AMBIENTE
const isDevelopment = () => {
    const hostname = window.location.hostname;
    
    // Lista completa de hostnames considerados desenvolvimento
    const devHostnames = [
        'localhost',
        '127.0.0.1',
        '::1',              // IPv6 localhost
        '0.0.0.0',
        ''                  // file:// protocol
    ];
    
    // Verifica se hostname está na lista ou começa com 192.168 ou 10.
    return devHostnames.includes(hostname) || 
           hostname.startsWith('192.168.') || 
           hostname.startsWith('10.') ||
           hostname.startsWith('172.');
};

// URL base da API (detecta automaticamente dev/prod)
const API_BASE_URL = isDevelopment() ? CONFIG.API.development : CONFIG.API.production;

// LOGS DE INICIALIZAÇÃO
console.log('========================================');
console.log('Classificador Inteligente de Emails');
console.log(`Versão: ${CONFIG.VERSION}`);
console.log(`Desenvolvedor: ${CONFIG.AUTHOR}`);
console.log('========================================');
console.log('DEBUG - Detecção de Ambiente:');
console.log(`   Hostname: ${window.location.hostname}`);
console.log(`   Protocol: ${window.location.protocol}`);
console.log(`   Port: ${window.location.port}`);
console.log(`   isDevelopment(): ${isDevelopment()}`);
console.log(`   Ambiente: ${isDevelopment() ? 'DESENVOLVIMENTO' : 'PRODUÇÃO'}`);
console.log(`   API URL: ${API_BASE_URL}`);
console.log('========================================');;

// Exportar para uso global (se necessário)
window.CONFIG = CONFIG;
window.API_BASE_URL = API_BASE_URL;