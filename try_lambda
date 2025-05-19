# gene is an integer in given range
integer_fn = ->(x) { x }

# limiting functions
skeleton_limit = ->(n) { n.clamp(-9,9) }
lenght_limit = ->(n) { n.clamp(2,12) }

# higher order function
# i - stands for integer function
# l - stands for limiting function
gene = -> (i, l) { 
  ->(n) { (i >> l)[n]}
 }

 # create gene
skeleton_gene = gene[integer_fn, skeleton_limit]
lengh_gene = gene[integer_fn, lenght_limit]

genotype_factory = ->(skeleton_fn, lengh_fn, size) {
  indices = ->(a,b,c) { (a..b).to_a.sample(c) }.(0, size-1, 7)
  Array.new(15) { |index| indices.include?(index) ? skeleton_fn[index] : 0 } +
  [lengh_fn.(rand(0..15))]
}

puts genotype_factory.(skeleton_gene, lengh_gene, 15).inspect # returns genotype
