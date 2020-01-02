import { LOAD_IMAGE, PREDICT } from './types';

export const loadImage = (image, crop) => {
    return {
        type: LOAD_IMAGE,
        image,
        crop
    }
};