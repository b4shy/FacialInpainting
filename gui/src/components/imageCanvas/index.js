import React, { Component } from 'react'
import { IMAGE_SIZE } from '../../constants'

export default class index extends Component {
    constructor(props) {
        super(props);
        this.state = {
            image: "",
            crop: {},
            size: 25,
            erase: false
        };
        this.canvasRef = React.createRef();
    }

    componentDidUpdate() {
        //console.log("image:", this.props.src);
        if (this.props.src !== "") {
            var image = new Image();
            image.src = this.props.src;


            const canvas = this.canvasRef.current;
            const context = canvas.getContext('2d');
            context.clearRect(0, 0, canvas.width, canvas.height);
            context.drawImage(
                image, 
                this.props.crop.x * image.width / 100,
                this.props.crop.y * image.height / 100,
                this.props.crop.width * image.width / 100,
                this.props.crop.height * image.height / 100,
                0, 
                0,
                IMAGE_SIZE.width,
                IMAGE_SIZE.height
                );
        }
    }

    render() {
        return (
            <canvas height={IMAGE_SIZE.height} width={IMAGE_SIZE.width} ref={this.canvasRef} style={{position: 'absolute', left: 0, top: 0, zIndex: 0}}>
            </canvas>
        )
    }
}
