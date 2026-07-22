try:
    import pandas as pd
except Exception:
    # Fallback lightweight DataFrame-like implementation when pandas is unavailable.
    import csv

    class SimpleDataFrame:
        def __init__(self, rows, columns):
            self._rows = rows
            self._columns = columns

        def iterrows(self):
            for i, row in enumerate(self._rows):
                yield i, row

        def __len__(self):
            return len(self._rows)

        def __getitem__(self, key):
            # return list of column values
            return [row.get(key) for row in self._rows]

    class pd:  # minimal namespace compatible with code below
        @staticmethod
        def read_csv(path):
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = [row for row in reader]
                return SimpleDataFrame(rows, reader.fieldnames)
from loguru import logger
from app.ai_engine.rag.retriever import Retriever

def evaluate_medical_qa():
    logger.info("Loading Architha's Medical QA Dataset...")
    df = pd.read_csv('medical_qa_dataset.csv')
    
    retriever = Retriever()
    correct_retrievals = 0
    total_tests = len(df)
    
    for idx, row in df.iterrows():
        question = row['Question']
        expected_source = row['Expected_Source']
        
        # Retrieve top document chunks
        results = retriever.retrieve(query=question, top_k=3)
        
        # Check if the expected source appears in the retrieved documents
        retrieved_sources = [res.document.source.upper() for res in results]
        
        match_found = any(expected_source.upper() in src for src in retrieved_sources)
        if match_found:
            correct_retrievals += 1
            
        if idx % 50 == 0:
            logger.info(f"Progress: {idx}/{total_tests} evaluated...")
            
    accuracy = correct_retrievals / total_tests
    logger.info(f"QA Retrieval Evaluation Complete. Accuracy: {accuracy * 100:.2f}%")
    return accuracy

if __name__ == "__main__":
    evaluate_medical_qa()