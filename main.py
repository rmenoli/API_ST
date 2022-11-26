from fastapi import FastAPI, status, Response

app = FastAPI()


@app.get('/',
         tags=['Health'],
         description='Health endpoint')
def health():
    return 'health'


@app.get('/listEmbeddedElements',
         tags=['Embeddings exploration'],
         description='Get the string of all the sentences present in the DB')
def get_all_embedded_values():
    return 'list emebdded elelems!'


@app.get('/getClosestEntity/{entity_to_embed}',
         tags=['Embeddings exploration'],
         description='Get the closest entity in the DB closer to the inputted entity')
def get_closest_entity(entity_to_embed):
    return f'trying to emebed the entity {entity_to_embed}'


@app.post('/addElement/{elem}',
          tags=['Embeddings modification'],
          description='Adds an element to de Db by embedding it')
def add_element_embedding_space(elem, response: Response):
    if elem == 'oldelem':
        response.status_code = status.HTTP_404_NOT_FOUND
        return 'element present'
    else:
        response.status_code = status.HTTP_200_OK
        return 'element added'


@app.post('/removeElement',
          tags=['Embeddings modification'],
          description='Removes an element already present in the DB')
def remove_element_embedding_space():
    return 'element removed'
