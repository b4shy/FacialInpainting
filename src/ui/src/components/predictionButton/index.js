import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import { IMAGE_SIZE } from '../../constants'
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogActions from '@material-ui/core/DialogActions';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';


export default class index extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            dialogOpen: false,
            model: "4",
            prediction: [],
            difference: [],
            resultType: "result"
        };
        this.handleClose = this.handleClose.bind(this);
        this.canvasRef = React.createRef();
        this.handleModelChange = this.handleModelChange.bind(this);
        this.handleResultTypeChange = this.handleResultTypeChange.bind(this);
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
                model: parseInt(this.state.model),
                image: newImage,
            })
        }).then(response => response.json())
            .then(response => {
                console.log("response:", response);

                this.setState({ dialogOpen: true });

                const canvas = this.canvasRef.current;
                const ctx = canvas.getContext('2d');

                var imgData = ctx.createImageData(canvas.width, canvas.height);
                var k = 0;
                var l = 0;
                var difference = [];
                var data = [];
                for (var i = 0; i < canvas.height; i++) {
                    for (var j = 0; j < canvas.width; j++) {
                        data[k++] = response.image[i][j][0];
                        data[k++] = response.image[i][j][1];
                        data[k++] = response.image[i][j][2];
                        data[k++] = 255;

                        //difference image
                        //var pred_gray = 0.3 * response.image[i][j][0] + 0.6 * response.image[i][j][1] + 0.11 * response.image[i][j][2];
                        //var img_gray = 0.3 * newImage[i][j][0] + 0.6 * newImage[i][j][1] + 0.11 * newImage[i][j][2];

                        var diff_red = Math.abs(response.image[i][j][0]-newImage[i][j][0]);
                        var diff_green = Math.abs(response.image[i][j][1]-newImage[i][j][1]);
                        var diff_blue = Math.abs(response.image[i][j][2]-newImage[i][j][2]);
                        difference[l++] = diff_red + diff_green + diff_blue;//Math.log2(diff_red + diff_green + diff_blue + 0.1);

                    }
                }

                console.log("data: ", data);

                for (var i = 0; i<data.length; i++){
                    imgData.data[i] = data[i];
                }

                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.putImageData(imgData, 0, 0);



                console.log("predData: ", imgData.data);

                this.setState({ prediction: data });

                //difference normalization:
                var max = 0.001;//Math.max.apply(Math,difference);
                difference.forEach(function(e) {
                    if (max < e) {
                        max = e;
                    }
                });

                var differenceImage = []
                var k = 0;

                for (var i = 0; i < difference.length; i++) {
                    difference[i] = Math.floor((difference[i] / max) * 255);

                    differenceImage[k++] = difference[i];
                    differenceImage[k++] = difference[i];
                    differenceImage[k++] = difference[i];
                    differenceImage[k++] = 255;
                }

                this.setState({ difference: differenceImage });


                this.setState({ isLoading: false });
            });
    }

    handleClose() {
        //console.log("this.state.dialogOpen");
        this.setState({ dialogOpen: false });
    };

    handleModelChange(event) {
        this.setState({ model: event.target.value });
    };

    handleResultTypeChange(event) {
        this.setState({ resultType: event.target.value });

        const canvas = this.canvasRef.current;
        const ctx = canvas.getContext('2d');
        var imgData = ctx.createImageData(canvas.width, canvas.height);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        if(event.target.value == "diff"){
            console.log("diff:", this.state.difference);
            for (let i = 0; i < imgData.data.length; i++) {
                imgData.data[i] = this.state.difference[i];
            }   
        }else{
            console.log("prediction:", this.state.prediction);
            for (let i = 0; i < imgData.data.length; i++) {
                imgData.data[i] = this.state.prediction[i];
            }
        }
        ctx.putImageData(imgData, 0, 0);

    };

    render() {
        return (
            <div style={{ position: 'relative' }}>
                <FormControl component="fieldset">
                    <FormLabel component="legend">Model</FormLabel>
                    <RadioGroup aria-label="position" name="position" value={this.state.model} onChange={this.handleModelChange} row>
                        <FormControlLabel
                            value="1"
                            control={<Radio color="primary" />}
                            label="v1"
                            labelPlacement="bottom"
                        />
                        <FormControlLabel
                            value="2"
                            control={<Radio color="primary" />}
                            label="v2"
                            labelPlacement="bottom"
                        />
                        <FormControlLabel
                            value="3"
                            control={<Radio color="primary" />}
                            label="v3"
                            labelPlacement="bottom"
                        />
                        <FormControlLabel
                            value="4"
                            control={<Radio color="primary" />}
                            label="v4"
                            labelPlacement="bottom"
                        />
                    </RadioGroup>
                </FormControl>
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
                        <FormControl component="fieldset">
                            <RadioGroup value={this.state.resultType} onChange={this.handleResultTypeChange} row>
                                <FormControlLabel
                                    value="result"
                                    control={<Radio color="primary" />}
                                    label="result"
                                />
                                <FormControlLabel
                                    value="diff"
                                    control={<Radio color="primary" />}
                                    label="diff"
                                />
                            </RadioGroup>
                        </FormControl>
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
