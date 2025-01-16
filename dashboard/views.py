from django.shortcuts import render
from django.shortcuts import redirect
from . forms import *
from django.contrib import messages
from django.views import generic
from googleapiclient.discovery import build
import requests
import wikipedia
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request, f'Notes Added from {request.user.username} successfully!')
    else:
        form = NotesForm()
        
    form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes , 'form': form}
    return render(request, 'dashboard/notes.html' , context)


def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    messages.success(request, 'Note Deleted Successfully!')
    return redirect('notes')


class NotesDetailView(generic.DetailView):
    model = Notes
    
@login_required
def assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_completed']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            assignments = Assignment(user=request.user, subject=request.POST['subject'], title=request.POST['title'], description=request.POST['description'], due=request.POST['due'], is_completed=finished)
            assignments.save()
            messages.success(request, f'Assignment Added from {request.user.username} successfully!')
    else:
        form = AssignmentForm()
    
    assignment = Assignment.objects.filter(user=request.user)
    if len(assignment) == 0:
        assignment_done = True
    else:
        assignment_done = False
    
    context = {'assignments': assignment, 'assignments_done': assignment_done, 'form': form}
    
    return render(request, 'dashboard/assignment.html' , context)


def update_assignment(request, pk=None):
    assignment = Assignment.objects.get(id=pk)
    if assignment.is_completed == True:
        assignment.is_completed = False
    else:
        assignment.is_completed = True
    assignment.save()
    return redirect('assignment')


def delete_assignment(request, pk=None):
    Assignment.objects.get(id=pk).delete()
    return redirect('assignment')

#AIzaSyDKWxYBLFHZS8-caVZs7kHxpTVgQ_xF6IQ
'''def youtube(request):
    if request.method == 'POST':
        form = DashboardFom(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/youtube.html', context)
            
    else:
        form = DashboardFom()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html' , context)'''
    


def youtube(request):
    if request.method == 'POST':
        form = DashboardFom(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            
            # Initialize YouTube API client
            youtube = build('youtube', 'v3', developerKey='AIzaSyDKWxYBLFHZS8-caVZs7kHxpTVgQ_xF6IQ')

            try:
                # Make a request to search videos
                search_response = youtube.search().list(
                    q=text,
                    part='snippet',
                    maxResults=10
                ).execute()

                # Parse results
                result_list = []
                for item in search_response.get('items', []):
                    if item['id']['kind'] == 'youtube#video':
                        result_list.append({
                            'title': item['snippet']['title'],
                            'thumbnail': item['snippet']['thumbnails']['default']['url'],
                            'channel': item['snippet']['channelTitle'],
                            'link': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                            'published': item['snippet']['publishedAt'],
                            'description': item['snippet']['description'],
                        })

                # Render the results
                return render(request, 'dashboard/youtube.html', {'form': form, 'results': result_list})
            except Exception as e:
                return render(request, 'dashboard/youtube.html', {'form': form, 'error': str(e)})
    else:
        form = DashboardFom()

    return render(request, 'dashboard/youtube.html', {'form': form})

@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_completed']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
                    
            except:
                finished = False
            
            todos = Todo(user=request.user, title=request.POST['title'], is_completed=finished)
            todos.save()
            messages.success(request, f'Todo Added from {request.user.username} successfully!')
            
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form': form,
        'todos': todo,
        'todos_done': todos_done
        }
    
    return render(request, 'dashboard/todo.html' , context)


def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_completed == True:
        todo.is_completed = False
    else:
        todo.is_completed = True
    todo.save()
    return redirect('todo')
    
    
'''def update_todo(request, pk=None):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, id=pk)
        todo.is_completed = not todo.is_completed
        todo.save()
        messages.success(request, f"Todo '{todo.title}' updated successfully!")
    return redirect('todo')'''



def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')


'''def books(request):
    if request.method == 'POST':
        form = DashboardFom(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle', 'N/A'),
                'description': answer['items'][i]['volumeInfo'].get('description', 'N/A'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount', 'N/A'),
                'categories': answer['items'][i]['volumeInfo'].get('categories', 'N/A'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating', 'N/A'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks', {}).get('thumbnail', 'N/A'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink', 'N/A'),
            }
            
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/books.html', context)
            
    else:
        form = DashboardFom()
    context = {'form': form}
    return render(request, 'dashboard/books.html' , context)'''
    

def books(request):
    if request.method == 'POST':
        form = DashboardFom(request.POST)
        text = request.POST['text']
        url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
        r = requests.get(url)
        answer = r.json()
        
        # Initialize an empty list to hold book results
        result_list = []
        
        # Check if the API response contains 'items'
        if 'items' in answer:
            for i, item in enumerate(answer['items'][:10]):  # Limit to 10 results
                volume_info = item.get('volumeInfo', {})
                image_links = volume_info.get('imageLinks', {})
                
                # Build the result dictionary
                result_dict = {
                    'title': volume_info.get('title', 'N/A'),
                    'subtitle': volume_info.get('subtitle', 'N/A'),
                    'description': volume_info.get('description', 'N/A'),
                    'count': volume_info.get('pageCount', 'N/A'),
                    'categories': volume_info.get('categories', []),
                    'rating': volume_info.get('averageRating', 'N/A'),
                    'thumbnail': image_links.get('thumbnail', 'N/A'),
                    'preview': volume_info.get('previewLink', 'N/A'),
                }
                result_list.append(result_dict)
        
        # Prepare context
        context = {
            'form': form,
            'results': result_list
        }
        return render(request, 'dashboard/books.html', context)
    
    else:
        form = DashboardFom()
    
    # Render template with empty form if GET request
    context = {'form': form}
    return render(request, 'dashboard/books.html', context)


def dictionary(request):
    if request.method == 'POST':
        form = DashboardFom(request.POST)
        text = request.POST['text']
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"
        r = requests.get(url)
        answer = r.json()

        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': '',
                'error': "No data found for the entered word.",
            }
        return render(request, 'dashboard/dictionary.html', context)

    else:
        form = DashboardFom()
        context = {'form': form}
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardFom(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardFom()
        context = {'form': form}
    return render(request, 'dashboard/wiki.html', context)


def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)

        # Check the selected measurement type
        if request.POST['measurement'] == 'length':  # Fixed the attribute case
            measurement_form = ConversionLengthForm()
            context = {'form': form, 'm_form': measurement_form, 'input': True}
            
            # Check if 'input' exists in the POST data
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = request.POST['input']
                answer = ''
                
                if input_value and int(input_value) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_value} yard = {int(input_value) * 3} foot'

                    if first == 'foot' and second == 'yard':
                        answer = f'{input_value} foot = {int(input_value) / 3} yard'

                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }

        if request.POST['measurement'] == 'mass':  # Fixed the attribute case
            measurement_form = ConversionMassForm()
            context = {'form': form, 'm_form': measurement_form, 'input': True}

            # Check if 'input' exists in the POST data
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = request.POST['input']
                answer = ''

                if input_value and int(input_value) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input_value} pound = {int(input_value) * 0.453592} kilogram'

                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input_value} kilogram = {int(input_value) * 2.20462} pound'

                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }

    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'dashboard/register.html', context)

@login_required
def profile(request):
    assignments = Assignment.objects.filter(is_completed=False, user=request.user)
    todos = Todo.objects.filter(is_completed=False, user=request.user)
    if len(assignments) == 0:
        assignments_done = True
    else:
        assignments_done = False
    
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
        
    assignments_done = not assignments.exists()
    todos_done = not todos.exists()
        
    context = {
        'assignments': assignments,
        'assignments_done': assignments_done,
        'todos': todos,
        'todos_done': todos_done
    }
    
    return render(request, 'dashboard/profile.html', context)


def custom_logout(request):
    logout(request)  
    #messages.success(request, "You have been successfully logged out.") 
    return render(request, 'dashboard/logout.html')
    #return redirect('logout')