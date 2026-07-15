import logging
import hashlib
from typing import List


from qdrant_client import QdrantClient

from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    PointIdsList,
)


from app.ai_engine.rag.embedding_service import EmbeddingService

from app.ai_engine.rag.schemas import (
    MedicalDocument,
    SearchResult,
)



logger = logging.getLogger(__name__)




class VectorStore:
    """
    Production Qdrant Vector Store.

    Responsibilities:

    - Create collection
    - Generate embeddings
    - Store medical knowledge
    - Semantic similarity retrieval
    - Delete documents


    Architecture:

    Medical Documents
            |
            v
    Embedding Engine
            |
            v
    Qdrant Vector Database
            |
            v
    RAG Retriever

    """



    COLLECTION_NAME = "clinical_medical_knowledge"



    def __init__(
        self,
        host="localhost",
        port=6333,
    ):


        self.embedding_engine = EmbeddingService()


        self.client = QdrantClient(

            host=host,

            port=port

        )


        self._create_collection()





    # ==================================================
    # Generate Stable Qdrant ID
    # ==================================================

    def _generate_point_id(
        self,
        document_id
    ):


        if isinstance(document_id, int):

            return document_id



        hash_value = hashlib.sha256(

            str(document_id).encode()

        ).hexdigest()



        return int(

            hash_value[:15],

            16

        )






    # ==================================================
    # Collection Creation
    # ==================================================

    def _create_collection(self):


        try:


            collections = (

                self.client
                .get_collections()
                .collections

            )


            exists = any(

                collection.name == self.COLLECTION_NAME

                for collection in collections

            )



            if not exists:


                logger.info(

                    "Creating Qdrant collection: %s",

                    self.COLLECTION_NAME

                )



                self.client.create_collection(


                    collection_name=self.COLLECTION_NAME,


                    vectors_config=VectorParams(

                        size=self.embedding_engine.dimension,

                        distance=Distance.COSINE

                    )

                )



                logger.info(
                    "Qdrant collection created"
                )



        except Exception as e:


            logger.exception(

                "Collection creation failed: %s",

                e

            )

            raise






    # ==================================================
    # Add Single Document
    # ==================================================

    def add_document(
        self,
        document: MedicalDocument
    ):


        vector = self.embedding_engine.embed_document(

            document.content

        )



        point = PointStruct(


            id=self._generate_point_id(

                document.id

            ),


            vector=vector,


            payload={


                "document_id":
                str(document.id),


                "title":
                document.title,


                "category":
                document.category,


                "source":
                document.source,


                "content":
                document.content

            }

        )



        self.client.upsert(


            collection_name=self.COLLECTION_NAME,


            points=[point]

        )



        logger.info(

            "Document indexed: %s",

            document.title

        )






    # ==================================================
    # Bulk Document Insert
    # ==================================================

    def add_documents(

        self,

        documents: List[MedicalDocument]

    ):



        if not documents:

            return



        vectors = self.embedding_engine.embed_documents(


            [

                doc.content

                for doc in documents

            ]

        )



        points = []



        for document, vector in zip(

            documents,

            vectors

        ):



            points.append(


                PointStruct(

                    id=self._generate_point_id(

                        document.id

                    ),


                    vector=vector,


                    payload={


                        "document_id":
                        str(document.id),


                        "title":
                        document.title,


                        "category":
                        document.category,


                        "source":
                        document.source,


                        "content":
                        document.content


                    }

                )

            )



        self.client.upsert(


            collection_name=self.COLLECTION_NAME,


            points=points

        )



        logger.info(

            "%s documents indexed",

            len(points)

        )







    # ==================================================
    # Semantic Search
    # ==================================================

    def similarity_search(

        self,

        query: str,

        top_k: int = 5

    ) -> List[SearchResult]:



        try:


            query_vector = self.embedding_engine.embed_query(

                query

            )



            response = self.client.query_points(


                collection_name=self.COLLECTION_NAME,


                query=query_vector,


                limit=top_k


            )



            results = response.points



            output = []



            for result in results:



                payload = result.payload or {}



                document = MedicalDocument(


                    id=payload.get(

                        "document_id"

                    ),


                    title=payload.get(

                        "title",

                        "Unknown"

                    ),


                    category=payload.get(

                        "category",

                        "medical"

                    ),


                    source=payload.get(

                        "source",

                        "unknown"

                    ),


                    content=payload.get(

                        "content",

                        ""

                    )

                )



                output.append(


                    SearchResult(


                        document=document,


                        similarity_score=result.score


                    )

                )



            return output



        except Exception as e:


            logger.exception(

                "Semantic search failed: %s",

                e

            )


            return []







    # ==================================================
    # Backward Compatibility
    # ==================================================

    def search(

        self,

        query: str,

        top_k: int = 5

    ):


        return self.similarity_search(

            query=query,

            top_k=top_k

        )







    # ==================================================
    # Delete Document
    # ==================================================

    def delete(

        self,

        document_id

    ):



        point_id = self._generate_point_id(

            document_id

        )



        self.client.delete(


            collection_name=self.COLLECTION_NAME,


            points_selector=PointIdsList(

                points=[point_id]

            )

        )



        logger.info(

            "Deleted document: %s",

            document_id

        )