import React, { Component } from 'react'
import { IMAGE_SIZE } from '../../constants'

export default class index extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isPainting: false,
            mousePosition: undefined
        };
        this.canvasRef = React.createRef();
    }

    componentDidMount() {
        const canvas = this.canvasRef.current;
        canvas.addEventListener('mouseup', this.exitPaint.bind(this));
        canvas.addEventListener('mouseleave', this.exitPaint.bind(this));
        canvas.addEventListener('mousedown', this.startPaint.bind(this));
        canvas.addEventListener('mousemove', this.paint.bind(this));

        //touchevents
        canvas.addEventListener('touchend', this.exitPaint.bind(this));
        canvas.addEventListener('touchstart', this.startPaint.bind(this));
        canvas.addEventListener('touchmove', this.paint.bind(this));
    }

    startPaint(event) {
        const coordinates = this.getCoordinates(event);
        if (coordinates) {
            this.setState({ mousePosition: coordinates });
            this.setState({ isPainting: true });
        }
    };


    paint(event) {
        if (this.state.isPainting) {
            const newMousePosition = this.getCoordinates(event);
            if (this.state.mousePosition && newMousePosition) {
                this.drawLine(this.state.mousePosition, newMousePosition);
                this.setState({ mousePosition: newMousePosition });
            }
        }
    }

    exitPaint() {
        this.setState({ mousePosition: undefined });
        this.setState({ isPainting: false });
    }

    getCoordinates(event) {
        const canvas = this.canvasRef.current;
        var rect = canvas.getBoundingClientRect();
        //console.log("rect:", rect);
        if (window.TouchEvent && event instanceof TouchEvent) {
            event.preventDefault();
            return { x: (event.touches[0].clientX - rect.left)/rect.width*IMAGE_SIZE.width, y: (event.touches[0].clientY - rect.top)/rect.height*IMAGE_SIZE.height };
        } else {
            //console.log("page:", event.pageY);
            //console.log("client:", event.clientY);
            //console.log("event:", event);
            return { x: (event.clientX - rect.left)/rect.width*IMAGE_SIZE.width, y: (event.clientY - rect.top)/rect.height*IMAGE_SIZE.height };
        }
        //console.log(event.pageY,canvas.offsetTop ,rect.top);
    };

    drawLine(originalMousePosition, newMousePosition) {
        const canvas = this.canvasRef.current;
        const context = canvas.getContext('2d');
        if (context) {
            context.strokeStyle = 'red';
            context.lineJoin = 'round';
            context.lineWidth = this.props.size;

            if (this.props.erase) {
                context.globalCompositeOperation = 'destination-out';
            } else {
                context.globalCompositeOperation = 'source-over';
            }

            context.beginPath();
            context.moveTo(originalMousePosition.x, originalMousePosition.y);
            context.lineTo(newMousePosition.x, newMousePosition.y);
            context.closePath();

            context.stroke();
        }
    };

    clearCanvas() {
        const canvas = this.canvasRef.current;
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
    }

    createBackground() {
        var data = 'url("' + this.props.imageUrl + '")';
        //console.log(data);
        return data;
    }

    render() {
        return (
            <canvas height={IMAGE_SIZE.height}
                width={IMAGE_SIZE.width}
                ref={this.canvasRef}
                style={{ border: '1px black solid', maxWidth: '98%', backgroundImage: this.createBackground(), backgroundSize: "100% 100%" }}>
            </canvas>
        )
    }
}