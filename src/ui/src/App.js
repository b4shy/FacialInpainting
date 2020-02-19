import React from 'react';
import './App.css';
import ResultCard from './components/resultCard';
import EditorCard from './components/editorCard';
import ImageLoaderModal from './components/imageLoaderModal';
import { Typography } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import { IMAGE_SIZE } from './constants'

const createEmptyImage = () => {
  const canvas = document.createElement('canvas');
  canvas.width = IMAGE_SIZE.width;
  canvas.height = IMAGE_SIZE.height;
  const context = canvas.getContext('2d');
  context.clearRect(0, 0, canvas.width, canvas.height);
  const imageData = context.getImageData(0, 0, IMAGE_SIZE.width, IMAGE_SIZE.height).data;
  const imageUrl = canvas.toDataURL("image/png");
  const result = { imageData: imageData, imageUrl: imageUrl }

  return result;
}

function App() {
  const [image, setImage] = React.useState(() => createEmptyImage());
  const [prediction, setPrediction] = React.useState(false);

  const imagecropCallbackFunction = (childData) => {
    setImage(childData.imageData);
    //console.log(childData.imageData);
  };

  const predictCallbackFunction = (prediction) => {
    console.log("pred", prediction);
    setPrediction(prediction);
  };

  

  return (
    <div className="App">
      <Typography variant="h1">
        DeFINe
      </Typography>
      <Grid container spacing={3} direction="row" justify="center" alignItems="center">
        <Grid item xs={12} sm={6}>
          <EditorCard image={image} parentCallback={predictCallbackFunction}></EditorCard>
        </Grid>
        <Grid item xs={12} sm={6}>
          <ResultCard prediction={prediction} imageData={image.imageData}></ResultCard>
        </Grid>
      </Grid>
      <ImageLoaderModal parentCallback={imagecropCallbackFunction} />
    </div>
  );
}

export default App;
