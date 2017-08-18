median.correlation.confidence <- function (g) {
  nums <- 0
  counts <- length(E(g)[V(g)[PHQ9.score >= 15]%--%V(g)[PHQ9.score >= 15]])
  for (i in 1:100000) {
    newg <- permute.vertices(g,sample(vcount(g)))
    if (length(E(newg)[V(newg)[V(g)$PHQ9.score >= 15]%--%V(newg)[V(g)$PHQ9.score >= 15]]) <= counts)
      nums <- nums + 1
  }
  return (nums)
}
