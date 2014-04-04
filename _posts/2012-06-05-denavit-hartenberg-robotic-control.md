---
layout: post
title: "Denavit-Hartenberg Analysis for Robotic Control"
category: Lessons
tags: []
---
{% include JB/setup %}

# Introduction

A couple months ago, I taught myself coordinate frame transformations and the Denavit-Hartenberg parameters for inverse kinematics in robotics, primarily from Chapter 3 of [Robot Modeling and Control by Spong et. al](http://www.amazon.com/Robot-Modeling-Control-Mark-Spong/dp/0471649902) and [this lecture from MIT](http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-07-dynamics-fall-2009/lecture-notes/MIT16_07F09_Lec03.pdf). But one does not truly understand something until one can teach it, so here goes. This should make sense to you if you know how to use the dot product and how to multiply matrices. 

[Part 1](/2012/06/05/denavit-hartenberg-robotic-control/)/[Part 2](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/)/[Part 3](/2012/06/10/denavit-hartenberg-for-robotics-part-3-the-d-h-parameters/)/[Part 4](/2012/06/19/denavit-hartenberg-parameters-part-4-existence-and-uniqueness/)/[Part 5](/2012/06/25/denavit-hartenberg-analysis-part-5-assigning-coordinate-frames/)/[Part 6](/2012/06/27/denavit-hartenberg-analysis-part-6-examples/)

# Motivation

Let's say we have a robot:

<img class="svg-figure" src="/img/2012-06-05/robot.svg">

"Hello, world!"

Now let's say we want to control our robot. Broadly speaking, this means that we want to decide *where* parts of him are at particular times. In order to define where something is, we need a frame of reference, so let's staple a coordinate system called "Frame 0" to his shoulder:

<img class="svg-figure" src="/img/2012-06-05/robot_with_frame_0.svg">


Great! Now we can describe our robot's location and orientation in Frame 0. It's at `\(x = 0\)`, `\(y = 0\)`. Fascinating.

To make things more interesting, let's add an arm to our robot friend:

<img class="svg-figure" src="/img/2012-06-05/robot_with_arm.svg">


We'll call the angle his arm makes to the horizontal `\(\theta\)`. Now we can also attach a coordinate frame to the end of his arm, which we'll clevely call Frame 1:

<img class="svg-figure" src="/img/2012-06-05/robot_with_arm_and_frame_1.svg">


Why do we bother?

Well, having a coordinate frame at the end of the robot's arm lets us figure out where things in the world are relative to that point, which is where we would put the robot's hand or gripper or death saw. For example, to grab an object, we need to move the arm until the object is at position `\(x_1 = 0\)`, `\(y_1 = 0\)`, like so:

<img class="svg-figure" src="/img/2012-06-05/robot_with_arm_and_frame_1_and_ball.svg">


This is great, but not very useful by itself. When we're controlling the robot, we can use the motor his shoulder to change the angle `\(\theta\)`, but it's not obvious in general what angle we want to get the ball to `\(x_1 = 0\)`, `\(y_1 = 0\)`. What we want is an [inverse kinematics](http://en.wikipedia.org/wiki/Inverse_kinematics), a way to go from a desired orientation for the business end of our arm to the angle of the arm's joints. That's what we're going to develop, over the course of a few pages of math. But there will be pictures, so hang in there. 

# Background: Coordinate Frame Transforms

Imagine a ball and a fixed coordinate frame:

<img class="svg-figure" src="/img/2012-06-05/ball_frame_0.svg">


We're going to use `\(x_1 \text{and } x_2 \)` instead of x and y here just so that the notation is a bit easier to generalize, but there's no reason you couldn't do this all in x, y, z if you preferred.

The vector from the origin (at the 0) to the ball is `\(\begin{bmatrix} x_1 = 4 \\ x_2 = 3 \end{bmatrix}\)` or just `\(\begin{bmatrix} 4 \\ 3 \end{bmatrix}\)` in this coordinate system (which we'll call Frame 0). 

Now let's add another coordinate frame, rotated by an angle `\(\theta\)`:

<img class="svg-figure" src="/img/2012-06-05/ball_frame_0_and_1.svg">


How do we represent the vector pointing to the ball in the primed (`\(x_1', x_2'\)`) frame? Simple: that's what the dot product is for. When we ask the question "How do we represent a vector `\(\vec{v}\)` in a coordinate system?" we're really just asking for the *projection* of `\(\vec{v}\)` onto the unit vectors (`\(i_1'\)` and `\(i_2'\)`) of the coordinate system. That is to say, we're looking for this representation of `\(\vec{v}\)`:

`\[
\vec{v}' = \begin{bmatrix} \vec{v} \cdot i_1' \\ \vec{v} \cdot i_2' \end{bmatrix}
\]`

Now, let's see if we can make a more general statement out of this. Let's define each of the components for our vector `\(\vec{v}\)`:

In the original frame:
`\(\vec{v} = v_1 i_1 + v_2 i_2\)`

And in the rotated frame:
`\(\vec{v} = v_1' i_1' + v_2' i_2'\)`

Where:
`\[
\begin{align}
v_1 &= \vec{v} \cdot i_1 \\
v_2 &= \vec{v} \cdot i_2 \\
v_1' &= \vec{v}' \cdot i_1' \\
v_2' &= \vec{v}' \cdot i_2' \\
\end{align}
\]`

Can we find a general equation for each component `\(v_j'\)`? Sure, just by doing some substitution:

`\[
\begin{align}
v_j' &= \vec{v} \cdot i_j' \\
\vec{v} &= v_1 i_1 + v_2 i_2 \\
v_j' &= (v_1 i_1 + v_2 i_2) \cdot i_j' \\
\end{align}
\]`
And, because the dot product is commutative and distributive:
`\[
\begin{align}
v_j' &= v_1 i_1 \cdot i_j' + v_2 i_2 \cdot i_j' \\
 &= v_1 i_j' \cdot i_1 + v_2 i_j' \cdot i_2 \\
\end{align}
\]`

Okay, now we have a general form for each component in the rotated coordinate system. However, this method is pretty messy: it would be nice if we could cleanly express this in a single equation. As it happens, matrices will serve us well here. The basic properties of matrix multiplication mean that we can write out the preceding lines as the following matrix equation:

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

Now, is there an even easier way to write this? Yes, as it turns out. Recall that we can calculate the dot product between two vectors from the angle between them:

`\[
\cos{\theta_{v u}} = \frac{\vec{v} \cdot \vec{u}}{\lVert v \rVert \lVert u \rVert}
\]`
where `\(\theta_{v u}\)` is the angle from the vector `\(\vec{v}\)` to the vector `\(\vec{u}\)` and `\(\lVert u \rVert\)` is the length of `\(\vec{u}\)`. For our unit vectors, this length is always equal to 1 by definition, so we can simplify the equation to:

`\[
\cos{\theta_{i_j' i_i}} = i_j' \cdot i_i
\]`
which we will shorten to
`\[
\cos{\theta_{j i}} = i_j' \cdot i_i
\]`
for the sake of convenience. Thus, we now have:
`\[
v_j' = v_1 \cos{\theta_{j 1}} + v_2 \cos{\theta_{j 2}} + v_3 \cos{\theta_{j 3}}
\]`
and, in matrix form:
`\[
\vec{v}' = \begin{bmatrix}
v_1' \\
v_2'
\end{bmatrix} =
\begin{bmatrix}
\cos{\theta_{1 1}} & \cos{\theta_{1 2}} \\
\cos{\theta_{2 1}} & \cos{\theta_{2 2}}
\end{bmatrix}
\begin{bmatrix}
v_1 \\
v_2
\end{bmatrix}
\]`

Let's call this matrix of cosines a *Rotation matrix* and denote it as 
`\[
\begin{align}
\left[ R \right] &\equiv \begin{bmatrix}
\cos{\theta_{1 1}} & \cos{\theta_{1 2}} \\
\cos{\theta_{2 1}} & \cos{\theta_{2 2}}
\end{bmatrix}\\
\vec{v}' &= \left[ R \right]\, \vec{v}
\end{align}
\]`

## Brief aside: inverting rotation matrices
We can use this angular definition to express a cool property of `\(\left[ R \right]\)`. Recall that we defined the angle `\(\theta_{i j}\)` as the angle from `\(i_i'\)` to `\(i_j\)`. Now, let's also define an angle `\(\phi_{i j}\)` as the angle from `\(i_i\)` to `\(i_j'\)`. Using this definition, we essentially just repeat all the prior steps with the names of the coordinate systems (x' and x) swapped, to get an equivalent relationship:
`\[
\vec{v} = \begin{bmatrix}
v_1 \\
v_2
\end{bmatrix} =
\begin{bmatrix}
\cos{\phi_{1 1}} & \cos{\phi_{1 2}} \\
\cos{\phi_{2 1}} & \cos{\phi_{2 2}}
\end{bmatrix}
\begin{bmatrix}
v_1' \\
v_2'
\end{bmatrix}
\]`

In addition, if `\(\phi_{i j}\)` is the angle from `\(i_i\)` to `\(i_j'\)` then it must be the negative of `\(\theta_{j i}\)`, which is the angle from `\(i_j'\)` to `\(i_i\)`. More concretely:
`\[
\phi_{i j} = - \theta_{j i}
\]`
and thus
`\[
\cos{\phi_{i j}} = \cos{\theta_{j i}}
\]`
Therefore, we can rewrite the above transformation as:
`\[
\vec{v} = 
\begin{bmatrix}
\cos{\theta_{1 1}} & \cos{\theta_{2 1}} \\
\cos{\theta_{1 2}} & \cos{\theta_{2 2}}
\end{bmatrix} \vec{v}'
\]`
This is just the [matrix transpose](http://en.wikipedia.org/wiki/Transpose) of the original rotation matrix `\(\left[ R \right]\)`:
`\[
\vec{v} = \left[ R \right]^T\, \vec{v}'
\]`
Substituting, we get:
`\[
\begin{align}
\vec{v} &= \left[ R \right]^T\, \left[ R \right]\, \vec{v} \\
 &= I\, \vec{v}\\
 &= \vec{v}
\end{align}
\]`
Where `\(I\)` is the [identity matrix](http://en.wikipedia.org/wiki/Identity_matrix). This is sufficient to show that `\(\left[ R \right]^T\)` is also the *matrix inverse* of `\(\left[ R \right]\)`:
`\[
\left[ R \right]^T = \left[ R \right]^{-1}
\]`
Thus:
`\[
\vec{v} = \left[ R \right]^{-1}\, \vec{v}' = \left[ R \right]^T\, \vec{v}'
\]`
Neat!

## Extending this to three dimensions
I won't go through the math here, but we can (not surprisingly) do all of this just as effectively in three dimensions instead of two. In that case, our vector `\(\vec{v}\)` will have three components: `\(v_1, v_2, v_3\)` and our rotation matrix `\(\left[ R \right]\)` will look like this:
`\[
\vec{v}' = \begin{bmatrix}
\cos{\theta_{1 1}} & \cos{\theta_{1 2}} & \cos{\theta_{1 3}} \\
\cos{\theta_{2 1}} & \cos{\theta_{2 2}} & \cos{\theta_{2 3}} \\
\cos{\theta_{3 1}} & \cos{\theta_{3 2}} & \cos{\theta_{3 3}}
\end{bmatrix}\, \vec{v}
\]`

If we want to describe rotation about just one axis, like in this cartoon:

<img class="svg-figure" src="/img/2012-06-05/3d_rotation_example.svg">


then this is pretty simple. We can see that `\(x_3 = x_3'\)`, so `\(\theta_{3 3} = 0\)`, and `\(\theta_{3 i} \text{ and } \theta_{i 3}\)` are both `\(\frac{\pi}{2}\)` for `\(i = 1 \text{ or } 2\)`. Similarly, `\(\theta_{1 1} \text{ and } \theta_{2 2}\)` are just equal to `\(\alpha\)`. 

Using some basic [trig identities](http://en.wikipedia.org/wiki/List_of_trigonometric_identities#Symmetry) we can see that `\(\theta_{2 1} = -\left( \frac{\pi}{2} + \alpha \right)\)` means that 
`\[
\cos{\theta_{2 1}} = \cos{-\left( \frac{\pi}{2} + \alpha \right)} = \cos{\frac{\pi}{2} + \alpha} = -\sin{\alpha}
\]`. 
And likewise
`\[
\cos{\theta_{2 1}} = \sin{\alpha}
\]`
Thus, our whole rotation matrix becomes this fairly simple form:
`\[
\begin{bmatrix}
\cos{\alpha} & -\sin{\alpha} & 0 \\
\sin{\alpha} & \cos{\alpha} & 0 \\
0 & 0 & 1
\end{bmatrix}
\]`

# Coming up: Homogeneous Matrices and You
Stay tuned for the [next installment](/2012/06/09/denavit-hartenberg-for-robotics-part-2-homogeneous-matrices/), in which we reveal why all this lovely rotation stuff is only half of the picture, and in which all our matrices get 78% bigger. 
