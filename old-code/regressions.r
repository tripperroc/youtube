data <- data.frame(name = V(full.graph.edges.only)$name, PHQ9_score=V(full.graph.edges.only)$PHQ9_score,
                   degree=V(full.graph.edges.only)$degree,
                   closeness=V(full.graph.edges.only)$closeness,
                   betweenness=V(full.graph.edges.only)$betweenness,
                   completed=V(full.graph.edges.only)$completed,
                   PHQ9_questions_answered=V(full.graph.edges.only)$PHQ9_questions_answered,
                   psychological_counseling_would_last_resort =V(full.graph.edges.only)$psychological_counseling_would_last_resort,
                   emotional_issues_with_my_family =V(full.graph.edges.only)$emotional_issues_with_my_family,
                   help_if_i_serious_problem=V(full.graph.edges.only)$help_if_i_serious_problem,
                   i_could_find_relief_counseling=V(full.graph.edges.only)$i_could_find_relief_counseling   )

trans <- transitivity (full.graph.edges.only, type="local")
trans[is.na(trans)] <- 0
data2 <- data.frame(name = V(full.graph.edges.only)$name,
                   degree=V(full.graph.edges.only)$degree,
                   closeness=V(full.graph.edges.only)$closeness,
                   betweenness=V(full.graph.edges.only)$betweenness, transitivity=trans)

d2<- merge (data2, survey, by.x="name", by.y="hashed_id", all.x=TRUE)

d3 <- d2[!is.na(d2$completed)&d2$completed=="true"&d2$PHQ9_questions_answered==9,]

m <- lm (PHQ9_score ~ log(degree), data=d3)
plot(PHQ9_score ~ log(degree), data=d3)
abline(m)

m <- lm (PHQ9_score ~ log(betweenness+1), data=d3)
plot(PHQ9_score ~ log(betweenness+1), data=d3)
abline(m)

supermodel <- lm(PHQ9_score ~ log(degree) + log(betweenness+1) + log(closeness) + help_if_i_serious_problem
                 +transitivity
+need_talk_about_my_worries
+make_too_many_demands_me                     
+ i_feel_comfortable_talking_with              
+ emotional_issues_with_my_family              
+ who_noticed_i_was_upset                      
+ their_emotions_good_and_bad                  
+ not_comfortable_discussing_emotional_issues
+  gay_bisexual_attracted_males_straight
+ i_could_find_relief_counseling               
+ fears_without_resorting_professional_help    
+ upset_for_long_period_time                   
+ psychological_counseling_would_last_resort   
+ tend_work_out_by_themselves
+ information_about_yourself_over_internet     
+ what_consequences_been,
                 data=d3)

supermodel2 <- lm(PHQ9_score ~
  i_could_find_relief_counseling               
+ upset_for_long_period_time        
+ gay_bisexual_attracted_males_straight
+ emotional_issues_with_my_family              
+ log(betweenness+1)
+ information_about_yourself_over_internet 
+ help_if_i_serious_problem, data=d3  )

supermodel3 <- lm (PHQ9_score ~ log(betweenness + 1)+information_about_yourself_over_internet+help_if_i_serious_problem ,
data=d3)

supermodel4 <- lm (PHQ9_score ~ tend_work_out_by_themselves
                   + gay_bisexual_attracted_males_straight+ transitivity
                   + log(closeness)
                   + emotional_issues_with_my_family
                   + log(betweenness + 1)
                   + information_about_yourself_over_internet
                   + upset_for_long_period_time
                   + help_if_i_serious_problem, data=d3) 

supermodel5 <- lm (PHQ9_score ~ emotional_issues_with_my_family + 
log(betweenness + 1)   +
upset_for_long_period_time  +
help_if_i_serious_problem, data=d3)

supermodel6 <- lm (PHQ9_score ~ log(betweenness + 1)+     
upset_for_long_period_time+
help_if_i_serious_problem, data=d3)


degree.lm <- lm(degree ~ PHQ9_score+emotional_issues_with_my_family+help_if_i_serious_problem+i_could_find_relief_counseling, data=d)
closeness.lm <- lm(closeness ~ PHQ9_score+emotional_issues_with_my_family+help_if_i_serious_problem+i_could_find_relief_counseling, data=d)
betweenness.lm <- lm(betweenness ~ PHQ9_score+emotional_issues_with_my_family+help_if_i_serious_problem+i_could_find_relief_counseling, data=d)

#cor.test(d$PHQ9_score, d$betweenness, method="spearman")
#cor.test(d$PHQ9_score, d$degree, method="spearman")

#cor.test(d$help_if_i_serious_problem[d$help_if_i_serious_problem>=0], d$degree[d$help_if_i_serious_problem>=0], method="spearman")
#cor.test(d$help_if_i_serious_problem[d$help_if_i_serious_problem>=0], d$betweenness[d$help_if_i_serious_problem>=0], method="spearman")
pdf("test3.pdf", width=7, height=2.5 )
#par(pin=c(8,4))
par(mfrow=c(1,3))
#plot.new()

mod <- lm(PHQ9_score ~ log(betweenness+1), data =d3)
plot(PHQ9_score ~ log(betweenness+1),  data=d3)
abline(sm.b)

sm.b <- lm ( PHQ9_score ~ upset_for_long_period_time , data=d3)
plot( PHQ9_score ~upset_for_long_period_time,  data = d3, xlab="I would want to get psychological help if I were worried or upset for a long period of time.")
abline(sm.b)

#plot.new()
sm.h <- lm ( PHQ9_score ~ help_if_i_serious_problem , data=d3)
plot (PHQ9_score~help_if_i_serious_problem,  data = d3)
abline(sm.h)
dev.off()

cor.test2 <- function (one, two) {
  # calculate the p value using QAP 
  count <- 0
  c <- cor(one, two)
  for (i in 1:10000) {
           
    newcorr = cor(sample(one),two)
   if ((c < newcorr & c > 0) | (c > newcorr & c < 0)) {
      count <- count + 1
    }
  }
  return (count/10000)
}
