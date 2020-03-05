import React, { Component } from 'react';
import ReactCrop from 'react-image-crop';
import 'react-image-crop/dist/ReactCrop.css';
import { IMAGE_SIZE } from '../../constants';
import Button from '@material-ui/core/Button';

//https://github.com/DominicTobias/react-image-crop


export default class ImageCrop extends Component {
    state = {
        src: null,
        crop: {
            unit: '%',
            width: 100,
            aspect: 1 / 1,
        },
    };

    onSelectFile = e => {
        if (e.target.files && e.target.files.length > 0) {
            const reader = new FileReader();
            reader.addEventListener('load', () =>
                this.setState({ src: reader.result })
            );
            reader.readAsDataURL(e.target.files[0]);
        }
    };

    // If you setState the crop in here you should return false.
    onImageLoaded = image => {
        this.imageRef = image;
    };

    onCropComplete = (crop, percentCrop) => {
        //this.makeClientCrop(percentCrop);
        this.props.parentCallback({crop: percentCrop, src: this.state.src});
    };

    onCropChange = (crop, percentCrop) => {
        // You could also use percentCrop:
        this.setState({ crop: percentCrop });
    };

    render() {
        const { crop, src } = this.state;

        return (
            <div>
                {!src &&
                    <Button variant="contained" component="label">
                        Upload Image
                        <input type="file" accept="image/*" onChange={this.onSelectFile} style={{ display: "none" }} />
                    </Button>}
                {src && (
                    <ReactCrop
                        src={src}
                        crop={crop}
                        ruleOfThirds
                        onImageLoaded={this.onImageLoaded}
                        onComplete={this.onCropComplete}
                        onChange={this.onCropChange}
                        keepSelection={true}
                    />
                )}
                <p>
                    <small>
                        *Images get resized to {IMAGE_SIZE.width} x {IMAGE_SIZE.height} after loading
                    </small>
                </p>
            </div>
        );
    }
}

