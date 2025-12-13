class Response:
    @staticmethod
    def error(msg:str, code:int):
        return Response.__response({"err":msg},code)

    @staticmethod
    def success(data = ""):
        return Response.__response(data, 200)

    @staticmethod
    def __response(data, code:int):
        return (data, code, {"Content-Type": "application/json"})
