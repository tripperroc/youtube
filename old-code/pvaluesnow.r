library("rjson")

d <- fromJSON(file="triangles_snow_all.json", method="C")
triangles.all <- do.call(rbind.data.frame,d)
triangles.all.data <- triangles.all[c(2:dim(triangles.all)[1]),]
triangles.all.real <- triangles.all[1,]
d <- fromJSON(file="degrees_snow_all.json", method="C")
degrees.all <- do.call(rbind.data.frame,d)
degrees.all.data <- degrees.all[c(2:dim(degrees.all)[1]),]
degrees.all.real <- degrees.all[1,]
d <- fromJSON(file="clustering_snow_all.json", method="C")
clustering.all <- do.call(rbind.data.frame,d)
clustering.all.data <- clustering.all[c(2:dim(clustering.all)[1]),]
clustering.all.real <- clustering.all[1,]
d <- fromJSON(file="core_number_snow_all.json", method="C")
core_number.all <- do.call(rbind.data.frame,d)
core_number.all.data <- core_number.all[c(2:dim(core_number.all)[1]),]
core_number.all.real <- core_number.all[1,]

d <- fromJSON(file="lccs_snow.json", method="C")
lccs.all <- do.call(rbind.data.frame,d)
lccs.all.real <- lccs.all[1,]
lccs.all.data <- lccs.all[c(2:dim(lccs.all)[1]),]

pdf("paper/core-number-respondent-snow.pdf")
hist(core_number.all.data$union.all.full,xlim=c(5,150),main="Histogram of Median Core Numbers",xlab="Median Core Numbers", probability=T, cex=1.5)
axis(1, at=57, font=2)
abline(v=57,lwd=3,lty=2)
dev.off()

pdf("paper/degree-respondent-snow.pdf")
hist(degrees.all.data$union.all.full,xlim=c(5,140),main="Histogram of Median Degrees",xlab="Median Degrees",probability=T, cex=1.5)
abline(v=degrees.all.real$union.all.full,lwd=3,lty=2)
axis(1, at=degrees.all.real$union.all.full, font=2)
dev.off()

pdf("paper/triangles-respondent-snow.pdf")
hist(triangles.all.data$union.all.full,xlim=c(0,1400),main="Histogram of Median Triangles",xlab="Median Triangles",probability=T, cex=1.5)
axis(1, at=triangles.all.real$union.all.full, font=2)
abline(v=triangles.all.real$union.all.full,lwd=3,lty=2)
dev.off()


pdf("paper/clustering-respondent-snow.pdf")
hist(clustering.all.data$union.all.full, main="Histogram of Median Clustering Coefficient",xlab="Median Clustering Coefficient",probability=T, cex=1.5)
abline(v=clustering.all.real$union.all.full,lwd=3,lty=2)
dev.off()

clustering.all.real$union.all.full


pdf("paper/connected-components-respondent-snow.pdf")
hist(lccs.all.data$cc, xlim=c(0,300),main="Histogram of Largest Connected Component Size",xlab="Largest Connected Component Size",probability=T, cex=1.5)
abline(v=lccs.all.real$cc,lwd=3,lty=2)
axis(1, at=lccs.all.real$cc, font=2)
dev.off()

pdf("paper/biconnected-components-respondent-snow.pdf")
hist(lccs.all.data$bicc, xlim=c(0,330),main="Histogram of Largest Biconnected Component Size",xlab="Largest Biconnected Component Size",probability=T, cex=1.5)
abline(v=lccs.all.real$bicc,lwd=3,lty=2)
axis(1, at=lccs.all.real$bicc, font=2)
dev.off()

