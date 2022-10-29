function L_I = get_interaction_matrix_gray(image_gray, Para_Camera_Intrinsic, image_depth)
%% 计算灰度误差的交互矩阵（直接视觉伺服DVS）
[row, col] = size(image_gray);
[I_x, I_y] = get_image_gradient(image_gray, Para_Camera_Intrinsic);
L_I = zeros(row*col, 6);
%% L_e
cnt = 1;
for i = 1 : col
    for j = 1 : row
        point = [i; j; 1];
        corn_right_norm = Para_Camera_Intrinsic \ point;
        x = corn_right_norm(1);
        y = corn_right_norm(2);
%         Z_inv = planar_parameter' * corn_right_norm;
        Z_inv = 1 / image_depth(j,i);
        L_I(cnt, :) = [I_x(j,i)*Z_inv, ...
                       I_y(j,i)*Z_inv, ...
                       -(x*I_x(j,i) + y*I_y(j,i))*Z_inv, ...
                       -x*y*I_x(j,i) - (1+y^2)*I_y(j,i), ...
                       (1+x^2)*I_x(j,i) + x*y*I_y(j,i), ...
                       -y*I_x(j,i) + x*I_y(j,i)];
        cnt = cnt + 1;
    end
end
end
    