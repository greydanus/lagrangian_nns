[Lagrangian Neural Networks](https://arxiv.org/abs/2003.04630) 
=======
Miles Cranmer, Sam Greydanus, Stephan Hoyer, Peter Battaglia, David Spergel, Shirley Ho
Accepted to ICLR 2020 Workshop on Deep Differential Equations

![overall-idea.png](static/overall-idea.png)

* [Paper](https://arxiv.org/abs/2003.04630)
* [Blog](https://greydanus.github.io/2020/03/10/lagrangian-nns/)
* [Self-Contained Tutorial](https://colab.research.google.com/drive/1CSy-xfrnTX28p1difoTA8ulYw0zytJkq)
* [Paper example notebook: double pendulum](https://github.com/MilesCranmer/lagrangian_nns/blob/master/notebooks/DoublePendulum.ipynb)
* [Paper example notebook: special relativity](https://github.com/MilesCranmer/lagrangian_nns/blob/master/notebooks/SpecialRelativity.ipynb)
* [Paper example notebook: wave equation](https://github.com/MilesCranmer/lagrangian_nns/blob/master/notebooks/WaveEquation.ipynb)

Summary
--------

In this project we propose Lagrangian Neural Networks (LNNs), which can parameterize arbitrary Lagrangians using neural networks. In contrast to Hamiltonian Neural Networks, these models do not require canonical coordinates and perform well in situations where generalized momentum is difficult to compute (e.g., the double pendulum). This is particularly appealing for use with a learned latent representation, a case where HNNs struggle. Unlike [previous work on learning Lagrangians](https://arxiv.org/pdf/1907.04490.pdf), LNNs are fully general and extend to non-holonomic systems such as the 1D wave equation.

|	| Neural Networks  | [Neural ODEs](https://arxiv.org/abs/1806.07366) | [HNN](https://arxiv.org/abs/1906.01563)  | [DLN (ICLR'19)](https://arxiv.org/abs/1907.04490) | LNN (this work) |
| ------------- |:------------:| :------------:| :------------:| :------------:| :------------:|
| Learns dynamics | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Learns continuous-time dynamics | | ✔️ | ✔️ | ✔️ | ✔️ |
| Learns exact conservation laws | | | ✔️ | ✔️ | ✔️ |
| Learns from arbitrary coordinates| ✔️ | ✔️ || ✔️ | ✔️ |
| Learns arbitrary Lagrangians | | |  | | ✔️ |




Dependencies
--------
 * Jax
 * NumPy
 * MoviePy (visualization)
 * celluloid (visualization)
 
This project is written in Python 3.
