
                                        # To install all packages needed,
# uncomment and run the following code:
#source("http://sna.stanford.edu/setup.R")
#install.packages("NetData")

# I think these operations are self-evident
library(igraph)
library(NetData)
library(ggplot2)
library(gplots)
#library(rgl)
setwd('/Users/cmh/sn/ts/TSpace')
# read in attributes. file is scrubbed version of 'pagerank_scores_x5_with_PHQ9.txt', which had
# duplicate values in the some of the first two columns
attributes <- read.csv('pagerank_scores_nodupes.txt')
# Clean up attribute hashids
d <- attributes$Hashed.ID
d <- gsub (" +", "", d)
attributes <- cbind(d, attributes)
attributes$TrevorSpace.ID = NULL
attributes$Hashed.ID = NULL

read.in.graph <- function (file.name, attributes) {
  data<-read.csv(file.name, header=F)
  colnames(data) <- c('ego', 'alter')
                                        # Gather all unique vertices
  d1 <- data[1]
  d2 <- data[2]
  colnames(d2) <- 'ego'
  verts <- rbind(d1,d2)
  verts <- unique(verts)
                                        # We're doing an outer join because there are elements in attributes not in verts
  fulldata <- merge(verts, attributes, by.x="ego", by.y="d", all=T)
                                        # Delete trevorspace name from data
  graph <- as.undirected(graph.data.frame(d = data, vertices = fulldata), mode='collapse')
  graph1 <- delete.vertices(graph, V(graph)[is.na(get.vertex.attribute(graph, name = "Completed."))])
  graph2 <- delete.vertices(graph1, V(graph1)[get.vertex.attribute(graph1, name = "Completed.") == " false"])
  graphs <- decompose.graph(graph2)
                                        # counts the vertices in each component
                                        # sapply(graphs, vcount)
 # degree(graph1)
 # degree(graph, V(graph)[!is.na(get.vertex.attribute(graph1, name = "Completed."))])
 # pdf("PHQ9vPRC.pdf")
  plot(get.vertex.attribute(graph2, 'X2012.04.10'), get.vertex.attribute(graph2, 'PHQ9.score'))
  dev.off()
  paths2 = shortest.paths(graph2)
  phq9 <- get.vertex.attribute(graph2, 'PHQ9.score')
  
                                        # This is interesting
  summary (attributes$PHQ9.score[attributes$Completed.== " true"])
                                        #   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
                                        #  0.000   4.000   9.000   9.328  13.000  26.000 
  degree1 <- degree(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true"  & V(graph)$PHQ9.questions.answered == 9])
  degree.under <- degree(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score < 15 & V(graph)$PHQ9.questions.answered == 9])
  degree.over <- degree(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 15 & V(graph)$PHQ9.questions.answered == 9] )
  summary(degree.under)
                                        #   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
                                        #    0.0    29.5    91.0   214.0   189.0  2158.0 
  summary(degree.over)
                                        #   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
                                        #    0.0    13.5    44.0   158.9   136.0  2879.0
  
                                        # V(graph)[V(graph1)$name]$name gets verts in graph by name
                                        # c(1:length(V(graph)))[V(graph)[V(graph1)$name]] gets indices in graph by name in graph1

  dist1 <- degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE )
  dist.over <- degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 15  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE)
  dist.under <- degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score < 15  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE)

  pdf("over-under-15.pdf")
  plot(dist.over[c(1:500)], col="red", type='l')
  points(dist.under[c(1:500)], col="green", type='l')
  dev.off()
  
  all.true.verts <- V(graph)[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.questions.answered == 9 ]
  scores.low.deg <- all.true.verts$PHQ.score[degree1 <= 14] 
  scores.high.deg <- all.true.verts$PHQ.score[degree1 > 180] 
#  points(dist.under, col = "green")
#  plot(dist.over, col = "red")
  output <- list()
  output$degree.under <- degree.under
  output$degree.over <- degree.over
  output$dist.under <- dist.under
  output$dist.over <- dist.over
  output$degree1 <- degree1
  output$graph <- graph
  output$graph1 <- graph1
  output$graph2 <- graph2
  output$graphs <- graphs
  output$all.true.verts <- all.true.verts
  output$scores.low.deg <- scores.low.deg
  output$scores.high.deg <- scores.high.deg

  pdf("deg-dist-by-phq9.pdf")
  dist.lowest <- degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 1  & V(graph)$PHQ9.score <= 4  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE)
  dist.low <- degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 5  & V(graph)$PHQ9.score <= 9  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE)
  dist.med <- degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 10  & V(graph)$PHQ9.score <= 14  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE)
  dist.high <- degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 15  & V(graph)$PHQ9.score <= 19  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE)
  dist.highest <- degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 20  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE)

  output$dist.lowest <- dist.lowest
  output$dist.low <- dist.low
  output$dist.med <- dist.med
  output$dist.high <- dist.high
  output$dist.highest <- dist.highest
  
  plot(degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 5  & V(graph)$PHQ9.score <= 9  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE), col="orange", type='l', log="xy")
  points(degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 10  & V(graph)$PHQ9.score <= 14  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE), col="blue", type='l')
  points(degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 20  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE), col="red", type='l')
  points(degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 15  & V(graph)$PHQ9.score <= 19  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE), col="green", type='l')
  points(degree.distribution(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 1  & V(graph)$PHQ9.score <= 4  & V(graph)$PHQ9.questions.answered == 9], cumulative=TRUE), col="purple", type='l')
  dev.off()

  degree.lowest <- degree(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 1  & V(graph)$PHQ9.score <= 4  & V(graph)$PHQ9.questions.answered == 9])
  degree.low <- degree(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 5  & V(graph)$PHQ9.score <= 9  & V(graph)$PHQ9.questions.answered == 9])
  degree.med <- degree(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 10  & V(graph)$PHQ9.score <= 14  & V(graph)$PHQ9.questions.answered == 9])
  degree.high <- degree(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 15  & V(graph)$PHQ9.score <= 19  & V(graph)$PHQ9.questions.answered == 9])
  degree.highest <- degree(graph, v=V(graph)$name[!is.na(V(graph)$Completed.) & V(graph)$Completed.==" true" & V(graph)$PHQ9.score >= 20  & V(graph)$PHQ9.questions.answered == 9])

  output$degree.lowest <- degree.lowest
  output$degree.low <- degree.low
  output$degree.med <- degree.med
  output$degree.high <- degree.high
  output$degree.highest <- degree.highest
 
  return(output)
}


d03 <- read.in.graph('edges_encrypted_3-21-12.txt', attributes)
d04 <- read.in.graph('edges_encrypted_4-20-12.txt', attributes)

deg <- degree(d04$graph, v=V(d04$graph)$name[!is.na(V(d04$graph)$Completed.) & V(d04$graph)$Completed.==" true"  & V(d04$graph)$PHQ9.questions.answered == 9])
phq9 <- V(d04$graph)$PHQ9.score[!is.na(V(d04$graph)$Completed.) & V(d04$graph)$Completed.==" true" & V(d04$graph)$PHQ9.questions.answered == 9]

# Creates a perspective 2D histogram
# CMH rgl library not loading, so we are skipping this step
#h2d <- hist2d(deg[deg < 4000], phq9[deg < 4000])
#persp3d(h2d$x, h2d$y, h2d$counts, xlab="degree", zlab="counts", ylab="PHQ 9 score")
#rgl.snapshot('deg-vs-ph9-low-degree-3d.png')

# Generate a histogram for the participants with among the 50% smallest and largest degrees, respectively
hist(phq9[deg > 56], breaks=c(0:26), right=TRUE, ylim = range(c(0:14)))
hist(phq9[deg <= 56], breaks=c(0:26), right=TRUE, ylim = range(c(0:14)))
deg.cent <- data.frame(Degree = c("below median","below median","above median","above median"), PHQ9 = c("<15", ">=15","<15", ">=15"), Counts = c(length(phq9[deg <= 56 & phq9 < 15]),length(phq9[deg <= 56 & phq9 >= 15]),length(phq9[deg > 56 & phq9 < 15]),length(phq9[deg > 56 & phq9 >= 15])))
ggplot(data=deg.cent, aes(x=Degree, y=Counts, fill = PHQ9))  + geom_bar()

# not currently using this but it is mighty cool; composes two functions
`%c%` = function(x,y)function(...)x(y(...))

# compute closeness centrality
pathz <- shortest.paths(d04$graph,  v=V(d04$graph)$name[!is.na(V(d04$graph)$Completed.) & V(d04$graph)$Completed.==" true"  & V(d04$graph)$PHQ9.questions.answered == 9])
meanpaths <- matrix(apply(pathz, 1, function(x)mean(x[is.finite(x)])), nrow(pathz))
hist(phq9[meanpaths <= 2.216], breaks=c(0:26), right=TRUE)
hist(phq9[meanpaths > 2.216], breaks=c(0:26), right=TRUE)
close2.cent <- data.frame(closeness = c("<= 2.317","<= 2.317",">2.317",">2.317"), phq9 = c("<15", ">=15","<15", ">=15"), counts = c(length(phq9[meanpaths <= 2.317 & phq9 < 15]),length(phq9[meanpaths <= 2.317 & phq9 >= 15]),length(phq9[meanpaths > 2.317 & phq9 < 15]),length(phq9[meanpaths > 2.317 & phq9 >= 15])))
ggplot(data=close2.cent, aes(x=closeness, y=counts, fill = phq9))  + geom_bar()

# compute closeness
totpaths <- as.vector(matrix(apply(pathz, 1, function(x)(sum(x[is.finite(x)]))), nrow(pathz)))
 totpaths[totpaths == 0] <- Inf
#pdf('hist-phq-cc-1.pdf')
hist(phq9[totpaths <= 48628], breaks=c(0:26), right=TRUE)
#pdf('hist-phq-cc-2.pdf')
hist(phq9[totpaths > 48628], breaks=c(0:26), right=TRUE)
#dev.off()
close.cent <- data.frame(Closeness = c("below median","below median","above median","above median"), PHQ9 = c("<15", ">=15","<15", ">=15"), Counts = c(length(phq9[totpaths <= 48630 & phq9 < 15]),length(phq9[totpaths <= 48630 & phq9 >= 15]),length(phq9[totpaths > 48630 & phq9 < 15]),length(phq9[totpaths > 48630 & phq9 >= 15])))
ggplot(data=close.cent, aes(x=Closeness, y=Counts, fill = PHQ9))  + geom_bar()

# Compute betweenness centrality
betw <- betweenness(d04$graph, v=V(d04$graph)$name[!is.na(V(d04$graph)$Completed.) & V(d04$graph)$Completed.==" true"  & V(d04$graph)$PHQ9.questions.answered == 9])
pdf('phq-hist-bt-1.pdf')
hist(phq9[betw <= 897 ], breaks=c(0:26), right=TRUE)
hist(phq9[betw > 897 ], breaks=c(0:26), right=TRUE)
betw.cent <- data.frame(Betweenness = c("below median","below median","above median","above median"), PHQ9 = c("<15", ">=15","<15", ">=15"), Counts = c(length(phq9[betw <= 897 & phq9 < 15]),length(phq9[betw <= 897 & phq9 >= 15]),length(phq9[betw > 897 & phq9 < 15]),length(phq9[betw > 897 & phq9 >= 15])))
ggplot(data=betw.cent, aes(x=Betweenness, y=Counts, fill = PHQ9))  + geom_bar()

# Now get additional info on the growth in friends over time
names <- V(d04$graph)$name[!is.na(V(d04$graph)$Completed.) & V(d04$graph)$Completed.==" true" & V(d04$graph)$PHQ9.questions.answered == 9]
d04.data <- as.data.frame(cbind(deg,phq9,names))

deg.3 <- degree(d03$graph, v=V(d03$graph)$name[!is.na(V(d03$graph)$Completed.) & V(d03$graph)$Completed.==" true"  & V(d03$graph)$PHQ9.questions.answered == 9])
phq9.3 <- V(d03$graph)$PHQ9.score[!is.na(V(d03$graph)$Completed.) & V(d03$graph)$Completed.==" true" & V(d03$graph)$PHQ9.questions.answered == 9]
names.3 <- V(d03$graph)$name[!is.na(V(d03$graph)$Completed.) & V(d03$graph)$Completed.==" true" & V(d03$graph)$PHQ9.questions.answered == 9]
d03.data <- as.data.frame(cbind(deg.3,phq9.3,names.3))

almostalld34<-merge(d03.data, d04.data, by.x="names.3", by.y ="names")
fdiff <- as.integer(as.vector(almostalld34$deg)) - as.integer(as.vector(almostalld34$deg.3))

phqdiff <- as.integer(as.vector(almostalld34$phq9))

h34 <- hist2d(fdiff,phqdiff)
persp3d(h34$x, h34$y, h34$counts, xlab="degree", zlab="counts", ylab="PHQ 9 score")
hist(phqdiff[fdiff<= 14], breaks=c(0:26), right=TRUE)
hist(phqdiff[fdiff > 14], breaks=c(0:26), right=TRUE)

#adjust the lights
rgl.clear(type="lights")
light3d(theta = 90,phi=0)

# Plots two ecdfs superimposed onto one graph
plot(ecdf(d04$degree.low[d04$degree.low<200]))
points(d04$degree.high[d04$degree.high<200],ecdf(d04$degree.high[d04$degree.high<200])(d04$degree.high[d04$degree.high<200]))

median.correlation.confidence <- function (x,y,dep.thresh,count.thresh) {
  nums <- 0
  counts <- length(x[x >= summary(x)["Median"] & y <= dep.thresh])
  for (i in 1:100000) {
    newx <- sample(x)
    if (length(newx[newx >= summary(x)["Median"] & y<=dep.thresh]) >= count.thresh)
      nums <- nums + 1
  }
  return (nums)
}
correlation.confidence <- function () {
  # calculate the p value using QAP 
  corr <- cor(deg, phq9)
  count <- 0
  for (i in 1:100000) {
    newcorr = cor(sample(deg), phq9, method="kendall")
    if (corr >= newcorr) {
      count <- count + 1
    }
  }
  return (count)
}

red.meat <- function () {
  pdf('phq9-hist.pdf')
  hist(phq9, breaks=c(0:26), right=FALSE, xlab="PHQ 9 score", main="Histogram of PHQ 9 Scores")
  dev.off()
  pdf('deg-vs-phq9-scatter.pdf')
  plot (deg, phq9, xlab="Degree", ylab="PHQ 9 Score", main="Degree vs. PHQ 9 Score")
  dev.off()
}

new.shortest.paths <- function (g, g1) {
  output <- list ()
  for (i in 1:vcount(g1)) {
    paths <- get.shortest.paths(g, from=V(g)[V(g1)$name[i]], to=V(g)[V(g1)$name])
    pathlens <- lapply(paths, length) # functional programming attack!!
    output <- rbind(output, pathlens)
  }
  return (output)
}
get.diffs.by.sp <- function (g, g1, attrib) {
  paths = shortest.paths(g)
  index <- 1
  datadiff <- vector()
  pathdiff <- vector()
  for (i in 1:vcount(g1)) {
    if (i < vcount(g)) {
      for (j in (i+1):vcount(g)) {
        if (is.finite(paths[i,j])) {
          datadiff[index] <- abs(attrib[i] - attrib[j])
          pathdiff[index] <- paths[[j]]
          index <- index + 1
        }
      }
    }
  }
  return (cbind(pathdiff, datadiff))
}

get.ave.by.paths  <- function (g,g1, attrib) {
  paths <- new.shortest.paths(g,g1)
  index <- 1
  count <- vector(mode="integer")
  pathdiff <- vector(mode="integer")
  for (i in 1:vcount(g)) {
    if (i < vcount(g)) {
      for (j in (i+1):vcount(g)) {
        if (is.finite(paths[[i,j]])) {
          if (is.na(pathdiff[paths[[i,j]]+1])) {
            pathdiff[paths[[i,j]]+1] <- 0
            count[paths[[i,j]]+1] <- 0
          }
          pathdiff[paths[[i,j]]+1] <- pathdiff[paths[[i,j]]+1] + abs(attrib[i] - attrib[j])
          count[paths[[i,j]]+1] <- count[paths[[i,j]]+1] + 1
        }
      }
    }
  }
  for (i in 1:length(count)) {
    pathdiff[i] <- pathdiff[i] / count[i]
  }
  return (pathdiff)
}
# If we had set directed=T above, then we could make it undirected like so:
# tsfull_sym <- as.undirected(tsfull_sym, mode='collapse')

# This creates an array of connected components
#tsfull_comps <- 3(tsfull_sym)
# There are nine connected components, all but the first one has
# exactly 2 verts
#graph1 <- tsfull_comps[[1]]
#deg_graph1 <- degree(graph1)

# Gives statistical summary of graph
#summary(graph1)
# Gives statistical summargy of degree distribution
#summary(deg_graph1)
# plots min, quartiles, median, and max of distribution
#fivenum(deg_graph1)

# This will plot the data using some as yet unknown layout
# (which is moot because there is too much data here
#pdf("full.pdf")
#plot(tsfull_sym)
#dev.off()


