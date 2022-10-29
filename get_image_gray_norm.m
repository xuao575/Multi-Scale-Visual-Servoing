function image_gray_norm = get_image_gray_norm(image_gray)
%% 经灰度图[0,255]转换到[0,1], 并且255->0, 0->1
image_gray_norm = -1/255.*double(image_gray) + 1;


end