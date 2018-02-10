from flask_restful import Resource, reqparse
from models.user import UserModel



class UserRegister(Resource):
    parser = reqparse.RequestParser()

# adding a comment to test build

    parser.add_argument('username',
        type=str,
        required=True,
        help="Username field can not be blank"
    )

    parser.add_argument('password',
        type=str,
        required=True,
        help="Password field can not be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
