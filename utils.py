import toml

def get_secrets_from_secret_file():
    return toml.load('secrets.toml')


# utils function
def embed_entity(setnence_transformer, entity):
    return setnence_transformer.encode([entity])[0]
