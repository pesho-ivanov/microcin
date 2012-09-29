function draw_matrix(m, color, titl, xlab, ylab)
    figure;
    imagesc(m)
    colormap(color)
    title(titl)
    xlabel(xlab);
    ylabel(ylab);
    %axis([synthesis_rate(1), synthesis_rate(end), output_rate(1), output_rate(end)])
end
