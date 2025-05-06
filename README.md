# MicroscopeServo

## 项目简介

本项目是微型伺服控制系统，实现显微镜的自动对焦和目标精确控制。系统能够通过摄像头捕捉图像，利用图像处理算法进行自动对焦，并驱动伺服电机调整显微镜平台，以适应不同倍率的镜头，是对以下学术论文中提出的框架的复现：

**Multi-Scale Visual Servoing Framework for Optical Microscopy based on SIFT Matching**

访问以下链接查看原论文：
[IEEE Xplore: Multi-Scale Visual Servoing Framework for Optical Microscopy based on SIFT Matching](https://ieeexplore.ieee.org/abstract/document/10287399/)

## 主要功能

*   **硬件初始化**: 初始化主机、MATLAB 引擎、视频捕捉设备和电机串口通信。
*   **外参优化**: 执行相机外参的优化校准。
*   **多镜头支持**: 支持多种放大倍率的镜头 (例如 10x, 20x, 40x)，并能自动切换。
*   **自动对焦**:
    *   针对不同镜头倍率，执行自动对焦算法，确定最佳焦距。
    *   `autofocus_simple` 方法用于实现基本的自动对焦逻辑。
*   **伺服控制**:
    *   读取目标图像，并将其转换为灰度图。
    *   结合自动对焦结果和目标图像，通过树莓派和 MATLAB 引擎控制伺服电机进行精确定位。
*   **镜头旋转**: 通过串口控制电机旋转切换不同倍率的镜头。

## 核心文件

*   `pi_init.py`: 用于硬件的初始化。
*   `sift/`: 包含 SIFT 特征点相关的图像处理算法。
*   `extrinsic/`: 包含外参标定相关的代码。
*   `intrinsic/`: 包含内参标定相关的代码。

## 运行流程

1.  **初始化**:
    *   启动 MATLAB 引擎，并切换到 `servo` 目录。
    *   初始化视频捕捉设备。
    *   打开与电机控制板的串口连接。
2.  **外参优化**:
    *   运行 `extrinsic_optimize()` 进行相机外参标定。
3.  **针对每个镜头进行操作**:
    *   选择一个镜头倍率。
    *   **自动对焦**: 使用 `autofocus_simple` 找到当前镜头的最佳对焦点 `target_z`。
    *   **伺服定位**:
        *   加载预定义的 `target{i}.png` 目标图像。
        *   调用 `servo()` 函数，结合树莓派、MATLAB 引擎、视频输入、自动对焦模块和目标图像，驱动伺服电机进行对准。
    *   **旋转镜头**: 如果不是最后一个镜头，则通过串口发送指令旋转镜头到下一个倍率，并等待旋转完成。
4.  **结束**: 所有镜头操作完成后，程序结束。

## 安装与配置 (示例)

*确保已安装 Python 环境及必要的库，如 OpenCV, pyserial, MATLAB Engine API for Python 等。*
*配置树莓派硬件，连接相机和伺服电机控制板。*
*确保 MATLAB 已安装并配置了 Engine API。*

```bash
# 示例依赖安装 (具体依赖请根据项目实际情况调整)
pip install opencv-python pyserial
# MATLAB Engine API for Python 通常需要从 MATLAB 安装目录中手动安装
# cd "matlabroot/extern/engines/python"
# python setup.py install
```

## 使用方法

直接运行主程序:
```bash
python main.py
```

**注意**:
*   确保所有硬件连接正确且已上电。
*   确保 `servo` 目录及相关的 MATLAB 脚本存在且路径正确。
*   目标图像 `target0.png`, `target1.png`, `target2.png` 需要预先准备好。
*   串口号 (`COM4`) 和波特率 (`9600`) 需要根据实际情况修改。
