import logging
import hashlib
from typing import List


from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)




class EmbeddingEngine:


    """
    Production Embedding Engine.

    Responsibilities:

    Text
      ↓
    Embedding Model
      ↓
    Vector Representation

    Features:

    - Configurable model
    - GPU support
    - Batch processing
    - Embedding cache
    - Normalized vectors
    """



    DEFAULT_MODEL = "all-MiniLM-L6-v2"



    def __init__(

        self,

        model_name: str | None = None,

        device: str | None = None,

    ):


        self.model_name = (

            model_name

            or self.DEFAULT_MODEL

        )


        self.device = device


        self.cache = {}



        logger.info(

            f"Loading embedding model: {self.model_name}"

        )



        try:


            self.model = SentenceTransformer(

                self.model_name,

                device=self.device

            )


            logger.info(

                "Embedding model loaded successfully"

            )


        except Exception as error:


            logger.exception(

                "Failed loading embedding model"

            )

            raise error





    def _hash_text(

        self,

        text: str

    ) -> str:


        return hashlib.sha256(

            text.encode(

                "utf-8"

            )

        ).hexdigest()





    def embed_text(

        self,

        text: str

    ) -> List[float]:


        if not text.strip():

            raise ValueError(

                "Input text cannot be empty"

            )



        cache_key = self._hash_text(

            text

        )



        # -------------------------
        # Cache Lookup
        # -------------------------

        if cache_key in self.cache:


            logger.debug(

                "Returning cached embedding"

            )


            return self.cache[cache_key]




        embedding = self.model.encode(

            text,

            convert_to_numpy=True,

            normalize_embeddings=True,

        )



        vector = embedding.tolist()



        self.cache[cache_key] = vector



        return vector





    def embed(

        self,

        text: str

    ) -> List[float]:


        return self.embed_text(

            text

        )






    def embed_batch(

        self,

        texts: List[str],

        batch_size: int = 32,

    ) -> List[List[float]]:


        if not texts:


            raise ValueError(

                "Text list cannot be empty"

            )



        embeddings = self.model.encode(

            texts,

            batch_size=batch_size,

            convert_to_numpy=True,

            normalize_embeddings=True,

            show_progress_bar=False,

        )



        return embeddings.tolist()





    def get_dimension(

        self

    ) -> int:


        return self.model.get_embedding_dimension()





    def get_model_name(

        self

    ) -> str:


        return self.model_name