def calculate_precision(true_positives: int, false_positives: int) -> float:
    if true_positives + false_positives == 0:
        return 0.0
    return true_positives / (true_positives + false_positives)

def calculate_recall(true_positives: int, false_negatives: int) -> float:
    if true_positives + false_negatives == 0:
        return 0.0
    return true_positives / (true_positives + false_negatives)

def calculate_f1_score(precision: float, recall: float) -> float:
    if precision + recall == 0.0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def calculate_accuracy(correct: int, total: int) -> float:
    if total == 0:
        return 0.0
    return correct / total

def evaluate_ner(extracted_entities: set, expected_entities: set) -> dict:
    """
    Evaluates Named Entity Recognition (NER) performance.
    """
    tp = len(extracted_entities.intersection(expected_entities))
    fp = len(extracted_entities - expected_entities)
    fn = len(expected_entities - extracted_entities)
    
    precision = calculate_precision(tp, fp)
    recall = calculate_recall(tp, fn)
    f1 = calculate_f1_score(precision, recall)
    
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }
