from flask import Flask, request, jsonify
from waitress import serve as serve


class Sculpture(object):
    def __init__(self, inference_function):
        self._inference_function = inference_function

        self._app = Flask(__name__)
        self._app.add_url_rule("/api/inference", methods=["POST"], view_func=self.inference)

    def inference(self):
        request_body = request.get_json()
        result = self._inference_function(request_body)
        return jsonify({"result": result})

    def serve(self, debug: bool = False):
        if debug:
            self._app.run(port=9000, debug=True)
        else:
            serve(self._app, port=8000)
