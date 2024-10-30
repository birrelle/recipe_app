# from functools import wraps
# from flask import request, jsonify
# import jwt
# from flask import current_app

# def jwt_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'Authorization' in request.headers:
#             token = request.headers['Authorization'].split(' ')[1]
        
#         if not token:
#             return jsonify({'error': 'Token is missing'}), 401
        
#         try:
#             data = jwt.decode(
#                 token,
#                 current_app.config['JWT_SECRET_KEY'],
#                 algorithms=['HS256']
#             )
#             request.user_id = data['user_id']
#         except:
#             return jsonify({'error': 'Token is invalid'}), 401
        
#         return f(*args, **kwargs)
#     return decorated

#AI generated^^^