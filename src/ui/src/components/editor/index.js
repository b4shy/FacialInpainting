import React, { Component } from 'react'
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import RestoreIcon from '@material-ui/icons/Restore';
import { withStyles } from '@material-ui/core/styles';
import Switch from '@material-ui/core/Switch';
import Slider from '@material-ui/core/Slider';
import BrushIcon from '@material-ui/icons/Brush';
import FormatColorResetIcon from '@material-ui/icons/FormatColorReset';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';

import EditCanvas from '../editCanvas';

const marks = [
    {
        value: 5,
        label: '5px',
    },
    {
        value: 30,
        label: '30px',
    },
];

function valuetext(value) {
    return `${value}px`;
}

export default class index extends Component {
    constructor(props) {
        super(props);
        this.state = {
            //image: "",
            //crop: {},
            size: 10,
            erase: false
        };
        this.editCanvas = React.createRef();
    }

    handlePenChange(e) {
        this.setState({ erase: !this.state.erase });
    }
    handleSizeChange(value) {
        this.setState({ size: value });
    }

    handleClearDrawing(e) {
        this.editCanvas.current.clearCanvas();
        this.setState({ erase: false });
    }

    handleAlignment(event, newAlignment) {
        console.log(this.state.erase);
        this.setState({ erase: !this.state.erase });
    };

    componentDidMount() {
        this.props.parentCallback(this.editCanvas);
    }

    render() {
        //javascript code der bild in canvas lädt
        //console.log(this.props.imageData);
        return (
            <div>
                <EditCanvas size={this.state.size} erase={this.state.erase} ref={this.editCanvas} imageUrl={this.props.imageUrl} />
                <Grid container spacing={3}>
                    <Grid item xs={4}>
                        <Grid item xs={12}>
                            Size
                    </Grid>
                        <Grid item xs={8}>
                            <Slider
                                defaultValue={this.state.size}
                                getAriaValueText={valuetext}
                                step={5}
                                valueLabelDisplay="auto"
                                marks={marks}
                                min={5}
                                max={30}
                                onChangeCommitted={(event, value) => this.handleSizeChange(value)}
                            />
                        </Grid>
                    </Grid>
                    <Grid item xs={4}>
                        <ToggleButtonGroup
                            exclusive
                            onChange={this.handleAlignment.bind(this)}
                            aria-label="erase"
                        >
                            <ToggleButton value="true" selected={!this.state.erase} aria-label="pen">
                                <BrushIcon/>
                            </ToggleButton>
                            <ToggleButton value="false" selected={this.state.erase} aria-label="erase">
                                <FormatColorResetIcon/>
                            </ToggleButton>
                        </ToggleButtonGroup>
                    </Grid>
                    <Grid item xs={4}>
                        <Button
                            variant="outlined"
                            color="secondary"
                            size="small"
                            startIcon={<RestoreIcon />}
                            onClick={this.handleClearDrawing.bind(this)}
                        >
                            Clear
                    </Button>
                    </Grid>
                </Grid>
            </div>
        )
    }
}
