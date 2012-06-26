---
layout: post
title: "Denavit Hartenberg Analysis, Part 2: Homogeneous Matrices"
category: 
tags: []
---
{% include JB/setup %}

[Part 1](/2012/06/05/denavit-hartenberg-robotic-control/)/[Part 2](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/)/[Part 3](/2012/06/10/denavit-hartenberg-for-robotics-part-3-the-d-h-parameters/)/[Part 4](/2012/06/19/denavit-hartenberg-parameters-part-4-existence-and-uniqueness/)/[Part 5](/2012/06/25/denavit-hartenberg-analysis-part-5-assigning-coordinate-frames/)

# The Problem

In [Part 1](/2012/06/05/denavit-hartenberg-robotic-control/) of this series, in which I attempt to explain the Denavit-Hartenberg convention for inverse kinematics I talked about coordinate frames and rotational transformations using matrices. This left open a pretty obvious question, though: turning coordinate frames is great and all, but how do we *move* them? If we want to describe the transformation from Frame 1 to Frame 0 here:
 
<img src="/img/2012-06-05/robot_with_arm_and_frame_1_d.png">

Then we need to express the rotation by the angle `\(\theta\)` (which we figured out last time) *and* the translation by the distance `\(d\)` (which we don't know how to do yet). 

To make this a little more clear, let's look at an example of a translation by a vector `\(\vec{t}\)`:
`\[
\begin{align}
\vec{v}' &= \vec{v} + \vec{t} \\
\begin{bmatrix}
v_1' \\
v_2' \\
v_3'
\end{bmatrix} &=
\begin{bmatrix}
v_1 \\
v_2 \\
v_3
\end{bmatrix} + \begin{bmatrix}
t_1 \\
t_2 \\
t_3 
\end{bmatrix}
\end{align}
\]`

Given how we handled rotation matrices [last time](http://blog.robindeits.com/2012/06/05/denavit-hartenberg-robotic-control/), we'd really like to find a matrix such that we can write down that translation as a matrix multiplication:
`\[
\vec{v}' = \left[ T \right] \, \vec{v}
\]`
For some magical unknown matrix `\(\left[ T \right]\)`. But...we can't. You can try. In fact, go for it! It's a useful exercise, but it's going to be futile, and we can show that pretty easily. As an example, let's see what happens if we set `\(\vec{v}\)` to be all zeros:
`\[
\vec{v}' = \left[ T \right] \, \begin{bmatrix}
0 \\
0 \\
0
\end{bmatrix}
\]`
No matter what we set `\(\left[ T \right]\)` to be, `\(\vec{v}'\)` will always just be zeros. So clearly this method won't work.

# The Solution: Homogeneous Coordinates

It turns out that there's a pretty simple fix for this, and it involves adding an extra term to each of our vectors. If we add a 1 to the end of each of our vectors `\(\vec{v}\)`, then they end up looking like this:
`\[
\vec{v} = \begin{bmatrix}
v_1 \\
v_2 \\
v_3 \\
1
\end{bmatrix}
\]`
As it happens, we can now write out our translation matrix `\(\left[ T \right]\)` using this coordinate system:
`\[
\begin{align}
\vec{v}' &= \vec{v} + \vec{t} \\
\begin{bmatrix}
v_1' \\
v_2' \\
v_3' \\
1
\end{bmatrix} &= \begin{bmatrix}
1 & 0 & 0 & t_1 \\
0 & 1 & 0 & t_2 \\
0 & 0 & 1 & t_3 \\
0 & 0 & 0 & 1
\end{bmatrix}\,
\begin{bmatrix}
v_1 \\
v_2 \\
v_3 \\
1
\end{bmatrix} 
\end{align}
\]`
If we write out the matrix multiplication, then we get the following equations:
`\[
\begin{align}
v_1' &= v_1 + t_1 \\
v_2' &= v_2 + t_2 \\
v_3' &= v_3 + t_3
\end{align}
\]`
which is exactly what we wanted! Rotations also work just fine in this coordinate system:
`\[
\vec{v}' = \begin{bmatrix}
\cos{\theta_{1 1}} & \cos{\theta_{1 2}} & \cos{\theta_{1 3}} & 0 \\
\cos{\theta_{2 1}} & \cos{\theta_{2 2}} & \cos{\theta_{2 3}} & 0 \\
\cos{\theta_{3 1}} & \cos{\theta_{3 2}} & \cos{\theta_{3 3}} & 0 \\
0 & 0 & 0 & 1
\end{bmatrix} \, \begin{bmatrix}
v_1 \\
v_2 \\
v_3 \\
1
\end{bmatrix}
\]`
The real kicker is that we can now combine translation and rotation just by multiplying our matrices together. For example, performing a rotation and then a translation might look like this:
`\[
\vec{v}' = \begin{bmatrix}
1 & 0 & 0 & t_1 \\
0 & 1 & 0 & t_2 \\
0 & 0 & 1 & t_3 \\
0 & 0 & 0 & 1
\end{bmatrix} \,
\begin{bmatrix}
\cos{\theta_{1 1}} & \cos{\theta_{1 2}} & \cos{\theta_{1 3}} & 0 \\
\cos{\theta_{2 1}} & \cos{\theta_{2 2}} & \cos{\theta_{2 3}} & 0 \\
\cos{\theta_{3 1}} & \cos{\theta_{3 2}} & \cos{\theta_{3 3}} & 0 \\
0 & 0 & 0 & 1
\end{bmatrix} \, 
\begin{bmatrix}
v_1 \\
v_2 \\
v_3 \\
1
\end{bmatrix}
\]`
We can use the [associative property](http://en.wikipedia.org/wiki/Associative_property) of matrix multiplication to simplify this:
`\[
\begin{align}
\vec{v}' &= \left(
\begin{bmatrix}
1 & 0 & 0 & t_1 \\
0 & 1 & 0 & t_2 \\
0 & 0 & 1 & t_3 \\
0 & 0 & 0 & 1
\end{bmatrix} \,
\begin{bmatrix}
\cos{\theta_{1 1}} & \cos{\theta_{1 2}} & \cos{\theta_{1 3}} & 0 \\
\cos{\theta_{2 1}} & \cos{\theta_{2 2}} & \cos{\theta_{2 3}} & 0 \\
\cos{\theta_{3 1}} & \cos{\theta_{3 2}} & \cos{\theta_{3 3}} & 0 \\
0 & 0 & 0 & 1
\end{bmatrix} \right) \, 
\begin{bmatrix}
v_1 \\
v_2 \\
v_3 \\
1
\end{bmatrix} \\
 &= \begin{bmatrix}
\cos{\theta_{1 1}} & \cos{\theta_{1 2}} & \cos{\theta_{1 3}} & t_1 \\
\cos{\theta_{2 1}} & \cos{\theta_{2 2}} & \cos{\theta_{2 3}} & t_2 \\
\cos{\theta_{3 1}} & \cos{\theta_{3 2}} & \cos{\theta_{3 3}} & t_3 \\
0 & 0 & 0 & 1
\end{bmatrix} \, 
\begin{bmatrix}
v_1 \\
v_2 \\
v_3 \\
1
\end{bmatrix}
\end{align}
\]`
Notice how the rotation and translation components of this resulting transformation stay in their own sections of the matrix. We'll use that nice property to devise a shorthand for this kind of transformation matrix. Let:
`\[
\textbf{H} \equiv \begin{bmatrix}
R & T \\
0 & 1
\end{bmatrix} \equiv \begin{bmatrix}
\cos{\theta_{1 1}} & \cos{\theta_{1 2}} & \cos{\theta_{1 3}} & t_1 \\
\cos{\theta_{2 1}} & \cos{\theta_{2 2}} & \cos{\theta_{2 3}} & t_2 \\
\cos{\theta_{3 1}} & \cos{\theta_{3 2}} & \cos{\theta_{3 3}} & t_3 \\
0 & 0 & 0 & 1
\end{bmatrix}
\]`
Where R represents the rotation component and T represents the translation component. 

# Next time: putting it all together

In the [next installment](/2012/06/10/denavit-hartenberg-for-robotics-part-3-the-d-h-parameters/), we'll use all of this coordinate transformation business to build a system that will let us figure out how to control our robot's arm. 