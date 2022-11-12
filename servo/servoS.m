function Sc = servoS(pose, Para_Camera_Intrinsic, image_gray_new, image_depth_new, image_gray_old)

% T_b_v = [1, 0, 0, 0.03; 0, 1, 0, 0.05; 0, 0, 1, 0.03; 0, 0, 0, 1];
% T_t_c = [sqrt(3)/2, 1/2, 0, 0.178 * 0.001; 1/2, -sqrt(3)/2, 0, 145.678 * 0.001; 0, 0, -1, 8.450 * 0.001; 0, 0, 0, 1];
T_t_c = [0, -1, 0, (126-1) * 0.001; -1, 0, 0, (0) * 0.001; 0, 0, -1, -58 * 0.001; 0, 0, 0, 1];

T_w_t = get_Object_Transform(pose);

% coder.extrinsic('quat2axang');
% ppose = [pose(7); pose(4:6)]';
% A = quat2axang(ppose);
% qpose = zeros(6,1);0
% qpose = [pose(1:3)', A(4) * [A(1:3)]]';
% 
% T_w_nb = [MatrixExp3(VecToso3(qpose(4:6))), qpose(1:3); 0 0 0 1];

% 读取当前灰度图和深度图

% [~, ~, image_gray_new] = get_vrep_Camera_g u0)(k1 r2 + k2 r4)
% vd = v + (v − v0)(k1 r2 + k2 r4)ray(vrep, clientID, VisionHandle_Vision_new);
image_gray_new_norm = get_image_gray_norm(image_gray_new);
% [~, ~, image_depth_new] = get_vrep_Camera_depth(vrep, clientID, VisionHandle_Vision_new);

image_gray_old_norm = get_image_gray_norm(image_gray_old);
%% 计算特征误差和交互矩阵
[error_s, L_e] = get_FeaturesError_InteractionMatrix_DVS(...
                    image_gray_new_norm, image_gray_old_norm, ...
                    Para_Camera_Intrinsic, image_depth_new);
% 计算摄像头速度
% disp(abs(mean(error_s)));
% disp(mean(abs(error_s)));

if mean(abs(error_s)) < 0.07
    para = [-1,0,0;
    0,-1,0;
    0,0,-0.5;
    ];
    disp(1)
else
    para = [-10,0,0;
    0,-10,0;
    0,0,-5;
    ];
    disp(2)
end

Vc = para * (pinv(L_e) * error_s);
% vd = v + (v − v0)(k1 r2 + k2 r4)
% disp(mean(error_s));

%% 相机运动
% 计算下一时刻摄像头速度旋量及位

% camera
Bc = [Vc(1:2);0;0;0;Vc(3)];
% Bc = [0; 0; 0; 0; 0; 0.05];
% Bc = [0.0000; 0.0000; 0; 0; 0; 0.005];

% Bc = [0;0;0;0;0;0.002];


T_c_next = [MatrixExp3(VecToso3(Bc(4:6))), Bc(1:3); 0 0 0 1];
% 下一时刻摄像头位姿

T_w_c = T_w_t * T_t_c;

T_w_next = T_w_c * T_c_next;

T_w_next_tip = T_w_next * TransInv(T_t_c);

Translation = T_w_next_tip(1:3,4) * 1000;

Rotation = rotm2eul(T_w_next_tip(1:3,1:3), 'XYZ') / pi * 180.0;

Sc = [Translation; Rotation'];

% Sc = [0.0000; 0.0000; 0; 0; 0; 0.005];

% 
% T_w_nb_next = T_w_nb * T_next;
% T_w_next_tip = T_w_nb_next * TransInv(T_b_v);
% T_w_tip = T_w_nb * TransInv(T_b_v);
% 
% 
% t = T_w_next_tip(1:3, 4) - T_w_tip(1:3, 4);
% % VecToso3(w * theta)*(T_w_nb_next(1:3, 4) - T_w_nb(1:3, 4));
% 
% Sc = [t; T_w_nb(1:3,1:3) * Bc(4:6)];

end