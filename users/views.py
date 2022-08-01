from django.shortcuts import render
from .models import Profile, Skill, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def showsth(request): #Test
    context= {'tempvar': "Them say make I show something..."}
    return render(request, 'users/profiles.html', context)

from .utilities import searchProfiles, paginateProfiles
def allprofiles(request):
    #29/12/21  20:349 ============================
    some_profilevar, somevar_search_query = searchProfiles(request)

    #feb 13 2022 -- 22:14
    var_custom_range, some_profilevar = paginateProfiles(request, some_profilevar, 1 )  #step2, pass custom_range to context
    
    context = {'tempvar': some_profilevar, 'tempvar_search_query':somevar_search_query,     'tempvar_custom_range': var_custom_range   } 
    return render(request, 'users/profiles.html', context)   #

#step 2: our user profiles function to be followed by step3. urls
def userprofile(request, pk):
    some_user_instance = Profile.objects.get(id =pk)

    defined_skill = some_user_instance.skill_set.exclude(description__exact = "")#we already know, skill is a child to profile, hence the _set being added.
    #the above line reads in defined skill variable, store, the skills of our some user instance, excludn those with empty description field
    other_skill = some_user_instance.skill_set.filter(description = "")
    #dis line reads, in our otherskill variable, store the skills of user instance that have an empty description field.



    context = {'tempvar' : some_user_instance, 'temp_defskill': defined_skill, 'temp_otherskill':other_skill}
    return render(request, 'users/user-profile.html', context)

#19 November 2021 -- Authentication chapter 7 == 17:14
#----------------------------------------------------------
# from our our login_register template STEP 3...here to give it a function for rendering and later assign a url focus is now on login
 
#STEP 2: IMPORT REDIRECT FROM DJANGO.SHORTCUTS, 
from django.shortcuts import redirect

#STEP 3: FROM DJANGO.CONTRIB.AUTH IMPORT LOGIN, AUTHENTICATE...to be explained later on
from django.contrib.auth import login, authenticate #this login is the reserved fxn dennis referred to earlier

def loginfxn(request):      #dennis says be sure not to name your function for login just "Login/Logout"...as these are reserved words in django
    var_pagetype = 'login'
    if request.user.is_authenticated:   #could be done with decorators
        return redirect('profiles_link')

    if request.method == 'POST':
        #BUILDING THE LOGIN PAGE
        #STEP 1: CREATE VARIABLES TO HOLD USERNAME & PASSWORDS
        var_username = request.POST['username']
        var_password  = request.POST['password']

#STEP 4:using the try block...we will test if username exist in database, if it does, we store the info of said user
        try:
            somevar_user = User.objects.get(username = var_username) #REQUIRES WE IMPORT USER MODEL cNTRL + V FROM MODELS.PY
        except:     #IF USER DOES NOT EXIST...DO THAT AND JUMP TO END OF FXN ...WILL LATER CHANGE PRINT FXN TO DJANGO REQUIRED MSGS
            #before django.contrib.messages....print('Username does not exist...')
            messages.error(request,'Username does not exist...')
        
        #NOW WE SEE WHAT THE AUTH FXN DOES, COMPARES USER NAME AND PASSWORD TO THAT OF ALL OF OUR USER INSTANCES IN DB AND STORES IT IN VARIABLE
        somevar_user = authenticate(request, username = var_username, password = var_password)

        #NOW IF OUR authenticate FXN IS SUCESSFUL, WE GO DOWN HERE, WHERE THE DJANGO LOGIN FXN CREATES A SESSION FOR THE USER, WHICH IS A XTIC'S OF LOGINS
        if somevar_user is not None:  #i.e if user exists in database...
            login(request, somevar_user)
            #folder 10 - reviews edit- return redirect('profiles_link'== didnt work to comment out proposed change and reinstate old)
            return redirect(request.GET['next'] if 'next' in request.GET else 'useraccount')
        else:
            #before django.contrib.messages....print ('Username or Password is incorrect...')
            messages.error(request, 'Username does not exist...')


    return render(request, 'users/login_register.html') #STEP 4 : NOW GET A URL

#now we deal with our logout shit
from django.contrib.auth import logout

def logoutfxn(request):
    logout(request)
    #messages.error(request, "Logged out successfully...") #messages.error neeeds to be messages.info; for colouring purposes 22/12/21 16:52
    messages.info(request, "Logged out successfully...")
    return redirect('loginlink')    #redirect us to the login page.


#Registering users vid 002 of chapter 7
#from django.contrib.auth.forms import UserCreationForm
from .forms import myCustomizedUserCreationForm, myMessageForm

def registerfxn(request):
    var_pagetype  = 'register'
    #var_form = UserCreationForm()
    var_form = myCustomizedUserCreationForm()
    
    if request.method == 'POST':
        #var_form = UserCreationForm(request.POST)
        var_form = myCustomizedUserCreationForm(request.POST)
        if var_form.is_valid():   
           somevar_user = var_form.save(commit = False)
           somevar_user.username = somevar_user.username.lower()
           somevar_user.save()

           messages.success(request,"User account created successfully.")
           login(request, somevar_user) #login user instance right after signup
           
           # 26/12/21 23:19 - redirecting new users to edit profile page rather than profiles page
           #return redirect('profiles_link') #new user should see the profiles page 1st
           return redirect('edit_acct') #new user should see the profiles page 1st
      
    else: messages.error(request, "Error occured during registration")
    context = { 'tempvar_pagetype' : var_pagetype, 'tempvar_form': var_form }
    return render(request, 'users/login_register.html', context)


@login_required(login_url='loginlink') #this ensures dt, if user isnt logged in, we redirect them to login page
def userAccountfxn(request):
    somevar_profile = request.user.profile

    somevar_skills = somevar_profile.skill_set.all()
    somevar_projects = somevar_profile.project_set.all()
    
    context= {'tempvar_profile':somevar_profile, 'tempvar_skill':somevar_skills, 'tempvar_project':somevar_projects}
    return render(request, 'users/account.html', context)


from .forms import  myProfileForm
@login_required(login_url= 'loginlink')
def editAccountfxn(request):
    somevar_profile = request.user.profile #26/12/21 9:57pm
    somevar_form = myProfileForm( instance = somevar_profile) #the instance prefills the form to hold existing data of logged in user

    if request.method == 'POST': ##26/12/21 9:55pm
        somevar_form = myProfileForm(request.POST, request.FILES, instance=somevar_profile)
        if somevar_form.is_valid():
            somevar_form.save()

            return redirect('useraccount')

    context = {'tempvar_form':somevar_form}
    return render(request, 'users/edit_profile_form.html',context)


#######################################################################################
from .forms import mySkillForm
@login_required(login_url = 'loginlink')
def createSkill(request):
    somevar_profile =  request.user.profile #after all skill need to belong to profiles
    somevar_form = mySkillForm()

    if request.method == 'POST':
        somevar_form = mySkillForm(request.POST )
        if somevar_form.is_valid:
            somevar_skill = somevar_form.save(commit = False)
            somevar_skill.owner = somevar_profile
            somevar_skill.save()
            messages.success(request,"Skill was added successfully.")            
            return redirect('useraccount') 
    context = {'tempvar_form': somevar_form}
    return render(request, 'users/skill_form.html', context)

#from .forms import mySkillForm #need not repeat
@login_required(login_url = 'loginlink')
def updateSkill(request, pk):
    somevar_profile =  request.user.profile #after all skill need to belong to profiles
    var_skill = somevar_profile.skill_set.get(id= pk)
    somevar_form = mySkillForm(instance = var_skill)

    if request.method == 'POST':
        somevar_form = mySkillForm(request.POST, instance = var_skill )
        if somevar_form.is_valid:
            #somevar_skill = somevar_form.save(commit = False)
            #somevar_skill.owner = somevar_profile
            somevar_form.save()
            messages.success(request,"Skill was updated successfully.")

            return redirect('useraccount') 
    context = {'tempvar_form': somevar_form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url = 'loginlink')
def deleteSkill(request, pk):
    somevar_profile =  request.user.profile #after all skill need to belong to profiles
    var_skill = somevar_profile.skill_set.get(id= pk)

    if request.method == 'POST':
        var_skill.delete()
        messages.success(request, 'Skill was deleted successfully')
        return redirect('useraccount')
    
    context = {'object': var_skill} #ideally should hv been tempvar_object but...
    return render(request, 'delete_obj.html', context)

#we pass it a login decorator so logged in users only can access it
@login_required(login_url = 'loginlink')
def inbox(request):
    var_profile = request.user.profile      #get and store logged in user
    messageRequests = var_profile.messages.all() #get messages of logged in user
    unreadCount = messageRequests.filter(is_read = False).count #filter user's message and count the unread ones.
    context = {'temp_messageRequests' : messageRequests, 'temp_unreadCount' : unreadCount }
    return render(request, 'users/inbox.html', context)


@login_required(login_url = 'loginlink')
def viewMessage(request, pk):
    var_profile = request.user.profile
    var_message = var_profile.messages.get(id = pk)      #NB: get message of logged in user with id set 2 pk. 

    if var_message.is_read == False:
        var_message.is_read = True      #upon getting the message, we exchange the is_read attribute to True as in read.
        var_message.save()
    
    context = {'tempvar_msg':var_message }
    return render(request, 'users/message.html', context)

#we dont have to login to create a message so we leave out the login decorator.
def createMessage(request, pk):
    var_recepient = Profile.objects.get(id = pk)  #we create a variable to get the instance of the profile we intend 2 text
    var_form = myMessageForm()

    try:
        var_sender = request.user.profile
    except:
        var_sender = None
    if request.method == 'POST':
        var_form = myMessageForm(request.POST)     #var to store form to post to backend
        if var_form.is_valid():
            var_message = var_form.save(commit = False) #store teh form temporarily in this var till we done updating some fields
            var_message.sender = var_sender             #add sender to temporary instance of form
            var_message.recepient = var_recepient       #add recepient to "         "     of form

            if var_sender:              #if we have a sender, as in a logged in user
                var_message.name = var_sender.name          #we assign the name field of the form with the name of logged in user
                var_message.email = var_sender.email        #do same with the email 
            
            var_message.save()

            messages.success(request, 'Your Message Was Successfuly Sent!')
            return redirect('user_profile_link', pk = var_recepient.id)        #Upon completion we return to the page of recepient

    context ={'tempvar_recepient' : var_recepient, 'tempvar_form':var_form}  #pass it into the context variable
    return render(request, 'users/message_form.html', context)