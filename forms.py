from flask.ext.wtf import Form, TextField, IntegerField, BooleanField, TextAreaField, SubmitField, validators, ValidationError

class ContactForm(Form):
	#Personal contact info
	name = TextField("Name", [validators.Required("Please enter your name.")])
	email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter a valid email address.")])
	phone = TextField("Phone", [validators.Required("Please enter your phone number."),])

	#Men's names
	mname1 = TextField("Name 1")
	mg1 = BooleanField()
	mname2 = TextField("Name 2")
	mg2 = BooleanField()
	mname3 = TextField("Name 3")
	mg3 = BooleanField()
	mname4 = TextField("Name 4")
	mg4 = BooleanField()
	mname5 = TextField("Name 5")
	mg5 = BooleanField()

	#Women's names
	wname1 = TextField("Name 1")
	wg1 = BooleanField()
	wname2 = TextField("Name 2")
	wg2 = BooleanField()
	wname3 = TextField("Name 3")
	wg3 = BooleanField()
	wname4 = TextField("Name 4")
	wg4 = BooleanField()
	wname5 = TextField("Name 5")
	wg5 = BooleanField()

	same_seats = BooleanField("Check the box if you would like the same seats as the previous year")
	guest_number = IntegerField("Number of guest seats to be purchased", [validators.NumberRange(min=0, max=50, message="Please enter the number of guest seats needed (either 0 or more).")])
	comments = TextAreaField("Comments",)
	submit = SubmitField("Submit Form")