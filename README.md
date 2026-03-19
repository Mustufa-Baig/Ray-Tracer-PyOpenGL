# Path Tracer (PyOpenGL)
A real-time, GPU-accelerated path tracer written in Python and GLSL. This project shifts the heavy mathematical lifting from the CPU to the GPU using PyOpenGL and fragment shaders, allowing for interactive framerates, progressive denoising, and environment-based lighting. 

## Installation

Simply download or clone this repository. You will need three packages to run the engine.

1. **Pygame** is used to create the window, handle user input, and load the HDRI sky texture. 
   ```
   pip install pygame
   ```
2. **PyOpenGL** provides the bindings to compile and communicate with the GLSL shaders on your GPU.
   ```
   pip install PyOpenGL
   ```
3. **Numpy** is used to handle the 3D vector math and matrix operations for the camera system.
   ```
   pip install numpy
   ```
*NOTE: Ensure you have an equirectangular environment map named `hdri.png` in the root directory for the HDRI lighting to work.*

## Usage

To start the path tracer, simply run the main Python file:
```
python app.py
```

### Camera Controls
Unlike a static CPU renderer, this project features a fully interactive first-person camera. Moving the camera will instantly clear the accumulation buffer, and standing still will allow the image to progressively refine and denoise.
* **W / S:** Move Forward / Backward
* **A / D:** Move Left / Right
* **Q / E:** Move Up / Down
* **Arrow Keys:** Look Around (Pitch and Yaw)

### Scene Configuration (Shaders)
Currently, the scene configuration is hardcoded directly into the GLSL shader for maximum execution speed, rather than reading from external text files. 

To modify the scene, open `shaders/fragment.txt`. Inside the `main()` function, you will find the scene definitions:

* **Spheres:** You can add or modify spheres in the `spheres` array. The format is `Sphere(center, radius, color, roughness)`. 
  > Example: `Sphere(vec3(0.0, 0.0, 0.0), 1.0, vec3(1.0, 0.0, 0.0), 0.8)` defines a rough red sphere at the origin.
* **Environment Exposure:** You can adjust the HDRI brightness in the "Handle Sky/Background Miss" section by altering the exposure multiplier.
* **Samples & Bounces:** The `NUM_SAMPLES` (rays per pixel per frame) and `MAX_BOUNCES` (light bounces per ray) can be adjusted in the main loop to balance performance and render quality.