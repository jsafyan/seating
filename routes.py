from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask.ext.mail import Message, Mail

mail = Mail()

app = Flask(__name__)

app.secret_key = 

app.config["MAIL_SERVER"] = "smtp.mailgun.org"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 
app.config["MAIL_PASSWORD"] = 

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
			msg = Message("Seating Preferences", sender='postmaster@app.mailgun.org', recipients=[''])
			gdict = { True : "(Guest)", False : "" }
			msg.body = """
			\nFrom: %s <%s>
			\nPhone #: %s
			\nMen's Section:
			\n 1) %s %s\n 2) %s %s\n 3) %s %s\n 4) %s %s\n 5) %s %s\n
			\nWomen's Section: 
			\n 1) %s %s\n 2) %s %s\n 3) %s %s\n 4) %s %s\n 5) %s %s\n
			\nNumber of guest seats needed: %d
			\nComments: %s
			""" % (form.name.data, form.email.data, form.phone.data, form.mname1.data, 
				gdict[form.mg1.data], form.mname2.data, gdict[form.mg2.data], 
				form.mname3.data, gdict[form.mg3.data], form.mname4.data, 
				gdict[form.mg4.data], form.mname5.data, gdict[form.mg5.data], 
				form.wname1.data, gdict[form.wg1.data], form.wname2.data, 
				gdict[form.wg2.data], form.wname3.data, gdict[form.wg3.data],
				form.wname4.data, gdict[form.wg4.data], form.wname5.data, 
				gdict[form.wg5.data], form.guest_number.data, form.comments.data)
			mail.send(msg)

			return render_template('contact.html', success=True)

	elif request.method == 'GET':
		return render_template('contact.html', form=form)

if __name__ == '__main__':
	app.run()