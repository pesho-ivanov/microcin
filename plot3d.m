function plot3d(results_file)
%PLOT3D plots a PRISM results file

    res = importdata(results_file, '\t');
    
    X = res.data(:, 1);
    Y = res.data(:, 2);
    Z = res.data(:, 3);
    
    cols = sqrt(size(X, 1));
    assert (cols*cols == size(X, 1), 'Matrix not square')
        
    X = vec2mat(X, cols);
    Y = vec2mat(Y, cols);
    Z = vec2mat(Z, cols);

    surf(X, Y, Z);
end
