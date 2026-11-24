# 速查表

## 复变函数

| 场景 | 内容 |
|---|---|
| 可导判据 | $u_x=v_y$，$u_y=-v_x$ |
| 极坐标形式 | $u_r=\\frac1r v_\\theta$，$v_r=-\\frac1r u_\\theta$ |
| 柯西积分公式 | $f(z_0)=\\frac{1}{2\\pi i}\\oint_C\\frac{f(z)}{z-z_0}dz$ |
| 高阶导数 | $f^{(n)}(z_0)=\\frac{n!}{2\\pi i}\\oint_C\\frac{f(z)}{(z-z_0)^{n+1}}dz$ |
| 一阶极点留数 | $\\operatorname{Res}f(z_0)=\\lim_{z\\to z_0}(z-z_0)f(z)$ |
| $m$ 阶极点留数 | $\\frac{1}{(m-1)!}\\lim_{z\\to z_0}\\frac{d^{m-1}}{dz^{m-1}}[(z-z_0)^mf(z)]$ |
| 留数定理 | $\\oint_C f\\,dz=2\\pi i\\sum\\operatorname{Res}$ |
| 有理函数实积分 | 补上半平面大圆弧，取上半平面留数 |
| 三角有理式 | $z=e^{i\\theta}$，$d\\theta=\\frac{dz}{iz}$，单位圆围道 |

## 积分变换

| 原函数 | 傅里叶变换 |
|---|---|
| $\\delta(x)$ | $1$ |
| $1$ | $2\\pi\\delta(k)$ |
| $e^{-a\\lvert x\\rvert}$ | $\\frac{2a}{a^2+k^2}$ |
| 矩形脉冲高 $1$ 宽 $2a$ | $\\frac{2\\sin ka}{k}$ |
| $e^{-x^2/(2\\sigma^2)}$ | $\\sigma\\sqrt{2\\pi}e^{-\\sigma^2k^2/2}$ |

| 性质 | 内容 |
|---|---|
| 位移 | $f(x-x_0)\\leftrightarrow e^{-ikx_0}F(k)$ |
| 缩放 | $f(ax)\\leftrightarrow\\frac{1}{\\lvert a\\rvert}F(k/a)$ |
| 求导 | $f'\\leftrightarrow ikF$，$f''\\leftrightarrow-k^2F$ |
| 卷积 | $f*g\\leftrightarrow FG$ |

| 拉普拉斯 | 内容 |
|---|---|
| $\\mathcal L[t^n]$ | $\\frac{n!}{s^{n+1}}$，$\\operatorname{Re}s>0$ |
| $\\mathcal L[e^{at}]$ | $\\frac{1}{s-a}$，$\\operatorname{Re}s>a$ |
| $\\mathcal L[f']$ | $sF(s)-f(0)$ |
| $\\mathcal L[f'']$ | $s^2F(s)-sf(0)-f'(0)$ |

## 方程与定解

| 方程 | 形式 | 初始条件个数 |
|---|---|---|
| 波动 | $u_{tt}=a^2\\Delta u$ | 2 |
| 热传导 | $u_t=a^2\\Delta u$ | 1 |
| 拉普拉斯/泊松 | $\\Delta u=0$ 或 $\\Delta u=-f$ | 0 |

| 边界 | 形式 | 物理 |
|---|---|---|
| Dirichlet | $u=g$ | 固定端、恒温 |
| Neumann | $\\partial_nu=g$ | 自由端、绝热 |
| Robin | $\\alpha u+\\beta\\partial_nu=g$ | 对流换热 |

## 解法

| 场景 | 公式 |
|---|---|
| 达朗贝尔 | $u=\\frac12[\\varphi(x-at)+\\varphi(x+at)]+\\frac{1}{2a}\\int_{x-at}^{x+at}\\psi(s)ds$ |
| 齐次 Dirichlet 本征函数 | $\\sin\\frac{n\\pi x}{l}$，$\\lambda_n=(\\frac{n\\pi}{l})^2$ |
| 齐次 Neumann 本征函数 | $\\cos\\frac{n\\pi x}{l}$，$n=0,1,2\\dots$ |
| 三维泊松基本解 | $\\frac{1}{4\\pi r}$ |
| 波动推迟格林函数 | $\\frac{\\delta(t-t'-r/a)}{4\\pi r}$ |

## 特殊函数

| 函数 | 关键性质 |
|---|---|
| $P_l$ | $\\int_{-1}^1P_lP_m=\\frac{2}{2l+1}\\delta_{lm}$，$P_l(1)=1$ |
| $P_0,P_1,P_2$ | $1$，$x$，$\\frac{3x^2-1}{2}$ |
| 勒让德递推 | $(l+1)P_{l+1}=(2l+1)xP_l-lP_{l-1}$ |
| $J_\\nu$ | $J_0(0)=1$，$Y_\\nu(0)=-\\infty$ |
| 贝塞尔递推 | $J_{\\nu-1}+J_{\\nu+1}=\\frac{2\\nu}{x}J_\\nu$ |
| 贝塞尔正交 | $\\int_0^aJ_\\nu(\\mu_mr)J_\\nu(\\mu_nr)r\\,dr=0$ |
| $j_0$，$n_0$ | $\\frac{\\sin x}{x}$，$-\\frac{\\cos x}{x}$ |

## 变分法

| 场景 | 内容 |
|---|---|
| 欧拉–拉格朗日 | $\\frac{d}{dx}F_{y'}-F_y=0$ |
| 不显含 $x$ | $F-y'F_{y'}=C$ |
| 不显含 $y$ | $F_{y'}=C$ |
| 哈密顿原理 | $\\delta\\int L\\,dt=0$ |
| 瑞利商 | $\\lambda=\\frac{\\int\\lvert\\nabla u\\rvert^2}{\\int u^2}$，上界 |
