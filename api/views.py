from rest_framework.response import Response
from rest_framework.decorators import api_view
from audio_scraper.models import AudioContent
from .serializers import AudioContentSerializer
from audio_scraper.utils import download_youtube_audio

@api_view(['POST'])
def scrape_audio(request):
    link = request.data.get("content_link")
    category = request.data.get("category")
    if not link or not category:
        return Response({"error": "content_link and category are required"}, status=400)
    
    try:
        title, file_path = download_youtube_audio(link, category)
    except Exception as e:
        return Response({"error": f"Failed to scrap audio: {str(e)}"}, status=500)
    
    audio = AudioContent.objects.create(
        title=title,
        content_link=link,
        audio_file=file_path,
        category=category
    )
    return Response(AudioContentSerializer(audio).data)

@api_view(['GET'])
def list_audios(request):
    category = request.GET.get("category")
    queryset = AudioContent.objects.all()
    if category:
        queryset = queryset.filter(category=category)

    if not queryset.exists():
        return Response({"message": "No audio files found"}, status=404)
    
    return Response(AudioContentSerializer(queryset, many=True).data, status=200)

@api_view(['GET'])
def get_audio(request, pk):
    try:
        audio = AudioContent.objects.get(pk=pk)
        return Response({
            "id": audio.id,
            "title": audio.title,
            "content_link": audio.content_link,
            "audio_file": audio.audio_file.url,
            "category": audio.category,
            "timestamp": audio.timestamp,
            }, status=200)
    
    except AudioContent.DoesNotExist:
        return Response({"error": "Audio not found"}, status=404)

@api_view(['DELETE'])
def delete_audio(request, pk):
    try:
        audio = AudioContent.objects.get(pk=pk)
        audio.delete()
        return Response({"message": "Audio  deleted successfully"}, status=200)
    except AudioContent.DoesNotExist:
        return Response({"error": "Audio not found"}, status=404)
