import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import { IMAGE_SIZE } from '../../constants'

export default class index extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }
    async predict() {
        const editCanvas = this.props.editCanvas.current.canvasRef.current;
        const editContext = editCanvas.getContext('2d');
        const editData = editContext.getImageData(0, 0, IMAGE_SIZE.width, IMAGE_SIZE.height).data;
        //console.log("predict:", this.props.editCanvas.current.canvasRef.current.toDataURL());
        const imageCanvas = this.props.imageCanvas.current.canvasRef.current;
        const imageContext = imageCanvas.getContext('2d');
        const imageData = imageContext.getImageData(0, 0, IMAGE_SIZE.width, IMAGE_SIZE.height).data;

        var newImage = new Array(IMAGE_SIZE.height);
        for (var y = 0; y < IMAGE_SIZE.height; y++) {
            var imageRow = new Array(IMAGE_SIZE.width);
            for (var x = 0; x < IMAGE_SIZE.width; x++) {
                var pixel = [
                    imageData[4 * (y * IMAGE_SIZE.width + x)], // red
                    imageData[4 * (y * IMAGE_SIZE.width + x) + 1], // green
                    imageData[4 * (y * IMAGE_SIZE.width + x) + 2], // blue
                    editData[4 * (y * IMAGE_SIZE.width + x) + 3], // alpha
                ];

                imageRow[x] = pixel;
            }
            newImage[y] = imageRow;
        }


        console.log("predict:", newImage);

        const fileName = "networkinput";
        const json = JSON.stringify(newImage);
        const blob = new Blob([json], { type: 'application/json' });
        const href = await URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = href;
        link.download = fileName + ".json";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        //TODO
        /*var xhr = new XMLHttpRequest()
        xhr.addEventListener('load', () => {
          console.log(xhr.responseText)
        })
        xhr.open('GET', 'https://dog.ceo/api/breeds/list/all')
        xhr.send()*/
    }

    render() {
        return (
            <Button variant="outlined" color="primary" onClick={this.predict.bind(this)}>
                Predict
            </Button>
        )
    }
}
