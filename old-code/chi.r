# Analysis of TrevorSpace data for CHI '13
# By Christopher Homan
library(igraph)
#library(NetData)
library(ggplot2)
library(gplots)
#library(sna)
#library(rgl)

get.vertex.attributes <- function(graph) {
  as.data.frame(unclass(graph)[[9]][[3]], stringsAsFactors=FALSE)
}

print ("working...")
# Change to your working directory
setwd('/Users/cmh/sn/ts/TSpace')

# Read data
source('functions.r')
survey <- read.csv('trevorspace_responses.csv', sep="^")
survey <- subset (survey, subset=(!duplicated(survey$hashed_id)))
graph.edges <- read.csv('edges_encrypted_3-21-12.txt')
graph.edges <- unique (graph.edges)
colnames(graph.edges) <- c('ego', 'alter')


#########################################
# Create various graphs from the input data
#
# Glean all vertex names from the graph.edges dataframe
ego <- graph.edges[1]
alter <- graph.edges[2]
colnames(alter) <- 'ego'
graph.verts <- unique(rbind(ego,alter))

# Merge the vertices with the respondent data, create master graph
fulldata <- merge (graph.verts, survey, by.x="ego", by.y="hashed_id", all=T)
full.graph <- as.undirected(graph.data.frame(d = graph.edges, vertices = fulldata), mode='collapse')

# Cull all nonrespondents from the master graph
respondent.graph <- delete.vertices(full.graph, V(full.graph)[is.na(get.vertex.attribute(full.graph, name="completed")) | completed=="false"])

# Now, omit isolated vertices (we do this because we don't really know the number of isolated
# verts in the full graph)
fulldata.edges.only <- merge (graph.verts, survey, by.x="ego", by.y="hashed_id", all.x=TRUE)
full.graph.edges.only <- as.undirected(graph.data.frame(d = graph.edges, vertices = fulldata.edges.only), mode="collapse")
full.graph.edges.only.respondents <- delete.vertices(full.graph.edges.only, V(full.graph.edges.only)[is.na(get.vertex.attribute(full.graph.edges.only, name="completed")) | completed=="false"])
full.graph.edges.only.phq9 <- delete.vertices(full.graph.edges.only.respondents, V(full.graph.edges.only.respondents)[PHQ9_questions_answered != 9])

# Get degree distributions, for master and respondent graphs
print("getting degree distributions...")
full.graph.degree.cdf <- degree.distribution(full.graph, cumulative=TRUE)
respondent.graph.degree.cdf <- degree.distribution(respondent.graph, cumulative=TRUE)

# ...and for the nonisolated vertices graph.
degree.dist.edges.only <- degree.distribution(full.graph.edges.only, cumulative=TRUE)
print("HELP!!!")
degree.dist.edges.only.respondents.only <- degree.distribution(full.graph.edges.only, v=V(full.graph.edges.only)[!is.na(V(full.graph.edges.only)$completed) & completed=="true"], cumulative=TRUE)
degree.dist.edges.only.phq <- degree.distribution(full.graph.edges.only,v=V(full.graph.edges.only)[!is.na(V(full.graph.edges.only)$completed) & completed=="true" & PHQ9_questions_answered == 9], cumulative=TRUE)

# get largest connected component of each graph
full.graph.edges.only <- decompose.graph(full.graph.edges.only)[[1]]
full.graph.edges.only.respondents <- decompose.graph(full.graph.edges.only.respondents)[[1]]
full.graph.edges.only.phq9 <- decompose.graph(full.graph.edges.only.phq9)[[1]]

# Get summary degree information for same
deg.all <- degree(full.graph.edges.only)
deg.resp <- degree(full.graph.edges.only, v=V(full.graph.edges.only)[!is.na(V(full.graph.edges.only)$completed) & completed=="true"])
deg.phq <- degree(full.graph.edges.only,v=V(full.graph.edges.only)[!is.na(V(full.graph.edges.only)$completed)  & completed=="true" & PHQ9_questions_answered == 9])

# Get graph density (# of actual edges / # possible edges)
# is slightly less in the respondent graph;
# could be because respondent graph has multiple components
print ("calculating graph density/clustering...")
dense.all <- graph.density(full.graph.edges.only)
dense.resp <- graph.density (full.graph.edges.only.respondents)
dense.PHQ <- graph.density(full.graph.edges.only.phq9)


# see http://sna.stanford.edu/lab.php?l=3
#make_k_core_plot <- function (g) {
#    lay1 <- layout.fruchterman.reingold(g)
#    plot(g, 
#         vertex.color = graph.coreness(g), 
#         layout=lay1, 
#         edge.arrow.size = .5)
#}
#make_k_core_plot(full.graph.edges.only.respondents)

# get clustering coefficients
# for respondents, this is slightly higher
cc.all <- transitivity (full.graph.edges.only, "global")
cc.resp <- transitivity (full.graph.edges.only.respondents, "global")
cc.phq9 <- transitivity (full.graph.edges.only.phq9, "global")

all.data <- list (graph = full.graph.edges.only, density = dense.all, cc = cc.all, degree = deg.all, degree.dist = degree.dist.edges.only)

                             
# Compute closeness centrality
print("calculating closeness...")
#paths <- shortest.paths(full.graph.edges.only)
#closeness.alt <- as.vector(matrix(apply(paths, 1, function(x)mean(x[is.finite(x)])), nrow(paths)))
#cloesness.alt[closeness.alt == 0] <- Inf
closeness.all <- closeness (full.graph.edges.only)

# Compute betweeness centrality
print("calculating betweenness...")
betweenness.all <- betweenness (full.graph.edges.only)

# Compute stress centrality
#stress.all <- stresscent(full.graph.edges.only)


signif.full <- signif(full.graph.edges.only,full.graph.edges.only.respondents, 10000)
signif.resp <- signif(full.graph.edges.only.respondents, full.graph.edges.only.phq9, 1000)

density.df <- data.frame(Graph = c("TrevorSpace", "Mean Respondent Size", "Mean PHQ", "Respondents Only", "PHQ9 > 9"), Density = c(dense.all, mean(signif.full$densities,na.rm = TRUE),  mean(signif.resp$densities,na.rm = TRUE), dense.resp, dense.PHQ))
ggplot(data=density.df, aes(x=Graph, y=Density,  fill = Graph))  + geom_bar()
ggsave("densities.pdf")

#print(paste("Density of entire graph:", dense.all))
#print(paste("Density of respondent graph:", dense.resp))

print("graphing...")

# Graph degree degree distributions of all vs. just respondents
edges.only.all.df <- data.frame(c(1:length(degree.dist.edges.only)), degree.dist.edges.only, "all")
edges.only.respondents.df <- data.frame(c(1:length(degree.dist.edges.only.respondents.only)), degree.dist.edges.only.respondents.only, "respondents")
edges.only.PHQ.df <- data.frame(c(1:length(degree.dist.edges.only.phq)), degree.dist.edges.only.phq , "PHQ9 < 10")
colnames(edges.only.all.df) <- c("degree", "density", "type")
colnames(edges.only.respondents.df) <- c("degree", "density", "type")
edges.only.df <- rbind(edges.only.al
                       l.df, edges.only.respondents.df)
qplot(log(degree), log(density), data=edges.only.df, geom="point", colour=type)
ggsave("deg.all.vs.respondents.pdf")

  
full.graph.edges.only <- set.vertex.attribute(full.graph.edges.only,"cc",value=cc.all)

full.graph.edges.only <- set.vertex.attribute(full.graph.edges.only,"betweenness",value=betweenness.all)
full.graph.edges.only <- set.vertex.attribute(full.graph.edges.only,"closeness",value=closeness.all)
full.graph.edges.only <- set.vertex.attribute(full.graph.edges.only,"closeness",value=closeness.all)
full.graph.edges.only <- set.vertex.attribute(full.graph.edges.only,"degree",value=deg.all)

## PHQ9 questions
# little_interest_doing_things
# feeling_down_depressed_hopeless
# falling_asleep_sleeping_too_much
# feeling_tired_having_little_energy
# poor_appetite_overeating
# let_yourself_your_family_down
# as_reading_newspaper_watching_television
# around_lot_more_than_usual
# dead_hurting_yourself_some_way

# get_along_with_other_people
