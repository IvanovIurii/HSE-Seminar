require 'rmagick'

module Metrics
  include Magick

  def self.pixels(img)
    img.dispatch(0, 0, img.columns, img.rows, 'I').map(&:to_i)
  end

  def self.manhattan(img, target)
    a = pixels(img)
    b = pixels(target)
    a.zip(b).map { |x, y| (x - y).abs }.sum
  end
end
