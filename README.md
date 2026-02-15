# astrodynamics Statefile

## Install and Download

You can find instructions on how to install .d32 Statefiles to your calculator [via the DM32 User Manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#_saving_and_loading_a_state). The process is extremely simple. You can download the .zip file from the release page from this GitHub repository.

Consulting this **Readme.md** before use is highly recommended. The program is simple enough to use, but the readme contains useful information. The file you will want to install on your calculator from the .zip file is **Astrodynamics.d32**.

## Using the Statefile

Using the program to calculate perfectly circular orbits from any main body in the Solar System (including the MOON) is really easy. The user uses a single variable (either orbit height, velocity, period, sidereal days, or circumference) to produce orbital data for the remaining variables. The Statefile leverages the DM32 four-line display to showcase orbital data in a clean and wildly understandable way.

### First Sample Problem ###

You wish to calculate orbital information for the International Space Station which has a mean orbital height of 407 km.

The known variable in this case is the height of the orbit from the surface of EARTH (407 km). What the user desires to know is the velocity, period, circumference, and sidereal day comparison of the orbit the station holds. We can confirm whether our calculation is correct by comparing the known mean orbital velocity of the ISS.

![First input the 407 km varible into the x-register.](assets/Example1.bmp)

User inputs 407 into the x-register. The user will run the **LBL H** *Initiator Program* because they are using the height variable as the known input. Start this program by pressing **XEQ H**.

![The first sub-routine will run and the user will be prompted for the Standard Gravitational Parameter and the radius of the main body.](assets/Example2.bmp)

The first sub-routine will run and the user will be prompted to input the [Standard Gravitational Parameter](https://en.m.wikipedia.org/wiki/Standard_gravitational_parameter) of the main body.

Note that values for the EARTH are present just above the input field in the y-register and values for the MOON are located above those in the z-register. These common values are pre-set for the user and can be used by selecting the R(down) key and placing the figures into the input field. The user can also input their own custom values or (aftering first running the LBL A program to store the values into indirect registers) can pull up values for any main body in the Solar System.

![User selects the EARTH value for our first problem.](assets/Example3.bmp)

Since for our first problem we are using an orbit around the EARTH, we are going to move the values for EARTH into the input field and press R/S to continue the sub-routine.

![User is prompted for radius](assets/Example5.bmp)

Following the gravitational parameter, the user will be prompted to input a value for the radius of the main body. This value is in meters. If you have selected the EARTH or MOON from the previous G input, be sure to select the same for this value, same for any custom value or indirect register value used.

![Selecting the EARTH value for radius for our first problem](assets/Example6.bmp)

The program continues to run and the LBL O sub-routine completes with the values displayed on the four-line display in addition to a VIEW of the sidereal comparion result.

![Final display results of the program.](assets/Example7.bmp)

The user can complete the program and display by selecting R/S (Note: that pressing C will also close the VIEW display but the program pointer will remain at line O07 and will not return to the top, ENTER can also be used by will push the stack up resulting in the height being dropped and the sidereal comparion taking up the x-register, the program pointer will remain at line O07). This will close the VIEW of the sidereal comparsion (which is not always relevant in orbital calculations beyond EARTH) and display the most common values on the four-line display. The order is as follows:

> - **T-REGISTER** / Height in km / Variable H
> - **Z-REGISTER** / Velocity in m/s / Variable V
> - **Y-REGISTER** / Circumference in km / Variable C
> - **X-REGISTER** / Period in min / Variable P

![Display results without the VIEW display activated.](assets/Example8.png)

We can compare our results to see how accurate our program runs. The ISS has a mean orbital velocity of 7.66 km/sec which our calculator displays accurately 7,664.601 m/s. While the orbit of the ISS is not a perfect circle, the eccenticity of it's orbit is low enough that using mean values, we can apply the theoretic oribital calculations simplified with a perfectly circular orbit and get very close results.

## Solar System Constants

The Statefile contains a routine program to store gravitational parameters, radii and relevant distances for planets within the Solar System and the MOON. This program can be run by the user by selecting XEQ A. The values are stored in indirect registers and are available between calculator states and are persistent with CLEAR VAR commands (but not calculator resets, which is why the program is available in the statefile to be run on reboots).

There is some method to the madness of how these values have been stored in the indirect global registers. Universal constants are stored in the -100 series. All other constants are stored in the -900 series. All planets are varied based on their relative position to the SUN in the Solar System (EARTH is always XX3, MARS XX4, JUPITER XX5, etc). The SUN is always XX0 and the MOON (owing to the fact that PLUTO is not present as a plantary body) is assigned XX9.

All gravitational constant values are stored in registers -90X with X being the main body variable outlined above. All radius are stored in registers -91X. And all distances are stored in registers -92X. Note that the distance value for the MOON is from the EARTH and not from the SUN.

![Values for indirect registers.](assets/constants.png)

You can find more information how how to use indirect registers and storing these values in the [DM32 User Manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#indirect_only).

### Second Sample Problem

Using the number of sidereal days in a solar year, we wish to know how fast the EARTH rotates the SUN in a perfectly circular orbit and what the circumference of that orbit would be in kilometers. There are 366.2422 sidereal days in a solar year.

Same as in our last problem we have a single variable and wish to know other unknown variables in the orbit equation. For our known variable we have the number of sidereal days, and so we will initiate our orbital calculations by using the **LBL D** routine. We are also going to need to have the G and R values for the SUN because we are calculating the orbit of the EARTH around that main body. For this we are going to use our indirect variables, so be sure to run XEQ A before starting this problem on the calculator.

![Input 366.2422 in the x-register and run the XEQ D program to commence the calculation.](assets/ExampleA.png)

We are prompted for the value of G and for this will we need to use our indirect register. Recall that all gravitational values are stored in -90X and main bodies are varied based on their position relative to the SUN. So the indirect variable for the G value of the SUN is -900 which we input in the x-register (do not worry about the input field) and then press STO i. Now we can call-up the value in this register by pressing RCL (i) and the value is taken up in the x-register and input field. Press R/S to input the value and carry on.

![Inputting the indirect register value and RCL the information for G.](assets/ExampleB.png)

Next, we are prompted for the radius. And same as for the G value we will use the indirect register. Recall that all radius values are stored in registers -91X and since we are calculating with the SUN as the main body, we need to call information from the -910 register. So we follow the steps as above only using -910 and we have the value in the x-register. Pressing R/S inputs the value and the program continues to run.

![Inputting indiret register value and RCL information for R.](assets/ExampleC.png)

Again the four-line display shows us the relevant information. 

![First display with VIEW.](assets/ExampleD.png)

We can see in the VIEW display that the value we inputted for the sidereal days is the same. We close this by pressing R/S and now we have the orbital period in minutes displaying in the x-register.

![The final results of our calcualtion.](assets/ExampleE.png)

We can see that the velocity of EARTH travalling around the SUN is 29,784.708 m/s and the circumference of this orbit is 939,950,152.948. We can actually already see that our calculation is a little off from the real life values because the height of the orbit is less than the official value of one astronomical unit (AU) which is the distance of the EARTH from the SUN (what should be the exact value of this height). But that is okay because we know what is happening here, and it is owning to the fact we are calculating based on a perfectly circular orbit. The difference between the actual value and what our calcaultion produced is 0.466%, so negliable for the purposes of understanding orbital mechanics.

The EARTH has an average velocity around the SUN of 29,784.8 m/s which is very near our calculation. This is owning to the low eccentricity of EARTH's real orbit around the SUN which makes cirular orbit calculations especially for speed and distances much more accurate to real world.

## Recalculation Feature

With the G and R values for the SUN already stored, we can run any other *Initiator Program* again with any other single variable and simple click R/S to use the same values again. No need to recall i or any registers again. Additionally, the EARTH and MOON values will still be available in the y-register and z-register as before.

## Variables and Labels Used

The following variables are used by this Statefile:

> - Variable C / Circumference
> - Variable D / Sidereal day
> - Variable G / Gravitational parameter of main body
> - Variable H / Orbit height
> - Variable P / Orbit period
> - Variable R / Radius of main body
> - Variable V / Orbit velocity
> - Variable i / *If indirect register RCL is used*

The following labels are used by this Statefile:

> - *Label O / Display sub-routine*
> - *Label Z / Constant sub-routine*
> - **Label H / Height initiator program**
> - **Label V / Velocity initiator program**
> - **Label P / Period initiator program**
> - **Label D / Sidereal day initiator program**
> - **Label C / Circumference initiator program**
> - Label A / Solar System constants routine

## Dedication

This humble Statefile and the tremendous (and often tedious) work that went into making it possible is dedicated to the vision and efforts of the thousands of unnamed individuals who contributed to the GEMINI and APOLLO programs culminating in landing man on the moon in the 20th century. Much of what we nerd out on and enjoy today by way of technology can be traced to their work and effort to put a man on the moon and we remain forever in their debt.

### By jacober-calc for SwissMicros DM32

> - [SwissMicros Website](https://www.swissmicros.com)
> - [DM32 product page](https://www.swissmicros.com/product/model-dm32)
> - [SwissMicros full products page](https://www.swissmicros.com/products)
> - [DM32 Online User Manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html)
> - [SwissMicros Calculator Forum](https://forum.swissmicros.com/index.php)