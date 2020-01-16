#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request
import os
import torch
import numpy as np
import time

from network.inference import inference
from network.model import DeFINe


app = Flask(__name__, static_folder="build/static", template_folder="build")

ckt_path = os.path.abspath(".") + "/network/1"  # args.ckt #TODO evtl von Request abhängig
use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
net = DeFINe()
net.to(device)
net.eval()

state_dict = torch.load(ckt_path, map_location=torch.device('cpu'))
net.load_state_dict(state_dict)


@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/inference', methods=['POST'])
def get_tasks():
    #print(request.json)
    data = np.array(request.json['image'])
    #print(data.shape)
    image = data[:,:,:3]
    mask = data[:,:,3]

    print(image.shape)
    print(mask.shape)

    tic = time.time()
    prediction = inference(net, image, mask, device)
    print(time.time() - tic)
    #print("yow")
    #print(prediction.shape)


    return jsonify({'image': prediction.tolist()})
    #return jsonify({'result': inference(image, mask)})


print('Starting Flask!')

app.debug=True
app.run(host='0.0.0.0', debug=False)