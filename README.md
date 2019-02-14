# SmartImageCropper
Smart Image Cropper

## Introduction
I have done this project to crop image backgrounds. It will identify all the images in the given folder and Crop them.

## What External Libraries it use
It uses numpy Library

## How does it work

* It identifies all the files in the given directory using a function in OS library.
* Then It will Iterate Through All Files
* First It will make a grayscale copy of the image and then it will find the Background Color of it.
* Then it will try to crop the image by finding the by finding the first point from all for sides where the background ends.