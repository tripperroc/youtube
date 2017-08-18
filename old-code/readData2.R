# clear work space and set directory
#rm(list = ls())
# laptop
#setwd('C:/Users/LamTran/Dropbox/twitterhealth/ts')
# home computer
#setwd('C:/Users/lam/Dropbox/twitterhealth/ts')

inputFile <- "trevorspace_responses.csv"
con  <- file(inputFile, open = "r")
dataList <- list()
close(con)
dataList  <- as.character(dataList)
responses    <- strsplit(dataList, "[/^]")

# find number of the question
numQuestion <- length(unlist(responses[1]))

# genearte matrix
resMat <- matrix(0, length(responses)-1, length(unlist(responses[1])) )


# response don't have same length, add 0 to the end to generate a matrix
for (i in 2:length(responses) ) {
   v <- unlist(responses[i])
   misNQ <-  length(unlist(responses[1])) - length(v)
   v <- c(v,  rep("", misNQ)) 
   resMat[i-1,] <- v
}


# remove subject that did not complete survey
index <- resMat[,7]==9
resMat <- resMat[index,]


# get unique ids
ids <- unique(resMat[,1])

# generate hash table
rm(hashtable)
hashtable<-new.env()
u <- 1
f <-  matrix(unlist(resMat[,1])) # convert list to matrix

# count survey each subject took
for( i in 1:length(f)){
   hashtable[[f[i]]] <- c(hashtable[[f[i]]], u)
   u <- u + 1
}

# convert hashtable into table
rm(hashList )
rowRemove = c()
hashList <- matrix("1", length(ids), 2 )
for( i in 1:length(ids)){
   v <- hashtable[[ids[i]]]
   w <- v[1]
   if( length(v) > 1 ){
     w <- paste(w, ",")
     for( j in 2:length(v)){
       rowRemove <- c(rowRemove, v[j])
       w <- paste(w, v[j], ",")
     }
   }
   hashList[i,] <- c(ids[i], w )
}





# count function
count <- function(x) {
   if(exists( x[1], hashtable) == TRUE ){
      hashtable[[x[1]]] <- hashtable[[x[1]]] + 1
	#hashtable[[x[2]]] <- hashtable[[x[2]]] + 1
   }

  if(exists( x[2], hashtable,) == TRUE ){
      hashtable[[x[2]]] <- hashtable[[x[2]]] + 1
   }
}

# Load edge file
edges  <- read.table("edges_encrypted_3-21-12.txt.mac")
edges  <- as.character(unlist(edges))
edgesp <- strsplit(edges, ",")

edges2  <- read.table("edges_encrypted_4-20-12.txt.mac")
edges2  <- as.character(unlist(edges))
edgesp2 <- strsplit(edges, ",")



#edgesp<- edgesp[1:1000]
edgesd <-do.call(rbind, edgesp)
edgesd2 <-do.call(rbind, edgesp2)

# find unique id and initialize it to zero.
hashtable<-new.env()
apply(matrix(ids) ,1,function(x) hashtable[[x]]<- 0 )
 
# assume that it is a undirected graph and count the number of edges.
apply(matrix(edgesd) ,1, function(x) count(x) )
apply(matrix(edgesd2) ,1, function(x) count(x) )



# convert hashtable into table
rm(hashList2)
hashList2 <- matrix("1", length(ids), 2 )
for( i in 1:length(ids)){
   v <- hashtable[[ids[i]]]
   hashList2[i,] <- c(ids[i], v )
}



