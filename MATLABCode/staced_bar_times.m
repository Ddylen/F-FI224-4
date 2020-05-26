%Code to generate a stacked bar plot like figure of the key recipe times

stackedbardata =    [21.3,	23.3,	12.8,	22.7,	25.4;
                    9.7,	44.4,	20,     19.8,	39.3;
                    9,      32.9,	10.1,	19.1,	16.9;
                    169.9,	104.9,	97.4,	129.8,	129.2;
                    1.9,	3.6,	1.5,	1.5,	1.2;
                    164,	51.5,	128,	66.8,	87.9;];
                
                

stackedbardata= fliplr(stackedbardata)
% Chef_A = stackedbardata(:,1)
% Chef_B = stackedbardata(:,1)
% Chef_C = stackedbardata(:,1)
% Chef_D = stackedbardata(:,1)
% Chef_E = stackedbardata(:,1)
% 
% all = [Chef_A, Chef_B, Chef_C, Chef_D, Chef_E]
% key = {'T_Stir Start', 'T_Stir End', 'Cook_1 Start', 'Cook_1 End', 'Cook_2 Start', 'Cook_2 End'}
% key2 = {'Chef A', 'Chef B', 'Chef C', 'Chef D', 'Chef E'}

H = barh(stackedbardata.', 'stacked')
%H.CData(1,:) = [0.5 0.5 0.5];
H(1).FaceColor = [0.5 0.5 0.5];
H(3).FaceColor = [0.5 0.5 0.5];
H(5).FaceColor = [0.5 0.5 0.5];
%H(:,[5 4 3 2 1])
xlabel('Time (S)') 
ylabel('Demonstrator')

%yticklabels('Chef A'; 'Chef B'; 'Chef C'; 'Chef D'; 'Chef E')
chefs = categorical({'Chef E', 'Chef D', 'Chef C', 'Chef B', 'Chef A'})
%chefs = reordercats(chefs, {'Chef E', 'Chef D', 'Chef C', 'Chef B', 'Chef A'})
set(gca,'yticklabel',chefs)
%legend('T\_Stir Start', 'T\_Stir End', 'Cook\_1 Start', 'Cook\_1 End', 'Cook\_2 Start', 'Cook\_2 End')
%legend('', 'T\_Stir', '', 'Cook\_1', '', 'Cook\_2')
lgd = legend(H([2,4,6]), 'T\_Stir', 'Cook\_1', 'Cook\_2')
title('Comparison of Demonstrations')


% figure(1)
% 
% X = categorical({'T\_Stir';'T\_Cook\_1';'T\_Cook\_2'});
% bar(X, plotresults)
% ylim([0 1])
% title('Correlation of Key Parameters with Quality Scores')
% %xlabel('Key Parameter') 
% ylabel('Distance Correlation') 
% 
% legendlabels= {'Appearance','Taste','Texture', 'Overall'}
% lgd = legend(legendlabels)
% lgd.NumColumns = 4
% lgd.Location = 'southoutside'
ax = gca;
ax.FontSize = 48;
lgd.NumColumns = 1;
lgd.Location = 'east';
% 
% figure(2)

% 
% X = categorical({'Appearance';'Taste';'Texture'});
% X = reordercats(X,{'Appearance';'Taste';'Texture'});
% bar(X, plotresults)
% ylim([0 1])
% title({'Correlation of Key Parameters';'with Quality Scores'})
% %xlabel('Key Parameter') 
% ylabel('Distance Correlation') 
% 
% legendlabels= {'T\_Stir','T\_Cook\_1','T\_Cook\_2'}
% lgd = legend(legendlabels)
% lgd.NumColumns = 3
% lgd.Location = 'southoutside'
% ax = gca;
% ax.FontSize = 40;
% xtickangle(0)
% ax.YGrid = 'on'
% set(ax,'YTick',0:0.1:1);
