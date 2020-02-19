import React from 'react';
import './App.css';
import ResultCard from './components/resultCard';
import EditorCard from './components/editorCard';
import ImageLoaderModal from './components/imageLoaderModal';
import { Typography } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';

function App() {
  const [src, setSrc] = React.useState(false);
  const [crop, setCrop] = React.useState(false);
  const [imageData, setImageData] = React.useState(false);
  const [result, setResult] = React.useState(false);

  const imagecropCallbackFunction = (childData) => {
    setCrop(childData.crop);
    setSrc(childData.src);
    setImageData(childData.imageData);
    //console.log(childData.imageData);
  };

  return (
    <div className="App">
      <Typography variant="h1">
        DeFINe
      </Typography>
      <Grid container spacing={3} direction="row" justify="center" alignItems="center">
        <Grid item xs={12} sm={6}>
          <EditorCard image={imageData}></EditorCard>
        </Grid>
        <Grid item xs={12} sm={6}>
          <ResultCard result={result}></ResultCard>
        </Grid>
      </Grid>
      <ImageLoaderModal parentCallback={imagecropCallbackFunction} />
    </div>
  );
}

export default App;
