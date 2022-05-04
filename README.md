# Airplay Ontable Prototype

## Introduction

This is the player detection part of the small on-table prototype of Airplay IGYM. The algorithm can detect the players with the FLIR camera of 82 frame rate and send the x, y position to the Unity, the game part, with UDP. Currently, threadcolordemo.py, localization.py, VideoGetColor.py are the program we use.

## Package installation and environment

environment: Python 3.7

package: simple_pyspin(acquire information from FLIR camera),  apriltag(pupil_apriltags: Python bindings for the apriltags3) 

## threadcolordemo.py

This is the main part of the program. It will detect the player by color.

## VideoGetColor.py

This offers a independent thread to acquire images from camera

## localization.py

This is the post processing of localizing the players position
