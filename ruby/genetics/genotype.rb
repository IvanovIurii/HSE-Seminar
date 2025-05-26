GENE_COUNT = 15
GENE_RANGE = -9..9
LAST_GENE_RANGE = 2..12

def get_random_genotype
  Array.new(GENE_COUNT) { rand(GENE_RANGE) } + [rand(LAST_GENE_RANGE)].freeze
end

def mutate_one(genotype)
  idx = rand(0...GENE_COUNT)
  delta = [1, -1].sample
  mutate_one_pure(genotype, idx, delta)
end

def mutate_one_pure(genotype, idx, delta)
  genotype
    .each_with_index
    .map { |gene, i|
      if i == idx
        limit = i < GENE_COUNT ? (GENE_RANGE) : (LAST_GENE_RANGE)
        (gene + delta).clamp(limit.min, limit.max)
      else
        gene
      end
    }
    .freeze
end