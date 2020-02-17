import React from 'react';
import './App.css';
import Editor from './components/editor';
import ImageLoaderModal from './components/imageLoaderModal';
import { Typography } from '@material-ui/core';

function App() {
  const [src, setSrc] = React.useState(false);
  const [crop, setCrop] = React.useState(false);
  const [result, setResult] = React.useState(false);

  const imagecropCallbackFunction = (childData) => {
    setCrop(childData.crop);
    setSrc(childData.src);
    console.log("image und crop gesetzt");
  };

  return (
    <div className="App">
      <Typography variant="h1">
        DeFINe
      </Typography>
      <Editor src={src} crop={crop} />
      <ImageLoaderModal parentCallback={imagecropCallbackFunction} />
    </div>
  );
}

export default App;
