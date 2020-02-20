import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import { IMAGE_SIZE } from '../../constants'
import ButtonGroup from '@material-ui/core/ButtonGroup';

import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import Tooltip from '@material-ui/core/Tooltip';
import Grid from '@material-ui/core/Grid';


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
    }

    async predict() {
        const editCanvas = this.props.editDataRef.current.canvasRef.current;
        const editContext = editCanvas.getContext('2d');
        const editData = editContext.getImageData(0, 0, IMAGE_SIZE.width, IMAGE_SIZE.height).data;

        var newImage = new Array(IMAGE_SIZE.height);
        for (var y = 0; y < IMAGE_SIZE.height; y++) {
            var imageRow = new Array(IMAGE_SIZE.width);
            for (var x = 0; x < IMAGE_SIZE.width; x++) {
                var pixel = [
                    this.props.imageData[4 * (y * IMAGE_SIZE.width + x)], // red
                    this.props.imageData[4 * (y * IMAGE_SIZE.width + x) + 1], // green
                    this.props.imageData[4 * (y * IMAGE_SIZE.width + x) + 2], // blue
                    editData[4 * (y * IMAGE_SIZE.width + x) + 3], // alpha
                ];

                imageRow[x] = pixel;
            }
            newImage[y] = imageRow;
        }
        console.log("request:", newImage);

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
                var d = new Date();
                var id = d.getTime();

                this.props.parentCallback({ id: id, image: response.image });

                this.setState({ isLoading: false });
            });
    }

    handleClose() {
        this.setState({ dialogOpen: false });
    };

    handleModelChange(event) {
        this.setState({ model: event.target.value });
    };

    //TODO: Select in ButtonGroup scheint Fehler zu werfen

    render() {
        return (
            <Grid container alignItems="flex-start" justify="flex-end" direction="row">
                <ButtonGroup variant="outlined" color="primary" aria-label="split button">
                    <Tooltip title="Network version">
                        <Select
                            id="selection"
                            value={this.state.model}
                            onChange={this.handleModelChange}
                        >
                            <MenuItem value={1}>v1</MenuItem>
                            <MenuItem value={2}>v2</MenuItem>
                            <MenuItem value={3}>v3</MenuItem>
                            <MenuItem value={4}>v4</MenuItem>
                        </Select>
                    </Tooltip>
                    <Button variant="contained" color="primary" onClick={this.predict.bind(this)} disabled={this.state.isLoading}>
                        Go
                {this.state.isLoading && <CircularProgress size={24} style={{
                            position: 'absolute', top: '50%',
                            left: '50%',
                            marginTop: -12,
                            marginLeft: -12
                        }} />}
                    </Button>
                </ButtonGroup>
            </Grid>
        )
    }
}
