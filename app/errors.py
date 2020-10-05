class Error():
    def __init__(self):
        self.SERVER_ERROR_500 = ({"message": "An error occured."}, 500)
        self.NOT_FOUND_404 = ({"message": "Resource could not be found."}, 404)
        self.NO_INPUT_400 = ({"message": "No input data provided."}, 400)
        self.INVALID_INPUT_422 = ({"message": "Invalid input."}, 422)
        self.ALREADY_EXIST = ({"message": "Already exists."}, 409)

        self.DOES_NOT_EXIST = ({"message": "Does not exists."}, 409)
        self.NOT_ADMIN = ({"message": "Admin permission denied."}, 999)
        self.HEADER_NOT_FOUND = ({"message": "Header does not exists."}, 999)
