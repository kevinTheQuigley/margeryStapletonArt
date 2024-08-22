from flask import Flask,render_template, request
import requests
import smtplib
from arsewards import arsewards_dict


app = Flask(__name__)

@app.route("/")
def home():
    photoData = requests.get("https://api.npoint.io/af83026d4e0579fc5161").json()
    print(photoData)
    return(render_template("index.html",blog = photoData))

@app.route("/about/")
def about():
    return(render_template("about.html"))

@app.route("/gallery/")
def gallery():
    photoData = requests.get("https://api.npoint.io/af83026d4e0579fc5161").json()
    return(render_template("gallery.html",blog = photoData))

@app.route("/contact/",methods =["GET"])
def contact():
    return(render_template("contact.html"))

@app.route("/contact",methods =["POST"])
def recieve_data():
    error = None
    if request.method == 'POST':
        if (request.form['name']) and (request.form['phone']):
            data = request.form
            send_email(data["name"], data["email"], data["phone"], data["text"])
            return(render_template("contact.html",result = "1" ,message = "Thank you for your message."))
            return "<h1> Username:" + request.form['name'] + "Password: "+request.form['phone'] +"</h1>"
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user = "KevinsFancyTester12@gmail.com",password =  arsewards_dict["KevinsFancyGmAppPassword"])
        connection.sendmail("KevinsFancyTester12@gmail.com", arsewards_dict["kevinsHiddenEmail"], email_message)
        connection.close()

@app.route("/blogPost/<int:id>")
def returnBlogpost(id):
    photoData = requests.get("https://api.npoint.io/af83026d4e0579fc5161").json()
    return(render_template("post.html",blog = photoData[int(id)-1]))

@app.route("/gallery/<int:id>")
def returnPhoto(id):
    photoData = requests.get("https://api.npoint.io/af83026d4e0579fc5161").json()
    return(render_template("post.html",blog = photoData[int(id)-1]))


while __name__ =="__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    blogData = requests.get("https://api.npoint.io/16c047af2b016b24c4fa")
    app.run(debug=True)


#<a href="{{url_for('about')}}">Read</a>
#          <a href="{{url_for('get_blog', id =blogPost['id'])}}">Read</a>
