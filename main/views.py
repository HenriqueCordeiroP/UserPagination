import requests
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from UserPagination.settings import API_URL

from .utils import get_user_by_id

# API consumption and global 'users' variable
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
    current_user = get_user_by_id(id, users)

    if current_user is None:
        return redirect("user_pages")

    curr_user_index = users.index(current_user)

    if request.method == "POST":
        users[curr_user_index] = {
            "id": id,
            "name": request.POST["name"],
            "age": request.POST["age"],
            "email": request.POST["email"],
        }
        return redirect("user_pages")

    return render(request, "edit.html", {"user": current_user})


def delete_user(request, id):
    user = get_user_by_id(id, users)
    if user is None:
        return redirect("user_pages")

    if request.method == "POST":
        users.remove(user)
        return redirect("user_pages")
    return render(request, "confirmDelete.html", {"user": user})
