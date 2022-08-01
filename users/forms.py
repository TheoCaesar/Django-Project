from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.forms import ModelForm

class myCustomizedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
    
    #22/12/21 15:29 -- copied and just changed the first arg of the line 12 to the classname of the form.
    def __init__(self, *args, **kwargs):            #arguments, andd keyword arguments
        super(myCustomizedUserCreationForm, self).__init__(*args, **kwargs) #super tells it which class we will be modifying i.e class)rojectForm
        
        for mykey, myval in self.fields.items():
            myval.widget.attrs.update( {'class': 'input', 'placeholder': 'Click to Add'}) 
            #be mindful of ' WIDGET.ATTRS' ENDED UP ADDING S TO THE WIDGET A NUMBER OF TIMES AND IVE PAID DEARLY WITH MY TIME

#26-12-21   creating the model form, for editing the user account...
from .models import Profile #this is a class, in our models.py file 

class myProfileForm(ModelForm):
    class Meta:
        model = Profile
        #fields = '__all__'  --access cntrl'
        
        fields = ['name', 'email', 'username', 'location' , 'short_intro', 
        'bio', 'profile_image', 'social_github', 'social_twitter', 
        'social_linkedin', 'social_youtube', 'social_website']
    
    def __init__(self, *args, **kwargs):            #arguments, andd keyword arguments
        super(myProfileForm, self).__init__(*args, **kwargs) #super tells it which class we will be modifying i.e class)rojectForm
        
        for mykey, myval in self.fields.items():
            myval.widget.attrs.update( {'class': 'input', 'placeholder': 'Click to Add'}) 
            #be mindful of ' WIDGET.ATTRS' ENDED UP ADDING S TO THE WIDGET A NUMBER OF TIMES AND IVE PAID DEARLY WITH MY TIME


# =========== 28/12/21 ==================
from .models import Skill
class mySkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner'] #knew there was some form of a shortcut, should have done same with class above.

    def __init__(self, *args, **kwargs):            #arguments, andd keyword arguments
        super(mySkillForm, self).__init__(*args, **kwargs) #super tells it which class we will be modifying i.e class)rojectForm
        
        for mykey, myval in self.fields.items():
            myval.widget.attrs.update( {'class': 'input', 'placeholder': 'Click to Add'}) 
            #be mindful of ' WIDGET.ATTRS' ENDED UP ADDING S TO THE WIDGET A NUMBER OF TIMES AND IVE PAID DEARLY WITH MY TIME


# ------------ 18/02/22 ----------------
from .models import Message
class myMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body'] #message fields we want displayed

    #for styling -- copied from above then replaced mySkillForm with myMessageForm  -- :
    def __init__(self, *args, **kwargs):            #arguments, andd keyword arguments
        super(myMessageForm, self).__init__(*args, **kwargs) #super tells it which class we will be modifying i.e class)rojectForm
        
        for mykey, myval in self.fields.items():
            myval.widget.attrs.update( {'class': 'input', 'placeholder': 'Click to Add'}) 
            #be mindful of ' WIDGET.ATTRS' ENDED UP ADDING S TO THE WIDGET A NUMBER OF TIMES AND IVE PAID DEARLY WITH MY TIME
