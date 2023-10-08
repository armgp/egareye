import re
import subprocess
import psutil
from django.http import JsonResponse
from egareye.helpers import getMovies, runOnVM
from egareye.constants import RUNNING, UPCOMING
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import MovieCityProcess, MovieCityPhoneNumber

@api_view(['GET'])
def getRunningMovies(request, city):
    running_movie_urls = getMovies(city, RUNNING)
    movie_names = {re.search(r'/movies/(.*?)-movie-detail-\d+', url).group(1).replace('-', ' ').title() for url in running_movie_urls}
    return JsonResponse({"running_movies": list(sorted(movie_names))}, safe=False)

@api_view(['GET'])
def getUpcomingMovies(request, city):
    upcoming_movie_urls = getMovies(city, UPCOMING)
    movie_names = {re.search(r'/movies/(.*?)-movie-detail-\d+', url).group(1).replace('-', ' ').title() for url in upcoming_movie_urls}
    return JsonResponse({"upcoming_movies": list(sorted(movie_names))}, safe=False)

@api_view(['GET'])
def getAllMovies(request, city):
    upcoming_movie_urls = getMovies(city, UPCOMING)
    running_movie_urls = getMovies(city, RUNNING)
    movie_urls = running_movie_urls+upcoming_movie_urls
    movie_names = {re.search(r'/movies/(.*?)-movie-detail-\d+', url).group(1).replace('-', ' ').title() for url in movie_urls}
    return JsonResponse({"all_movies": list(sorted(movie_names))}, safe=False)


# for monitoring in vm
@api_view(['POST'])
@csrf_exempt
def monitorMovie(request):
    try:
        data = request.data

        name = data.get('name', '')
        phoneNumber = data.get('phoneNumber', '')
        selectedMovie = data.get('movie', '')
        selectedCity = data.get('city', '')
        frequency = data.get('frequency', '')
        
        command = "python3 start.py "+selectedMovie.lower().replace(" ", "-")+" "+selectedCity+" "+phoneNumber
        runOnVM(command)

        return JsonResponse({"message": "Movie monitoring started successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

# uncomment this and comment the above monitorMovie() function for local monitoring    
# @api_view(['POST'])
# @csrf_exempt
# def monitorMovie(request):
#     try:
#         data = request.data
#         # print(data)
#         name = data.get('name', '')
#         phoneNumber = data.get('phoneNumber', '')
#         selectedMovie = data.get('movie', '')
#         selectedCity = data.get('city', '')
#         frequency = data.get('frequency', '')
#         # print(name, phoneNumber,selectedCity, selectedMovie, frequency)
#         # Construct the script path (replace this with your actual script path)
#         script_path = '/home/gp/Documents/Dev/plivo/monitor_script/start.py'
        
#         # Execute the Python script using subprocess
#         subprocess.run(['python3', script_path, selectedMovie.lower().replace(" ", "-"), frequency, selectedCity, phoneNumber])

#         return JsonResponse({"message": "Movie monitoring started successfully!"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
