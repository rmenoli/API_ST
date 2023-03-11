from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from fastapi.responses import JSONResponse
from fastapi import status, Depends, File

from db import get_list_all_keys, add_element_to_key, remove_element, knn_search, remove_all_elements, generate_index
from exception import ValueAlreadyInDB, ValueNotInDB
from auth.oauth2 import o_auth
import utils
from auth import auth_endpoints

# global values
app = FastAPI()
app.include_router(auth_endpoints.router)

secrets = utils.get_secrets_from_secret_file()
st = SentenceTransformer(secrets['path_sentence_transformer'])


# exception handler
# every time the code raise these exception, instead of return internal server error we return the resposne with the status code and the detail
@app.exception_handler(ValueAlreadyInDB)
@app.exception_handler(ValueNotInDB)
def handle_value_db_exception(request, exception):
    response = JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'detail': str(exception)}

    )
    return response


@app.get('/',
         tags=['Health'],  # tag for grouping in swagger
         description='Health endpoint')  # description in swagger
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
def get_closest_entity(entity_to_embed: str, # get method takes parameter form the link (2 lines above)
                       n_closes_element: int = 1):  # additional params specified after the path
    embeddings = utils.embed_entity(st, entity_to_embed)
    return knn_search(embeddings, k=n_closes_element)


class PostBody(BaseModel):
    entity: str


@app.post('/addElement',
          tags=['Single embeddings modification'],
          description='Adds an element to the Db')
def add_element_embedding_space(body_request: PostBody,
                                token: str = Depends(o_auth)):
    # post method takes parms from the body, defined above the elemnts of the Body
    # token for authentication
    embeddings = utils.embed_entity(st, body_request.entity)
    add_element_to_key(body_request.entity, embeddings)
    return 'element added'


@app.post('/removeElement/{elem}',
          tags=['Single embeddings modification'],
          description='Removes an element already present in the DB')
def remove_element_embedding_space(body_request: PostBody,
                                   token: str = Depends(o_auth)):
    remove_element(body_request.entity)
    return 'element removed'


@app.post('/removeAllElements',
          tags=['Multiple embeddings modification'],
          description='Removes all element already present in the DB')
def remove_all_elements_from_db(token: str = Depends(o_auth)):
    remove_all_elements()
    generate_index()
    return 'All elements removed'


@app.post('/AddMultipleElements',
          tags=['Multiple embeddings modification'],
          description='Add all the elements in the file .txt to the DB. If a element already exist it skip it')
def add_elements_from_file(file: bytes = File(media_type='txt'), token: str = Depends(o_auth)):
    file_content = file.decode('utf-8')
    lines = file_content.split('\n')
    for sentence in lines:
        embeddings = utils.embed_entity(st, sentence)
        add_element_to_key(sentence, embeddings)
    out_string = f'Added elements: {file_content}'
    return out_string
