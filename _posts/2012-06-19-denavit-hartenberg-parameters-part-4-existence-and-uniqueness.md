---
layout: post
title: "Denavit Hartenberg Analysis, Part 4: Existence and Uniqueness"
category: 
tags: []
---
{% include JB/setup %}

[Part 1](/2012/06/05/denavit-hartenberg-robotic-control/)/[Part 2](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/)/[Part 3](/2012/06/10/denavit-hartenberg-for-robotics-part-3-the-d-h-parameters/)/[Part 4](/2012/06/19/denavit-hartenberg-parameters-part-4-existence-and-uniqueness/)/[Part 5](/2012/06/25/denavit-hartenberg-analysis-part-5-assigning-coordinate-frames/)

In Parts [1](/2012/06/05/denavit-hartenberg-robotic-control/), [2](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/), and [3](/2012/06/10/denavit-hartenberg-for-robotics-part-3-the-d-h-parameters/) we developed some motivation for inverse kinematics, learned about transformation matrices, and wrote down a general transformation matrix with four parameters:

`\[
A_i = \begin{bmatrix}
\cos{\theta_i} & -\sin{\theta_i} \cos{\beta_i} & \sin{\theta_i} \sin{\beta_i} & a_i \cos{\theta_i} \\
\sin{\theta_i} & \cos{\theta_i} \cos{\beta_i} & -\cos{\theta_i} \sin{\beta_i} & a_i \sin{\theta_i} \\
0 & \sin{\beta_i} & \cos{\beta_i} & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}
\]`

`\[
\begin{align}
R(z, \theta_i)&: \quad \text{Rotation about z by an angle $\theta_i$ ("joint angle")} \\
T(z, d_i)&: \quad \text{Translation along z by a distance $d_i$ ("link offset")} \\
T(x, a_i)&: \quad \text{Translation along x by a distance $a_i$ ("link length")} \\
R(x, \beta_i)&: \quad \text{Rotation about x by an angle $\beta_i$ ("link twist")}
\end{align}
\]`

But we only had my word that this matrix is sufficient to describe all the transformations we need to fully describe any robot or manipulator. To prove this, we need to show two properties of this transformation, *existence* and *uniqueness*. Existence means that for any transformation we would want to write down, there is *at least* one way to write it out in the matrix form given above. Uniqueness means that there is *only* one way to write down each transformation with the combination of the four joint parameters. If we can show those two properties, then we know that this representation of transformations is good enough to handle any kind of joint we could imagine. 

To prove this, we're going to first take a step back. Let's say that we have two frames, 0 and 1, so there exists a homogeneous transformation matrix (like the kind we developed in [Part 2](2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/)) that transforms coordinates from Frame 1 into Frame 0.

Now, let's suppose that these two frames have the following two properties. These are important enough that we're going to name them:
`\[
\begin{align}
&\text{DH1: The axis $x_1$ is perpendicular to $z_0$}\\
&\text{DH2: The axis $x_1$ intersects $z_0$}
\end{align}
\]`

You can see what this might look like here:

<img src="/img/2012-06-19/d-h_axes2.png">

You can see that this satisfies our two requirements about `\(z_0\)` and `\(x_1\)`. We claim that given these two conditions, there exist *unique* numbers `\(a, d, \theta, \beta\)` such that
`\[
A = R(z, \theta_i)\, T(z, d_i)\, T(x, a_i)\, R(x, \beta_i)
\]`

To prove this, let's first write out `\(A\)` in its general form, which we derived in [Part 2](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/):
`\[
A = \begin{bmatrix}
R_1^0 & O_1^0 \\
0 & 1
\end{bmatrix}
\]`

## Rotation
First, let's just look at rotation. When we first looked at rotation matrices in [Part 1](/2012/06/05/denavit-hartenberg-robotic-control/), we wrote down the rotation matrix as a set of dot products:
`\[
\begin{bmatrix}
v_1' \\
v_2'
\end{bmatrix} =
\begin{bmatrix}
i_1' \cdot i_1 & i_1' \cdot i_2 \\
i_2' \cdot i_1 & i_2' \cdot i_2
\end{bmatrix}
\begin{bmatrix}
v_1 \\
v_2
\end{bmatrix}
\]`
Expanding this to three dimensions and rewriting it with the notation we're using now, we get this matrix:
`\[
R_1^0 \equiv \begin{bmatrix}
r_{1 1} & r_{1 2} & r_{1 3} \\
r_{2 1} & r_{2 2} & r_{2 3} \\
r_{3 1} & r_{3 2} & r_{3 3}
\end{bmatrix} = \begin{bmatrix}
x_1 \cdot x_0 & y_1 \cdot x_0 & z_1 \cdot x_0 \\
x_1 \cdot y_0 & y_1 \cdot y_0 & z_1 \cdot y_0 \\
x_1 \cdot z_0 & y_1 \cdot z_0 & z_1 \cdot z_0
\end{bmatrix}
\]`
We need to show that we can express this using only the rotation angles given in our matrix `\(A\)`. That is, we need to show that we can write `\(R_1^0\)` as:
`\[
R_1^0 = R(z, \theta) \, R(x, \beta) = \begin{bmatrix}
\cos{\theta} & -\sin{\theta}\cos{\beta} & \sin{\theta}\sin{\beta} \\
\sin{\theta} & \cos{\theta}\cos{\beta} & -\cos{\theta}\sin{\beta} \\
0 & \sin{\beta} & \cos{\beta}
\end{bmatrix}
\]`

Now let `\(r_i\)` denote the `\(i^{\text{th}}\)` column of `\(R_1^0\)`, so, for example,
`\[
r_1 = \begin{bmatrix}
x_1 \cdot x_0 \\
x_1 \cdot y_0 \\
x_1 \cdot z_0
\end{bmatrix} \equiv \begin{bmatrix}
r_{1 1} \\
r_{2 1} \\
r_{3 1}
\end{bmatrix}
\]`
This is actually just the representation of the unit vector `\(x_1\)` with respect to Frame 0. We can write this out as `\(x_1^0\)`, which is shorthand for "`\(x_1\)` with respect to Frame 0". 
Now, our condition DH1 requires that `\(x_1\)` be perpendicular to `\(z_0\)`. That means that the dot product of those two vectors will be zero in a given frame. Let's look at that in Frame 0 for convenience:
`\[
\begin{align}
0 &= x_1^0 \cdot z_0^0 \\
&= r_1 \cdot z_0^0 \\
&= \begin{bmatrix}
r_{1 1} \\
r_{2 1} \\
r_{3 1}
\end{bmatrix} \cdot \begin{bmatrix}
0 \\
0 \\
1
\end{bmatrix} \\
\therefore 0 &= r_{3 1}
\end{align}
\]`
Thus, for any set of coordinate frames that satisfies DH1, the rotation matrix between them will always have its bottom-left element set to zero. So what does this mean?

Well, recall that we stated that the column `\(r_1\)` is the representation of a unit vector `\(x_1\)` in Frame 0. A unit vector, by definition, has a magnitude (length) of 1, so we have:
`\[
\begin{align}
1 &= \lVert r_1 \rVert \\
&= r_{1 1}^2 + r_{2 1}^2 + 0^2 \\
&= r_{1 1}^2 + r_{2 1}^2
\end{align}
\]`
`\[
\therefore r_{1 1}^2 + r_{2 1}^2 = 1
\]`
By the same argument, we can see that the bottom *row* of `\(R_1^0\)` is just a representation of `\(z_0\)` with respect to Frame 1, so it must also have a unit length. That means that we must also have
`\[
r_{3 2}^2 + r_{3 3}^2 = 1
\]`
Now, it's a [trigonometric identity](http://en.wikipedia.org/wiki/List_of_trigonometric_identities#Pythagorean_identity) that `\(\cos{x}^2 + \sin{x}^2 = 1 \)` for any `\(x\)`. That means that for any `\(r_{1 1}\)` and `\(r_{2 1}\)` such that `\(r_{1 1}^2 + r_{2 1}^2 = 1\)`, we can find some unique angle `\(\theta\)` such that `\(r_{1 1} = \cos{\theta} \)` and `\( r_{2 1} = \sin{\theta} \)`. Likewise, we can find some unique angle `\(\beta\)` such that `\(r_{3 2} = \sin{\beta}\)` and `\(r_{3 3} = \cos{\beta}\)`. Applying this argument to all the rows and columns of `\(R_1^0\)` shows that all the elemnts are valid and unique.

## Translation
To show that we also have unique values for our two translation parameters, `\(a\)` and `\(d\)`, we'll use our second condition:
`\[
\text{DH2: The axis $x_1$ intersects $z_0$}
\]`
I'll repeat the diagram of our two frames here for convenience:

<img src="/img/2012-06-19/d-h_axes2.png">

As you can see from the diagram, traveling from the origin of Frame 0 (which we'll call `\(O_0\)`) to the origin of Frame 1 (which we'll call `\(O_1\)`) can be done by just moving along `\(z_0\)` and then `\(x_1\)`. Writing this out, we get
`\[
O_1 = O_0 + d z_0 + a x_1
\]`
Expressing this in the coordinates of Frame 0, we get
`\[
O_1^0 = O_0^0 + d z_0^0 + a x_1^0
\]`
`\(O_0^0\)` is the origin of Frame 0 with respect to Frame 0, which is just `\(\begin{bmatrix}0 \\ 0 \\ 0 \end{bmatrix}\)`. And `\(z_0^0\)` and `\(x_1^0\)` we saw when we did rotations, so we can substitute their values into the equation:
`\[
\begin{align}
O_1^0 &= O_0^0 + d z_0^0 + a x_1^0 \\
&= \begin{bmatrix}0 \\ 0 \\ 0 \end{bmatrix} + d 
\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} + a
\begin{bmatrix} \cos{\theta} \\ \sin{\theta} \\ 0 \end{bmatrix} \\
&= \begin{bmatrix}
a \cos{\theta} \\
a \sin{\theta} \\
d
\end{bmatrix}
\end{align}
\]`
This is precisely the translation component of our matrix `\(A\)`. Therefore, we've shown that we can uniquely express the transformation between any two frames meeting our criteria DH1 and DH2 with a matrix `\(A\)` consisting of only four independent parameters `\(a, d, \theta, \beta\)` and arranged as a sequence of two rotations and two translations. Bam, existence and uniqueness!
