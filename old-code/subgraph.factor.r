signif <- function(graph1, graph2, reps) {
  print ("calculating significance samples...")

  meandegree  <- numeric(0)
  mediandegree <- numeric(0)
  densities <- numeric(0)
  cc  <- numeric(0)
  for (i in 1:reps) {
    verts <- V(graph1)[sample(1:vcount(graph1), vcount(graph2))]
    g <- subgraph (graph1, v=verts)
    meandegree[i] <- mean(degree(graph1, v=verts))
    mediandegree[i] <- median(degree(graph1, v=verts))
    cc[i] <- transitivity (g, "global")
    densities[i] <- graph.density(g)
  }
  return (data.frame(MeanDegree=meandegree, MedianDegree = mediandegree, CC=cc, Densities = densities))
}

subgraph.by.factor <- function (graph1, verts, iterations, label, name) {
  deg.dist <- degree.distribution(graph1 ,v=verts, cumulative=TRUE)
  deg <- degree.distribution(graph1, v=verts, cumulative=TRUE)
  g <- subgraph (graph1, v=verts)
  dense <- graph.density(g)
  cc <- transitivity (g, "global")
  sig <- significance (graph1, g, iterations)
  
  return list (graph = g, degree.distribution = deg.dist, degree = deg, density = dense, significance = sig)
}
  
