# Rocket Interceptor with Reinforcement Learning

## Demo Videos
Here are some test videos after training the model with the current training parameters in ```src/training.py```.

<div style="display: flex; gap: 10px;">
  <img src="https://github.com/amiraliaali/defence/blob/main/demo_video.gif" width="900" height="500" />
</div>

## Overview
As I first heared and learned about the Iron Dome, I got curious how it works. With that in mind, I tried to implement a simple environment in which one attacking rocket tries to drop on a city and one defensive rocket tries to intercept it before reaching the city.

We train a Deep Q-Network agent with the abilities to turn the defensive rocket by five degrees either left or right and tzo increase the speed (with a maximum speed defined).

The attacking rocket in each iteration is positioned, orented and given a speed randomly.

## Project Structure
```
📂 project_root
├── images/  # Images for the environment setup like the rockets and buildings
├── readme_media/   # All the media used to be shown in the readme, like result videos etc.
├── src/
  ├── building.py         # Class definition for the builduings
  ├── dqn.py              # Our custom Neural Network
  ├── environment.py      # Custom environment
  ├── rocket_launcher.py  # Class definition for the rocket launcher on the ground
  ├── rocket.py           # Class definition for the rockets
  ├── test.py             # Test script for testing the tzrained agent and generating videos
  ├── ui_setup.py         # A script for setting up the UI to test the implementations
  └── training.py         # Training script
└── dqn_defense_model.pth    # The weights of the trained model

```

## Running the Training
Using vscode, simply run the task ```Training```.

## Running the Test and generating videos
Using vscode, simply run the task ```Test```.


## Author
Amir Ali Aali
amiraliaali@gmail.com