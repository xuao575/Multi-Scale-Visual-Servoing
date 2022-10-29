function error_s = get_feature_error_gray(image_gray_new, image_gray_old)
%% 计算直接视觉伺服特征误差
error_s = image_gray_new(:) - image_gray_old(:);

end