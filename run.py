#!/usr/bin/env python
import os
import logging
import yaml

from flask import Flask
import torch

from src.network.inference import InferenceManager
from src.network.model import DeFINe
from api.inference import register_inference_api


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
    app.logger.setLevel(webserver_config["logging_level"])

    inference_manager = InferenceManager(neural_network_config)
    register_inference_api(app, inference_manager)

    logger.info("Starting Flask!")
    app.run(host=webserver_config["host_address"],
            debug=webserver_config["debug"],
            port=webserver_config["port"])


if __name__ == '__main__':
    main()
