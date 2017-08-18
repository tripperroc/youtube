makesvs <- function (g) {
  data <- get.vertex.attributes(g)
  index <- 1
  mat <- matrix(nrow=dim(data)[1]*(dim(data)[1]-1), ncol=2*(dim(data)[2]-1)+1)
  for (i in 1:length(V(g))) {
    for (j in (i+1):length(V(g))) {
      if (V(g)[i] %in% neighbors(g, V(g)[j])) {
        class <- 1
      }
      else {
        class <- -1
      }
      print ("working...")
      dat <- c(class, data[i,2:dim(data)[2]], data[j,2:dim(data)[2]])
      mat[index,] <- matrix(dat, nrow=1, ncol=length(dat))
      index <- index + 1
      dat <- c(class, data[j,2:dim(data)[2]], data[i,2:dim(data)[2]])
      mat[index,] <- matrix(dat, nrow=1, ncol=length(dat))
      index <- index + 1
    }
  }
  return(mat)
}

make.svs <- function (g) {
    data <- get.vertex.attributes(g)
    return(matrix(nrow=length(V(g))*(length(V(g))-1), ncol=2*dim(data)[2]-1, ,byrow=TRUE, data=unlist(lapply (1:(length(V(g))-1), FUN=function (i) {
      lapply ((i+1):length(V(g)), FUN=function (j) {
        if (V(g)[i] %in% neighbors(g, V(g)[j])) {
          class <- 1
        }
        else {
          class <- -1
        }
        return (c(class, data[i,2:dim(data)[2]], data[j,2:dim(data)[2]], class, data[j,2:dim(data)[2]], data[i,2:dim(data)[2]])) })
    }))))
}
