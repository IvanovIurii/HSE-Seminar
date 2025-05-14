# lib/target_loader.rb
require 'rmagick'

module TargetLoader
  include Magick

  def self.load(path)
    img = Image.read(path).first
    img = img.resize_to_fill(150, 150)
    img = img.quantize(256, GRAYColorspace)
    img
  end
end
