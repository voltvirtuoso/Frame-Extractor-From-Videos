# Frame Extractor for Dataset Creation

## Overview

This Python script extracts frames from videos, processes them based on user-defined criteria, and saves them with metadata. The script includes optional features for resizing, augmentation, and correlation-based frame separation.

## Features

- **Blurry Frame Detection**: Skips frames that are detected as blurry based on a specified threshold.
- **Frame Correlation**: Computes similarity between frames to skip frames with high similarity based on a correlation threshold.
- **Resizing**: Optionally resizes frames to specified dimensions.
- **Augmentation**: Applies augmentations (e.g., flipping) to frames if enabled.
- **Metadata Generation**: Creates a JSON file with metadata about the processed frames.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

You can configure the script's behavior by setting the parameters in the `main.py` file or passing them as arguments when running the script.

### Parameters

- **`resize`**: Tuple of `(width, height)` to resize frames. Set to `None` for no resizing.
- **`augment`**: Boolean to enable or disable frame augmentation.
- **`blur_threshold`**: Float threshold for detecting blurry frames.
- **`correlation_threshold`**: Float threshold for frame correlation. If set to `None`, correlation is not computed.

## Usage

### Example Usage

To run the script with default configurations, simply execute:

```bash
python main.py
```

### Custom Configurations

You can modify the configurations directly in the `main.py` file:

```python
resize = (640, 480)  # Example resize dimensions; set to None for no resizing
augment = True       # Set to True to enable augmentation, False to disable
blur_threshold = 100.0  # Threshold for detecting blurry frames
correlation_threshold = 0.8  # Correlation threshold between frames; set to None to disable correlation-based separation
```

Or, you can change these values and run the script as follows:

```python
python main.py --resize 640 480 --augment --blur-threshold 100.0 --correlation-threshold 0.8
```

### Command-Line Arguments

- **`--resize`**: Specify the width and height to resize frames. Example: `--resize 640 480`. Omit to keep original dimensions.
- **`--augment`**: Enable augmentation by adding this flag.
- **`--blur-threshold`**: Set the threshold for detecting blurry frames. Example: `--blur-threshold 100.0`.
- **`--correlation-threshold`**: Set the correlation threshold between frames. Example: `--correlation-threshold 0.8`. Use `None` to disable correlation computation.

## Metadata File

The metadata file `metadata.json` contains information about the processed frames, including:

- **`frame`**: Filename of the extracted frame.
- **`index`**: Frame index in the video.
- **`augmentation`**: (Optional) Information about the type of augmentation applied.

## Troubleshooting

- **Error**: `ValueError: Input images must have the same dimensions.`
  - **Solution**: Ensure that `resize_dims` is consistent for both frames or set it to `None` if not resizing.

- **Error**: `AttributeError: module 'numpy' has no attribute 'int0'.`
  - **Solution**: Make sure your `numpy` version is up to date. The attribute `int0` should be `int32` in recent versions.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your improvements or fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

