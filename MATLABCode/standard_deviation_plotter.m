

Code to plot the standard deviations of the time distribution bar plot data 

data = [0.00105122 0.00165445 0.00182586 0.00147042].*100
%categorical(scoringworkbookS2{4,[2,3,4]})
X = categorical({'X','Y','Z', 'Overall'});
X = reordercats(X,{'X','Y','Z', 'Overall'});
bar(X,data)
hold on

%er = errorbar(means,X, errlow,errhigh, 'horizontal');   
title({'Standard Deviation In Recorded Stationary Positions'})

ylabel('Standard Deviation (cm)') 
xlabel('Axis') 
ax = gca;
ax.FontSize = 40;
er.Color = [0 0 0];                            
er.LineStyle = 'none';  
er.CapSize = 40;
er.LineWidth = 3;
ax.YGrid = 'on';
xtickangle(0);