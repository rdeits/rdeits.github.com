---
layout: post
title: "Denavit Hartenberg Analysis, Part 6: Examples"
category: 
tags: []
---
{% include JB/setup %}

[Part 1](/2012/06/05/denavit-hartenberg-robotic-control/)/[Part 2](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/)/[Part 3](/2012/06/10/denavit-hartenberg-for-robotics-part-3-the-d-h-parameters/)/[Part 4](/2012/06/19/denavit-hartenberg-parameters-part-4-existence-and-uniqueness/)/[Part 5](/2012/06/25/denavit-hartenberg-analysis-part-5-assigning-coordinate-frames/)/[Part 6](/2012/06/27/denavit-hartenberg-analysis-part-6-examples/)

# Example 1: Planar Elbow Manipulator

<object data="/img/2012-06-27/planar_elbow_manipulator.svg" type="image/svg+xml">
</object>

Let's first look at a simple arm with two links and two joints. Following the procedure from [last time](/2012/06/25/denavit-hartenberg-analysis-part-5-assigning-coordinate-frames#solving_the_entire_arm), we first identify the joint axes and assign `\(z_0 \dots z_n\)` to them:

<object data="/img/2012-06-27/planar_elbow_manipulator_z.svg" type="image/svg+xml">
</object>
The single dot for the axes indicates that they come directly out of the page.

Next, we establish the base frame with a convenient orientation and position along `\(z_0\)`:

<object data="/img/2012-06-27/planar_elbow_manipulator_base.svg" type="image/svg+xml">
</object>

We can see that `\(z_0\)` and `\(z_1\)` are parallel (both coming out of the page), so we use the parallel axes method from [Part 5](/2012/06/25/denavit-hartenberg-analysis-part-5-assigning-coordinate-frames#case_2__and__are_parallel) and choose `\(x_1\)` to be the vector perpendicular to `\(z_0\)` and `\(z_1\)` which passes through `\(O_0\)`. This also defines `\(y_1\)`:

<object data="/img/2012-06-27/planar_elbow_manipulator_frame1.svg" type="image/svg+xml">
</object>

Our last set of axes is the tool frame. We'll skip our normal rule of aligning z to the direction of approach in order to keep all of our x and y axes in the same plane (alternately, we'll pretend that our direction of approach is out of the page).

<object data="/img/2012-06-27/planar_elbow_manipulator_frame_n.svg" type="image/svg+xml">
</object>

We now have all the axes we need in order to calculate our transformation matrix. Let's create a table of our link parameters:
`\[
\begin{array}
\text{Joint} & a_i & d_i & \beta_i & \theta_i \\
1 & a_1 & 0 & 0 & \theta_1 \\
2 & a_2 & 0 & 0 & \theta_2
\end{array}
\]`

And now each of our transformation matrices:

`\[
A_i = \begin{bmatrix}
\cos{\theta_i} & -\sin{\theta_i} \cos{\beta_i} & \sin{\theta_i} \sin{\beta_i} & a_i \cos{\theta_i} \\
\sin{\theta_i} & \cos{\theta_i} \cos{\beta_i} & -\cos{\theta_i} \sin{\beta_i} & a_i \sin{\theta_i} \\
0 & \sin{\beta_i} & \cos{\beta_i} & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}
\]`

`\[
A_1 = \begin{bmatrix}
\cos{\theta_1} & -\sin{\theta_1} & 0 & a_1 \cos{\theta_i} \\
\sin{\theta_1} & \cos{\theta_1} & 0 & a_i \sin{\theta_i} \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\]`
`\[
A_2 = \begin{bmatrix}
\cos{\theta_2} & -\sin{\theta_2} & 0 & a_2 \cos{\theta_i} \\
\sin{\theta_2} & \cos{\theta_2} & 0 & a_i \sin{\theta_i} \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\]`

Multiplying these together, we get
`\[
T_2^0 = A_1 A_2 = \begin{bmatrix}
\cos{(\theta_1 + \theta_2)} & -\sin{(\theta_1 + \theta_2)} & 0 & a_1 \cos{\theta_1} + a_2 \cos{(\theta_1 + \theta_2)} \\
\sin{(\theta_1 + \theta_2)} & \cos{(\theta_1 + \theta_2)} & 0 & a_1 \sin \theta_1 + a_2 \sin{(\theta_1 + \theta_2)} \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\]`
Note that in order to get this result, we've skipped a few intermediate steps of the multiplication and used the trigonometric addition formulae:
`\[
\begin{align}
\cos a \cos b - \sin a \sin b &= \cos{(a + b)} \\
\sin a \cos b + \sin b \cos a &= \sin{(a + b)}
\end{align}
\]`
Now we can ask a question like "What are the coordinates in the base frame of the tip of the arm?" To answer this, we need to first write down the location of the tip of the arm in the tool frame:
`\[
O_2^2 = \begin{bmatrix}
0 \\ 0 \\ 0 \\ 1
\end{bmatrix}
\]`
Then we multiply by `\(T_2^0\)` to find the coordinates in the base frame:
`\[
O_2^0 = T_2^0 O_2^2 = \begin{bmatrix}
a_1 \cos{\theta_1} + a_2 \cos{(\theta_1 + \theta_2)} \\
a_1 \sin \theta_1 + a_2 \sin{(\theta_1 + \theta_2)} \\
0 \\
1 
\end{bmatrix}
\]`
We can then use this to solve for `\(\theta_1\)` and `\(\theta_2\)` if we want to move the end of the arm to a particular position in space.