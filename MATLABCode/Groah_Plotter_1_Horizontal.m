%Code to plot the error graph horizontally

%For the error graph
workbooktouse = scoringworkbookS4
means = workbooktouse{2,[2,3,4]}
errhigh = workbooktouse{3,[2,3,4]}
errlow= workbooktouse{3,[2,3,4]}
%categorical(workbooktouse{4,[2,3,4]})
X = categorical({'T\_Stir','T\_Cook\_1','T\_Cook\_2'});
X = reordercats(X,{'T\_Cook\_2', 'T\_Cook\_1','T\_Stir'});
barh(X,means)
%ylim([-5 3.5])

hold on

er = errorbar(means,X, errlow,errhigh, 'horizontal');   
title({'Mean Error In Automated Time Measurements'})
%xlabel('Measurement') 
xlabel('Mean Error (s)') 
ax = gca;
ax.FontSize = 48;
er.Color = [0 0 0];                            
er.LineStyle = 'none';  
er.CapSize = 40;
er.LineWidth = 3;
ax.YGrid = 'on';

xtickangle(0);
