require "minitest/autorun"
require_relative "../genotype"

class TestGenotype < Minitest::Test
  def setup
    @initial_genotype = get_random_genotype
  end

  def test_mutate_only_single_one_gene
    mutated = mutate_one_pure(@initial_genotype, 1)

    assert_equal @initial_genotype[0], mutated[0]
    assert_equal @initial_genotype[2..-1], mutated[2..-1]

    refute_equal @initial_genotype[1], mutated[1]

  end
end
