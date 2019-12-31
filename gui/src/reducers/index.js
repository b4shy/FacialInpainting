import { combineReducers } from 'redux';
import drawingReducer from './drawingReducer';

export default combineReducers({
  draw: drawingReducer
});