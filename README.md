# Voronoi Diagram with Fortune's Algorithm
(1) Ahmad Hanif Adisetya
(2) Ibni Shaquille Syauqi Ibrahim
(3) Muhammad Alif Ismady 

This project implements Fortune's Algorithm to generate a Voronoi diagram for a set of points on a bounded plane. The bounding box constrains the half-infinite edges, converting them to finite line segments that fit within the specified bounds.

## Features
- Bounding Box: The diagram is limited within a defined bounding box, which can use GUI window boundaries for easy visualization.
- Largest Empty Circle(s): The program identifies and displays the largest empty circle(s) that pass through three or more Voronoi sites. If multiple such circles exist, all are displayed.
- Flexible Input Options:
  - Text File: Load input points from a text file.
  - Interactive Mode: Users can add points directly onto the diagram using mouse clicks.
- Interactive GUI: Includes buttons and menu items for easy navigation and functionality control.
## Usage
- Load Points: Input points can be loaded from a .txt file or added interactively with the mouse.
- View Voronoi Diagram: The Voronoi diagram, bounded by the specified area, is displayed.
- Show Largest Empty Circles: Largest circles that pass through three or more points are identified and displayed.
## Requirements
- A GUI environment to support interactive input and diagram visualization.
- Text files should contain point coordinates in a format specified (e.g., one point per line: x y).

This project is developed to fulfill CSCE604045 Computational Geometry course Universitas Indonesia
