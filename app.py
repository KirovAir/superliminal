import json
import os
import logging
import subprocess
from flask import Flask, abort, request

CFG_DIR = '/config/' 
if not os.path.isdir(CFG_DIR):
    CFG_DIR = 'config/'
    if not os.path.isdir(CFG_DIR):
        os.makedirs(CFG_DIR)

CFG_FILE = CFG_DIR + 'arguments.txt'
SUBLIMINAL_LOG = CFG_DIR + 'subliminal_output.log'

if not os.path.exists(CFG_FILE):
    with open(CFG_FILE, 'w') as outfile:
        data = {'default':r'--cache-dir /config --addic7ed <user> <pass> --opensubtitles <user> <pass> download -p addic7ed -p opensubtitles -l en -m 85 -v "#FILE#"',
        'sonarr':None,
        'radarr':None}
        outfile.write(json.dumps(data, indent=4))

logging.basicConfig(filename=CFG_DIR + 'web.log',level=logging.INFO if not os.environ.get('DEBUG') else logging.DEBUG)
app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if not request.json:
        logging.debug('Skipping, request is not JSON.')
        abort(400)

    logging.debug('Got json request: ' + request.data.decode("utf-8"))
    
    eventType = request.json.get('eventType')
    if eventType == 'Test':
        return 'Test'
    
    mediaFile = ''
    isMovie = False
    if request.json.get('movieFile') and request.json.get('movie'):
        isMovie = True
        mediaFile = os.path.join(request.json['movie']['folderPath'], request.json['movieFile']['relativePath'])
    if request.json.get('episodeFile') and request.json.get('series'):
        mediaFile = os.path.join(request.json['series']['path'], request.json['episodeFile']['relativePath'])
        
    if not mediaFile:
        logging.warn('No media file found in request')
        abort(400)
    
    logging.info('Got ' + ('movie' if isMovie else 'episode') + ' download request! Running Subliminal for file: ' + mediaFile)
    
    data = json.load(open(CFG_FILE))
    cmd = data.get('radarr') if isMovie else data.get('sonarr')
    if not cmd:
        cmd = data.get('default')

    if not cmd:
        logging.warn('Parameter line is empty, please check your config..')
        abort(400)

    cmd = 'subliminal ' + cmd.replace('#FILE#', mediaFile)
    logging.debug('CMD: ' + cmd)
    
    try:
        with open(SUBLIMINAL_LOG, 'a') as outfile:
            subprocess.call(cmd, stdout=outfile, stderr=outfile, shell=True)
    except Exception as e:
        logging.error(e)

    return 'Ok :)'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8978)
