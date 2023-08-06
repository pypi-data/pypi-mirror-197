from knowledgegpt.extractors.base_extractor import BaseExtractor

from knowledgegpt.utils.utils_pdf import process_pdf, process_pdf_page
from io import BytesIO


class PDFExtractor(BaseExtractor):
    def __init__(self, pdf_file_path: str, extraction_type: str = "page", embedding_extractor: str = "hf",
                 model_lang: str = "en", is_turbo: bool = False):
        """
        Extracts paragraphs from a PDF file and computes embeddings for each paragraph,
        then answers a query using the embeddings.
        """
        super().__init__(embedding_extractor=embedding_extractor, model_lang=model_lang, is_turbo=is_turbo)

        self.pdf_file_path = pdf_file_path
        self.extraction_type = extraction_type

    def prepare_df(self):
        if self.df is None:
            if not self.verbose:
                print("Processing PDF file...")
                print("Extracting paragraphs...")
            with open(self.pdf_file_path, "rb") as f:
                pdf_file = BytesIO(f.read())

            if pdf_file.getvalue()[:4] != b'%PDF':
                raise ValueError("Only PDF files are allowed")

            if self.extraction_type == "page":
                self.df = process_pdf_page(pdf_file)
            else:
                self.df = process_pdf(pdf_file)
