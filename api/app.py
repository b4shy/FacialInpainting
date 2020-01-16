#!/usr/bin/env python
import time
import os
import logging
import yaml

from flask import Flask, render_template, jsonify, request
import torch
import numpy as np

from network.inference import inference, InferenceManager
from network.model import DeFINe



def main(config_file="config.yml"):
    with open(config_file) as cf:
        config = yaml.safe_load(cf.read())
    
    webserver_config = config["webserver"]
    neural_network_config = config["neural_network"]

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s - %(name)s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    app = Flask(__name__, static_folder=webserver_config["static_folder"], template_folder=webserver_config["template_folder"])

    checkpoint_path = os.path.abspath(".") + neural_network_config["checkpoint"]  # args.ckt #TODO evtl von Request abhängig
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    net = DeFINe()
    inference_manager = InferenceManager(app, device)

    net.to(device)
    net.eval()

    state_dict = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    net.load_state_dict(state_dict)

    # register_inference_api(app, )

    @app.route("/")
    def hello():
        return render_template('index.html')

    @app.route('/inference', methods=['POST'])
    def get_tasks():
        data = np.array(request.json['image'])
        image = data[:,:,:3]
        mask = data[:,:,3]
        logger.info(image.shape)
        logger.info(mask.shape)

        tic = time.time()
        prediction = inference(net, image, mask, device)
        logger.info(time.time() - tic)


        return jsonify({'image': prediction.tolist()})
        #return jsonify({'result': inference(image, mask)})


    logger.info("Starting Flask!")

    app.run(host='0.0.0.0', debug=False)


if __name__ == '__main__':
    main()
