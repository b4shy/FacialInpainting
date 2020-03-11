# FacialInpainting
Deep Learning based inpainting on (human) faces.
Based on <ul>
<li>
Guilin Liu, Fitsum A. Reda, Kevin J. Shih, Ting-Chun Wang, Andrew Tao: “Image Inpainting for Irregular Holes Using Partial Convolutions”, 2018; <a href='http://arxiv.org/abs/1804.07723'>arXiv:1804.07723</a>.
</li>
</ul>

Master: [![CircleCI](https://circleci.com/gh/b4shy/FacialInpainting/tree/master.svg?style=svg&circle-token=3ab0a90eab4df7d8dd1189a5205dc75de8a5fed1)](https://circleci.com/gh/b4shy/FacialInpainting/tree/master)

Dev: [![CircleCI](https://circleci.com/gh/b4shy/FacialInpainting/tree/dev.svg?style=svg&circle-token=3ab0a90eab4df7d8dd1189a5205dc75de8a5fed1)](https://circleci.com/gh/b4shy/FacialInpainting/tree/dev)

***

Install dependencies (Python 3.7 required) via:
```bash
pipenv install 
pipenv shell
```

Start the server backend via:
```bash
# make sure to adjust the config if necessary
python run.py
``` 

Start the UI at localhost port 3000:
```bash
# install via npm install
cd src/ui
npm start
```

Please refer to the `/src/ui/readme.md` file for production builds. 
