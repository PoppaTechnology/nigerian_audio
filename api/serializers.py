from rest_framework import serializers
from audio_scraper.models import AudioContent

class AudioContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioContent
        fields = '__all__'