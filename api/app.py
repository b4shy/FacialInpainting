#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request
from network.inference import inference
import numpy as np

app = Flask(__name__, static_folder="build/static", template_folder="build")




@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/inference', methods=['POST'])
def get_tasks():
    #print(request.json)
    data = np.array(request.json['image'])
    image = data[:,:,:3]
    mask = data[:,:,3]


    return jsonify({'image': image.tolist(), "maks": mask.tolist()})
    #return jsonify({'result': inference(image, mask)})


print('Starting Flask!')

app.debug=True
app.run(host='0.0.0.0')