import numpy as np
from src.utils.cos_similarity import cosine_similarity
from spacy.tokens.token import Token
from numpy import ndarray


def early_fusion(table_terms: list, query_terms: list, vector_size=300) -> float:
    '''
    DO NOT use this function directly, it is only part of 'fusion' function
    This function computes the early similarity measure.
    table_terms and query_terms must be of type numpy.ndarray
    '''
    table_avg = np.zeros(vector_size)
    for term in table_terms:
        table_avg += term

    table_avg /= len(table_terms)

    query_avg = np.zeros(vector_size)
    for term in query_terms:
        query_avg += term

    query_avg /= len(query_terms)
    return cosine_similarity(table_avg, query_avg)


def fusion(table_terms: list, query_terms: list, vector_size=300) -> dict:
    '''
    This function returns the similarity of the two lists using different measures
    Returns a dictionary with keys ["early", "late-max", "late-sum", "late-avg"]
    '''
    if len(table_terms) == 0 or len(query_terms) == 0:
        return {
            "early": 0.0,
            "late-max": 0.0,
            "late-sum": 0.0,
            "late-avg": 0.0
        }

    if type(table_terms[0]) == Token:
        table_terms = [term.vector for term in table_terms]

    if type(query_terms[0]) == Token:
        query_terms = [term.vector for term in query_terms]

    if type(table_terms[0]) != ndarray:
        raise Exception("table_terms should be of type ndarray")
    if type(query_terms[0]) != ndarray:
        raise Exception("query_terms should be of type ndarray")

    similarities: dict = {
        "early": early_fusion(table_terms, query_terms, vector_size=vector_size),
        "late-max": 0.0,
        "late-sum": 0.0,
        "late-avg": 0.0
    }

    max_sim: float = -100.0
    sum: float = 0.0
    counter: int = 0

    for table_term in table_terms:
        for query_term in query_terms:

            if np.linalg.norm(table_term) == 0:
                print(table_term)
                exit(-1)
            if np.linalg.norm(query_term) == 0:
                print(query_term)
                exit(-1)

            similarity = cosine_similarity(table_term, query_term)
            sum += similarity
            counter += 1
            if similarity > max_sim:
                max_sim = similarity

    similarities["late-max"] = max_sim
    similarities["late-sum"] = sum
    similarities["late-avg"] = sum / counter
    return similarities
