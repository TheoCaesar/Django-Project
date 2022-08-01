from .models import Profile, User
#from django.contrib.auth.models import User #without line 2, all was well, perhaps cos line 2 was already 
#mentioned in our models, and ourl line 1 pulled the User and Profiles from models.py...works fine sans it.

#testing out our signals.
#step 1: import the post save, which will be triggered when a profile is saved (/already)
from django.db.models.signals import post_save

#step 2: create receiver function, which we will be triggering: it will be taking some parameters
#so sender is the model that actually triggers it, and instance is that particular instance of our sender model
#created is a bool variable dt makes us aware if the instance was new or already existed.
#more importantly, **kwargs, stands for keyword arg
def profileUpdated(sender, instance, created, **kwargs): 
    print ("Profile Saved")         #should be displayed in our terminal...
    print ('Instance:',  instance)
    print ('Created:', created)

#now we connect the signal, and the action(function) we need to carry out as well as specify the model dt is
#  going to trigger the signal, in this case: profile, so whenever a new profile is saved, signal must notice and trigger
#the profile updated function

#post_save.connect(profileUpdated, sender = Profile)
#now lets enter our admin and create a new profile for an existing user, just click save sans editing anything


#now we are going to try the post_delete method
#step 1: import post_delete method
from django.db.models.signals import post_delete

#step 2: create the action/function to carry out, nb: we are deleting so no neeed for the created arg, else error
def profileDelete(sender, instance, **kwargs):
    print('Deleting Profile ', instance)

#step 3: connect the signal with the the function(action) we wanna carry out
#post_delete.connect(profileDelete, sender = Profile)
#so this reads, if a profile is deleted, do what's specified in the profileDelete function. i.e print deleting user
#now we going to go into our admin panel and delete the new instance we created

#Doing same shit with the receiver...NB: comment out the connection of signals and fxn(step 3), before this
#Step 1: Import receiver from django.dispatch
from django.dispatch import receiver

#step2: @receiver(post_save, sender = Profile)
# create a function and place "@receiver(signal type, sender)", 
# remember, sender is the model based on which signal listens  and triggers the function
#@receiver(post_save, sender = Profile) #reads the below fxn is our receiver and to be caried out upon a post save of a Profile
def profileUpdated(sender, instance, created, **kwargs):
    print('Profile Saved...')
    print('Instance : ', instance)
    print("Created : ", created)

#Now we need to go into the admin panel and save any instace of a profile sans edit

#Step 1: import the signals
from django.db.models.signals import post_save, post_delete

#step 2: create function, pass in the args, sender, instance, (created,), **kwargs
from django.core.mail import send_mail      #18 Feb 2022
#from django.core import mail #*send_mail      #18 Feb 2022
from django.conf import settings            #this is to take adv of the prerequisites needed for the mail
def createProfile(sender, instance , created, **kwargs): #be sure to chech out if user is imported.
    if created:     #(if the User instance is new or non existent  in our User model...)
        var_user = instance #we create a variable to hold the instance of our User model, only if this user instance is new.
        var_profile = Profile.objects.create(
            #now we are going to access the rows in our Profile model's table and assign or store data.
            user = var_user, 
            username = var_user.username, 
            email = var_user.email,
            name = var_user.first_name,
            #we see this isnt all the fields in our profile model, i think this is possible thanks to the null = True,
            #so all fields arent re+quired from us...now lets add the step 3, where we connect signal with function and sender

            #In our admin we are going to create new user, and this should automatically create a corresponding profile
        )

        subject = 'Welcome to DevSearch'
        message = 'We are quite glad to have you on board'

        send_mail(      #trigger send mail fxn when a profile is created
            subject, 
            message, 
            settings.EMAIL_HOST_USER, 
            [var_profile.email],
            fail_silently=False,     #copied from the documention 
        )





#Step 3: Connect signal to function and specify the sender
post_save.connect(createProfile, sender=User)
#Now lets enter admin and test this shit out...as no errors are in terminal, we'll create a user and a profile should be auto created

#Now we try to delete a user upon the deletion of a profile
#step 1 already taken care of ...from django.db.models.signals import post_delete

#step 2: come up with a function specifying what you want done upon the signal hearing an event
def deleteUser(sender, instance , **kwargs):    #nb: this is a delete signal, hence created is of no use here
    var_user = instance.user #this instance points to our sender, which is our profile, linked to one user
    var_user.delete()

#step 3: connect signal, passing it the arg of function and sender
post_delete.connect(deleteUser, sender = Profile) #no errors in our  terminal...of to admin
#and it worked like a charm...For cleaner code our man recommends we create a signal.py file for signals


#26/12/21 = 21:11
def updateUser(sender, instance, created, **kwargs):
    var_profile = instance
    var_user = var_profile.user
    if created == False:
        var_user.first_name = var_profile.name
        var_user.username = var_profile.username
        var_user.email = var_profile.email
        var_user.save()

post_save.connect(updateUser, sender = Profile)