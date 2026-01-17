import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# CONFIGURAÇÃO DE LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# CARREGAMENTO DE VARIÁVEIS DE AMBIENTE
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY não configurada no arquivo .env")
    raise RuntimeError("OPENAI_API_KEY ausente. Crie um arquivo .env com sua chave da OpenAI")

# CLIENTE OPENAI
client = OpenAI(api_key=OPENAI_API_KEY)
logger.info("Cliente OpenAI configurado com sucesso")

# CONSTANTES DA APLICAÇÃO
MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_TEXT_LENGTH = 4000
MIN_TEXT_LENGTH = 10

logger.info(f"  Configurações carregadas:")
logger.info(f"   - MAX_FILE_SIZE: {MAX_FILE_SIZE // (1024*1024)}MB")
logger.info(f"   - MAX_TEXT_LENGTH: {MAX_TEXT_LENGTH} chars")
logger.info(f"   - MIN_TEXT_LENGTH: {MIN_TEXT_LENGTH} chars")