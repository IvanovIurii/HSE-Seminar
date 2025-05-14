class Genotype
    attr_reader :genes
  
    def initialize(genes)
      @genes = genes
    end
  
    # Генерация случайного генотипа
    def self.random
      genes = Array.new(15) { rand(-9..9) } + [rand(2..12)]
      new(genes)
    end
  
    # Копия с мутацией ровно одного гена на ±1 в пределах границ
    def mutate_one
      new_genes = genes.dup
      idx = rand(0...16)
      delta = [1, -1].sample
      limit = idx < 15 ? (-9..9) : (2..12)
      new_value = (new_genes[idx] + delta).clamp(limit.min, limit.max)
      new_genes[idx] = new_value
      self.class.new(new_genes)
    end
  end
  