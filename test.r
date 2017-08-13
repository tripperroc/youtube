c <- cor(log(d$Pagerank.2012.05.21), d$PHQ9_score, use="pairwise.complete.obs")
f <- cor(log(d$Pagerank.2012.05.21), log(d$PHQ9_score+1), use="pairwise.complete.obs")
