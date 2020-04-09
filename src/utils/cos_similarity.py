from numpy import dot
from numpy.linalg import norm
from numpy import ndarray


def cosine_similarity(vect1: ndarray, vect2: ndarray) -> float:
    div = norm(vect1) * norm(vect2)

    if div == 0:
        print("************************")
        print(vect1)
        print(vect2)
        print("************************")

    return dot(vect1, vect2) / div