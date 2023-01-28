# Nidec Music

Raspberry Pi Pico MicroPython code to use the the Nidec Dynamo brushless motor to play music using its integrated GreenDrive motor controller.

If using the wiring harness that comes with the motor as sold on [AndyMark](https://www.andymark.com/products/dynamo-brushless-motor-controller), the blue wire (pin 7, PWM & Direction) should be connected to pin 19 on the Pico, while the white wire (pin 8, Enable) should be connected to pin 17 on the Pico. This should fit nicely with the black wire connected to ground and the red wire hanging off of the side of the board.