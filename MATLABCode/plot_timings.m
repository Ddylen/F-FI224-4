%  Code by Simon Hauser to plot example graphs of time, not used further
%% Tabula rasa
close all

%% Timing parameters
timings = 1/10*[169 1773 2524;
    178 1854 2456;
    124 1488 2264;
    135 1750 2354;
    210 2065 2744];

%% Plot
% set(gcf,'color','w');
% bar(timings')
% title('Cooking timings of human chefs')
% xlabel('stages')
% xticklabels({'stirring','first side','second side'})
% ylabel('time [s]')
% % legend('human chef 1','human chef 1','human chef 1','human chef 1','human chef 1','Location','NorthWest')
% grid on
% set(gca,'FontSize', 16);

%% Plot horizontally

set(gcf,'color','w');
barh(flipud(timings'))
title('Cooking timings of human chefs')
xlabel('time [s]')
ylabel('stages')
yticklabels({'second side','first side','stirring'})
% legend('human chef 1','human chef 1','human chef 1','human chef 1','human chef 1','Location','NorthWest')
grid on
set(gca,'FontSize', 16);