import React from 'react';
import SwipeableViews from 'react-swipeable-views';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import { IMAGE_SIZE } from '../../constants'
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';


export default function ResultCard() {
    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const handleChangeIndex = index => {
        setValue(index);
    };

    return (
        <Card>
            <CardContent>
                <Tabs
                    value={value}
                    onChange={handleChange}
                    indicatorColor="primary"
                    textColor="primary"
                    centered
                >
                    <Tab label="Result" />
                    <Tab label="Difference" />
                </Tabs>
                <SwipeableViews
                    index={value}
                    onChangeIndex={handleChangeIndex}
                >
                    <div hidden={value !== 0}>
                        <canvas height={IMAGE_SIZE.height} width={IMAGE_SIZE.width} style={{ border: '1px black solid', maxWidth: '98%' }}></canvas>
                    </div>
                    <div hidden={value !== 1}>
                        <canvas height={IMAGE_SIZE.height} width={IMAGE_SIZE.width} style={{ border: '1px black solid', maxWidth: '98%' }}></canvas>
                    </div>

                </SwipeableViews>
            </CardContent>
        </Card>
    );
}