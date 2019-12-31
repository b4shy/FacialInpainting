import { RESET, SET_PEN } from '../actions/types';

const initialState = {
  items: [],
  item: {}
};

export default function(state = initialState, action) {
  switch (action.type) {
    case RESET:
      return {
        ...state,
        items: action.payload
      };
    case SET_PEN:
      return {
        ...state,
        item: action.payload
      };
    default:
      return state;
  }
}