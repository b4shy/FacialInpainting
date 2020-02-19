import React from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import Editor from '../editor';
import PredictionButton from '../predictionButton';


export default function EditorCard(props) {
  const [editDataRef, setEditDataRef] = React.useState(false);
  //console.log(props.image);

  const editDataCallback = (canvas) => {
    setEditDataRef(canvas);
  };

  const predictionCallback = (prediction) => {
    //console.log("pred", prediction);
    props.parentCallback(prediction);
  };

  return (
    <Card>
      <CardContent>
        <Editor imageUrl={props.image.imageUrl} parentCallback={editDataCallback} />
        <PredictionButton editDataRef={editDataRef} imageData={props.image.imageData} parentCallback={predictionCallback}/>
      </CardContent>
    </Card>
  );
}