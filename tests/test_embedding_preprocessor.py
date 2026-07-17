import pytest
from app.rag.embedding_preprocessor import preprocess_for_embeddings

def test_abbreviation_expansion():
    text = "The Pt has a Hx of HTN and T2DM."
    expected = "The Patient has a History of Hypertension and Type 2 Diabetes Mellitus."
    assert preprocess_for_embeddings(text) == expected

def test_unit_standardization():
    text = "Take 10mgs PO BID."
    expected = "Take 10 mg By mouth Twice a day."
    assert preprocess_for_embeddings(text) == expected

    text2 = "Patient needs 50mcgs of medication."
    expected2 = "Patient needs 50 mcg of medication."
    assert preprocess_for_embeddings(text2) == expected2

def test_spacing_normalization():
    text = "Administer 50mg of drug."
    expected = "Administer 50 mg of drug."
    assert preprocess_for_embeddings(text) == expected

def test_case_preservation():
    # Only exact case matches for abbreviations will expand.
    # We don't expand "htn", only "HTN".
    text = "this is lower case htn."
    expected = "this is lower case htn."
    assert preprocess_for_embeddings(text) == expected
    
    # "T" should expand to "Temperature"
    text2 = "The T was normal."
    expected2 = "The Temperature was normal."
    assert preprocess_for_embeddings(text2) == expected2
    
    # "t" should NOT expand
    text3 = "Don't expand this t character."
    assert preprocess_for_embeddings(text3) == text3

def test_empty_string():
    assert preprocess_for_embeddings("") == ""
    assert preprocess_for_embeddings(None) == None
