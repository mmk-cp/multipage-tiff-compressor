from PIL import Image
import os


# Interface for Image Compression
class ImageCompressor:
    """
    Abstract class representing the interface for image compression.
    Subclasses need to implement the compress_image method.
    """

    def compress_image(self, image, compression_level):
        """
        Compress an image with the specified compression level.
        Should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this!")


# JPEG/PNG to TIFF Converter implementing the Image Compressor Interface
class JpegToTiffConverter(ImageCompressor):
    """
    Converter class that converts JPEG/PNG images to TIFF format,
    implementing the ImageCompressor interface.
    """

    def __init__(self, dpi_x=100, dpi_y=100):
        """
        Initializes the JpegToTiffConverter with default DPI values.
        :param dpi_x: DPI value for the x-axis (default=100)
        :param dpi_y: DPI value for the y-axis (default=100)
        """
        self.dpi_x = dpi_x
        self.dpi_y = dpi_y

    def convert_images_to_tiff(self, image_list, output_file, compression="jpeg", quality=70):
        """
        Converts a list of images into a multi-page TIFF file.
        :param image_list: List of images to convert
        :param output_file: Path where the output TIFF file will be saved
        :param compression: Compression type for the TIFF file (default="jpeg")
        :param quality: Compression quality, lower values = higher compression (default=70)
        """
        if image_list:
            # Save images as multi-page TIFF with specified compression
            image_list[0].save(output_file, save_all=True, append_images=image_list[1:],
                               dpi=(self.dpi_x, self.dpi_y),
                               compression=compression, quality=quality)
            print(f"testImages successfully saved to {output_file}")


# Interface Segregation for different operations
class ImageLoader:
    """
    Abstract class representing the interface for image loading.
    Subclasses need to implement the load_images method.
    """

    def load_images(self, folder_path, color_space):
        """
        Load images from the specified folder.
        Should be implemented by subclasses.
        :param folder_path: Path of the folder containing images
        :param color_space: Color space to convert the images (e.g., "RGB", "YCbCr")
        :return: List of loaded images and their DPI values
        """
        raise NotImplementedError("Subclasses should implement this!")


class JpegImageLoader(ImageLoader):
    """
    Loader class to load JPEG/PNG images from a folder, converting them to the specified color space.
    """

    def __init__(self):
        self.dpi_x = 100  # Initialize default DPI for x-axis
        self.dpi_y = 100  # Initialize default DPI for y-axis

    def load_images(self, folder_path, color_space="RGB"):
        """
        Loads images from a folder and converts them to the specified color space.
        :param folder_path: Path of the folder containing images
        :param color_space: Color space to convert images to (default="RGB")
        :return: Tuple of (list of images, DPI x, DPI y)
        """
        image_list = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(folder_path, filename)
                try:
                    with Image.open(file_path) as img:
                        # Attempt to get DPI from image metadata
                        dpi_info = img.info.get('dpi', (self.dpi_x, self.dpi_y))
                        self.dpi_x, self.dpi_y = round(dpi_info[0]), round(dpi_info[1])

                        # Convert to specified color space
                        compressed_img = img.convert(color_space)
                        image_list.append(compressed_img)
                except (IOError, OSError) as e:
                    print(f"Error loading image {filename}: {e}")

        return image_list, self.dpi_x, self.dpi_y


# Entry point with Dependency Injection
class ImageProcessor:
    """
    Processor class that coordinates loading images and converting them using
    the specified loader and converter (dependency injection).
    """

    def __init__(self, converter: ImageCompressor, loader: ImageLoader):
        """
        Initializes the ImageProcessor with a converter and loader.
        :param converter: An instance of ImageCompressor for image compression
        :param loader: An instance of ImageLoader for loading images
        """
        self.converter = converter
        self.loader = loader

    def process_images(self, folder_path, output_file, compression, quality, color_space):
        """
        Orchestrates loading and conversion of images.
        :param folder_path: Path of the folder containing input images
        :param output_file: Path where the output TIFF file will be saved
        :param compression: Compression type (e.g., "jpeg")
        :param quality: Compression quality (lower values = higher compression)
        :param color_space: Color space for the image conversion (e.g., "YCbCr", "RGB")
        """
        image_list, dpi_x, dpi_y = self.loader.load_images(folder_path, color_space)
        # Pass the DPI values from loader to converter
        self.converter.dpi_x = dpi_x
        self.converter.dpi_y = dpi_y
        self.converter.convert_images_to_tiff(image_list, output_file, compression, quality)


def main():
    """
    Main function to handle the image conversion process.
    """
    folder_path = "testImages"  # Folder containing input images
    output_file = "output_compressed.tif"  # Path for the output TIFF file
    compression = "jpeg"  # Compression type
    color_space = "YCbCr"  # Color space (can also use "RGB")
    quality = 30  # Compression quality

    # Dependency Injection for flexibility
    converter = JpegToTiffConverter()  # Initializes converter with default DPI
    loader = JpegImageLoader()  # Initializes loader for JPEG images
    processor = ImageProcessor(converter, loader)  # Inject dependencies

    # Process and convert images
    processor.process_images(folder_path, output_file, compression, quality, color_space)
    print(f"Conversion completed. Output saved as {output_file}.")


if __name__ == "__main__":
    main()
