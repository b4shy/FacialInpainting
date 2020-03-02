import logging
from pathlib import Path, PurePath, PurePosixPath

import numpy as np
from flask import Flask, jsonify, render_template, request, send_from_directory

from src.network.inference import InferenceManager


def register_inference_api(app: Flask, inference_manager: InferenceManager, build_base_path: str):
    logger = logging.getLogger(__name__)

    @app.route("/")
    def hello():
        return render_template('index.html')

    #TODO: Pfad mit Regex verallgemeinern und Ordner aus Config laden
    @app.route("/manifest.json")
    def manifest():
        build_path = PurePath(PurePosixPath(build_base_path))
        return send_from_directory(build_path, 'manifest.json')

    @app.route('/defaultImage.png')
    def favicon():
        build_path = PurePath(PurePosixPath(build_base_path))
        return send_from_directory(build_path, 'defaultImage.png')

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
