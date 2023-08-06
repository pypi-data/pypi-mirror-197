def check_embedding_extractor(embedding_extractor, embedding_extractor_acceptable_list=None):
    if embedding_extractor_acceptable_list is None:
        embedding_extractor_acceptable_list = ["hf", "openai"]

    if not isinstance(embedding_extractor, str):
        raise Exception("Embedding Extractor must be a string")

    if embedding_extractor not in embedding_extractor_acceptable_list:

        raise Exception(f"Embedding Extractor is not allowed. "
                        f"Please choose one of : {embedding_extractor_acceptable_list}")
