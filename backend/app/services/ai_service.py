import logging
import re
from app.config import client, MAX_TEXT_LENGTH
from app.utils.json_utils import clean_and_parse_json

logger = logging.getLogger(__name__)

def analyze_with_gpt(text: str) -> dict:
    """
    Analisa o texto do email usando GPT-3.5-turbo e retorna a classificação.
    
    Args:
        text (str): Texto do email a ser analisado
        
    Returns:
        dict: Dicionário com categoria, confianca, razao e resposta_sugerida
    """
    
    # 1. Preparação do Texto
    truncated = text[:MAX_TEXT_LENGTH]
    text_len = len(text.strip())
    
    logger.info(f"Analisando texto com {text_len} caracteres (truncado: {len(truncated)})")

    # 2. Engenharia de Prompt APRIMORADA
    prompt = f"""
    Você é um classificador sênior de emails corporativos. Analise o texto abaixo.

    TEXTO:
    \"\"\"{truncated}\"\"\"

    REGRAS DE CLASSIFICAÇÃO:
    - "Produtivo": Requer ação, suporte, dúvidas, pagamentos, relatórios, solicitações técnicas, testes de API/sistema, desenvolvimento.
    - "Improdutivo": Apenas saudações, spam, agradecimentos vagos ou conteúdo ilegível.

    CRITÉRIOS DE CONFIANÇA APRIMORADOS (0-100%):
    
    ALTA CONFIANÇA (85-100%):
    - Verbos de ação claros: "Pagar", "Resolver", "Testar", "Desenvolver", "Implementar", "Corrigir"
    - Termos técnicos específicos: "API", "código", "bug", "erro", "sistema", "banco de dados"
    - Valores monetários ou datas específicas
    - Solicitações explícitas mesmo que curtas
    
    MÉDIA CONFIANÇA (60-84%):
    - Contexto financeiro/corporativo sem ação explícita
    - Menção a processos sem urgência clara
    - Termos genéricos de negócio
    
    BAIXA CONFIANÇA (0-59%):
    - Apenas fragmentos sem contexto ("Segue anexo", "Ok")
    - Texto ambíguo ou ilegível
    - Saudações isoladas

    IMPORTANTE: 
    - Textos curtos (menos de 50 chars) MAS com termos técnicos específicos ou ações claras DEVEM ter confiança ALTA (85%+)
    - A brevidade não é problema se o conteúdo é claro e objetivo
    - "Testar API", "corrigir bug", "pagar fatura" são exemplos de textos curtos mas com alta confiança

    Retorne APENAS JSON:
    {{
      "categoria": "Produtivo" ou "Improdutivo",
      "confianca": (inteiro 0-100),
      "razao": "Explicação técnica e direta.",
      "resposta_sugerida": "Resposta formal e direta."
    }}
    """

    try:
        logger.info("Enviando requisição para OpenAI GPT-3.5-turbo...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )

        raw_content = response.choices[0].message.content
        logger.info(f"Resposta recebida da OpenAI")
        
        parsed = clean_and_parse_json(raw_content)

        # 3. Lógica de Pós-Processamento INTELIGENTE
        categoria = parsed.get("categoria", "Indefinido")
        confianca = int(parsed.get("confianca", 0))
        
        logger.info(f"Classificação inicial: {categoria} ({confianca}%)")
        
        # Lógica de Análise Semântica
        # Palavras-chave que indicam ALTA importância mesmo em textos curtos
        keywords_alta_importancia = {
            'acao': ['pagar', 'resolver', 'corrigir', 'implementar', 'desenvolver', 'testar', 
                     'configurar', 'instalar', 'atualizar', 'revisar', 'analisar', 'verificar'],
            'tecnico': ['api', 'bug', 'erro', 'sistema', 'código', 'deploy', 'servidor', 
                        'banco', 'dados', 'endpoint', 'request', 'response', 'integração'],
            'financeiro': ['pagar', 'fatura', 'boleto', 'pagamento', 'valor', 'r$', 'reais', 
                          'débito', 'crédito', 'cobrança', 'pendência'],
            'urgencia': ['urgente', 'imediato', 'asap', 'prioritário', 'crítico', 'bloqueio']
        }
        
        texto_lower = text.lower()
        
        # Contadores de palavras-chave por categoria
        score_acao = sum(1 for word in keywords_alta_importancia['acao'] if word in texto_lower)
        score_tecnico = sum(1 for word in keywords_alta_importancia['tecnico'] if word in texto_lower)
        score_financeiro = sum(1 for word in keywords_alta_importancia['financeiro'] if word in texto_lower)
        score_urgencia = sum(1 for word in keywords_alta_importancia['urgencia'] if word in texto_lower)
        
        score_total = score_acao + score_tecnico + score_financeiro + score_urgencia
        
        logger.info(f"Análise semântica: ação={score_acao}, técnico={score_tecnico}, "
                   f"financeiro={score_financeiro}, urgência={score_urgencia}, total={score_total}")
        
        # Detectar valores monetários
        tem_valor_monetario = bool(re.search(r'r\$\s*\d+|reais|\d+[.,]\d+', texto_lower))
        
        # Detectar datas
        tem_data = bool(re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}/\d{1,2}', texto_lower))
        
        # REGRAS DE AJUSTE DE CONFIANÇA        
        ajuste_aplicado = False
        razao_ajuste = ""
        
        # REGRA 1: Texto curto MAS com conteúdo relevante
        if text_len < 50:
            if score_total >= 2 or tem_valor_monetario or (score_acao >= 1 and score_tecnico >= 1):
                # Texto curto mas objetivo e claro
                if confianca < 85:
                    confianca_antiga = confianca
                    confianca = 85
                    ajuste_aplicado = True
                    razao_ajuste = f" (Confiança aumentada de {confianca_antiga}% para {confianca}% devido a termos específicos e objetivos apesar da brevidade)"
                    logger.info(f"BOOST aplicado: {confianca_antiga}% → {confianca}% (texto curto mas objetivo)")
            
            elif score_total == 0 and confianca > 20:
                # Texto curto E genérico
                confianca_antiga = confianca
                confianca = 20
                ajuste_aplicado = True
                razao_ajuste = f" (Confiança ajustada de {confianca_antiga}% para {confianca}% devido à brevidade e falta de contexto)"
                logger.info(f"Penalidade aplicada: {confianca_antiga}% → {confianca}% (texto curto e genérico)")
        
        # REGRA 2: Produtivo com múltiplos indicadores fortes
        elif categoria == "Produtivo" and (score_total >= 3 or (tem_valor_monetario and score_acao >= 1)):
            if confianca < 90:
                confianca_antiga = confianca
                confianca = min(95, confianca + 15)  # Boost mas com teto
                ajuste_aplicado = True
                razao_ajuste = f" (Confiança aumentada de {confianca_antiga}% para {confianca}% devido a múltiplos indicadores de importância)"
                logger.info(f"BOOST aplicado: {confianca_antiga}% → {confianca}% (múltiplos indicadores)")
        
        # REGRA 3: Produtivo com urgência explícita
        elif categoria == "Produtivo" and score_urgencia >= 1:
            if confianca < 90:
                confianca_antiga = confianca
                confianca = max(90, confianca)
                ajuste_aplicado = True
                razao_ajuste = f" (Confiança ajustada para {confianca}% devido a indicadores de urgência)"
                logger.info(f"Urgência detectada: confiança → {confianca}%")
        
        # REGRA 4: Improdutivo muito curto
        if categoria == "Improdutivo" and text_len < 30:
            if confianca < 95:
                confianca = 95
                ajuste_aplicado = True
                logger.info(f"Improdutivo curto confirmado: confiança → {confianca}%")
        
        # Adicionar razão do ajuste se aplicado
        if ajuste_aplicado and razao_ajuste:
            parsed["razao"] += razao_ajuste

        # Ajustar resposta sugerida para Improdutivos muito curtos
        if categoria == "Improdutivo" and text_len < 30:
            parsed["resposta_sugerida"] = "Nenhuma ação necessária."

        # Retorno Normalizado
        result = {
            "categoria": categoria,
            "confianca": min(100, max(0, confianca)),  # Garante 0-100
            "razao": parsed.get("razao", "Sem explicação."),
            "resposta_sugerida": parsed.get("resposta_sugerida", "Analisar manualmente.")
        }
        
        logger.info(f"Classificação final: {result['categoria']} ({result['confianca']}%)")
        
        return result

    except Exception as e:
        logger.error(f"Erro ao processar com IA: {str(e)}")
        return {
            "categoria": "Erro",
            "confianca": 0,
            "razao": f"Falha técnica na consulta à IA: {str(e)}",
            "resposta_sugerida": "Tente novamente mais tarde ou verifique a configuração da API."
        }