import React, { Component } from 'react'
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import RestoreIcon from '@material-ui/icons/Restore';
import { withStyles } from '@material-ui/core/styles';
import Switch from '@material-ui/core/Switch';
import Slider from '@material-ui/core/Slider';

import EditCanvas from '../editCanvas';

const AntSwitch = withStyles(theme => ({
    root: {
        width: 28,
        height: 16,
        padding: 0,
        display: 'flex',
    },
    switchBase: {
        padding: 2,
        color: theme.palette.grey[500],
        '&$checked': {
            transform: 'translateX(12px)',
            color: theme.palette.common.white,
            '& + $track': {
                opacity: 1,
                backgroundColor: theme.palette.primary.main,
                borderColor: theme.palette.primary.main,
            },
        },
    },
    thumb: {
        width: 12,
        height: 12,
        boxShadow: 'none',
    },
    track: {
        border: `1px solid ${theme.palette.grey[500]}`,
        borderRadius: 16 / 2,
        opacity: 1,
        backgroundColor: theme.palette.common.white,
    },
    checked: {},
}))(Switch);

const marks = [
    {
        value: 5,
        label: '5px',
    },
    {
        value: 100,
        label: '100px',
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
            size: 25,
            erase: false
        };
    }

    handlePenChange(e) {
        this.setState({ erase: !this.state.erase });
    }
    handleSizeChange(value) {
        this.setState({ size: value });
    }

    render() {
        //javascript code der bild in canvas lädt
        return (
            <Grid container spacing={3}>
                <Grid item xs={4}>
                    <Grid item xs={12}>
                        Stiftgröße
                    </Grid>
                    <Grid item xs={8}>
                        <Slider
                            defaultValue={this.state.size}
                            getAriaValueText={valuetext}
                            step={5}
                            valueLabelDisplay="auto"
                            marks={marks}
                            min={5}
                            max={100}
                            onChangeCommitted={(event, value) => this.handleSizeChange(value)}
                        />
                    </Grid>
                </Grid>
                <Grid item xs={4}>
                    <Grid component="label" container alignItems="center" spacing={1}>
                        <Grid item>Pen</Grid>
                        <Grid item>
                            <AntSwitch
                                checked={this.state.erase}
                                onChange={this.handlePenChange.bind(this)}
                            />
                        </Grid>
                        <Grid item>Eraser</Grid>
                    </Grid>
                </Grid>
                <Grid item xs={4}>
                    <Button
                        variant="contained"
                        color="secondary"
                        startIcon={<RestoreIcon />}
                    >
                        Reset
                    </Button>
                </Grid>
                <Grid item xs={12}>
                    <EditCanvas crop={this.props.crop} src={this.props.src}/>
                </Grid>
            </Grid>
        )
    }
}
