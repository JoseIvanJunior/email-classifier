/**
 * Referências dos Elementos do DOM
 * Centraliza todos os getElementById em um único lugar
 */

const elements = {

    // ENTRADA
    fileInput: document.getElementById('fileInput'),
    fileLabel: document.getElementById('fileLabel'),
    emailText: document.getElementById('emailText'),
    charCount: document.getElementById('charCount'),
    

    // CONTROLES
    btn: document.getElementById('classifyBtn'),
    btnText: document.getElementById('btnText'),
    copyBtn: document.getElementById('copyBtn'),
    

    // FEEDBACK E STATUS
    error: document.getElementById('errorMsg'),
    errorText: document.getElementById('errorText'),
    

    // ESTADOS DA UI
    initialState: document.getElementById('initialState'),
    loading: document.getElementById('loadingState'),
    result: document.getElementById('resultContent'),
    

    // RESULTADO
    catBadge: document.getElementById('resCategoria'),
    confValor: document.getElementById('resConfiancaValor'),
    confBarra: document.getElementById('resConfiancaBarra'),
    razao: document.getElementById('resRazao'),
    resposta: document.getElementById('resResposta')
};


// VALIDAÇÃO (Verifica se todos os elementos existem)
const validateElements = () => {
    const missing = [];
    
    for (const [key, element] of Object.entries(elements)) {
        if (!element) {
            missing.push(key);
        }
    }
    
    if (missing.length > 0) {
        console.error('Elementos não encontrados no DOM:', missing);
        return false;
    }
    
    console.log('Todos os elementos do DOM carregados com sucesso');
    return true;
};

// Executar validação
validateElements();

// Exportar para uso global
window.elements = elements;