require_relative 'genotype'
require_relative 'renderer'
require_relative 'metrics'

OUTPUT_DIR = 'output'
MAX_STAGNANT = 10
OFFSPRING = 10
MAX_GEN = 100

Dir.mkdir(OUTPUT_DIR) unless Dir.exist?(OUTPUT_DIR)

initial_genotype = get_random_genotype
initial = Renderer.render(initial_genotype)

# create black square
target = Image.new(150, 150) do |opts|
  opts.background_color = "black"
end

target.write(File.join(OUTPUT_DIR, "target.png"))
initial.write(File.join(OUTPUT_DIR, "initial.png"))

create_offsprings = -> parent {
  OFFSPRING.times.map { mutate_one(parent) }
}

puts "Start evolution"

initial_state = {
  genotype: initial_genotype,
  best_score: Float::INFINITY,
  stagnant: 0,
  generation: 0,
  target: target,
  image: nil
}

# always returns a new state instead of mutations
evolve = ->(state, candidates, gen) {
  scores, images = candidates.map { |genes|
    img = Renderer.render(genes)
    score = manhattan_diff(img, state[:target])
    puts score
    [score, img]
  }.transpose

  current_best = scores.min

  best_idx = scores.index(current_best)
  best_genes = candidates[best_idx]
  best_img = images[best_idx]

  if current_best < state[:best_score]
    new_stagnant = 0
    new_best_score = current_best
    new_genotype = best_genes
  else
    new_stagnant = state[:stagnant] + 1
    new_best_score = state[:best_score]
    new_genotype = state[:genotype]
  end

  {
    genotype: new_genotype,
    best_score: new_best_score,
    stagnant: new_stagnant,
    generation: gen,
    target: state[:target],
    image: best_img
  }
}

(1..MAX_GEN).reduce(initial_state) do |state, gen|
  # impure operations
  puts "Generation #{gen}"

  candidates = create_offsprings.(state[:genotype])

  # pure operation
  next_state = evolve.(state, candidates, gen)

  # impure operations
  next_state[:image].write(File.join(OUTPUT_DIR, "selected_gen%03d.png" % gen))
  break next_state if next_state[:stagnant] >= MAX_STAGNANT
  next_state
end

puts "End"
