function [error_s, L_e] = get_FeaturesError_InteractionMatrix_DVS(...
                        image_gray_new, image_gray_old, ...
                        Para_Camera_Intrinsic, image_depth_new)
%% 计算特征误差和交互矩阵 直接伺服伺服(DVS)
% 计算特征误差
error_s = get_feature_error_gray(image_gray_new, image_gray_old);

% 计算交互矩阵
L_e = get_interaction_matrix_gray(image_gray_new,  Para_Camera_Intrinsic, image_depth_new);
% L_I_old = get_interaction_matrix_gray(image_gray_old, planar_parameter_old,  Para_Camera_Intrinsic, image_depth_old);
% L_e = 0.5*(L_I_new + L_I_old);

%% 计算交互矩阵





