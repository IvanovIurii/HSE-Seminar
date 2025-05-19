require 'rmagick'
include Magick

def load_target_image(path, size: 150)
  Image.read(path)
       .first
       .resize_to_fill(size, size)
       .quantize(256, GRAYColorspace)
end

