import redis
from redis.commands.search.field import VectorField
from redis.commands.search.query import Query
from fastapi import HTTPException, status
import numpy as np
import toml

secrets = toml.load('secrets.toml')
redis_client = redis.Redis(
    host=secrets['redis_host'],
    port=18815,
    password=secrets['redis_password'],
    decode_responses=True
)
INDEX_NAME = 'embedding_index'


def get_list_all_keys():
    return redis_client.keys()


def add_element_to_key(elem_to_add, embeddings):
    keys_db = get_list_all_keys()
    if elem_to_add in keys_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Element {elem_to_add} already in DB")
    np_vector = embeddings.astype(np.float32)
    redis_client.hset(elem_to_add, mapping={'v': np_vector.tobytes()})


def remove_element(elemnt_to_remove):
    keys_db = get_list_all_keys()
    if elemnt_to_remove not in keys_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Element {elemnt_to_remove} not in DB")
    redis_client.delete(elemnt_to_remove)


def remove_all_elements():
    redis_client.flushall()


def knn_search(embeddings, k=1):
    element_to_search = embeddings.astype(np.float32).tobytes()
    q = Query(f"*=>[KNN {k} @v $vec]").return_field("__v_score").dialect(2)
    results = redis_client.ft(INDEX_NAME).search(q, query_params={"vec": element_to_search})

    list_out = []
    for result in results.docs:
        list_out.append({'key': result.id, 'distance': result.__v_score})
    return list_out


def generate_index():
    schema = (VectorField("v", "FLAT", {"TYPE": "FLOAT32", "DIM": 768, "DISTANCE_METRIC": "COSINE"}),)
    redis_client.ft(INDEX_NAME).create_index(schema)
