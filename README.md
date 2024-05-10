# corporaGen

## Overview

corporaGen is a forensic image file generator designed to assist forensic analysts in creating test scenarios or generating sample data for their investigations. This tool is particularly useful for generating a variety of image files (PNG, PDF, TXT, XLSX, etc.) that can be used in forensic analysis.

As this is meant to be an artifact from a group project, it's capabilities at this point is fairly barebones. The image generator doesn't acually generate image files, but instead it generates a set amount of random files in the so far supported file formats.

## Features

- **Multiple File Types**: Generate a wide range of filetypes including PNG, PDF, TXT, XLSX, and more in the future.
- **Customizable Content**: Create image files with customizable content to suit various forensic analysis scenarios.
- **Easy to Use**: A simple and intuitive interface for generating image files with just a few clicks.

### Installation

1. Clone the repository:
```git clone https://github.com/wrappedbaggage/corporaGen.git```

2. Navigate to the project directory:
```cd corporaGen```

3. Install the required Python libraries:
```pip install -r requirements.txt```


## Usage

To generate content, run the corporaGen.py script.
You will be prompted to enter how many files you would like to create, and then what target directory you would like the files to be put in. The target directory entered is the relative path from the location that the scripts are located.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

Simen Gåsland, simengasland@gmail.com

Project Link: [https://github.com/wrappedbaggage/corporaGen](https://github.com/wrappedbaggage/corporaGen)
