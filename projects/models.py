from django.db import models
import uuid

from django.db.models.deletion import SET_NULL

from users.models import Profile
# Create your models here.
class ProjecT(models.Model):
    #++++++++++++++++++++++++++++++ added on 17/11/21 7:29am ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #we are linking our projects.models (i.e. ProecT) instances to users.models instances known as profiles, we will need to import the Profile model from users.models
    owner = models.ForeignKey(Profile, blank=True, null = True, on_delete=models.SET_NULL)
    #=======================================================================================
    title = models.CharField(max_length = 200)
    description = models.TextField( null=True, blank = True) #null is set to true so we can skip this part when filling the database, by default null is set to false so the line above will alwasy need to be filled, the blank arg is for submission of forms, and it being true translate to the same thing as the true of null but the repeat is neccessary for forms
    featured_img = models.ImageField(null = True, blank = True, default = 'default.jpg')
    demo_link = models.CharField(max_length=2000, null = True, blank = True)
    source_link  = models.CharField(max_length=2000, null=True, blank = True)
    #======================================================================================================================================
    #============>>>   09-11-21 19:09 created way later after migrations had been made  ==================================================================================================
    tags = models.ManyToManyField('Tag', blank=True) #the name of the db or table we want to link up is passed as an arg, however since we defined it way down below this db/table, we had to place it in "" to prevent an error

    vote_total = models.IntegerField(default = 0, null = True, blank = True)
    vote_ratio = models.IntegerField(default = 0, null = True, blank = False)
    #===========================================================================================
    #==========================================================================================
    created = models.DateTimeField(auto_now_add=True) #which auto creates a timestamp when a creation is made
    id =  models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        #ordering = ['created'] #this orders the projects in ascending order(FCFS), preced it with a hyphen to change it to descending
        ordering = ['-vote_ratio', '-vote_total', 'title'] #

    def __str__(self):
        return self.title
    
    #get existing voters on a project
    @property
    def voters(self):           #dennis named his reviewers
        queryset = self.review_set.all().values_list('owner__id', flat = True) 
        #owner__id is double underscore, else if test which uses the queryset wont work fully as expected
        return queryset

    
    #updating vote count and ratio per each review
    @property #this makes it run as an attribute and not a methdod
    def getVoteCount(self):
        var_reviews = self.review_set.all()
        var_upvotes = var_reviews.filter(value = 'up').count() #to generat a number 
        var_total_votes = var_reviews.count()

        var_ratio = (var_upvotes/var_total_votes) *100 #to make percentage

        self.vote_total = var_total_votes       #vote_total is an attribute of the project model
        self.vote_ratio = var_ratio             #vote_ratio is also an attribute for "      "

        self.save()     #then we save the updated review and vote in addiion to existing ones



#create another model or database
class review(models.Model):
    VOTE_TYPE = (                   #set up to ensure structured review, for analysis
        ('up', 'Up Vote'), 
        ('down', 'Down Vote')    #so the first arg in each tuple refers to how data will be referenced in our database , the second is what will be displayed on the front
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    project = models.ForeignKey(ProjecT , on_delete=models.CASCADE)       #notice the arg it takes: the name of the db(tables) you want to link it with, on delete which is our second arg is set to cascade, so should a proj be deleted it will trickle down and delete it's reviews as well
    body = models.TextField(null = True, blank = True)
    value = models.CharField(max_length=200, choices = VOTE_TYPE) #the choices should provide a drop down list of up and down votes
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value
    
    #updating vote count and ratio per each review
    @property #this makes it run as an attribute and not a methdod
    def getVoteCount(self):
        var_reviews = self.review_set.all()
        var_upvotes = var_reviews.filter(value = 'up').count() #to generat a number 
        var_total_votes = var_reviews.count()

        var_ratio = (var_upvotes/var_total_votes) *100 #to make percentage

        self.vote_total = var_total_votes       #vote_total is an attribute of the project model
        self.vote_ratio = var_ratio             #vote_ratio is also an attribute for "      "

        self.save()     #then we save the updated review and vote in addiion to existing ones

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created  = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key=True, editable = False)

    def __str__(self):
        return self.name
        