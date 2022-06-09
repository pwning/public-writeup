# Navigation Rebooting

In this problem, we were tasked with determining the position and veolcity of a satellite given psuedorange and velocity data relative to other satellites with known orbits at a fixed point in time.  Initially, misunderstanding the difference between a _range_ and a _pseudorange_, I formulated a solution that solved for the least-squares error on the position and velocity while treating the provided measurements as truth.  The least-squares solution for position arose from the following derivation:

$$
\begin{align*}
\vec{p} &= \text{position of the satellite we want to solve for} \\
\vec{q}&= \text{known position of another satellite} \\
\vec{r}&= \text{known position of a second satellite} \\
\\
\left\Vert \vec{p} - \vec{s} \right\Vert^2 &= \left\Vert \vec{p} \right\Vert^2 - 2 \left( \vec{p} \cdot \vec{s} \right) + \left\Vert \vec{s} \right\Vert^2 & \text{for any satellite $s$} \\
\Rightarrow \: \: \left\Vert \vec{p} - \vec{q} \right\Vert^2 - \left\Vert \vec{p} - \vec{r} \right\Vert^2 &= \left( \left\Vert \vec{p} \right\Vert^2 - 2 \left( \vec{p} \cdot \vec{q} \right) + \left\Vert \vec{q} \right\Vert^2 \right) - \left( \left\Vert \vec{p} \right\Vert^2 - 2 \left( \vec{p} \cdot \vec{r} \right) + \left\Vert \vec{r} \right\Vert^2 \right) \\
\Rightarrow \: \: \left\Vert \vec{p} - \vec{q} \right\Vert^2 - \left\Vert \vec{p} - \vec{r} \right\Vert^2 - \left\Vert \vec{q} \right\Vert^2 + \left\Vert \vec{r} \right\Vert^2 &= 2 \left( \vec{p} \cdot \vec{r} - \vec{p} \cdot \vec{q} \right) \\
\Rightarrow \: \: \left\Vert \vec{p} - \vec{q} \right\Vert^2 - \left\Vert \vec{p} - \vec{r} \right\Vert^2 - \left\Vert \vec{q} \right\Vert^2 + \left\Vert \vec{r} \right\Vert^2 &= 2 p_x (r_x - q_x) + 2 p_y (r_y - q_y) + 2 p_z (r_z - q_z) \\
\end{align*}
$$

Since all of these values are known except for $p_x$, $p_y$, and $p_z$, we can approximate the solution by the least squares solution to

$$
\begin{align*}
A \begin{bmatrix} p_x \\ p_y \\ p_z \end{bmatrix} &= b \\
\\
\text{where} \\
\\
A &= \begin{bmatrix}
2 (r_{1,x} - q_x) & 2 (r_{1,y} - q_y) & 2 (r_{1,z} - q_z) \\
2 (r_{2,x} - q_x) & 2 (r_{2,y} - q_y) & 2 (r_{2,z} - q_z) \\
\vdots & \vdots & \vdots \\
\end{bmatrix} \\
b &= \begin{bmatrix}
\left\Vert \vec{p} - \vec{q} \right\Vert^2 - \left\Vert \vec{p} - \vec{r_1} \right\Vert^2 - \left\Vert \vec{q} \right\Vert^2 + \left\Vert \vec{r_1} \right\Vert^2 \\
\left\Vert \vec{p} - \vec{q} \right\Vert^2 - \left\Vert \vec{p} - \vec{r_2} \right\Vert^2 - \left\Vert \vec{q} \right\Vert^2 + \left\Vert \vec{r_2} \right\Vert^2 \\
\vdots
\end{bmatrix}
\end{align*}
$$

by picking one of the satellites with known orbit to act as $q$ and using the other satellites as the various values of $r_i$.

For velocity, we used the following derivation:

$$
\begin{align*}
v_{pq} &= \text{rate of change of distance from $p$ to $q$ (known)} \\
\vec{v_p} &= \text{velocity of $p$ (unknown)} \\
\vec{v_q} &= \text{velocity of $q$ (known)} \\
\hat{pq} &= \text{unit vector from $p$ to $q$ (known)} \\
\\
v_{pq} &= \left( \vec{v_q} - \vec{v_p} \right) \cdot \hat{pq} \\
\Rightarrow \: \: v_{pq} &= \vec{v_q} \cdot \hat{pq} - \vec{v_p} \cdot \hat{pq} \\
\Rightarrow \: \: \vec{v_p} \cdot \hat{pq} &= \vec{v_q} \cdot \hat{pq} - v_{pq}
\end{align*}
$$

Since the only unknown is $\vec{v_p}$, we can solve for it by finding the least-squares solution to

$$
\begin{align*}
A \begin{bmatrix} {v_p}_x \\ {v_p}_y \\ {v_p}_z \end{bmatrix} &= b \\
\\
\text{where} \\
\\
A &= \begin{bmatrix}
\hat{pq_1}_x & \hat{pq_1}_y & \hat{pq_1}_z \\
\hat{pq_2}_x & \hat{pq_2}_y & \hat{pq_2}_z \\
\vdots & \vdots & \vdots \\
\end{bmatrix} \\
b &= \begin{bmatrix}
\vec{v_{q_1}} \cdot \hat{pq_1} - v_{pq_1} \\
\vec{v_{q_2}} \cdot \hat{pq_2} - v_{pq_2} \\
\vdots
\end{bmatrix}
\end{align*}
$$

using the known satellites for the various values of $q_i$.

Running this solution got us _close_, but not close enough.  The reason for this is that we were given _pseudoranges_ rather than ranges, the difference being that ranges are treated as absolute distance measurements while pseudoranges may have errors caused by receiver clock bias and path delays.

To solve using the pseudoranges, I implemented the algorithm described [in this helpful summary of the topic](http://www.grapenthin.org/notes/2019_03_11_pseudorange_position_estimation/); see the implementation in `solve_pseudo.py`.  Once you work through all of the math, it boils down to iterating on this linear system until you sufficiently converge on a solution:

$$
\begin{align*}
\vec{p} &= \text{our current solution for the position of the satellite} \\
t &= \text{our current solution for the clock bias} \\
\vec{s_i} &= \text{known position of satellite $i$ at time of observation} \\
\rho_i &= \text{observed distance to satellite $i$} \\
c &= \text{the speed of light} \\
\ell &= \text{gradient rate (we used 0.01)}
\\
\\
\text{Solve} \; \; A \begin{bmatrix}\Delta p_x \\ \Delta p_y \\ \Delta p_z \\ \Delta t\end{bmatrix} &= b \\
\text{where} \; \; A &= \begin{bmatrix}
	\frac{{s_1}_x}{\left\Vert \vec{p} - \vec{s_1} \right\Vert} &
	\frac{{s_1}_y}{\left\Vert \vec{p} - \vec{s_1} \right\Vert} &
	\frac{{s_1}_z}{\left\Vert \vec{p} - \vec{s_1} \right\Vert} &
	c \\
	\vdots & \vdots & \vdots & \vdots
\end{bmatrix} \\
b &= \begin{bmatrix}
	\rho_1 - \left\Vert \vec{p} - \vec{s_1} \right\Vert - c t \\
	\vdots
\end{bmatrix} \\
\\
\\
\text{and then update} \; \; \vec{p'} &= \vec{p} + \ell \begin{bmatrix}\Delta p_x \\ \Delta p_y \\ \Delta p_z\end{bmatrix} \\
t' &= t + \ell \Delta t
\end{align*}
$$

Note that this solves only for position and not for velocity.

We tried submitting this solution with the best velocity value found from our old solver, but this wasn't close enough.  However, we noticed that the solution that our pseudorange solver converged upon was consistent with almost exactly 50 microseconds of clock bias, or 15km of distance error.  By hardcoding this 15km into the original solver, we were able to produce a solution that was close enough to get a flag; see `solve.py`, and note the hardcoded value on line 85.
