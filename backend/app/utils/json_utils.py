import json
import logging

logger = logging.getLogger(__name__)

def clean_and_parse_json(text: str) -> dict:
    """
    Remove marcações markdown e faz parse de JSON retornado pela IA.
    
    Args:
        text (str): String JSON possivelmente com ```json ou ```
        
    Returns:
        dict: Dicionário parseado ou dict de erro caso falhe
    """
    try:
        # Remove marcações de código markdown se existirem
        clean = text.replace("```json", "").replace("```", "").strip()
        
        # Parse do JSON
        return json.loads(clean)
        
    except json.JSONDecodeError as e:
        logger.warning(f"Erro ao fazer parse do JSON da IA: {e}")
        logger.warning(f"Texto recebido: {text[:200]}...")
        
        # Retorna estrutura de erro padrão
        return {
            "categoria": "Erro",
            "confianca": 0,
            "razao": "Resposta inválida da IA - formato JSON incorreto",
            "resposta_sugerida": "Tente novamente. Se o erro persistir, verifique a configuração da API."
        }
    except Exception as e:
        logger.error(f"Erro inesperado ao processar JSON: {e}")
        return {
            "categoria": "Erro",
            "confianca": 0,
            "razao": f"Erro ao processar resposta: {str(e)}",
            "resposta_sugerida": "Tente novamente."
        }