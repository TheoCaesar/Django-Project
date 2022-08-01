from django.core import paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required   #26-11-21

# Create your views here.
from django.http import HttpResponse

#--10/11/21 11:03
from .models import ProjecT #as models and views are in the same subdirectiory you know dada

#10/11/21 -- 17:16
from .forms import ProjecTForm

def projects(request):
    #return HttpResponse('Here are our products')
    return render(request, 'projects/product.html')


def services(request):
    #return HttpResponse('Here are our services')
    return render(request,'projects/services.html')

#def bespoke_services(request,order):
    #return HttpResponse('Custom Service: ' + str(order))
    #return render(request, 'projects/bespoke.html')


#09th November 2021 11am -- passing python vars and code into our html 
  #09/11/21 12:57 pm 
projectlist = [                       
        {
            'id' :'001' ,
            'name' : 'Auto Parts Management System',
            'description': 'We will use harmonys enterprise as our case study...we would like to implement a cargo management system, include the cargo removal services, debtors and creditors management, inventory level mgt, warehouse mgt, customer mgt with complaint and suggestions, billing systems and wmployee management. Abossey Okai online community this should be enough'

        },
        {
            'id' : '002',
            'name': 'Auto Repair Shop Management System',
            'description':' It should have a billing system, a mailing list for customers to be reminded of vehicle servicing, customers to register platinum and be able to order house calls, request for roadaid, speak to a mechanic, and mechanic can also track inverntory levels, employee performance, generate expense reports, suppliers and affiliates, enquiries'
        },
        {
            'id':'003',
            'name': 'Car Rental Management systems',
            'description': 'For this one I actually dont give a hoot'
        }
    ]
def projectwork(request):       #this is a  funciton to serve our home page
    #variables
    varname='Projects Work'
    services = ['Car Rental Management systems', 'Auto Repair Shop Mangement','Auto Parts Management System']

    #we could also bring our context dict into a var and store it over here should it get so long and all...
    #var_context = {'our_name': varname, 'options' : services}

    #a list of dictionaries

    return render(request, 'projects/project_work.html', {'our_name':varname, 'options': services, 'proj_dict': projectlist})

def projectwork(request):
    varname='Projects Work'
    services = ['Auto Parts Management System']

    var_proj = ProjecT.objects.all()
    context = {'proj_dict':var_proj }
    return render(request, 'projects/project_work.html', {'our_name':varname, 'options': services, 'proj_dict': projectlist})


def project_WORK(request, pk):
    projectx = None
    for each in projectlist: 
        if each['id'] == pk:
            projectx = each
    return render(request,'projects/bespoke.html', {'proj': projectx} )


#=====================================================================================================================
#=====================================================================================================================
#=====================================================================================================================


#10-Nov-21 10:45am -- we creating a new pg with which we will gather our queries
#29-12-21 21:40
from .utilities import searchproject
#30-12-21 --
""" from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  Feb 13 20:40"""
from .utilities import paginateProjects  #we could have added it to line 84 above, but no yawa

def finalproj(request):
    project_var, search_query = searchproject(request)

    custom_range_var, project_var = paginateProjects(request, project_var, 3)
    #the above CANT be any var SINCE  LINE 90 USES TEH SAME PROJECT VAR TO PASS IT VALUES TO CONTXT

    #somevar = ProjecT.objects.all() 
    context = {'var_projModel': project_var , 'tempvar_searchquery' :search_query,     'temp_custom_range':custom_range_var}
    return render(request, 'projects/finalproj.html',context ) #finalProjQ

from .forms import ReviewForm  #import model form
from django.contrib import messages                 #for flash messages
def finproj(request, pk):
   projObj = ProjecT.objects.get(id = pk)
   
   #so it has worked now; but we will like to render our tags as most of our entries in the description sect was empty
   #we already have a var holding all project obj named proj obj so we go on straight to fetch it's tags
   nvar_tags = projObj.tags.all()
   var_form = ReviewForm()      #var-form

   if request.method == 'POST':
       var_form = ReviewForm(request.POST)  #should give as the vote and the comment
       var_review = var_form.save(commit=False)    #commit false creates a temporary instance of saved form in var_review
       var_review.project = projObj     #we give that temporary instance a project to which the review belongs
       var_review.owner = request.user.profile  #then go on to give it an owner(profile)
       var_review.save()            #last last we save it...overriding the commit false

       #update project vote's count. 
       projObj.getVoteCount     #remember its a property and not a method
       print('Vote Count ->', projObj.getVoteCount)

       messages.success(request, 'Your review was succesfully submitted')

   #print('Project Instance:', projObj)
   context = {'proJModel': projObj, 'proj_tags': nvar_tags, 'tempvar_form' : var_form}  #context
   return render(request, 'projects/finprojren.html', context) #now dt we done we need to comment out the above and add the hyper linkds


@login_required (login_url= 'loginlink')#26-11-21 9:48am
def create_proj(request):
    #27/12/21 01:22 am
    somevar_profile = request.user.profile  #step1
    somevar = ProjecTForm()

    #later added @19:30 after class... in attempt to save things keyed in the form to our database...
    if request.method == "POST":
        #print(request.POST) #used to test if data keyed in was successful..as it will generate a csrf token in our terminal---after which we know we can carry on and comment this out
        somevar = ProjecTForm(request.POST) #so we store our new data in a variable, used the same name and commented it above and it works all the same
        somevar = ProjecTForm(request.POST, request.FILES) #so we are taking images from the form template, and need to ensure it gets to the backend, hence the request.FILEs
        if somevar.is_valid():
            #somevar.save()                              '''step2'''
            somevar_project = somevar.save(commit=False)#'''step2b'''
            somevar_project.owner = somevar_profile       #step 3
            somevar_project.save()                      #step4
            return redirect('fprojq')   #the redirect is some shortcut provided by django to take us to our page for all our projects in our database the moment a new one is added

    context = {'tempvar': somevar}   #to be filled later said by tutor---filled now: temp var stands for template var
    return render(request, 'projects/proj_form.html', context) #off to create our forms.py and proj_form.html

    #10/11/21   17:15 now we're done with the two , we will have to goup and import our ProjecTForm from our forms.py
    # we will have to go up in our create_proj fxn and fill that context with our model form obj, to do that we need some placeholder variable

@login_required #26-11-21 9:48am
def update_proj(request, pk):       #updates should pretty much be the same as  create except we will use the .get()  querry and pass it with an id == primary key
    #28/12/21 04:01 am
    somevar_profile = request.user.profile #-------step 1--------#

    #someprojobj = ProjecT.objects.get(id=pk) #=====step 2 -------#
    someprojobj = somevar_profile.project_set.get(id=pk) #-------step 2b =====#
    somevar = ProjecTForm(instance=someprojobj)

    if request.method == 'POST':
        #somevar = ProjecTForm(request.POST,  instance = someprojobj) #without the second argument/attribute, the update ends up creating a new project altogether.
        somevar = ProjecTForm(request.POST, request.FILES,  instance = someprojobj) #without the second argument/attribute, the update ends up creating a new project altogether.
        if somevar.is_valid():
            somevar.save()
            return redirect('fprojq')
    context = { 'tempvar': somevar }
    return render(request, 'projects/proj_form.html', context) #Praveen has a way of naming his template in the rennder arg where he assigns a variable with the string directtory and just names that variable in teh render arg
    #now create a url for our projupdate...


#for the delete method , ivy's utube vids explains it better...
@login_required #26-11-21 9:48am
def delete_proj(request, pk):
    #28/12/21 04:01 am
    somevar_profile = request.user.profile #-------step 1--------#
    
    #someprojobj = ProjecT.objects.get(id = pk) #we querry the object we want to delete, pass it to our conext for rendering 
    someprojobj = somevar_profile.project_set.get(id=pk) #-------step 2b =====#

    if request.method == 'POST':
        someprojobj.delete()
        return redirect ('fprojq')
    context = {'del_tempvar': someprojobj}
    #  28-12 21  return render (request, 'projects/delete_obj.html', context)
    return render (request, 'delete_obj.html', context)

