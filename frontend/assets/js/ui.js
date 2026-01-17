/**
 * Funções de Interface do Usuário
 * Gerencia visualização, animações e feedback visual
 */

// GERENCIAMENTO DE ERROS
function showError(msg) {
    elements.errorText.textContent = msg;
    elements.error.classList.remove('hidden');
    elements.error.classList.add('slide-in');
    
    // Auto-hide após timeout configurado
    setTimeout(hideError, CONFIG.TIMING.errorAutoHide);
    
    console.error('Erro exibido:', msg);
}

function hideError() {
    elements.error.classList.add('hidden');
}

// ESTADOS DA UI
function showLoading() {
    elements.initialState.classList.add('hidden');
    elements.result.classList.add('hidden');
    elements.loading.classList.remove('hidden');
    elements.btn.disabled = true;
    elements.btnText.textContent = CONFIG.MESSAGES.loading.processing;
}

function hideLoading() {
    elements.loading.classList.add('hidden');
    elements.btn.disabled = false;
    elements.btnText.textContent = 'Classificar Email';
}

function showInitialState() {
    elements.initialState.classList.remove('hidden');
    elements.result.classList.add('hidden');
    elements.loading.classList.add('hidden');
}

function showResult() {
    elements.initialState.classList.add('hidden');
    elements.loading.classList.add('hidden');
    elements.result.classList.remove('hidden');
    elements.result.classList.add('fade-in');
}

// RENDERIZAÇÃO DE RESULTADO
function renderResult(data) {
    hideLoading();
    showResult();

    // Renderizar categoria
    renderCategory(data.categoria);
    
    // Renderizar confiança
    renderConfidence(data.confianca);
    
    // Renderizar textos
    elements.razao.textContent = data.razao || 'Não informado';
    elements.resposta.textContent = data.resposta_sugerida || 'Não foi possível gerar uma resposta';
    
    console.log('Resultado renderizado:', data);
}

function renderCategory(categoria) {
    elements.catBadge.textContent = categoria;
    
    const categoryConfig = CONFIG.CATEGORIES[categoria] || CONFIG.CATEGORIES.Erro;
    
    elements.catBadge.className = `px-4 py-1.5 rounded-full text-sm font-bold shadow-sm ${categoryConfig.bg} ${categoryConfig.text} border ${categoryConfig.border}`;
}

function renderConfidence(confianca) {
    const confValue = parseInt(confianca) || 0;
    elements.confValor.textContent = `${confValue}%`;
    
    // Animação da barra com delay para efeito visual
    setTimeout(() => {
        elements.confBarra.style.width = `${confValue}%`;
        
        // Cor dinâmica baseada no nível
        let colorClass;
        if (confValue >= CONFIG.CONFIDENCE.high.threshold) {
            colorClass = CONFIG.CONFIDENCE.high.color;
        } else if (confValue >= CONFIG.CONFIDENCE.medium.threshold) {
            colorClass = CONFIG.CONFIDENCE.medium.color;
        } else {
            colorClass = CONFIG.CONFIDENCE.low.color;
        }
        
        elements.confBarra.className = `progress-bar ${colorClass} h-2.5 rounded-full`;
    }, CONFIG.TIMING.progressBarAnimation);
}

// CONTADOR DE CARACTERES
function updateCharCount() {
    const count = elements.emailText.value.length;
    elements.charCount.textContent = count;
    
    // Aviso visual quando próximo do limite
    if (count > CONFIG.LIMITS.charWarningThreshold) {
        elements.charCount.classList.add('text-red-500', 'font-bold');
    } else {
        elements.charCount.classList.remove('text-red-500', 'font-bold');
    }
}

// UPLOAD DE ARQUIVO
function handleFileUpload(file) {
    const fileName = file.name;
    const fileSize = (file.size / 1024).toFixed(1);
    
    // Verificar tamanho
    if (file.size > CONFIG.LIMITS.maxFileSize) {
        showError(CONFIG.MESSAGES.errors.fileTooLarge);
        resetFileLabel();
        return false;
    }
    
    // Atualizar label
    elements.fileLabel.innerHTML = `📎 ${fileName} <span class="text-xs text-gray-400">(${fileSize}KB)</span>`;
    elements.fileLabel.classList.add('text-blue-600', 'font-bold');
    
    console.log(`Arquivo carregado: ${fileName} (${fileSize}KB)`);
    return true;
}

function resetFileLabel() {
    elements.fileInput.value = '';
    elements.fileLabel.innerHTML = '<span class="block text-2xl mb-2">📄</span><span class="text-sm">Clique ou arraste um arquivo (.txt/.pdf)</span>';
    elements.fileLabel.classList.remove('text-blue-600', 'font-bold');
}

function copyResponse() {
    const texto = elements.resposta.textContent;
    
    navigator.clipboard.writeText(texto)
        .then(() => {
            alert(CONFIG.MESSAGES.success.copied);
            console.log('Texto copiado para clipboard');
        })
        .catch(err => {
            console.error('Erro ao copiar:', err);
            alert('Não foi possível copiar o texto');
        });
}

function initializeUI() {
    // Verificar API periodicamente
    setInterval(CONFIG.TIMING.healthCheckInterval);
    
    console.log('UI inicializada');
}

// Exportar funções para uso global
window.UI = {
    showError,
    hideError,
    showLoading,
    hideLoading,
    showInitialState,
    showResult,
    renderResult,
    updateCharCount,
    handleFileUpload,
    resetFileLabel,
    copyResponse,
    initializeUI
};