function [I_x, I_y] = get_image_gradient(image, Para_Camera_Intrinsic)
%% 计算图像梯度
[I_u, I_v] = gradient(image);
I_x = I_u .* Para_Camera_Intrinsic(1,1); 
I_y = I_v .* Para_Camera_Intrinsic(2,2);
end