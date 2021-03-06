from flask import Flask, request, make_response
import requests
import sys

app = Flask(__name__)
app.debug=True

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/export', methods=['GET'])
def pkktranslate():
    pkkpath = 'http://pkk5.rosreestr.ru/arcgis/rest/services/Cadastre/Cadastre/MapServer/export'
    # make request
    params = {
        'layers' : request.args.get('layers'),
        'FORMAT' : request.args.get('FORMAT'),
        'TRANSPARENT' : request.args.get('TRANSPARENT'),
        'DPI' : request.args.get('DPI'),
        'F' : request.args.get('F'),
        'SIZE' : request.args.get('SIZE'),
        'MAXZOOM' : request.args.get('MAXZOOM'),
        'OPACITY' : request.args.get('OPACITY'),
        'bbox' : request.args.get('bbox'),
        'BBOXSR' : request.args.get('BBOXSR'),
        'IMAGESR' : request.args.get('IMAGESR'),
        'bbox' : request.args.get('bbox')
    }
    headers = {
        'Accept' : 'image/webp,image/*,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    }
    r = requests.get(pkkpath, params=params, headers=headers, timeout=5)
    # prepare response
    resp = make_response(r.content, 200)
    resp.headers['Content-Type'] = 'image/png'
    resp.headers['Accept-Ranges'] = 'bytes'
    return resp


@app.route('/search', methods=['GET'])
def pkksearch():
    pkkpath = 'http://pkk5.rosreestr.ru/api/features/'
    objtype = request.args.get('objtype')
    params = {
        'text': request.args.get('text'),
        'tolerance': 40,
        'limit': 5
    }
    r = requests.get(pkkpath + objtype, params=params, timeout=5)
    resp = make_response(r.content, 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/objinfo/<obj_id>', methods=['GET'])
def pkkobjectinfo(obj_id):
    objtype = request.args.get('objtype')
    pkkpath = 'http://pkk5.rosreestr.ru/api/features/' + objtype + '/' + obj_id
    r = requests.get(pkkpath, timeout=5)
    resp = make_response(r.content, 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run()
