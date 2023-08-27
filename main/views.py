from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
import requests
from UserPagination.settings import API_URL

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    users = data["users"]
except requests.RequestException as e:
    print(f"Could not access API. Code: {e} ")


def user_pages(request):
    per_page = 10
    paginator = Paginator(users, per_page)
    page_number = request.GET.get("page")
    users_page = paginator.get_page(page_number)
    return render(request, "index.html", {"users_page": users_page})


def edit_user(request, id):
    for user in users:
        if user["id"] == id:
            current_user = user
            curr_user_index = users.index(user)

    if request.method == "POST":
        updated_user = {
            "id": id,
            "name": request.POST["name"],
            "age": request.POST["age"],
            "email": request.POST["email"],
        }
        users[curr_user_index] = updated_user
        return redirect("user_pages")

    return render(request, "edit.html", {"user": current_user})


def delete_user(request, id):
    for user in users:
        if user["id"] == id:
            break
    if request.method == "POST":
        users.remove(user)
        return redirect("user_pages")
    return render(request, "confirmDelete.html", {"user": user})
