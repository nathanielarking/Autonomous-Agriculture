# Autonomous Agriculture
 Automated Garden Information System

 My name is Nathaniel and I'm very interested in sustainability. This is a project I've been working on with the goal of automating as much of the information side of agriculture as possible.

 I've completed a few different stages of the project:

 1. Integrate soil temperature sensor into excel sheet containing calendar of plant specific temperature data (https://www.youtube.com/watch?v=w0TwPI7bLp8)
 2. Convert software into a python webapp, eventually run on raspberry pi

 The project is split into a few different folder:
 1. data/ is the directory where I've put my sqlite database as well as any other files, as well as a module of functions to use with my database
 2. webapp/ is the directory where I've put my flask application, and dashapps/ is where I've put my dash applications. The dash applications are converted to html and displayed into flash with render_template
 3. localapp/ is the directory where I've put the part of the project that will talk to my sensors
 4. esp/ is the directory where I've put all the code for the microcontrollers

The installation process is as follows:
1. Clone the repository into the desired location
2. Create a Python virtual environment in a command terminal with python -m venv env
3. Activate virtual environment (on linux, this is done by typing source env/bin/activate)
4. Install requirements by running pip install -r requirements.txt
5. Run the program by running python main.py, and/or running it in a bash script on startup or as a service

The next stage of this project is going to cover an irrigation system in my backyard.
