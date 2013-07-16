from flask import Flask, render_template, request, flash, session
from forms import ContactForm
from flask.ext.mail import Message, Mail
import stripe

stripe_keys = {
	'secret_key' : '',
	'publishable_key' : ''
}

stripe.api_key = stripe_keys['secret_key']

mail = Mail()

app = Flask(__name__)

app.secret_key = ""

app.config["MAIL_SERVER"] = "smtp.mailgun.org"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = ""
app.config["MAIL_PASSWORD"] = ""

mail.init_app(app)



@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
	form = ContactForm()

	if request.method == 'POST':
		if form.validate() == False:
			flash("All fields are required.")
			return render_template('contact.html', form=form)
		else:
			gdict = { True : "(Guest)", False : "" }
			ticket_count = (form.mg1.data + form.mg2.data + form.mg3.data
			 + form.mg4.data + form.mg5.data + form.wg1.data + form.wg2.data
			  + form.wg3.data + form.wg4.data + form.wg5.data)

			memdict = {'yesod' : 0, 'chai' : 0, 'chesed' : 5000, 'member' : 10000, 'assoc' : 10000, 'non-member' : 12000}
			seat_number = 0
			if form.membership.data == 'assoc':
				seat_number = ticket_count + 1
			elif form.membership.data == 'non-member':
				seat_number = ticket_count + 1
			else:
				seat_number = ticket_count
			bill = memdict[form.membership.data] * seat_number

			#dollar value of bill
			bill_in_dollars = bill / 100.00



			session['email'] = form.email.data
			session['bill'] = bill
			session['bill_in_dollars'] = bill_in_dollars

			session['msg'] = """
				\nFrom: %s <%s>
				\nPhone #: %s
				\nMen's Section:
				\n 1) %s %s\n 2) %s %s\n 3) %s %s\n 4) %s %s\n 5) %s %s\n
				\nWomen's Section: 
				\n 1) %s %s\n 2) %s %s\n 3) %s %s\n 4) %s %s\n 5) %s %s\n
				\nSame Seats? %s
				\nComments: %s
				\nGuest count: %d
				\nMembership: %s
				\nPayment: $%d
				""" % (form.name.data, form.email.data, form.phone.data, form.mname1.data, 
				gdict[form.mg1.data], form.mname2.data, gdict[form.mg2.data], 
				form.mname3.data, gdict[form.mg3.data], form.mname4.data, 
				gdict[form.mg4.data], form.mname5.data, gdict[form.mg5.data], 
				form.wname1.data, gdict[form.wg1.data], form.wname2.data, 
				gdict[form.wg2.data], form.wname3.data, gdict[form.wg3.data],
				form.wname4.data, gdict[form.wg4.data], form.wname5.data, 
				gdict[form.wg5.data], form.same_seats.data, 
				form.comments.data, ticket_count, form.membership.data, bill_in_dollars)


			if bill == 0:
				msg = Message("High Holy Days Seating Preferences", 
					sender='', recipients=[''])
				msg.body = session['msg']
				mail.send(msg)
				return render_template('contact.html', success=True)
			else:
				return render_template('checkout.html', key=stripe_keys['publishable_key'], amount=bill)


	elif request.method == 'GET':
		return render_template('contact.html', form=form)

@app.route('/checkout')
def checkout():
	return render_template('checkout.html', key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
	#amount in cents
	amount = session['bill']

	customer = stripe.Customer.create(
		email=session['email'],
		card=request.form['stripeToken']
	)

	charge = stripe.Charge.create(
		customer=customer.id,
		amount=amount,
		currency='usd',
		description='Flask Charge'
	)

	msg = Message("High Holy Days Seating Preferences", 
					sender='', recipients=[''])
	msg.body = session['msg']
	mail.send(msg)
	receipt = Message("Thank you for reserving your seats!", 
		sender='postmaster@app16794441.mailgun.org', recipients=[session['email']])
	receipt.body = """
	We've received for your payment of $%d for your High Holiday seats at Shaare Torah.
		""" % (session['bill_in_dollars'])
	mail.send(receipt)

	return render_template('charge.html', amount=amount)

if __name__ == '__main__':
	app.run()