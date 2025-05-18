require_relative 'genotype'
require_relative 'renderer'
require_relative 'target_loader'
require_relative 'metrics'

OUTPUT_DIR = 'output'
MAX_STAGNANT = 10

Dir.mkdir(OUTPUT_DIR) unless Dir.exist?(OUTPUT_DIR)

target = load_target_image('sample.png')

# this holds an array of genes
genotype = get_random_genotype

best_score = 0
stagnant = 0

# Generate parent + 9 mutated offspring
def create_offspring(parent)
  children = (0...9).map { mutate_one(parent) }
  [parent] + children
end

images = []

puts "Start evolution"

# generations
(1..1000).each do |gen|
  puts "Generation: " + gen.to_s
  candidates = create_offspring(genotype)

  scores = candidates.map.with_index do |genes, idx|
    img = Renderer.render(genes)
    img.write(File.join(OUTPUT_DIR, "gen%03d_#%02d.png" % [gen, idx]))
    score = manhattan_diff(img, target)
    images.push(img)
    score
  end

  current_best, best_idx = scores.max, scores.index(scores.max)

  best_img = images[best_idx]
  best_img.write(File.join(OUTPUT_DIR, "selected_gen%03d.png" % gen))

  if current_best > best_score
    genotype = candidates[best_idx]
    best_score = current_best
    stagnant = 0
  else
    stagnant += 1
  end

  break if stagnant >= MAX_STAGNANT

end

puts "End"