import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import MuiDialogContent from '@material-ui/core/DialogContent';
import MuiDialogActions from '@material-ui/core/DialogActions';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Typography from '@material-ui/core/Typography';
import { IMAGE_SIZE } from '../../constants'

import ImageCrop from '../imageCrop';

const styles = theme => ({
  root: {
    margin: 0,
    padding: theme.spacing(2),
  },
  closeButton: {
    position: 'absolute',
    right: theme.spacing(1),
    top: theme.spacing(1),
    color: theme.palette.grey[500],
  },
});

const DialogTitle = withStyles(styles)(props => {
  const { children, classes, onClose, ...other } = props;
  return (
    <MuiDialogTitle disableTypography className={classes.root} {...other}>
      <Typography variant="h6">{children}</Typography>
      {onClose ? (
        <IconButton aria-label="close" className={classes.closeButton} onClick={onClose}>
          <CloseIcon />
        </IconButton>
      ) : null}
    </MuiDialogTitle>
  );
});

const DialogContent = withStyles(theme => ({
  root: {
    padding: theme.spacing(2),
  },
}))(MuiDialogContent);

const DialogActions = withStyles(theme => ({
  root: {
    margin: 0,
    padding: theme.spacing(1),
  },
}))(MuiDialogActions);



export default function CustomizedDialogs(props) {
  const [open, setOpen] = React.useState(false);
  const [crop, setCrop] = React.useState(false);
  const [src, setSrc] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  const handleLoad = () => {
    var imageData = createImageData();
    console.log(imageData);
    props.parentCallback({imageData: imageData});
    setOpen(false);
    setCrop({});
    setSrc("");
  };
  const imagecropCallbackFunction = (childData) => {
    setCrop(childData.crop);
    setSrc(childData.src);
    //this.setState({message: childData})
  };
  const createImageData = () => {
    var result = {};

    if (src !== "") {
      var image = new Image();
      image.src = src;


      const canvas = document.createElement('canvas');
      canvas.width = IMAGE_SIZE.width;
      canvas.height = IMAGE_SIZE.height;
      const context = canvas.getContext('2d');
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.drawImage(
          image, 
          crop.x * image.width / 100,
          crop.y * image.height / 100,
          crop.width * image.width / 100,
          crop.height * image.height / 100,
          0, 
          0,
          IMAGE_SIZE.width,
          IMAGE_SIZE.height
          );
          const imageData = context.getImageData(0, 0, IMAGE_SIZE.width, IMAGE_SIZE.height).data;
          const imageUrl = canvas.toDataURL("image/png");
          result = {imageData: imageData, imageUrl: imageUrl}
  }

    return result;
  }

  return (
    <div>
      <Button variant="outlined" color="secondary" onClick={handleClickOpen} style={{margin:"10px"}}>
        Load Image
      </Button>
      <Dialog onClose={handleClose} aria-labelledby="load-dialog-title" open={open}>
        <DialogTitle id="load-dialog-title" onClose={handleClose}>
          Load Image
        </DialogTitle>
        <DialogContent dividers>
          <ImageCrop parentCallback={imagecropCallbackFunction}/>
        </DialogContent>
        <DialogActions>

          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button autoFocus onClick={handleLoad} color="primary">
            Load
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}