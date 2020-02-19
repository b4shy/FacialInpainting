import React, { Component } from 'react'
import SwipeableViews from 'react-swipeable-views';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import { IMAGE_SIZE } from '../../constants'
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';


export default class index extends Component {
    constructor(props) {
        super(props);
        this.state = {
            value: 0
        };
        this.resultCanvasRef = React.createRef();
        this.differenceCanvasRef = React.createRef();
        this.handleChange = this.handleChange.bind(this);
        this.handleChangeIndex = this.handleChangeIndex.bind(this);
    }

    handleChange(event, newValue) {
        this.setState({ value: newValue });
    };

    handleChangeIndex(index) {
        this.setState({ value: index });
    };

    componentDidUpdate() {

        var newImage = new Array(IMAGE_SIZE.height);
        for (var y = 0; y < IMAGE_SIZE.height; y++) {
            var imageRow = new Array(IMAGE_SIZE.width);
            for (var x = 0; x < IMAGE_SIZE.width; x++) {
                var pixel = [
                    this.props.imageData[4 * (y * IMAGE_SIZE.width + x)], // red
                    this.props.imageData[4 * (y * IMAGE_SIZE.width + x) + 1], // green
                    this.props.imageData[4 * (y * IMAGE_SIZE.width + x) + 2], // blue
                    255, // alpha
                ];

                imageRow[x] = pixel;
            }
            newImage[y] = imageRow;
        }



        //console.log("asd");
        console.log(this.props.prediction);
        const resultCanvas = this.resultCanvasRef.current;
        const resultCtx = resultCanvas.getContext('2d');
        const differenceCanvas = this.differenceCanvasRef.current;
        const differenceCtx = differenceCanvas.getContext('2d');

        if (this.props.prediction) {
            //console.log("asd");

            var imgData = resultCtx.createImageData(resultCanvas.width, resultCanvas.height);
            var k = 0;
            var l = 0;
            var difference = [];
            var data = [];
            for (var i = 0; i < resultCanvas.height; i++) {
                for (var j = 0; j < resultCanvas.width; j++) {
                    data[k++] = this.props.prediction.image[i][j][0];
                    data[k++] = this.props.prediction.image[i][j][1];
                    data[k++] = this.props.prediction.image[i][j][2];
                    data[k++] = 255;

                    var diff_red = Math.abs(this.props.prediction.image[i][j][0] - newImage[i][j][0]);
                    var diff_green = Math.abs(this.props.prediction.image[i][j][1] - newImage[i][j][1]);
                    var diff_blue = Math.abs(this.props.prediction.image[i][j][2] - newImage[i][j][2]);
                    difference[l++] = diff_red + diff_green + diff_blue;
                    //difference[l++] = Math.log2(diff_red + diff_green + diff_blue + 0.1);

                }
            }

            for (var i = 0; i < data.length; i++) {
                imgData.data[i] = data[i];
            }

            resultCtx.clearRect(0, 0, resultCanvas.width, resultCanvas.height);
            resultCtx.putImageData(imgData, 0, 0);


            //difference normalization:
            var max = 0.001;//Math.max.apply(Math,difference);
            difference.forEach(function (e) {
                if (max < e) {
                    max = e;
                }
            });

            //var differenceImage = []
            var k = 0;

            var diffImgData = differenceCtx.createImageData(differenceCanvas.width, differenceCanvas.height);
            for (var i = 0; i < difference.length; i++) {
                difference[i] = Math.floor((difference[i] / max) * 255);

                diffImgData.data[k++] = difference[i];
                diffImgData.data[k++] = difference[i];
                diffImgData.data[k++] = difference[i];
                diffImgData.data[k++] = 255;
            }




            differenceCtx.clearRect(0, 0, resultCanvas.width, resultCanvas.height);
            differenceCtx.putImageData(diffImgData, 0, 0);
        }


    }


    render() {
        return (
            <Card>
                <CardContent>
                    <Tabs
                        value={this.state.value}
                        onChange={this.handleChange}
                        indicatorColor="primary"
                        textColor="primary"
                        centered
                    >
                        <Tab label="Result" />
                        <Tab label="Difference" />
                    </Tabs>
                    <SwipeableViews
                        index={this.state.value}
                        onChangeIndex={this.handleChangeIndex}
                    >
                        <div hidden={this.state.value !== 0}>
                            <canvas ref={this.resultCanvasRef} height={IMAGE_SIZE.height} width={IMAGE_SIZE.width} style={{ border: '1px black solid', maxWidth: '98%' }}></canvas>
                        </div>
                        <div hidden={this.state.value !== 1}>
                            <canvas ref={this.differenceCanvasRef} height={IMAGE_SIZE.height} width={IMAGE_SIZE.width} style={{ border: '1px black solid', maxWidth: '98%' }}></canvas>
                        </div>

                    </SwipeableViews>
                </CardContent>
            </Card>
        )
    }
}