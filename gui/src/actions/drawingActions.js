
import { SET_PEN, RESET } from './types';

export const fetchPosts = () => dispatch => {
    dispatch({
        type: RESET,
        payload: null
    })
};

export const createPost = pen => dispatch => {
    dispatch({
        type: SET_PEN,
        payload: pen
    })
};