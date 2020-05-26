%Code to plot the graph of the distribution of timings present in the data

%For the time distrbution graph
workbooktouse = scoringworkbookS1
means = workbooktouse{2,[2,3,4]}
errhigh = workbooktouse{3,[2,3,4]}
errlow= workbooktouse{3,[2,3,4]}
%categorical(scoringworkbookS2{4,[2,3,4]})
X = categorical({'T\_Stir','T\_Cook\_1','T\_Cook\_2'});
X = reordercats(X,{'T\_Stir','T\_Cook\_1','T\_Cook\_2'});
bar(X,means)
ylim([0 160])
hold on

er = errorbar(X,means,errlow,errhigh);   
title({'Mean Automated';'Time Measurement'})
%xlabel('Measurement') 
ylabel('Mean Time (s)') 
ax = gca;
ax.FontSize = 22;
er.Color = [0 0 0];                            
er.LineStyle = 'none';  
er.CapSize = 60;
er.LineWidth = 3;
ax.YGrid = 'on';
xtickangle(0);