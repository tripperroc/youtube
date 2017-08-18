pdf("paper/core-number-respondent.pdf")
hist(core_number.all.data$union.all.full,xlim=c(5,59),main="Histogram of Median Core Numbers",xlab="Median Core Numbers", probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
axis(1, at=57, font=2)
abline(v=57,lwd=3,lty=2)
dev.off()

pdf("paper/degree-respondent.pdf")
hist(degrees.all.data$union.all.full,xlim=c(5,70),main="Histogram of Median Degrees",xlab="Median Degrees",probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
abline(v=degrees.all.real$union.all.full,lwd=3,lty=2)
axis(1, at=degrees.all.real$union.all.full, font=2)
dev.off()

pdf("paper/triangles-respondent.pdf")
hist(triangles.all.data$union.all.full,xlim=c(0,700),main="Histogram of Median Triangles",xlab="Median Triangles",probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
axis(1, at=triangles.all.real$union.all.full, font=2)
abline(v=triangles.all.real$union.all.full,lwd=3,lty=2)
dev.off()


pdf("paper/clustering-respondent.pdf")
hist(clustering.all.data$union.all.full, main="Histogram of Median Clustering Coefficient",xlab="Median Clustering Coefficient",probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
abline(v=clustering.all.real$union.all.full,lwd=3,lty=2)
dev.off()

clustering.all.real$union.all.full


pdf("paper/connected-components-respondent.pdf")
hist(lccs.all.data$cc, xlim=c(0,170),main="Histogram of Largest Connected Component Size",xlab="Largest Connected Component Size",probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
abline(v=lccs.all.real$cc,lwd=3,lty=2)
axis(1, at=lccs.all.real$cc, font=2)
dev.off()

pdf("paper/biconnected-components-respondent.pdf")
hist(lccs.all.data$bicc, xlim=c(0,130),main="Histogram of Largest Biconnected Component Size",xlab="Largest Biconnected Component Size",probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
abline(v=lccs.all.real$bicc,lwd=3,lty=2)
axis(1, at=lccs.all.real$bicc, font=2)
dev.off()

pdf("paper/core-number-phq9.pdf")
hist(core_number.data$union.low.full - core_number.data$union.high.full ,main="Histogram of Median Core Numbers",xlab="Median Core Numbers", probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
abline(v=core_number.real$union.low.full,lwd=3,lty=2)
dev.off()

pdf("paper/degree-phq9.pdf")
hist(degrees.data$union.low.full-degrees.data$union.high.full,main="Histogram of Median Degrees",xlab="Median Degrees",probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
abline(v=degrees.real$union.low.full-degrees.real$union.high.full,lwd=3,lty=2)
dev.off()

pdf("paper/triangles-phq9.pdf")
hist(triangles.data$union.low.full-triangles.data$union.high.full,main="Histogram of Median Triangles",xlab="Median Triangles",probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
abline(v=triangles.real$union.low.full-triangles.real$union.high.full,lwd=3,lty=2)
dev.off()


pdf("paper/clustering-phq9.pdf")
hist(clustering.data$union.low.full-clustering.data$union.high.full, main="Histogram of Median Clustering Coefficient",xlab="Median Clustering Coefficient",probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
abline(v=clustering.real$union.low.full-clustering.real$union.high.full,lwd=3,lty=2)
dev.off()

clustering.real$union.full


pdf("paper/connected-components-phq9.pdf")
hist(lccs.data$cc.low-lccs.data$cc.high , main="Histogram of Largest Connected Component Size",xlab="Largest Connected Component Size",probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
abline(v=lccs.real$cc.low-lccs.real$cc.high,lwd=3,lty=2)
dev.off()

pdf("paper/biconnected-components-phq9.pdf")
hist(lccs.data$bicc.low-lccs.data$bicc.high,main="Histogram of Largest Biconnected Component Size",xlab="Largest Biconnected Component Size",probability=T, cex=1.5, cex.lab=1.5, cex.main=1.5, cex.axis=1.5)
abline(v=lccs.real$bicc.low-lccs.real$bicc.high,lwd=3,lty=2)
dev.off()


summary(lccs.data$cc.low-lccs.data$cc.high >=  lccs.real$cc.low-lccs.real$cc.high)
summary(lccs.data$bicc.low-lccs.data$bicc.high >=  lccs.real$bicc.low-lccs.real$bicc.high)
summary(triangles.data$union.low.full-triangles.data$union.high.full >=  triangles.real$union.low.full-triangles.real$union.high.full)
summary(degrees.data$union.low.full-degrees.data$union.high.full >=  degrees.real$union.low.full-degrees.real$union.high.full)
summary(clustering.data$union.low.full-clustering.data$union.high.full >=  clustering.real$union.low.full-clustering.real$union.high.full)
summary(core_number.data$union.low.full-core_number.data$union.high.full >=  core_number.real$union.low.full-core_number.real$union.high.full)

