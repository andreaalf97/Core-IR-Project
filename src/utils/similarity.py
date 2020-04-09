import numpy as np
from src.utils.cos_similarity import cosine_similarity


def early_fusion(table_terms: list, query_terms: list, vector_size=300) -> float:
    table_avg = np.zeros(vector_size)
    for term in table_terms:
        table_avg += term.vector

    table_avg /= len(table_terms)

    query_avg = np.zeros(vector_size)
    for term in query_terms:
        query_avg += term.vector

    query_avg /= len(query_terms)
    return cosine_similarity(table_avg, query_avg)


def fusion(table_terms: list, query_terms: list, vector_size=300) -> dict:

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

            if np.linalg.norm(table_term.vector) == 0:
                print(table_term)
                exit(-1)
            if np.linalg.norm(query_term.vector) == 0:
                print(query_term)
                exit(-1)

            similarity = cosine_similarity(table_term.vector, query_term.vector)
            sum += similarity
            counter += 1
            if similarity > max_sim:
                max_sim = similarity

    similarities["late-max"] = max_sim
    similarities["late-sum"] = sum
    similarities["late-avg"] = sum / counter
    return similarities
