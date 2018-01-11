from jobplus.app import create_app





app = create_app('production')


if __name__ == '__main__':
    from gevent import pywsgi

    server = pywsgi.WSGIServer(('', 5001), app)
    server.serve_forever()

