import setuptools

setuptools.setup(
    name = "py4math",
    author = "Harsh Gupta",
    version='0.0.3',
    author_email = "harshnkgupta@gmail.com",
    description = "A Perfect Math Module For Beginners. ",
    long_description="This module is extensively designed for non-math coders and beginners. The user need not know math to solve complex math problems. This module does it all for you.The most special feature of this module is its search() function. Now Just search your query after importing the module and it would be resolved. This module consists over 50+ math formulas and is still developing.\n\n Syntax: \n\n >>>import py4math \n\n >>>py4math.search(<Type your problem here>) \n\n Example: >>>py4math.search(\'area of triangle\') \n\n Example: >>>py4math.search(\'convert binary to hexadecimal\') \n\n Example: >>>py4math.search(\'is 3557 a prime number\') \n\n\nType >>>py4math.help() for further help.",
    packages=['py4math'],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
 ],
    )
