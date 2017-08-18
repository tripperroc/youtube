signif <- function(graph1, graph2, reps) {
  print ("calculating significance samples...")

  meandegree  <- numeric(0)
  mediandegree <- numeric(0)
  Densities <- numeric(0)
  betw <- numeric(0)
  CC  <- numeric(0)
  for (i in 1:reps) {
    verts <- V(graph1)[sample(1:vcount(graph1), vcount(graph2))]
    g <- subgraph (graph1, v=verts$name)
    meandegree[i] <- mean(degree(full.graph.edges.only, v=verts$name))
    mediandegree[i] <- median(degree(full.graph.edges.only, v=verts$name))
    CC[i] <- transitivity (g, "global")
    Densities[i] <- graph.density(g)
    betw[i] <- mean(betweenness(g))
  }
#  meandegree[i+1] <- mean(degree(graph2))
#  betw[i+1] <- mean(betweenness(graph2))
#  print(betw[i+1])
  return (list(MeanDegree=meandegree, MedianDegree = mediandegree, cc=CC, densities = Densities, vertices = verts$name, betweenness = betw))
}

  

subgraph.by.factor <- function (graph.df, verts, iterations, name1, name2) {
  deg.dist <- degree.distribution(full.graph.edges.only ,v=verts$name, cumulative=TRUE)
  deg <- degree(full.graph.edges.only, v=verts$name)
  g <- subgraph (graph.df$graph, v=verts)
  dense <- graph.density(g)
  CC <- transitivity (g, "global")
  CC[is.na(CC)] <- 0
  sig <- signif (graph.df$graph, g, iterations)
  print("plotting...")
  betw <-betweenness(g)
  print (mean(betw))

  plotit (name1, name2, mean(graph.df$degree), sig$MeanDegree, mean(deg), "Mean_Degree", paste(name2, "_meandeg.pdf", sep=""))
  plotit (name1, name2, graph.df$density, sig$densities, dense, "Density", paste(name2, "_densities.pdf", sep=""))
  plotit (name1, name2, graph.df$cc, sig$cc, CC, "Clustering_Coefficient", paste(name2, "_cc.pdf", sep=""))
  plotit (name1, name2, mean(graph.df$betweenness), sig$betweenness, mean(betw), "Betweenness", paste(name2, "_betw.pdf", sep=""))
  
  return (list (graph = g, density = dense, degree.dist = deg.dist, cc = CC, degree = deg,  significance = sig, betweenness=betw))
}

plotit <- function (name1, name2, graph.dat, sig.dat, dat, label,name) {
  pdf(name)
  r<-hist(sig.dat, plot=FALSE, breaks=100)
  r$counts<-r$counts/sum(r$count)
  plot(r, xlim=c(0,max(c(r$breaks[[length(r$breaks)]], dat))), main=paste(name2, "from", name1), xlab=label, ylab="Frequency")
  five <- quantile(sig.dat, .05, na.rm=TRUE)
  ninefive <- quantile(sig.dat, .95, na.rm=TRUE)
  lines(c(five, five), c(0,max(r$counts)), lty=2, lwd=4)
  lines(c(ninefive, ninefive), c(0,max(r$counts)), lty=2, lwd=4)
  lines(c(dat,dat), c(0,max(r$counts)), lwd=4, col="red")
   dev.off()
}
  
plotit2 <- function (name1, name2, graph.dat, sig.dat, dat, label,name) {
   plot.data <- data.frame(c(name1, "95% Confidence", name2), c(graph.dat, quantile(sig.dat, .95, na.rm=TRUE), dat))
  colnames(plot.data) <- c('Source', label)
  plot.data$Source <- factor(plot.data$Source, levels=unique(plot.data$Source))
  ggplot (data = plot.data, stat="identity", aes_string(x ="Source", y=label)) + geom_bar(position="dodge")
   ggsave(name)
 }

plotit3 <- function (name1, name2, graph.dat, sig.dat, dat, label,name) {
  data.vec <- c(graph.dat, dat)
  names(data.vec) <- c(name1, name2)
#  pdf(name)
  barplot2(data.vec, plot.ci=TRUE, ci.l = c(quantile(sig.dat, .05, na.rm=TRUE), dat), ci.u = c(quantile(sig.dat, .95, na.rm=TRUE), dat), ylab=label, main=name2)
#  dev.off()
 }
