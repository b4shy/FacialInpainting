import logging
from flask import Flask, render_template, jsonify, request
import numpy as np
from src.network.inference import InferenceManager

def register_inference_api(app: Flask, inference_manager: InferenceManager):
    logger = logging.getLogger(__name__)

    @app.route("/")
    def hello():
        return render_template('index.html')

    @app.route('/inference', methods=['POST'])
    def get_tasks():
        model = np.array(request.json['model'])
        logger.info("Model: {model}".format(model=model))
        data = np.array(request.json['image'])
        image = data[:,:,:3]
        mask = data[:,:,3]
        logger.debug("Image shape: {shape}".format(shape=image.shape))
        logger.debug("Mask shape: {shape}".format(shape=mask.shape))

        logger.info("Start prediction.")
        prediction = inference_manager.infer(image, mask)
        logger.info("Finished prediction.")

        return jsonify({'image': prediction.tolist()})