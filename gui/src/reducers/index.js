import { combineReducers } from 'redux';
import drawingReducer from './drawingReducer';
import fileHandlingReducer from './fileHandlingReducer'

export default combineReducers({
  draw: drawingReducer,
  file: fileHandlingReducer
});