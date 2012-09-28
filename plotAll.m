function plotAll()
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here
    [synthesis_rate, output_rate, McCin] = plot3d('1.out');
    [~,~,McCout] = plot3d('2.out');
    [~,~,death_prob] = plot3d('3.out');
    
    draw_matrix(McCin, gray, 'McCin', 'synthesis\_rate', 'output\_rate');
    draw_matrix(McCout, bone, 'McCout', 'synthesis\_rate', 'output\_rate');
    draw_matrix(death_prob, autumn, 'death\_prob', 'synthesis\_rate', 'output\_rate');
    
    draw_matrix(McCout ./ McCin, autumn, 'McCout/McCin', 'synthesis\_rate', 'output\_rate');
end
