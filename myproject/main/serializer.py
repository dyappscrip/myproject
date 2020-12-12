from rest_framework import serializers
from news.models import News
from cat.models import Cat

class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ['pk','name','date']

class CatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cat
        fields = '__all__'
