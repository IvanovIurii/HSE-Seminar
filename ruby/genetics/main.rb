require_relative 'genotype'
require_relative 'renderer'
require_relative 'target_loader'
require_relative 'metrics'

OUTPUT_DIR = 'output'
MAX_STAGNANT = 10
OFFSPRING = 9
MAX_GEN = 1_000

Dir.mkdir(OUTPUT_DIR) unless Dir.exist?(OUTPUT_DIR)
initial_target = load_target_image('sample.png')

# this holds an array of genes
initial_genotype = get_random_genotype

create_offspring = -> parent {
  [parent] + OFFSPRING.times.map { mutate_one(parent) }
}

puts "Start evolution"

initial_state = {
  genotype: initial_genotype,
  best_score: 0,
  stagnant: 0,
  generation: 1,
  target: initial_target
}

# always returns a new state instead of mutations
evolve = ->(state, gen) do
  candidates = create_offspring.(state[:genotype])

  scores, images = candidates.map { |genes|
    img = Renderer.render(genes)
    score = manhattan_diff(img, state[:target])
    [score, img]
  }.transpose

  current_best = scores.max
  best_idx = scores.index(current_best)
  best_genes = candidates[best_idx]
  best_img = images[best_idx]

  # compute next state immutably
  if current_best > state[:best_score]
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
    target: best_img
  }
end

(1..MAX_GEN).reduce(initial_state) do |state, gen|
  puts "Generation #{gen}"
  next_state = evolve.(state, gen)
  # impure IO
  next_state[:target].write(File.join(OUTPUT_DIR, "selected_gen%03d.png" % gen))
  break next_state if next_state[:stagnant] >= MAX_STAGNANT
  next_state
end

puts "End"
