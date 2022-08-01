#this is what weve createdd to store all our  model forms

from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms    #added on hte 16/11/21 @ 10:03 as a prerequisite to the styling of our createproject template...
from .models import ProjecT

#to create a model form we are going to have to create a class give it a name
class ProjecTForm(ModelForm):        #the class name by convertion should be the name of its model wf a form appended
    class Meta:                     #at a minimum the modelform needs two fields
        model = ProjecT             #first field should be dt of model and the name of  the model are form is to mimick
        #fields = '__all__'             #second will be the fields ; which could be a list of all the column names we want present in our form 
#                                    #OR specify '__all__' for django to do the work...it will create fields for all columns dt are editable and not dependent on django like the created column which has the auto add featue
#16Nov  #fields = ['title', 'description', 'demo_link' , 'source_link', 'tags'] #so end user cant maipulate votes

        #16/11/21 -- added a new field to our model, table to take images and we will like endusers to upload through the form
        #so here we are going to edit the fields displayed to our form template.
        fields = ['title', 'featured_img','description', 'demo_link' , 'source_link', 'tags'] 

        #10:00 on 16/11/21 create project form styling...
        #coming from rendering our form template which worked just fine but had some lackluster styling, tutor proposed some editing which could have been handled by javascript but since we are yet to learn it..here we are. 
        #to do the editing with django, we will be needing the forms library, then create a widgets dict variable, which triggers, django.forms to import widgets in addition to the ModelForm library...on line 3...you know what, lets not import the django.forms yet and try the widgets laidat and see...

        widgets = {
            'tags' : forms.CheckboxSelectMultiple(), #theree is quite a healthy variant of editing you could choose from...go check it out and see it rendered.
        }

    #now we are gonna add the css classes to the files by overiding he init method...be careful not to place the function under the meta class..this will fail to render the styling took me close to 15 mins to notice
    def __init__(self, *args, **kwargs):            #arguments, andd keyword arguments
            super(ProjecTForm, self).__init__(*args, **kwargs) #super tells it which class we will be modifying i.e class)rojectForm

            # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'add a title'}) 
            # #so we are telling it that it should take it's field named 'title' and update the class to css input input field...check it out and it should work... 
            # # we could copy the above lines and set em for all other fields or try the loop which i would comment out as this is much more understandable 
            # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': 'add a description'}) 
            # self.fields['demo_link'].widget.attrs.update({'class': 'input', 'placeholder': 'add a demo link'}) 
            # self.fields['source_link'].widget.attrs.update({'class': 'input', 'placeholder': 'add a source link'}) 
            # #the tags are being handled by checkboxes so we sorta safe for now...

            #LOOPWAY...note that our db  each project is some sort of a dictionary with labels being a key and its values being a fields so we loop through it with booth key and val
            for mykey, myval in self.fields.items():
                myval.widget.attrs.update( {'class': 'input', 'placeholder': 'Click to Add'}) #be mindful of ' WIDGET.ATTRS' ENDED UP ADDING S TO THE WIDGET A NUMBER OF TIMES AND IVE PAID DEARLY WITH MY TIME

from .models import review      #could have added it to the top but dont mind .
class ReviewForm(ModelForm):
    class Meta:
        model = review
        fields = ['value', 'body']
    
        labels = {
            'value' : 'Place your vote', 
            'body'  : 'Add a comment with your vote'
        }
    
    #below function is copied from above and edited
    def __init__(self, *args, **kwargs):            #arguments, andd keyword arguments
        super(ReviewForm, self).__init__(*args, **kwargs) #super tells it which class we will be modifying i.e class)rojectForm

        for mykey, myval in self.fields.items():
                myval.widget.attrs.update( {'class': 'input', 'placeholder': 'Click to Add'}) #be mindful of ' WIDGET.ATTRS' ENDED UP ADDING S TO THE WIDGET A NUMBER OF TIMES AND IVE PAID DEARLY WITH MY TIME
