require 'rmagick'
include Magick

def manhattan_diff(img, target)
  pixels = -> (img) { img.dispatch(0, 0, img.columns, img.rows, 'I').map(&:to_i) }
  pixels.call(img)
        .zip(pixels.call(target))
        .map { |a, b| (a - b).abs }
        .sum
end
