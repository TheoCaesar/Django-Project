from projects.views import projects
from .models import ProjecT, Tag
from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProjects(request, project_var, var_results):
    
    var_page = request.GET.get('page') #we  have to append 2 url ?page = 'int'  ...where int is a pagenumber 
    #var_results = 3  #later dennis deleted it in 41:51 of pagination video,saying we already pass it figures in the views and this just updates it again 
    var_paginator = Paginator(project_var, var_results)

    try:
        project_var = var_paginator.page(var_page)
    
    except PageNotAnInteger:
        var_page = 1
        project_var = var_paginator.page(var_page)
    
    except EmptyPage: #should a query be set beyond the range of available pages.
        var_page = var_paginator.num_pages 
        project_var = var_paginator.page(var_page) 

#feb 13 2022 -- 2:20
    leftIndex = (int(var_page) - 4)    #show pagination of 4 tabs to the left of existing tab
    if leftIndex < 1:
        leftIndex = 1                  #to handle negative tabs

    rightIndex = (int(var_page) + 5)
    if rightIndex > var_paginator.num_pages:     #if rightIndex exceeds total num of availale pages
        rightIndex = var_paginator.num_pages + 1
   
    #now we pass these indices to the range function to claculate custom range
    custom_range_var = range(leftIndex, rightIndex)
    return custom_range_var, project_var


def searchproject(request):
    search_query = '' #this is no mere variable, we got this from our profile template. that tag we altered.

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    print('Search Results: ',search_query )#=========================

    #29/12/21  21:46 ===========
    tag_var = Tag.objects.filter(name__icontains = search_query)

    project_var = ProjecT.objects.distinct().filter(Q(title__icontains = search_query) |
     Q(description__icontains = search_query)  |   Q(owner__name__icontains = search_query ) 
    |   Q(tags__in = tag_var) )

    return project_var, search_query
