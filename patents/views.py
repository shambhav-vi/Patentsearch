import json
from .graph_utils import generate_graph_data
from django.shortcuts import render, redirect
from database.arangodb import connect_to_arangodb
from .api import search_patent, fetch_patent_details, fetch_patent_details_from_api
from django.contrib.auth.decorators import login_required


def custom_authenticate(username, password):
    # Fetch the user from ArangoDB based on the provided username
    db = connect_to_arangodb()
    user_collection = db["user"]
    user_document = user_collection.fetchFirstExample({'username': username})
    
    if user_document:
        # Verify the password
        user_data = user_document[0]
        if user_data['password'] == password:
            return True

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Custom authentication logic
        authenticated = custom_authenticate(username, password)
        if authenticated:
            # Set a cookie to indicate authentication
            response = redirect('home')
            response.set_cookie('authenticated', 'true')
            return response
        
        error_message = "Invalid username or password."
        return render(request, 'login.html', {'error_message': error_message})
    
    else:
        return render(request, 'login.html')

def logout_view(request):
    # Clear the authentication cookie
    response = redirect('home')
    response.delete_cookie('authenticated')
    return response

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if name and username:
            db = connect_to_arangodb()

            collection = db["user"]

            # Checking if the username is already taken
            existing_user = collection.fetchFirstExample({'email': email})
            if existing_user:
                error_message = "Email already exists. Please use a different email address."
                return render(request, "signup.html", {"error_message": error_message})
    
            example_query = {'username': username}
            existing_users = collection.fetchByExample(example_query, batchSize=1)  
            if len(existing_users) > 0:
                error_message = "Username already exists. Please choose a different username."
                return render(request, "signup.html", {"error_message": error_message})

            # Checking if the passwords match
            if password != confirm_password:
                error_message = "Passwords do not match. Please re-enter the passwords."
                return render(request, "signup.html", {"error_message": error_message})

            # Creating a new document and setting the user data
            user = collection.createDocument()
            user["name"] = name
            user["username"] = username
            user["email"] = email
            user["password"] = password
            user.save()

            authenticated = custom_authenticate(username, password)
            if authenticated:
                # Set a cookie to indicate authentication
                response = redirect('home')
                response.set_cookie('authenticated', 'true')
                return response

        else:
            error_message = "Name and username are required fields."
            return render(request, "signup.html", {"error_message": error_message})

    return render(request, "signup.html")

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

def search_patents(request):
    query = request.GET.get('query')
    if query:
        patents = search_patent(query)
        if patents:
            patents_with_details = fetch_patent_details(patents)
            return render(request, 'search.html', {'patents': patents_with_details, 'query': query})
        else:
            # Handle case when no patents are found
            return render(request, 'search.html', {'query': query})
    return render(request, 'search.html')

def patent_detail(request, patent_id):
    query = request.GET.get('query', patent_id)   # Get the query parameter from the search page
    patent_details = fetch_patent_details_from_api(patent_id)
    if patent_details:
        inventor = patent_details.get('inventor', '') 
        graph = generate_graph_data(inventor)  
        if graph:
            graph_json = json.dumps(graph)
            context = {
                'patent_details': patent_details,
                'graph_json': graph_json,
            }

            return render(request, 'patent_detail.html', context)
        else:
            # Handle case when graph data is not available
            return render(request, 'patent_detail.html', {'patent_details': patent_details, 'query': query})
    else:
        return render(request, 'search.html')




