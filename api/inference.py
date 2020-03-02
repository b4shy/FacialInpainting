import logging
from flask import Flask, render_template, jsonify, request, send_from_directory
import numpy as np
from src.network.inference import InferenceManager

def register_inference_api(app: Flask, inference_manager: InferenceManager):
    logger = logging.getLogger(__name__)

    @app.route("/")
    def hello():
        return render_template('index.html')

    #TODO: Pfad mit Regex verallgemeinern und Ordner aus Config laden
    @app.route("/manifest.json")
    def manifest():
        return send_from_directory('./build', 'manifest.json')

    @app.route('/defaultImage.png')
    def favicon():
        return send_from_directory('./build', 'defaultImage.png')

    @app.route('/inference', methods=['POST'])
    def get_tasks():
        model = np.array(request.json['model'])
        logger.info("Model: {model}".format(model=model))
        inference_manager.change_selected_checkpoint(model)
        data = np.array(request.json['image'])
        image = data[:,:,:3]
        mask = data[:,:,3]
        logger.debug("Image shape: {shape}".format(shape=image.shape))
        logger.debug("Mask shape: {shape}".format(shape=mask.shape))

        logger.info("Start prediction.")
        prediction = inference_manager.process(image, mask)
        logger.info("Finished prediction.")

        return jsonify({'image': prediction.tolist()})