This program is written in Python flask ( http://flask.pocoo.org/ )

Unit tests are located in:
unitTest.py

Meat of the code is in:
app/__init__.py

To run the unit tests:
python unitTest.py

To run the program:
python app/__init__.py

NOTES:
1. The first line in the requirements file is misleading.
According to internet standards GET requests cannot contain a payload, so it is impossible for a get request to accept JSON.

I have used query parameters for the GET request in the application, but a POST request that contained the supplied data could do so with a JSON format.


2. Its a bit odd that the footnote list in the params goes 1, 3, 2. It would be more clear if that was reorded to 1, 2, 3.

3. The 3rd character on line 24 should probably be a - not a . e.g.: 10-14.99 not 10.14.

4. According to http://www.wikihow.com/Calculate-Mortgage-Payments the interest rate to include in the formula is the interest rate divided by the payment frequency (e.g. monthly interest rate for monthly payments), which brings the calculation in line with other online mortgage calculators. This might be something you wish to add in the requirements file.

5. The return value of the rate route specified monthy payments, but other online calculators return the payment rate you submit. I followed the convention used by the online calculators.
