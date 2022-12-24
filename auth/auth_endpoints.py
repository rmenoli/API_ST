from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.oauth2 import fake_user_db, create_access_token

router = APIRouter(
    tags=['Auth']
)


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends()):
    input_user = request.username
    input_psw = request.password

    if (input_user, input_psw) not in fake_user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Wrong username/psw'
        )
    token = create_access_token(data={'sub': input_user})
    return {
        'access_token': token,
        'token_type': 'bearer'
    }
