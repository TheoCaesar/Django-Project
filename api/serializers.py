from rest_framework import serializers
from projects.models import ProjecT

""" class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjecT
        fields = '__all__'  #double underscore.
 """

from projects.models import Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'  #double underscore.

from users.models import Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'  #double underscore.


from projects.models import review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = review
        fields = '__all__'  #double underscore.

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many = False) #one owner per project
    tags = TagSerializer(many = True) #one proj may have many tags
    
    reviews = serializers.SerializerMethodField()   #add an attribute or field to json obj

    class Meta:
        model = ProjecT
        fields = '__all__'  #double underscore.
    
    def get_reviews(self, obj):   #note that with the api every function starts with get, self refers to the serializer class, 
    #                               object is the obj/instance we are serializing  i.e. ProjecT
        var_reviews = obj.review_set.all()          #gets all projects review
        var_serializer = ReviewSerializer(var_reviews, many = True).data
        return var_serializer
