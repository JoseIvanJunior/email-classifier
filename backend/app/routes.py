from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import logging

from app.services.file_service import extract_text_from_file
from app.services.ai_service import analyze_with_gpt
from app.config import MAX_FILE_SIZE, MIN_TEXT_LENGTH

logger = logging.getLogger(__name__)

router = APIRouter()

# Modelos Pydantic para documentação automática
class ClassificationResponse(BaseModel):
    """Modelo de resposta da classificação"""
    categoria: str = Field(..., description="Categoria do email: Produtivo, Improdutivo ou Erro")
    confianca: int = Field(..., ge=0, le=100, description="Nível de confiança da classificação (0-100)")
    razao: str = Field(..., description="Explicação técnica da classificação")
    resposta_sugerida: str = Field(..., description="Resposta sugerida para o email")

class ErrorResponse(BaseModel):
    """Modelo de resposta de erro"""
    detail: str = Field(..., description="Descrição do erro")
    status_code: int = Field(..., description="Código HTTP do erro")

@router.post(
    "/classify",
    response_model=ClassificationResponse,
    responses={
        200: {
            "description": "Classificação realizada com sucesso",
            "model": ClassificationResponse
        },
        400: {
            "description": "Dados de entrada inválidos",
            "model": ErrorResponse
        },
        500: {
            "description": "Erro interno do servidor",
            "model": ErrorResponse
        }
    },
    summary="Classificar Email",
    description="Analisa e classifica um email usando IA (GPT-3.5-turbo)"
)
async def classify_email(
    text: Optional[str] = Form(
        None, 
        description="Texto do email a ser classificado",
        max_length=5000
    ),
    file: Optional[UploadFile] = File(
        None,
        description="Arquivo PDF ou TXT contendo o email"
    )
):
    """
    ## Classificação Inteligente de Emails
    
    Este endpoint recebe um email (via texto ou arquivo) e retorna:
    - Categoria (Produtivo/Improdutivo)
    - Nível de confiança (0-100%)
    - Razão da classificação
    - Resposta sugerida
    
    ### Parâmetros:
    - **text**: Texto do email (opcional se enviar arquivo)
    - **file**: Arquivo PDF ou TXT (opcional se enviar texto)
    
    ### Retorno:
    ```json
    {
      "categoria": "Produtivo",
      "confianca": 95,
      "razao": "Email contém solicitação clara de pagamento",
      "resposta_sugerida": "Olá! Vou processar o pagamento..."
    }
    ```
    """
    
    logger.info("Nova requisição de classificação recebida")
    
    # 1. Validação de entrada
    if not text and not file:
        logger.warning("Requisição sem texto nem arquivo")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Por favor, envie um texto ou selecione um arquivo (.txt ou .pdf)"
        )
    
    # 2. Extração de texto
    final_text = ""
    
    try:
        if file:
            # Validação do tipo de arquivo
            allowed_extensions = [".pdf", ".txt"]
            file_ext = file.filename.split(".")[-1].lower()
            
            if f".{file_ext}" not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Tipo de arquivo não suportado. Use: {', '.join(allowed_extensions)}"
                )
            
            # Validação do tamanho
            file.file.seek(0, 2)
            size = file.file.tell()
            file.file.seek(0)
            
            logger.info(f"Arquivo recebido: {file.filename} ({size} bytes)")
            
            if size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE // (1024*1024)}MB"
                )
            
            final_text = extract_text_from_file(file)
            
        elif text:
            final_text = text.strip()
            logger.info(f"Texto recebido: {len(final_text)} caracteres")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar entrada: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar entrada: {str(e)}"
        )
    
    # 3. Tratamento de texto insuficiente (Failover)
    if not final_text or len(final_text) < MIN_TEXT_LENGTH:
        logger.warning("Texto insuficiente - Ativando failover")
        
        failover_response = {
            "categoria": "Improdutivo",
            "confianca": 100,
            "razao": "O conteúdo enviado não contém texto suficiente para análise. Pode ser uma imagem digitalizada ou arquivo sem texto selecionável.",
            "resposta_sugerida": "O sistema não conseguiu extrair texto do arquivo. Por favor, verifique o conteúdo e tente novamente com um arquivo que contenha texto selecionável."
        }
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=failover_response
        )
    
    # 4. Processamento com IA
    try:
        logger.info("Enviando para análise da IA...")
        result = analyze_with_gpt(final_text)
        
        logger.info(f"Classificação concluída: {result['categoria']} ({result['confianca']}%)")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )
        
    except Exception as e:
        logger.error(f"Erro na análise IA: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar com IA. Verifique sua API Key da OpenAI e tente novamente."
        )