# Container Water Distribution System

This project demonstrates a Python implementation of a `Container` class
that models water distribution across connected containers.

## Features

-   Each container stores an internal amount of water.
-   Containers can be connected or disconnected.
-   Water automatically redistributes equally across all containers in a
    connected component.
-   Adding water to any container rebalances the entire connected
    structure.

## How It Works

1.  **Connecting containers** forms a graph where water levels equalize.
2.  **Disconnecting containers** splits the system into independent
    subgraphs, each redistributing internally.
3.  **Adding water** to any container triggers redistribution across its
    connected group.

## Example Usage

The included demo:

-   Creates 5 containers: A, B, C, D, E
-   Adds different water amounts to each
-   Connects A--B--C, equalizing their water
-   Connects D--E, equalizing their water
-   Connects the two groups, equalizing all five containers


## Running the Script

Run with:

``` bash
python main.py
```

This will print water levels before and after each connection.

## Purpose

This implementation is useful for educational simulations of distributed
systems, graph-based equalization, and resource balancing.
