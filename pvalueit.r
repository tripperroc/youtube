library("rjson")
d <- fromJSON(file="triangles_med.json", method="C")
triangles <- do.call(rbind.data.frame,d)
triangles.data <- triangles[c(2:dim(triangles)[1]),]
triangles.real <- triangles[1,]
d <- fromJSON(file="degrees_med.json", method="C")
degrees <- do.call(rbind.data.frame,d)
degrees.data <- degrees[c(2:dim(degrees)[1]),]
degrees.real <- degrees[1,]
d <- fromJSON(file="clustering_med.json", method="C")
clustering <- do.call(rbind.data.frame,d)
clustering.data <- clustering[c(2:dim(clustering)[1]),]
clustering.real <- clustering[1,]
d <- fromJSON(file="core_number_med.json", method="C")
core_number <- do.call(rbind.data.frame,d)
core_number.data <- core_number[c(2:dim(core_number)[1]),]
core_number.real <- core_number[1,]

d <- fromJSON(file="lccs.json", method="C")
lccs <- do.call(rbind.data.frame,d)
lccs.real <- lccs[1,]
lccs.data <- lccs[c(2:dim(lccs)[1]),]

d <- fromJSON(file="triangles_med_all.json", method="C")
triangles.all <- do.call(rbind.data.frame,d)
triangles.all.data <- triangles.all[c(2:dim(triangles.all)[1]),]
triangles.all.real <- triangles.all[1,]
d <- fromJSON(file="degrees_med_all.json", method="C")
degrees.all <- do.call(rbind.data.frame,d)
degrees.all.data <- degrees.all[c(2:dim(degrees.all)[1]),]
degrees.all.real <- degrees.all[1,]
d <- fromJSON(file="clustering_med_all.json", method="C")
clustering.all <- do.call(rbind.data.frame,d)
clustering.all.data <- clustering.all[c(2:dim(clustering.all)[1]),]
clustering.all.real <- clustering.all[1,]
d <- fromJSON(file="core_number_med_all.json", method="C")
core_number.all <- do.call(rbind.data.frame,d)
core_number.all.data <- core_number.all[c(2:dim(core_number.all)[1]),]
core_number.all.real <- core_number.all[1,]

d <- fromJSON(file="lccs_all.json", method="C")
lccs.all <- do.call(rbind.data.frame,d)
lccs.all.real <- lccs.all[1,]
lccs.all.data <- lccs.all[c(2:dim(lccs.all)[1]),]

pdf("paper/core-number-respondent.pdf")
hist(core_number.all.data$union.all.full,xlim=c(5,59),main="",xlab="",ylab="",yaxt = "n", probability=T, cex.lab=3)
axis(1, at=57, font=2)
abline(v=57,lwd=3,lty=2)
 mtext(side = 1, text = "Median Core Numbers", line = 3.5, cex = 3)
mtext(side = 2, text = "Density", line = 1, cex =3)
dev.off()

pdf("paper/degree-respondent.pdf")
hist(degrees.all.data$union.all.full,xlim=c(5,70),main="",xlab="",ylab="",yaxt = "n",probability=T, cex.lab=2, cex=3)
abline(v=degrees.all.real$union.all.full,lwd=3,lty=2)
axis(1, at=degrees.all.real$union.all.full, font=2)
 mtext(side = 1, text = "Median Degree", line = 3.5, cex =3)
 mtext(side = 2, text = "Density", line = 1, cex =3)
dev.off()

pdf("paper/triangles-respondent.pdf")
hist(triangles.all.data$union.all.full,xlim=c(0,700),main="",xlab="",yaxt = "n",ylab="",probability=T, cex=1.5)
axis(1, at=triangles.all.real$union.all.full, font=2)
abline(v=triangles.all.real$union.all.full,lwd=3,lty=2)
 mtext(side = 1, text = "Median Triangles", line = 3.5, cex = 3)
dev.off()


pdf("paper/clustering-respondent.pdf")
hist(clustering.all.data$union.all.full, xlab="",main="",yaxt = "n",ylab="",probability=T, cex=1.5)
abline(v=clustering.all.real$union.all.full,lwd=3,lty=2)
 mtext(side = 1, text = "Median Clustering Coefficient", line = 3.5, cex = 3)
dev.off()

clustering.all.real$union.all.full

pdf("paper/connected-components-respondent.pdf")
hist(lccs.all.data$cc, xlim=c(0,170),main="",yaxt = "n",ylab="",xlab="",probability=T, cex=1.5)
abline(v=lccs.all.real$cc,lwd=3,lty=2)
axis(1, at=lccs.all.real$cc, font=2)

 #mtext(side = 1, text = "Largest", line = 2, cex = 2)
 mtext(side = 1, text = "Max Connected Component", line = 4, cex = 3)
dev.off()

pdf("paper/biconnected-components-respondent.pdf")
hist(lccs.all.data$bicc, xlim=c(0,130),main="",yaxt = "n",ylab="",xlab="",probability=T, cex=1.5)
abline(v=lccs.all.real$bicc,lwd=3,lty=2)
axis(1, at=lccs.all.real$bicc, font=2)
# mtext(side = 1, text = "Largest", line = 2, cex = 2)
 mtext(side = 1, text = "Max Biconnected Component", line = 4, cex = 3)
dev.off()

pdf("paper/core-number-phq9.pdf")
hist(core_number.data$union.low.full - core_number.data$union.high.full,main="",yaxt = "n",xlab="",ylab="", probability=T, cex=1.5)
abline(v=core_number.real$union.low.full,lwd=3,lty=2)
 mtext(side = 2, text = "Density", line = 1, cex =3)
 mtext(side = 1, text = "Median Core Numbers", line = 3.5, cex = 3)
dev.off()

pdf("paper/degree-phq9.pdf")
hist(degrees.data$union.low.full-degrees.data$union.high.full,yaxt = "n",main="",xlab="",ylab="",probability=T, cex=1.5)
abline(v=degrees.real$union.low.full-degrees.real$union.high.full,lwd=3,lty=2)
 mtext(side = 2, text = "Density", line = 1, cex =3)
 mtext(side = 1, text = "Median Degrees", line = 3.5, cex = 3)
dev.off()

pdf("paper/triangles-phq9.pdf")
hist(triangles.data$union.low.full-triangles.data$union.high.full,yaxt = "n",main="",ylab="",xlab="",probability=T, cex=1.5)
abline(v=triangles.real$union.low.full-triangles.real$union.high.full,lwd=3,lty=2)
 mtext(side = 1, text = "Median Triangles", line = 3.5, cex = 3)
dev.off()


pdf("paper/clustering-phq9.pdf")
hist(clustering.data$union.low.full-clustering.data$union.high.full,main="",yaxt = "n",ylab="", xlab="",probability=T, cex=1.5)
abline(v=clustering.real$union.low.full-clustering.real$union.high.full,lwd=3,lty=2)
 mtext(side = 1, text = "Median Clustering Coefficient", line = 3.5, cex = 3)
dev.off()

clustering.real$union.full


pdf("paper/connected-components-phq9.pdf")
hist(lccs.data$cc.low-lccs.data$cc.high ,main="",xlab="",yaxt = "n",ylab="",probability=T, cex=1.5)
abline(v=lccs.real$cc.low-lccs.real$cc.high,lwd=3,lty=2)
 mtext(side = 1, text = "Max Connected Component", line = 3.5, cex = 3)
dev.off()

pdf("paper/biconnected-components-phq9.pdf")
hist(lccs.data$bicc.low-lccs.data$bicc.high,main="",yaxt = "n",ylab="",xlab="",probability=T, cex=1.5)
abline(v=lccs.real$bicc.low-lccs.real$bicc.high,lwd=3,lty=2)
mtext(side = 1, text = "Max Biconnected Component", line = 3.5, cex = 3)
dev.off()

