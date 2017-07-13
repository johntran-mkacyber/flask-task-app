from flask import Flask, make_response
from flask import request

app = Flask(__name__, static_folder='static', static_url_path='/static/')

@app.route('/string/', methods=['GET', 'POST'])
def return_string():
    return 'Hello, World!'

@app.route('/object/', methods=['GET', 'POST'])
def return_object():
    hdrs = {'Content-Type': 'text/plain'}
    return make_response('Hello, World!', 200, hdrs)

@app.route('/tuple/', methods=['GET', 'POST'])
def return_tuple():
    return 'Hello, World!', 200, {'Content-Type': 'text/plain'}

def dump_request_detail(request):
    request_detail = """
        # Before Request #
        request.endpoint: {request.endpoint}
        request.method: {request.method}
        request.view_args: {request.view_args}
        request.args: {request.args}
        request.form: {request.form}
        request.user_agent: {request.user_agent}
        request.files: {request.files}
        request.is_xhr: {request.is_xhr}

        ## request.headers ##
        {request.headers}
    """.format(request=request).strip()
    return request_detail

@app.before_request
def callme_before_every_request():
    # Demo only: the before_request hook
    app.logger.debug(dump_request_detail(request))

@app.after_request
def callme_after_every_response(response):
    # Demo only: the after_request hook
    app.logger.debug('# After Request #\n' + repr(response))
    return response

if __name__ == '__main__':
    app.run(debug=True)