import React, { Component } from 'react';
import ReactCrop from 'react-image-crop';
import 'react-image-crop/dist/ReactCrop.css';
import { IMAGE_SIZE } from '../../constants';
import Button from '@material-ui/core/Button';


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
        //this.setState({ crop });
    };

    async makeClientCrop(crop) {
        if (this.imageRef && crop.width && crop.height) {
            const croppedImageUrl = await this.getCroppedImg(
                this.imageRef,
                crop,
                'newFile.jpeg'
            );
            this.setState({ croppedImageUrl });
            console.log(crop);
        }
    }

    getCroppedImg(image, crop, fileName) {
        /*const canvas = document.createElement('canvas');
        const scaleX = image.naturalWidth / image.width;
        const scaleY = image.naturalHeight / image.height;
        canvas.width = crop.width;
        canvas.height = crop.height;
        const ctx = canvas.getContext('2d');

        ctx.drawImage(
            image,
            crop.x * scaleX,
            crop.y * scaleY,
            crop.width * scaleX,
            crop.height * scaleY,
            0,
            0,
            crop.width,
            crop.height
        );

        return new Promise((resolve, reject) => {
            canvas.toBlob(blob => {
                if (!blob) {
                    //reject(new Error('Canvas is empty'));
                    console.error('Canvas is empty');
                    return;
                }
                blob.name = fileName;
                window.URL.revokeObjectURL(this.fileUrl);
                this.fileUrl = window.URL.createObjectURL(blob);
                resolve(this.fileUrl);
            }, 'image/jpeg');
        });*/
    }

    render() {
        const { crop, croppedImageUrl, src } = this.state;

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
                {/*croppedImageUrl && (
          <img alt="Crop" style={{ maxWidth: '100%' }} src={croppedImageUrl} />
                )*/}
                <p>
                    <small>
                        *Images get resized to {IMAGE_SIZE.width} x {IMAGE_SIZE.height} after loading
                    </small>
                </p>
            </div>
        );
    }
}

