import React from 'react';
import './App.css';
import EditCanvas from './components/editCanvas';
import ImageLoaderModal from './components/imageLoaderModal';
import {Provider} from 'react-redux';
import store from './store'

import Button from '@material-ui/core/Button';


function App() {
  return (
    <Provider store={store}>
      <div className="App">
        <EditCanvas />
        <ImageLoaderModal/>
      </div>
    </Provider>
  );
}

export default App;
