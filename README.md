# Solar System "Simulation"

This project started out with me wanting to visualize the full scale movement of planetary bodies in the solar system. After about an hour of programming I realized how rediculous that would have been. Instead, I shifted to a concept that simulated a solar system composed of 1 sun, 3 planets and a moon with the goal of allowing the user to experience how slight differences in velocities can have big impacts on an objects motion through space.

This is a simple solar system simulation built using Python and Pygame. The simulation models the movement of planets and moons using basic gravitational mechanics and allows user interaction through zooming, selecting planets, adjusting simulation speed, and resetting the system.

## Features

- **Elliptical Orbits**: Planets and moons follow elliptical orbits around their parent bodies.
- **Gravitational Influence**: The simulation approximates gravity's effect on planetary motion.
- **Zoom & Pan**: Users can zoom in and out using the mouse wheel.
- **Interactive Selection**: Clicking on a planet allows for adjusting its velocity.
- **Simulation Speed Control**: A slider lets users control the speed of the simulation.
- **Reset & Exit Buttons**: Easily restart the simulation or exit.

## Installation

1. Ensure you have Python installed.
2. Install dependencies using:
   ```bash
   pip install pygame pygame_gui
   ```
3. Run the simulation:
   ```bash
   python ss.py
   ```

## Controls

- **Mouse Wheel**: Zoom in and out.
- **Left Click on a Planet**: Select the planet to adjust its velocity.
- **Reset Button**: Restart the simulation.
- **Exit Button**: Close the application.

## Acknowledgments

- Planet and Sun images were sourced from **[[opengameart.org]](https://opengameart.org/users/darklighterdesigns)**. Special thanks to darklighter_designs for making these assets available!
