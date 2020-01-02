import { LOAD_IMAGE, PREDICT } from '../actions/types';

const initialState = {
  image: "",
  crop: {}
};

export default function(state = initialState, action) {
  switch (action.type) {
    case LOAD_IMAGE:
      return {
        image: action.image,
        crop: action.crop
      };
    case PREDICT:
      return {
        ...state,
        item: action.payload
      };
    default:
      return state;
  }
}