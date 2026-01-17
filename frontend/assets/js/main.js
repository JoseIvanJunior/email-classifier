/**
 * Lógica Principal da Aplicação
 * Gerencia eventos, validações e comunicação com API
 */

// VALIDAÇÃO DE ENTRADA
function validateInput(text, file) {
    // Nenhuma entrada fornecida
    if (!text && !file) {
        UI.showError(CONFIG.MESSAGES.errors.noInput);
        return false;
    }

    // Texto muito curto
    if (text && text.length < CONFIG.LIMITS.minTextLength) {
        UI.showError(CONFIG.MESSAGES.errors.textTooShort);
        return false;
    }

    return true;
}

// COMUNICAÇÃO COM API
async function classifyEmail(text, file) {
    // Preparar FormData
    const formData = new FormData();
    if (file) formData.append('file', file);
    if (text) formData.append('text', text);

    try {
        console.log('Enviando para:', `${API_BASE_URL}/classify`);
        
        const response = await fetch(`${API_BASE_URL}/classify`, {
            method: 'POST',
            body: formData
        });

        console.log('Status:', response.status);

        // Tratar erros HTTP
        if (!response.ok) {
            const errorMessage = await handleAPIError(response);
            throw new Error(errorMessage);
        }

        // Parse da resposta
        const data = await response.json();
        console.log('Resposta recebida:', data);
        
        // Validar resposta
        if (!data.categoria || !data.razao || !data.resposta_sugerida) {
            throw new Error(CONFIG.MESSAGES.errors.incompleteResponse);
        }
        
        return data;

    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

async function handleAPIError(response) {
    let errorMessage = `Erro ${response.status}`;
    
    try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
    } catch (e) {
        try {
            errorMessage = await response.text() || errorMessage;
        } catch (e2) {
            // Manter mensagem padrão
        }
    }
    
    return errorMessage;
}

// TRATAMENTO DE ERROS
function handleError(error) {
    let errorMsg = CONFIG.MESSAGES.errors.unknown;
    
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        errorMsg = CONFIG.MESSAGES.errors.networkError;
    } else if (error.message.includes('500')) {
        errorMsg = CONFIG.MESSAGES.errors.serverError;
    } else if (error.message.includes('400')) {
        errorMsg = `${CONFIG.MESSAGES.errors.invalidData} ${error.message}`;
    } else {
        errorMsg = error.message;
    }
    
    UI.showError(errorMsg);
    UI.hideLoading();
    UI.showInitialState();
}

// HANDLER PRINCIPAL DE CLASSIFICAÇÃO
async function handleClassify() {
    const text = elements.emailText.value.trim();
    const file = elements.fileInput.files[0];

    // Validar entrada
    if (!validateInput(text, file)) {
        return;
    }

    // Preparar UI
    UI.hideError();
    UI.showLoading();

    try {
        // Classificar email
        const result = await classifyEmail(text, file);
        
        // Renderizar resultado
        UI.renderResult(result);
        
    } catch (error) {
        handleError(error);
    } finally {
        UI.hideLoading();
    }
}

// EVENT LISTENERS
function setupEventListeners() {
    // Contador de caracteres
    elements.emailText.addEventListener('input', UI.updateCharCount);

    // Upload de arquivo
    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            const file = e.target.files[0];
            UI.handleFileUpload(file);
        }
    });

    // Botão classificar
    elements.btn.addEventListener('click', handleClassify);

    // Copiar resposta
    elements.copyBtn.addEventListener('click', UI.copyResponse);

    // Enter para classificar (opcional)
    elements.emailText.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handleClassify();
        }
    });

    console.log('Event listeners configurados');
}

// INICIALIZAÇÃO DA APLICAÇÃO
function initializeApp() {
    console.log('========================================');
    console.log('Inicializando aplicação...');
    console.log('========================================');

    // Inicializar UI
    UI.initializeUI();

    // Configurar eventos
    setupEventListeners();

    console.log('========================================');
    console.log('Aplicação pronta para uso!');
    console.log('Dica: Pressione Ctrl+Enter para classificar rapidamente');
    console.log('========================================');
}

// EXECUTAR QUANDO DOM ESTIVER PRONTO
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

// Exportar para debug (opcional)
window.APP = {
    classifyEmail,
    validateInput,
    handleError
};