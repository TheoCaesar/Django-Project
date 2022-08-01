from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])  #   This decorator changes function based view into apiClassView
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},
        
        {'POST': '/api/users/token'},       #json web tokens have an expiration
        {'POST': '/api/users/token/refresh'},#so we pass he refresh to keep user logged in 
    ]
    #return JsonResponse(routes, safe = False)   
    return Response(routes )   

from .serializers import ProjectSerializer
from projects.models import ProjecT

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def getProjects(request):
    var_projects = ProjecT.objects.all()
    var_serializer = ProjectSerializer(var_projects, many = True) #the many parameter ensures that more than one obj is serialized
    return Response(var_serializer.data)    # we apply the data attribute so we get the actual serialized objects

@api_view(['GET'])
def getProject(request, pk):
    # var_projects = ProjecT.objects.all()
    var_project = ProjecT.objects.get(id = pk)
    var_serializer = ProjectSerializer(var_project, many = False) #the many parameter ensures that more than one obj is serialized
    return Response(var_serializer.data) 


from projects.models import review
@api_view(['POST'])
@permission_classes([IsAuthenticated]) #be mindful of []
def projectVote(request, pk):
    var_proj = ProjecT.objects.get(id=pk) #get project user intends to vote on
    var_user = request.user.profile     #thanks to api decorateor, user is generated from token
    var_data = request.data             #data to be passed in from front end

    #print('DATA :==> ', var_data)   
    var_review, created = review.objects.get_or_create(
        owner = var_user, 
        project = var_proj,
    )

    var_review.value = var_data['value'] #we get that review obj, be it new or old and change it, to what we pass in (json)
    var_review.save()                       #we now save the updated review.

    var_proj.getVoteCount               #in our review model this was an innerfunction with a property decorator that enabled us call 
    #                                       function as an attribute, and update vote total and vote ratio

    # we convert the data to json data then apply the data attribute so we get the actual serialized objects
    var_serializer = ProjectSerializer(var_proj, many = False)
    return Response(var_serializer.data)

#the getorcreate checks if there is a review object in the database with an owner equivalent to current user 
# and project same as that being voted on. so in the absence of such a review, we go ahead to create one. 
# if there happens to be an existing review then per the rules, 1 user review is to 1 particular project so we cant
#create but its going to get that object and return it to us.

#the var_review, will be the variable that holds the returned object whether new or existing. and the created will be bool