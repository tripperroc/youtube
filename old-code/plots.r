pdf("test3.pdf", width=7, height=2.5 )
#par(pin=c(8,4))
par(mfrow=c(1,3))
#plot.new()

mod <- lm(PHQ9_score ~ log(betweenness+1), data =d3)
plot(PHQ9_score ~ log(betweenness+1),  data=d3, xlab="Betweenness", ylab="PHQ 9")
abline(sm.b)

sm.b <- lm ( PHQ9_score ~ upset_for_long_period_time , data=d3)
plot( PHQ9_score ~upset_for_long_period_time,  data = d3, xlab="Want psychological help if upset for long", ylab="")
abline(sm.b)

#plot.new()
sm.h <- lm ( PHQ9_score ~ help_if_i_serious_problem , data=d3)
plot (PHQ9_score~help_if_i_serious_problem,  data = d3, xlab="Can rely friends if have a serious problem", ylab="")
abline(sm.h)
dev.off()
