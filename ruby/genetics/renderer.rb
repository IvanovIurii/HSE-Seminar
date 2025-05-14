# lib/renderer.rb
require 'rmagick'
require_relative 'genotype'

module Renderer
  include Magick

  CANVAS_SIZE         = 150
  CENTER              = CANVAS_SIZE / 2.0
  BACKGROUND_COLOR    = 'black'
  LINE_COLOR          = 'white'
  LINE_WIDTH          = 2
  SEGMENT_SAMPLE_SIZE = 7 

  # this was taken from https://github.com/mtzynb/biomorph/blob/master/js/biomorph.js
  # 7 genes taken todo: make it random
  def self.calculate_stems(genes)
    [
      { x:  0,             y:  genes[0] },
      { x:  genes[1],      y:  genes[2] },
      { x:  genes[3],      y:  0        },
      { x:  genes[4],      y: -genes[5] },
      { x:  0,             y: -genes[6] },
      { x: -genes[4],      y: -genes[5] },
      { x: -genes[3],      y:  0        },
      { x: -genes[1],      y:  genes[2] }
    ]
  end

  def self.render_segments(spec = {})
    length  = spec[:length]
    stems   = spec[:stems]
    dir     = (spec[:dir] || 0) % stems.size

    old_pos = spec[:old_pos] || { x: CENTER, y: CENTER }
    new_pos = {
      x: old_pos[:x] + length * stems[dir][:x],
      y: old_pos[:y] + length * stems[dir][:y]
    }

    segments = [{ start: old_pos, finish: new_pos }]

    if length > 1
      segments += render_segments(length: length - 1, stems: stems, dir: dir + 1, old_pos: new_pos)
      segments += render_segments(length: length - 1, stems: stems, dir: dir - 1, old_pos: new_pos)
    end

    segments
  end

  def self.render(genotype)
    genes  = genotype.genes
    length = genes[15]
    stems  = calculate_stems(genes)

    segments = render_segments(length: length, stems: stems)

    # draw them
    img  = Image.new(CANVAS_SIZE, CANVAS_SIZE) { |opts| opts.background_color = BACKGROUND_COLOR }

    draw = Draw.new
    draw.stroke(LINE_COLOR).stroke_width(LINE_WIDTH)

    # todo: rewrite it
    segments.each do |seg|
      s, f = seg[:start], seg[:finish]
      draw.line(s[:x], s[:y], f[:x], f[:y])
    end

    draw.draw(img)
    img
  end
end
