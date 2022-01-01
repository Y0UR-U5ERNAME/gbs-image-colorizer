# GB Studio Image Colorizer
A tool to convert colorful pictures to GB Studio-compatible colorized backgrounds. Made by NalaFala/Yousurname/Y0UR-U5ERNAME.

## Requirements
- Python (install from https://www.python.org/downloads/)
- Pillow (install using the instructions [here](https://pillow.readthedocs.io/en/stable/installation.html))

## Instructions
Run the program using the command `py img2gbc.py`. The program will ask for the file location of the image. It will resize the image to 160x144 and output a colorized image (note that the colors in this image are not 15-bit) and an uncolorized image (to use in GB Studio). It will also output palette and colorization data to paste into the project file.

To insert the palette data, first create 8 palettes in GB Studio. Next, choose those palettes to use in your scene. Then, open the .gbsproj project file in a text editor, find the names of those palettes, and insert the palette data in the `"colors"` array of each palette, then find the scene and insert the colorization data in the `"tileColors"` array.

Results can vary depending on the image and method used. Method A is fast but can be inaccurate, method B is like method A but blockier and with more accurate colors, method C is the slowest and works better on images with not many colors, and methods D and E are the fastest and work better on images with many colors (D works well on grayscale images though). You are welcome to help optimize the program or add more accurate methods that are less blocky.

## Examples
|Input|Output|
|-----|------|
|<img width=160 height=144 src=https://user-images.githubusercontent.com/50276952/147837695-05bb5b77-e7f0-4cd7-b0d0-cee0caaa4d17.jpg>|![](https://user-images.githubusercontent.com/50276952/147837713-53bb4e7e-11f5-4cc5-b4f2-de576eccf92c.png)|
|<img width=160 height=144 src=https://user-images.githubusercontent.com/50276952/147837829-90f72eaf-1ea2-43c3-9379-592b7d3d2e20.jpg>|![](https://user-images.githubusercontent.com/50276952/147837843-982456b5-d1ce-4822-8217-97781eea0aba.png)|
|<img width=160 height=144 src=https://user-images.githubusercontent.com/50276952/147837914-b2c7356a-eec2-4b59-8c23-d5be244d3796.jpg>|![](https://user-images.githubusercontent.com/50276952/147861750-128e3308-5d1c-41dd-90c1-e6b1b7f471fc.png)|
