# templates

from flask import Flask, request, url_for, render_template, redirect
app = Flask(__name__)

@app.route("/contact") # 이메일 보내는 폼이 보이는 기능 구현
def contact():
	return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"], endpoint="contact_complete")
def contact_complete():
	if request.method == "POST":

		return redirect(url_for("contact_complete"))

	return render_template("contact_complete.html")

if __name__ == "__main__":
	app.run(debug=True)