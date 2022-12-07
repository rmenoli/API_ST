from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from db import get_list_all_keys, add_element_to_key, remove_element, knn_search, remove_all_elements, generate_index

app = FastAPI()
st = SentenceTransformer(
    '/Users/riccardomenoli/Documents/ontology_nnew/ontology-service/models/normalization-models/sentece-trasformers/cross-en-de-roberta-sentence-transformer')

def embed_entity(entity):
    return st.encode([entity])[0]


@app.get('/',
         tags=['Health'],
         description='Health endpoint')
def health():
    return 'health'


@app.get('/listEmbeddedElements',
         tags=['Embeddings exploration'],
         description='Get the string of all the sentences present in the DB')
def get_all_embedded_values():
    return get_list_all_keys()


@app.get('/getClosestEntity/{entity_to_embed}',
         tags=['Embeddings exploration'],
         description='Get the closest entity in the DB closer to the inputted entity')
def get_closest_entity(entity_to_embed):
    embeddings = embed_entity(entity_to_embed)
    return knn_search(embeddings, k=2)


class PostBody(BaseModel):
    entity: str


@app.post('/addElement',
          tags=['Embeddings modification'],
          description='Adds an element to the Db')
def add_element_embedding_space(body_request: PostBody):
    embeddings = embed_entity(body_request.entity)
    add_element_to_key(body_request.entity, embeddings)
    return 'element added'



@app.post('/removeElement/{elem}',
          tags=['Embeddings modification'],
          description='Removes an element already present in the DB')
def remove_element_embedding_space(body_request: PostBody):
    remove_element(body_request.entity)
    return 'element removed'

@app.post('/removeAllElements',
          tags=['Embeddings modification'],
          description='Removes all element already present in the DB')
def remove_all_elements_from_db():
    remove_all_elements()
    generate_index()
    return 'All elements removed'