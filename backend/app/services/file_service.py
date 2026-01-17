import logging
from fastapi import UploadFile
from pypdf import PdfReader
from pypdf.errors import PdfReadError

logger = logging.getLogger(__name__)

def extract_text_from_file(file: UploadFile) -> str:
    try:
        file.file.seek(0)

        if file.filename.lower().endswith(".pdf"):
            reader = PdfReader(file.file)
            text = ""

            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"

            return text.strip()

        elif file.filename.lower().endswith(".txt"):
            raw = file.file.read()
            for enc in ("utf-8", "latin-1", "cp1252"):
                try:
                    return raw.decode(enc).strip()
                except UnicodeDecodeError:
                    continue
            return ""

        return ""

    except PdfReadError:
        logger.error("Erro ao ler PDF")
        return ""
    except Exception as e:
        logger.error(f"Erro arquivo: {e}")
        return ""
