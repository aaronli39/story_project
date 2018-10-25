#Team SKAR - Sophia Xia, Kevin Lin, Aaron Li, Ricky Lin

from util import auth, story
from flask import Flask, request, render_template, session, url_for, redirect, flash
import os

app = Flask(__name__) #Create instance of class Flask

app.secret_key = os.urandom(32)

@app.route("/") #Assign fxn to route
def index():
    #if the user is logged in redirect them to their profile page
    if 'user' in session:
        return redirect('/profile')
    #if not, load the login page
    return render_template("index.html")


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/auth",methods = ['POST'])
def authenticate():
    loginStatus = ''
    #if the user got here without entering a form, redirect them to the index
    if not('user' in request.form.keys()):
        redirect('/')
    #checks the user's login info
    if "pass2" in request.form.keys():
        loginStatus =  auth.createAcc(request.form['user'],request.form['pass1'],request.form['pass2'])
    else: loginStatus = auth.checkInfo(request.form["user"],request.form["pass"])
    #if the user successsfully logs in or creates an acount, redirect them to their profile page
    if loginStatus in ["Account creation successful","Login Successful"]:
        session['user'] = request.form['user']
        return redirect('/profile')
    else:
        flash(loginStatus)
        #Redirects to previous page or root if there is none
        return redirect(request.referrer or '/')


@app.route('/profile')
def profile():
    #if the user isn't logged in, redirect them to the login page
    if not('user' in session):
        return redirect('/')
    #otherwise, load the user's profile page
    storiesList = story.getStories(session['user'])
    if len(storiesList) == 0:
        storiesList = ['You have not contributed to any stories!']
    return render_template('profile.html',user = session['user'], stories = storiesList)

@app.route('/logout')
def logout():
    #if the user is logged in, log them out and redirect to the login page
    if 'user' in session:
        session.pop('user')
        flash('Sucessfully Logged Out')
    return redirect('/')

@app.route('/discover')
def discover():
    def getA(storyname):
        return story.getAuthor(storyname)
    def getSA(storyname, content):
        return story.getSpecificAuthor(storyname, content)
    if not('user' in session):
        return redirect('/')
    storiesList = story.getDiscoverDict(session['user'])
    if len(storiesList) == 0:
        storiesList = ['WOW you\'ve contributed to all stories available!']
    return render_template('discover.html', keys = storiesList.keys(), dct = storiesList, ga = getA, gsa = getSA)

@app.route('/edit')
def edit():
    storyname = ''
    try:
        storyname = request.args['story']
    except:
        return redirect("/discover")
    if 'user' in session:
        if not storyname in story.getStories(session['user']):
            storycontent = story.getLast(storyname)[0]
        else: return redirect('/profile')
    else:
        return redirect('/')
    return render_template('edit.html', story_title = storyname, story = storycontent, contributor = story.getAuthor(storyname))

@app.route('/editchanges', methods = ["POST","GET"])
def editChanges():
    if not('story' in request.args): return redirect('/')
    if not('user' in session):
        return redirect('/')
    storyname = request.args['story']
    storycontent = request.form['story_content']
    story.editStory(storyname, session['user'], storycontent)
    return redirect("/profile")

@app.route("/contribute", methods = ["POST", "GET"])
def contribute():
    if not('user' in session):
        return redirect('/')
    method = request.method
    if method == "POST":
        return redirect("/profile")
    else:
        return render_template("contribute.html")

@app.route("/contributechanges", methods = ["POST", "GET"])
def contributechanges():
    if not('user' in session) or not('story_title' in request.form):
        return redirect('/')
    storyname = request.form['story_title']
    story_content = request.form['story_content']
    story.createStory(storyname, session['user'], story_content)
    return redirect("/profile")

@app.route("/forbidden")
def forbidden():
    return "Forbidden"

@app.route('/view')
def view():
    def getSA(storyname, content):
        return story.getSpecificAuthor(storyname, content)
    storyname = ''
    try:
        storyname = request.args['story']
    except:
        return redirect("/profile")
    storycontent = ''
    if 'user' in session:
        if storyname in story.getStories(session['user']):
            storycontent = story.getFull(storyname)
    else:
        storycontent = story.getLast(storyname)
    return render_template('view.html', story = storyname, content = storycontent, gsa = getSA)

if __name__ == "__main__":
    app.debug = True
    app.run()
