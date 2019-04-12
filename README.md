# Mandel-Plot
*Mandelbrot Plotter in Python 3*

Project by David Ryan to plot the Mandelbrot set.

Run project using `python3 src/run.py`.


## Set up virtualenv to run project

``` sh
python3 -m venv ~/.virtualenvs/mandel-plot
source ~/.virtualenvs/mandel-plot/bin/activate

pip3 install numpy
pip3 install numba
pip3 install Pillow
pip3 install opencv-python

pip3 list
deactivate
```


## What is each package doing?

- numpy: numeric arrays
- numba (jit): just in time processing of functions, large speed-up
- Pillow (PIL, Image): image manipulation
- opencv-python (cv2): display image in window
