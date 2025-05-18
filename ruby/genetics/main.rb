require_relative 'genotype'
require_relative 'renderer'
require_relative 'target_loader'
require_relative 'metrics'

OUTPUT_DIR = 'output'
MAX_STAGNANT = 10
OFFSPRING = 9
MAX_GEN = 1_000

Dir.mkdir(OUTPUT_DIR) unless Dir.exist?(OUTPUT_DIR)
target = load_target_image('sample.png')

# this holds an array of genes
genotype = get_random_genotype

best_score = 0
stagnant = 0

create_offspring = -> parent {
  [parent] + OFFSPRING.times.map { mutate_one(parent) }
}

images = []

puts "Start evolution"
(1..MAX_GEN).each do |gen|
  puts "Generation: " + gen.to_s
  candidates = create_offspring.call(genotype)
  scores = candidates.map.with_index do |genes|
    img = Renderer.render(genes)
    score = manhattan_diff(img, target)
    images.push(img)
    score
  end

  current_best, best_idx = scores.max, scores.index(scores.max)

  if current_best > best_score
    # I am not sure it is a functional way to do it, most likely it is not
    genotype = candidates[best_idx]
    best_score = current_best
    stagnant = 0
  else
    stagnant += 1
  end

  best_img = images[best_idx]
  target = best_img
  best_img.write(File.join(OUTPUT_DIR, "selected_gen%03d.png" % gen))

  break if stagnant >= MAX_STAGNANT
end
puts "End"
