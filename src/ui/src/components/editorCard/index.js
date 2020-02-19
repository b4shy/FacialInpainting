import React from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import Editor from '../editor';


export default function EditorCard(props) {
  //console.log(props.image);

  return (
    <Card>
      <CardContent>
      <Editor image={props.image}/>
      </CardContent>
    </Card>
  );
}