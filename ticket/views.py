from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import Ticket_Request
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.models import User
from .forms import PasswordChangeForm
from  django.contrib.auth.hashers import check_password
from .forms import EditForm
# Check if there is already a ticket cache table in the session.
cache.add('rem_tickets', 10)

if(cache.get("rem_tickets") == None or cache.get("rem_tickets") < 0):
    cache.set("rem_tickets", 10)

#set values for max extra ticket and max base ticket number
extra_tickets = 2
base_tickets = 10
value = '''Congratulations, you did it!
                All the hard work and long hours have paid off. You only have one last thing to do, so take a deep breath, relax and get ready to make a memory that will last a lifetime.

                Texas Wesleyan cordially invites you and your guests to share this memorable moment. Let's Rams up! It’s time to walk the stage and graduate.'''

#declare a variable for error messages
message = 'Invalid Credentials'
msg = "Student ID Not in Database or Typed Incorrectly"
#Default Route
def index(request):
    #Check if the user has logged in, if not redirect else take to home
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
#redirect to homepage
    return render(request, 'tickets/home.html', {"available": cache.get("rem_tickets")})


#add route, add tickets
def add(request):
#Check if user is logged in if not redirtect to login route
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login") )
#Check if the user has submitted a form
    if (request.method == "POST"):
#Put form Values into the model and set the database
        users = Ticket_Request(first_name = request.POST["first"], last_name = request.POST["last"], studentID = request.POST["sid"], tickets_ordered = request.POST["base_number"])
        user = User.objects.get(username = request.user.username)
        nid = user.student.sid
        if(int(nid) == int(request.POST['sid'])):
    #Check if the data gotten from the form already exists, by checking for th uniquer value of Student ID
            if Ticket_Request.objects.filter(studentID = request.POST['sid']):
    #Return the User info they submitted and redirect them to the make a new submittion and delete thier old one
                info = Ticket_Request.objects.get(studentID = request.POST["sid"])
                return render(request, 'tickets/registrants.html', {'info': info,
                                                                    "available": cache.get("rem_tickets")})
    #If it doesnt exist, check if the value they submitted exceed the available tickets, if it does submit an error message
            #elif(int(request.POST["extra_number"]) > cache.get("rem_tickets")):
                #return render(request, "tickets/ticket_form.html", {
                    #"message": "Number of Extra Tickets Ordered exceed the Number of Tickets Available, Adjust the Amount Ordered",
                    #"available": cache.get("rem_tickets")
                #})
    #If all those arent the case, save the users information into the database
            users.save()
    #Check if the user requested all of their base tickets, if not add it to extra tickets and subtract whatever extra ticket they asked from the number available
            if(int(request.POST["base_number"]) < base_tickets):
                free = cache.get("rem_tickets")  + (base_tickets - int(request.POST["base_number"]))
                #free = (free - int(request.POST["extra_number"]))
                cache.set("rem_tickets", free)
            #else:
                #cache.set("rem_tickets", (cache.get("rem_tickets") - int(request.POST["extra_number"])))
    #Redirect to a success page
            return render(request, 'tickets/confirm.html', {"available": cache.get("rem_tickets")})
        return render(request, 'tickets/ticket_form.html', {
            "base_tickets": range(1, base_tickets + 1),
           "extra_tickets": range(1, extra_tickets + 1),
            "base": base_tickets,
            "available": cache.get("rem_tickets"),
            "message": "Incorrect Txwes Student ID"
        })
    #Redirect to ticket form page if the request isnt POST
    return render(request, 'tickets/ticket_form.html', {
            "base_tickets": range(1, base_tickets + 1),
           "extra_tickets": range(1, extra_tickets + 1),
            "base": base_tickets,
            "available": cache.get("rem_tickets")
        })

#Logout route, logs the user out using the logout function, prints success message
def logt(request):
    logout(request)
    return render(request, 'tickets/login.html', {"check": "You have logged out succesfully!"
                                                  })
#Edit Form Route
def editForm(request):
#Redirects user to registration page to delete old data
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login") )
    return render(request, 'tickets/registrants.html')

#Login Route
def logn(request):
#Check if the user submitted a form
    if request.method == 'POST':
#check user details against the database using the authenticate function
        user = authenticate(request, username = request.POST["username"], password = request.POST["password"])
#If user is valid, redirect them to the default route for confirmation
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
#If user does not exist print out error message
        else:
            return render(request, 'tickets/login.html',
                          {"message": message})
#If user hasnt submitted a form renders the login page
    return render(request, 'tickets/login.html')

#New Form Route
def newForm(request):
#Check if users unique id exists in the database
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login") )
    try:
#Saves users information
        user = Ticket_Request.objects.get(studentID = request.POST["id"])
#Check if any of the users base tickets were added to extra tickets
        if(int(user.tickets_ordered) < base_tickets and int(user.tickets_ordered) != 0):
#Subtract added values from available tickets and add subtracted values
            new = cache.get("rem_tickets")  - (base_tickets - int(user.tickets_ordered))
            new = (new + int(user.extra_tickets))
#Save new value to table
            cache.set("rem_tickets", new)
#If no base tickets were added, just subtract formerly ordered extra tickets if any
        else:
#save new value
            cache.set("rem_tickets", (cache.get("rem_tickets") + int(user.extra_tickets)))
#Delete user information from the database
        user.delete()
#redirect user to add route
        return HttpResponseRedirect(reverse(add))
#If unique user id doesnt exist print an error message
    except Exception:
        return render(request, 'tickets/registrants.html', {'message': msg,
                                                            "available": cache.get("rem_tickets")})
def extraTicket(request):
#Check if user is logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login") )
#check if form was submitted
    if(request.method == "POST"):
#check if there are enough tickets to fulfill the order
        if (cache.get("rem_tickets") > 0 and int(request.POST["extra"]) <= cache.get("rem_tickets")):
#Check if user ID exists
                if(Ticket_Request.objects.filter(studentID = request.POST["id"])):
#get the user
                    user = Ticket_Request.objects.get(studentID = request.POST["id"])
#check if the user has ordered before
                    if(user.extra_tickets == 0):
#set users extra tickets to the number ordered
                       user.extra_tickets = int(request.POST["extra"])
#save user
                       user.save()
#Subtract added values from available tickets
                       new = cache.get("rem_tickets")  - int(user.extra_tickets)
#Save new value to cache
                       cache.set("rem_tickets", new)
#render a success page
                       return render(request, 'tickets/confirm.html')
#if they have ordered before, display their information
                    info = Ticket_Request.objects.get(studentID = request.POST["id"])
                    return render(request, 'tickets/registrants.html', {'info': info})
#If the user hasnt ordered anything before and isnt in the database create data and add information
                user = User.objects.get(username = request.user.username)
#Gets the saved id of the user and checks if they typed it correctly
                nid = user.student.sid

                if(int(nid) == int(request.POST['id'])):
                    user = Ticket_Request(extra_tickets = request.POST["extra"], studentID = request.POST["id"], first_name = request.user.first_name, last_name = request.user.last_name)
                    user.save();
#Subtract added values from available tickets
                    new = cache.get("rem_tickets")  - int(user.extra_tickets)
#Save new value to table
                    cache.set("rem_tickets", new)
#render a success page
                    return render(request, 'tickets/confirm.html')
#renders error message for incorrect student id
                return render(request, 'tickets/extra_tickets.html', {'message': "Enter a Valid Student ID",
                                                                "extra_tickets": range(1, extra_tickets + 1),
                                                                  "available": cache.get("rem_tickets")})
#renders error message for not enough tickets for order
        return render(request, 'tickets/extra_tickets.html', {'message': "Not Enough Extra Tickets To Complete Your Order",
                                                                "extra_tickets": range(1, extra_tickets + 1),
                                                                    "available": cache.get("rem_tickets")})
#if first loading page, render template
    return render(request, 'tickets/extra_tickets.html', {"extra_tickets": range(1, extra_tickets + 1),
                                                            "available": cache.get("rem_tickets"),
                                                            'message': ""})

def new_password(request):
#Check if user is logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
#Check if form was submitted
    if request.method == 'POST':
#get the values of the submitted form
        form = PasswordChangeForm(request.POST)
#Check if values were entered corrctly
        if form.is_valid():
#saves the old password into a variable
            old_password = form.cleaned_data['old_password']
#saves the new passwortd into a variable
            new_password = form.cleaned_data['new_password']
#save the second entry of the new password into a variable
            re_password = form.cleaned_data['re_password']
#get the current user
            user = User.objects.get(username = request.user.username)
#check if the old_password entered was correct
            if check_password(old_password, user.password):
#check if new password and reentered password are the same
                if new_password == re_password:
#set users password to the new password
                    user.set_password(new_password)
#save the user
                    user.save()
#render a success message
                    return render(request, "tickets/password_message.html", {'message':"Password Reset Succesful"})
                else:
#renders are unmatching passwords error message
                    return render(request, 'tickets/new_password.html', {'forms': form,
                                                                            'message':"New Password Fields Not Matching"})
#renders an incorrect correct password error message
            return render(request, 'tickets/new_password.html', {'forms': form,
                                                                    'message':"Incorrect Current Password"})
    else:
#if method is get creates a new form
        form = PasswordChangeForm()
        return render(request, 'tickets/new_password.html', {'forms': form})

def edit(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            global value
            value = form.cleaned_data['Value']
        return HttpResponseRedirect(reverse("index"))
    else:
        form = PasswordChangeForm()
        return render(request, 'tickets/home.html', {'forms': form})
