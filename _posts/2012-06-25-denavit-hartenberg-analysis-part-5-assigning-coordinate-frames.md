---
layout: post
title: "Denavit Hartenberg Analysis, Part 5: Assigning Coordinate Frames"
category: 
tags: []
---
{% include JB/setup %}

[Part 1](/2012/06/05/denavit-hartenberg-robotic-control/)/[Part 2](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/)/[Part 3](/2012/06/10/denavit-hartenberg-for-robotics-part-3-the-d-h-parameters/)/[Part 4](/2012/06/19/denavit-hartenberg-parameters-part-4-existence-and-uniqueness/)/[Part 5](/2012/06/25/denavit-hartenberg-analysis-part-5-assigning-coordinate-frames/)/[Part 6](/2012/06/27/denavit-hartenberg-analysis-part-6-examples/)

Last time, we showed that we can use a sequence of four particular transformations to uniquely describe the transformation between two coordinate systems which satisfy the following two properties:

`\[
\begin{align}
&\text{DH1: The axis $x_1$ is perpendicular to $z_0$}\\
&\text{DH2: The axis $x_1$ intersects $z_0$}
\end{align}
\]`

For example, these two frames:

<object data="/img/2012-06-19/d-h_axes2.svg" type="image/svg+xml">
</object>

This is great, but it's only generally useful if we can show that we can always describe the joints and arms of our robot in a way that satisfies these two constraints. We'll show just how to do that now by considering the three possible arrangements ([1](#case_1__and__are_not_coplanar), [2](#case_2__and__are_parallel), [3](#case_3__intersects_)) of joint axes. We'll then explain how to [compute the link parameters](#computing_the_link_parameters) and thus construct the transformation matrix.

To do it, let's first bring back our robot from [Part 1](/2012/06/05/denavit-hartenberg-robotic-control/):

<object data="/img/2012-06-05/robot_with_arm.svg" type="image/svg+xml">
</object>

To make him a little more useful, let's add another joint to each arm and number the links and joints in one arm:

<object data="/img/2012-06-25/robot_2_joints.svg" type="image/svg+xml">
</object>

As we did before, we've named the <font color="ff3c3c">joints</font> and links so that when joint `\(i\)` is activated, link `\(i\)` will move.

Let's simplify this drawing for now:

<object data="/img/2012-06-25/simple_arm.svg" type="image/svg+xml">
</object>

Now we begin assigning coordinate frames. Let's first choose something intuitive for `\(z_0\)`. Specifically, let's choose the axis of rotation of joint 1. In general, we will will say the following:
`\[
\text{Let $z_i$ be the axis of actuation for joint $i+1$ (rotation or translation, as appropriate)}
\]`
We can then choose `\(O_0\)` (the origin of coordinate system 0) anywhere we like along `\(z_0\)` and place `\(x_0\)` wherever we want (we'll make it horizontal just for convenience here). Once we have `\(z_0\)` and `\(x_0\)`, the [right hand rule](http://en.wikipedia.org/wiki/Cartesian_coordinate_system#In_three_dimensions) dictates where `\(y_0\)` must go. Let's add this to the simplified robot arm (`\(z_0\)` comes right out of the page, so it isn't shown here):

<object data="/img/2012-06-25/simple_arm_frame0.svg" type="image/svg+xml">
</object>

Now that we have somewhere to start, we will define each new frame `\(i\)` using the position and orientation of the previous frame `\(i-1\)`. Remember that we've defined each `\(z_i\)` as the axis of rotation or translation for joint `\(i+1\)`. There are three cases that we'll need to address to decide how to chose the origins `\(O_i\)` and the other unit vectors `\(x_i\)` and `\(y_i\)`.

## Case 1: `\(z_{i-1}\)` and `\(z_i\)` are not coplanar
Two vectors in three dimensional space are _non-coplanar_ if they can't lie in the same flat plane. For example, consider these two vectors:

<object data="/img/2012-06-25/non-coplanar_vectors.svg" type="image/svg+xml">
</object>

An interesting property of non-coplanar vectors is that we can show that there is exactly one line segment which is perpendicular to both vectors and which connects them with the shortest length. We've labeled that line segment `\(a\)` above. If our robot has two adjacent joints whose axes are non-coplanar, then we will use the following procedure to assign the new frame `\(i\)`:

1. Find the shortest line connecting the two axes which is perpendicular to both and call it `\(\vec{v}\)`.

2. The point where `\(\vec{v}\)` intersects `\(z_{i}\)` becomes `\(O_{i}\)`

3. `\(x_{i}\)` goes through `\(O_{i}\)` in the same direction as `\(\vec{v}\)`

4. `\(y_{i}\)` is defined by the [right hand rule](http://en.wikipedia.org/wiki/Cartesian_coordinate_system#In_three_dimensions)

You can see this procedure in action here. First, the joint setup, with the axes marked:

<object data="/img/2012-06-25/non-coplanar_with_arm.svg" type="image/svg+xml">
</object>

Then the assignment of coordinate frames:

<object data="/img/2012-06-25/non-coplanar.svg" type="image/svg+xml">
</object>

## Case 2: `\(z_{i-1}\)` and `\(z_i\)` are parallel

Two parallel vectors have infinitely many common normals (vectors `\(\vec{v}\)` which are perpendicular to both of them), so we can choose any one of these to be the direction of `\(x_{i}\)`. For convenience, we'll pick `\(x_{i}\)` so that it passes through `\(O_{i-1}\)`. So, our procedure is:

1. Find the vector `\(\vec{v}\)` which is perpendicular to `\(z_{i-1}\)` and `\(z_{i}\)` and which passes through `\(O_{i-1}\)`. Call it `\(\vec{v}\)`. 

2. The point where `\(\vec{v}\)` intersects `\(z_{i}\)` becomes `\(O_{i}\)`

3. `\(x_{i}\)` goes through `\(O_{i}\)` in the same direction as `\(\vec{v}\)`

4. `\(y_{i}\)` is defined by the [right hand rule](http://en.wikipedia.org/wiki/Cartesian_coordinate_system#In_three_dimensions)

You can see this procedure in action here. First, the joint setup, with the axes marked:

<object data="/img/2012-06-25/parallel_with_arm.svg" type="image/svg+xml">
</object>

Then the assignment of coordinate frames:

<object data="/img/2012-06-25/parallel_with_axes.svg" type="image/svg+xml">
</object>

## Case 3: `\(z_{i-1}\)` intersects `\(z_i\)`

If `\(z_{i-1}\)` and `\(z_i\)` intersect, then we just choose `\(x_{i}\)` to be perpendicular to both vectors (this gives us two opposing possible directions for `\(x_{i}\)`, so we pick whichever we like). Our procedure is:

1. Define `\(x_{i}\)` to be perpendicular to both `\(z_{i-1}\)` and `\(z_{i}\)`.

2. Place `\(O_{i}\)` anywhere along `\(z_{i}\)`. For convenience, let's pick the point of intersection with `\(z_{i-1}\)`.

3. `\(y_{i}\)` is defined by the [right hand rule](http://en.wikipedia.org/wiki/Cartesian_coordinate_system#In_three_dimensions)

Once more, the joint setup, with the axes marked:

<object data="/img/2012-06-25/intersect_with_arm.svg" type="image/svg+xml">
</object>

Then the assignment of coordinate frames:

<object data="/img/2012-06-25/intersect_with_axes.svg" type="image/svg+xml">
</object>

# Computing the Link Parameters

Now that we've determined the exact position and orientation of the adjacent coordinate frames, we need to find the transformation matrix between each pair of frames. To do that, we find the link parameters that were introduced in [Part 3](/2012/06/10/denavit-hartenberg-for-robotics-part-3-the-d-h-parameters/) for each joint. The parameters are calculated as follows:
`\[
\begin{align}
a_i &= \text{Distance along $x_i$ from $O_i$ to the intersection of $x_i$ and $z_{i-1}$} \\
d_i &= \text{Distance along $z_{i-1}$ from $O_{i-1}$ to the intersection of $x_i$ and $z_{i-1}$} \\
\beta_i &= \text{Angle from $z_{i-1}$ to $z_i$, measured about $x_i$} \\
\theta_i &= \text{Angle from $x_{i-1}$ to $x_i$, measured about $z_{i-1}$}
\end{align}
\]`
Once we've done this, we know exactly the transformation matrix from Frame `\(i-1\)` to Frame `\(i\)`:
`\[
A_i = \begin{bmatrix}
\cos{\theta_i} & -\sin{\theta_i} \cos{\beta_i} & \sin{\theta_i} \sin{\beta_i} & a_i \cos{\theta_i} \\
\sin{\theta_i} & \cos{\theta_i} \cos{\beta_i} & -\cos{\theta_i} \sin{\beta_i} & a_i \sin{\theta_i} \\
0 & \sin{\beta_i} & \cos{\beta_i} & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}
\]`
If our joint `\(i\)` is revolute (rotating), then only `\(\theta_i\)` will vary. If it's prismatic (sliding), then only `\(d_i\)` varies. 

# Assigning the Final Frame

Our final coordinate frame is called the "tool frame," and it goes at the very end of the robot's arm. We call it the tool frame because it is the only frame in which the position of the robot's tool (gripper, drill, welding arm, death laser, etc.) is fixed. This is by far the most useful frame, because, for example, if we want to move the arm until an object is at the center of the gripper, we simply need to move the joints until the position of the object is (0, 0, 0) in the tool frame.

By convention, we align the tool frame so that the origin is between the fingers of the gripper or at the point of the tool. We orient `\(z_n\)` to the direction of approach and `\(y_n\)` to the direction along which the fingers of the gripper move. This defines the orientation of `\(x_n\)`. You can see an example of this here:

<object data="/img/2012-06-25/tool_with_arm.svg" type="image/svg+xml">
</object>

The calculation of the link parameters for this pair of frames is done exactly the same as with every other pair.

# Solving the Entire Arm

We now know everything we need to put together a set of transformation matrices to describe an arm consisting of any number of revolute and prismatic in any configuration we can imagine. Our general method is as follows (this is taken primarily from Chapter 3 of [Robot Modeling and Control by Spong et. al](http://www.amazon.com/Robot-Modeling-Control-Mark-Spong/dp/0471649902)):

1. Locate and label the joint axes `\(z_0 \dots z_{n-1}\)`. 

2. Establish the base frame by choosing an origin `\(O_0\)` somewhere along `\(z_0\)`, and choose convenient directions for `\(x_0\)` and `\(y_0\)`.

3. For each additional joint `\(i\)`, locate the origin `\(O_i\)` where the common normal to `\(z_i\)` and `\(z_{i-1}\)` intersects `\(z_i\)`. If `\(z_i\)` intersects `\(z_{i-1}\)`, then place `\(O_i\)` at their intersection. If `\(z_i\)` is parallel to `\(z_{i-1}\)`, then place `\(O_i\)` anywhere along `\(z_i\)`.

4. Locate `\(x_i\)` along the common normal between `\(z_{i-1}\)` and `\(z_i\)` through `\(O_i\)`, or in the direction normal to the plane containing `\(z_{i-1}\)` and `\(z_i\)` if they intersect.

5. Locate `\(y_i\)` using the right hand rule.

6. Repeat steps 3 through 5 for each joint frame `\(i=1 \dots n-1\)`.

7. Create the final (tool) frame `\(O_n, x_n, y_n, z_n\)` as described in the [tool frame](#assigning_the_final_frame) section.

8. Create a table of the link parameters `\(a_i, d_i, \beta_i, \theta_i\)` between each adjacent pair of coordinate frames.

9. Form the homogeneous transformation matrices `\(A_i\)` by substituting these parameters into the matrix equation:
`\[
A_i = \begin{bmatrix}
\cos{\theta_i} & -\sin{\theta_i} \cos{\beta_i} & \sin{\theta_i} \sin{\beta_i} & a_i \cos{\theta_i} \\
\sin{\theta_i} & \cos{\theta_i} \cos{\beta_i} & -\cos{\theta_i} \sin{\beta_i} & a_i \sin{\theta_i} \\
0 & \sin{\beta_i} & \cos{\beta_i} & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}
\]`

10. Determine the overall transformation from the base of the arm to its end by multiplying the `\(A_i\)` matrices together:
`\[
T_n^0 = A_1 A_2 \dots A_{n-1} A_n
\]`

# Conclusion

That's it! We've covered the entire theory behind Denavit-Hartenberg analysis. In the next and final post, we'll go through a few examples and talk about non-standard joints (joints which aren't simply revolute or prismatic). Enjoy!