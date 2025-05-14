require_relative 'genotype'
require_relative 'renderer'
require_relative 'target_loader'

genotype = Genotype.random

img = Renderer.render(genotype)

img.write('result.png')
