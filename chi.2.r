print("calculating closeness...")
#paths <- shortest.paths(full.graph.edges.only)
#closeness.alt <- as.vector(matrix(apply(paths, 1, function(x)mean(x[is.finite(x)])), nrow(paths)))
#cloesness.alt[closeness.alt == 0] <- Inf
closeness.all <- closeness (full.graph.edges.only)

# Compute betweeness centrality
print("calculating betweenness...")
betweenness.all <- betweenness (full.graph.edges.only)

# Compute stress centrality
# commented out until I can figure out sna
#stress.all <- stresscent(full.graph.edges.only)

# Test confidence by samplings
print ("calculating confidence samples...")
meandegree  <- numeric(0)
mediandegree <- numeric(0)
densities <- numeric(0)
cc  <- numeric(0)
for (i in 1:10000) {
  verts <- V(full.graph.edges.only)[sample(1:vcount(full.graph.edges.only), vcount(full.graph.edges.only.respondents))]
  g <- subgraph (full.graph.edges.only, v=verts)
  meandegree[i] <- mean(degree(full.graph.edges.only, v=verts))
  mediandegree[i] <- median(degree(full.graph.edges.only, v=verts))
  cc[i] <- transitivity (g, "global")
   densities[i] <- graph.density(g)
}

print("graphing...")

# Graph degree degree distributions of all vs. just respondents
edges.only.all.df <- data.frame(c(1:length(degree.dist.edges.only)), degree.dist.edges.only, "all")
edges.only.respondents.df <- data.frame(c(1:length(degree.dist.edges.only.respondents.only)), degree.dist.edges.only.respondents.only, "respondents")
colnames(edges.only.all.df) <- c("degree", "density", "type")
colnames(edges.only.respondents.df) <- c("degree", "density", "type")
edges.only.df <- rbind(edges.only.all.df, edges.only.respondents.df)
qplot(degree, density, data=edges.only.df, geom="path", colour=type)
ggsave("densities.all.vs.respondents.pdf")

  
