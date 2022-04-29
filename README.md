# Simple RGB image viewer (CLI)
Zoom and pan by: https://www.reddit.com/r/pygame/comments/drzukj/i_made_a_simple_zoomandpan_program_for_images_but/

Structured, CLI interface and RGB picker by me.

Simple CLI tool to view image and check the RGB value per pixel. More tests to be added and improved tool to be created. (Part of my Journey to learn pygame).

#
Python required 3.6+
```
git clone https://github.com/essamgouda97/rgb-image-viewer
cd rgb-image-viewer
python -m venv ./venv/
. ./venv/bin/activate
pip install -e .
```

# USAGE
Using command line tool:
```
rgb_image_viewer -p '/path/to/image.png'
```

Using python script:
```
python main.py -p './path/to/image.png'
```
