GENE_COUNT = 15
GENE_RANGE = -9..9
LAST_GENE_RANGE = 2..12

def get_random_genotype
  Array.new(GENE_COUNT) { rand(GENE_RANGE) } + [rand(LAST_GENE_RANGE)]
end

def mutate_one(genotype)
  idx = rand(0...GENE_COUNT + 1)
  delta = [1, -1].sample

  genotype
    .each_with_index
    .map do |gene, i|
    if i == idx
      limit = i < GENE_COUNT ? (GENE_RANGE) : (LAST_GENE_RANGE)
      (gene + delta).clamp(limit.min, limit.max)
    else
      gene
    end
  end
end