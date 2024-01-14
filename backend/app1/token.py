
from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user, user_type):

    refresh = RefreshToken.for_user(user)
    if user_type == 'god':
        refresh['user_type'] = 'god'
    elif user_type == 'admin':
        refresh['user_type'] = 'admin'

    elif user_type == 'teacher':
        refresh['user_type'] = 'teacher'
    else:
        refresh['user_type'] = 'regular'  


    refresh['id'] = user.id

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

