pdf("test.pdf")
par(mfrow=c(4,3))
dats <- subgraph.by.factor(all.data,V(all.data$graph)[!is.na(V(all.data$graph)$completed) & completed=="true"], 10000, 'TrevorSpace', 'Respondents')
resdats <- subgraph.by.factor(dats,V(dats$graph)[PHQ9_questions_answered == 9 & PHQ9_score <= 15], 1000, 'Respondents', 'PHQ9_Under_16')
resdats <- subgraph.by.factor(dats,V(dats$graph)[PHQ9_questions_answered == 9 & help_if_i_serious_problem > 2], 1000, 'Respondents', 'Rely_on_Friends_More_than_2')
resdats <- subgraph.by.factor(dats,V(dats$graph)[PHQ9_questions_answered == 9 & i_could_find_relief_counseling  > 1], 1000, 'Respondents', 'Rely_on_Counseling')
dev.off()

pdf("test2.pdf")
par(mfrow=c(3,4))

resdats <- subgraph.by.factor(dats,V(dats$graph)[PHQ9_questions_answered == 9 &  psychological_counseling_would_last_resort  > 1], 1000, 'Respondents', 'Counseling_Last_Resort')

resdats <- subgraph.by.factor(dats,V(dats$graph)[PHQ9_questions_answered == 9 & PHQ9_score > 9], 1000, 'Respondents', 'PHQ9_Over_9')
resdats <- subgraph.by.factor(dats,V(dats$graph)[PHQ9_questions_answered == 9 & help_if_i_serious_problem <= 2], 1000, 'Respondents', 'Rely_on_Friends_Under_3')
resdats <- subgraph.by.factor(dats,V(dats$graph)[PHQ9_questions_answered == 9 & ever_seriously_considered_attempted_suicide=="Yes"], 1000, 'Respondents', 'Suicidal_Thoughts')
dev.off()
