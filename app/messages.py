class Message():
    def __init__(self):
        self.data = None

    def set_data(self, data):
        self.data = data
        self.SUCCESS = ({"staus" : "success", "data" : self.data}, 200)
        self.SERVER_ERROR_500 = ({"staus" : "error", "data" : self.data}, 500)
        self.NOT_FOUND_404 = ({"staus" : "fail", "data" : self.data}, 404)
        self.NO_INPUT_400 = ({"staus" : "fail", "data" : self.data}, 400)
        self.INVALID_INPUT_422 = ({"staus" : "fail", "data" : self.data}, 422)
        self.ALREADY_EXIST = ({"staus" : "fail", "data" : self.data}, 409)
        self.DOES_NOT_EXIST = ({"staus" : "fail", "data" : self.data}, 409)
        self.UNAUTHORIZED = ({"staus" : "fail", "data" : self.data}, 401)
        self.FORBIDDEN = ({"staus" : "fail", "data" : self.data}, 403)
        self.HEADER_NOT_FOUND = ({"staus" : "fail", "data" : self.data}, 403)


