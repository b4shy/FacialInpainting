import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import { IMAGE_SIZE } from '../../constants'
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogActions from '@material-ui/core/DialogActions';


export default class index extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            dialogOpen: false
        };
        this.handleClose = this.handleClose.bind(this);
        this.canvasRef = React.createRef();
    }
    async predict() {
        const editCanvas = this.props.editCanvas.current.canvasRef.current;
        const editContext = editCanvas.getContext('2d');
        const editData = editContext.getImageData(0, 0, IMAGE_SIZE.width, IMAGE_SIZE.height).data;
        //const maskPNG = editCanvas.toDataURL("image/png");
        //console.log("predict:", this.props.editCanvas.current.canvasRef.current.toDataURL());
        const imageCanvas = this.props.imageCanvas.current.canvasRef.current;
        const imageContext = imageCanvas.getContext('2d');
        const imageData = imageContext.getImageData(0, 0, IMAGE_SIZE.width, IMAGE_SIZE.height).data;
        //const imgPNG = imageCanvas.toDataURL("image/png");

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


        //console.log("predict:", newImage);
        /*
        var fileName = "networkInputImage";
        //const json = JSON.stringify(newImage);
        //const blob = new Blob([json], { type: 'application/json' });
        //const href = await URL.createObjectURL(blob);
        var link = document.createElement('a');
        link.href = imgPNG;
        link.download = fileName + ".png";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        fileName = "networkInputMask";
        //const json = JSON.stringify(newImage);
        //const blob = new Blob([json], { type: 'application/json' });
        //const href = await URL.createObjectURL(blob);
        var link = document.createElement('a');
        link.href = maskPNG;
        link.download = fileName + ".png";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);*/

        //TODO
        this.setState({ isLoading: true });
        fetch('/inference', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: newImage,
            })
        }).then(response => response.json())
        .then(response => {
            this.setState({ isLoading: false });
            console.log(response.image.length)
            console.log(response)
            console.log(response.image[0].length)
            this.setState({ dialogOpen: true });

            
            const canvas = this.canvasRef.current;
            const ctx = canvas.getContext('2d');

            var imgData = ctx.createImageData(canvas.width, canvas.height);
            var k = 0;
            for (var i = 0; i < canvas.height; i++) {
                for (var j = 0; j < canvas.width; j++) {
                  imgData.data[k++] = response.image[i][j][0];
                  imgData.data[k++] = response.image[i][j][1];
                  imgData.data[k++] = response.image[i][j][2];
                  imgData.data[k++] = 255;
                }
            }
            
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.putImageData(imgData, 0, 0);
        });
    }

    handleClose() {
        //console.log("this.state.dialogOpen");
        this.setState({ dialogOpen: false });
    };

    render() {
        return (
            <div style={{ position: 'relative' }}>
                <Button variant="outlined" color="primary" onClick={this.predict.bind(this)} disabled={this.state.isLoading}>
                    Predict
                {this.state.isLoading && <CircularProgress size={24} style={{
                        position: 'absolute', top: '50%',
                        left: '50%',
                        marginTop: -12,
                        marginLeft: -12
                    }} />}
                </Button>
                <Dialog onClose={this.handleClose} aria-labelledby="dialog-title" open={this.state.dialogOpen}>
                    <DialogTitle id="dialog-title" onClose={this.handleClose}>
                        Load Image
                    </DialogTitle>
                    <DialogContent dividers>
                        <canvas ref={this.canvasRef} height={IMAGE_SIZE.height} width={IMAGE_SIZE.width}></canvas>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleClose} color="primary">
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>
        )
    }
}
