---
layout: post
title: "Denavit Hartenberg Analysis, Part 3: The D-H Parameters"
category: 
tags: []
---
{% include JB/setup %}

[Part 1](/2012/06/05/denavit-hartenberg-robotic-control/)/[Part 2](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/)/[Part 3 (this page)](/2012/06/10/denavit-hartenberg-for-robotics-part-3-the-d-h-parameters/)/[Part 4](/2012/06/19/denavit-hartenberg-parameters-part-4-existence-and-uniqueness/)

In [Part 1](/2012/06/05/denavit-hartenberg-robotic-control/) and [Part 2](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/) of this series, we talked about why inverse kinematics could be useful, and did some background on coordinate transformations and homogeneous matrices. Now we're going to put that together to start understanding the Denavit-Hartenberg parameters. 

# Terminology

First, let's establish the particular jargon we'll be using for this explanation. Imagine a robot arm with `\(n\)` joints and `\(n+1\)` links, like so:

<img src="/img/2012-06-10/manipulator_links.png">
In this case, `\(n=2\)` and we've labeled the joints in <font color="ff3c3c">red</font> and the links in black. The naming convention here means that when join `\(i\)` is actuated, link `\(i\)` moves. In this example, joint 1 is *revolute*, meaning that it rotate *around* a single axis when actuated, and joint 2 is *prismatic* meaning that it slides *along* a single axis. The real world has lots of other kinds of joints (like a ball-and-socket, which can turn in all directions), but we're going to figure out a way to represent all possible joints as a combination of these two simple types. 

Now that we've identified each of our joints, let's assign a "joint variable" which describes the state of each joint. For our revolute joints, it will be their current angle of rotation, and for the prismatic joints, it will be their position along their axis of travel. We'll write these out like this:

`\[
q_i = \left\{  \begin{array}{l}
\theta_i \text{ if joint i is revolute} \\
d_i \text{ if joint i is prismatic} 
\end{array} \right.
\]`

Now, let's attach a coordinate system to each link such that every point on a link `\(i\)` is fixed in Frame `\(i\)`:

<img src="/img/2012-06-10/manipulator_links_frames.png">

Since there is no joint 0, Frame 0 consisting of `\(O_0, x_0, y_0, z_0\)` cannot move (`\(O_0\)` is just our notation for the Origin of Frame 0).

Now, here's where the matrices come in:

Let `\(A_i\)` be the homogeneous transformation matrix that expresses the position and orientation of `\(O_i, x_i, y_i, z_i\)` with respect to `\(O_{i-1}, x_{i-1}, y_{i-1}, z_{i-1}\)`. This matrix A will be some combination of rotations and translations, just like we described [last time](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/). As each joint moves, each transformation `\(A_i\)` will change. But each joint only has one variable, `\(q_i\)`, so `\(A_i\)` can only depend on `\(q_i\)`.

Next, let `\(T_j^i\)` be the transformation matrix which expresses the position and orientation of `\(O_j, x_j, y_j, z_j\)` with respect to `\(O_i, x_i, y_i, z_i\)`. By this definition, 
`\[
T_j^i = A_j \quad \text{if $i = j-1$}
\]`
More generally, we can say that:
`\[
T_j^i = \left\{
\begin{array}{l l}
A_{i+1} A_{i+2} A_{i+3} \dots A_{j-1} A_j & \text{if $i < j$}\\
I & \text{if $i=j$} \\
\left( T_i^j \right) ^{-1} & \text{if $j > i$}
\end{array}
\right.
\]`

This is a nice way to break up a complicated transformation, but it's still not easy enough. We can construct the transformation matrix `\(T\)` from each of the transformations `\(A_i\)`, but we still don't know how to *find* each `\(A_i\)`.

To do that, we're going to make an assumption, which will be justified soon, that makes life much easier. Let's assert that each homogeneous transformation matrix `\(A_i\)` can be represented as a product of four basic transformations:
`\[
A_i = R(z, \theta_i) \; T(z, d_i) \; T(x, a_i) \; R(x, \beta_i)
\]`
These transformations are:
`\[
\begin{align}
R(z, \theta_i)&: \quad \text{Rotation about z by an angle $\theta_i$ ("joint angle")} \\
T(z, d_i)&: \quad \text{Translation along z by a distance $d_i$ ("link offset")} \\
T(x, a_i)&: \quad \text{Translation along x by a distance $a_i$ ("link length")} \\
R(x, \beta_i)&: \quad \text{Rotation about x by an angle $\beta_i$ ("link twist")}
\end{align}
\]`
(Actually, `\(\alpha\)` is traditionally used instead of `\(\beta\)`, but it's maddeningly similar-looking to `\(a\)`, so we won't use it here). Using the framework we developed in the previous two parts, we can write down all of these transformations as matrices:
`\[
A_i = \begin{bmatrix}
\cos{\theta_i} & -\sin{\theta_i} & 0 & 0 \\
\sin{\theta_i} & \cos{\theta_i} & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix} \; \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}\; \begin{bmatrix}
1 & 0 & 0 & a_i \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix} \; \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & \cos{\beta_i} & -\sin{\beta_i} & 0 \\
0 & \sin{\beta_i} & \cos{\beta_i} & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\]`
Multiplying these all together gives us this:
`\[
A_i = \begin{bmatrix}
\cos{\theta_i} & -\sin{\theta_i} \cos{\beta_i} & \sin{\theta_i} \sin{\beta_i} & a_i \cos{\theta_i} \\
\sin{\theta_i} & \cos{\theta_i} \cos{\beta_i} & -\cos{\theta_i} \sin{\beta_i} & a_i \sin{\theta_i} \\
0 & \sin{\beta_i} & \cos{\beta_i} & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}
\]`
If our joint `\(i\)` is revolute (rotating), then only `\(\theta_i\)` will vary. If it's prismatic (sliding), then only `\(d_i\)` varies. 

Cool! We've gotten a lot closer to the answer to our original question of determining the positions for each joint of our robot needed to reach a desired end configuration. There are two big steps remaining, though, which I'll cover in the next two parts: first, we need to prove that this breakdown of each matrix `\(A_i\)` into four transformations is valid, and second, we need to figure out how to find all of the joint parameters `\(\theta_i, d_i, a_i, \beta_i\)`. Stay tuned!
