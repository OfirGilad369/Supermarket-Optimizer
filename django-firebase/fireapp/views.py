from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

import pyrebase
import json
from datetime import datetime
import urllib
from collections import defaultdict
import heapq
import skimage.io
from PIL import Image


# Create your views here.
config = {
    "apiKey": "AIzaSyDA8ElLhy4e3iLN0qFJyB8GlvrnICqQE8c",
    "authDomain": "stochasticoptimizationproject.firebaseapp.com",
    "databaseURL": "https://stochasticoptimizationproject-default-rtdb.firebaseio.com",
    "projectId": "stochasticoptimizationproject",
    "storageBucket": "stochasticoptimizationproject.appspot.com",
    "messagingSenderId": "851769269343",
    "appId": "1:851769269343:web:bbb1e50779845911b6cfea",
    "measurementId": "G-CWYM02S504",
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()


def index(request):
    name = database.child('Data').child('Name').get().val()
    stack = database.child('Data').child('Stack').get().val()
    framework = database.child('Data').child('Framework').get().val()

    context = {
        'name': name,
        'stack': stack,
        'framework': framework
    }
    return render(request, 'index.html', context)


def uploadToFirebase(filePath):
    fileName = filePath.split("/")[1]
    storage.child(fileName).put(filePath)

    email = "ofirgila@post.bgu.ac.il"
    password = "Aa123456"
    user = auth.sign_in_with_email_and_password(email, password)
    url = storage.child(fileName).get_url(user['idToken'])
    print(url)

    return url


@csrf_exempt
def Images(request, id=0):
    # Getting images from firebase
    if request.method == 'GET':
        images = database.child('Images').get().val()
        for image in images:
            metadataURL = image['metadata']
            try:
                metadata = urllib.request.urlopen(metadataURL).read().decode('ascii')
            except:
                metadata = '{}'
            image['metadata'] = metadata

            productsURL = image['products']
            try:
                products = urllib.request.urlopen(productsURL).read().decode('ascii')
            except:
                products = '{}'
            image['products'] = products

        return JsonResponse(images, safe=False)

    # Uploading image to firebase
    if request.method == 'POST':
        name = request.POST.get('name')
        image_name = request.POST.get('image_name')
        image = request.FILES.get('image')
        metadata = '{}'
        products = '{}'

        utc = str(datetime.utcnow())
        utc = utc.replace(":", ".")

        # Saving image locally and uploading to firebase
        original_image = skimage.io.imread(image)
        pil_img = Image.fromarray(original_image)
        pil_img.save("ImageUpload/" + utc + "-" + image_name)
        url = uploadToFirebase("ImageUpload/" + utc + "-" + image_name)

        # Creating Metadata txt file
        file1 = open("ImageMetadata/metadata-" + utc + ".txt", "a")
        file1.write(metadata)
        file1.close()

        MetadataURL = uploadToFirebase("ImageMetadata/metadata-" + utc + ".txt")

        # Creating Products txt file
        file2 = open("ImageProducts/products-" + utc + ".txt", "a")
        file2.write(products)
        file2.close()

        ProductsURL = uploadToFirebase("ImageProducts/products-" + utc + ".txt")

        images = database.child('Images').get().val()

        new_data = {
          "metadata": MetadataURL,
          "name": name,
          "products": ProductsURL,
          "url": url
        }

        i = len(images)
        database.child('Images').child(str(i)).set(new_data)

        return JsonResponse("Map Saved", safe=False)

    # Deleting image from firebase
    if request.method == 'DELETE':
        params = request.body.decode()
        params = json.loads(params)
        url = params["url"]

        images = database.child('Images').get().val()

        i = 0
        found_flag = False
        images_length = len(images)
        for image in images:
            imageURL = image['url']
            if imageURL == url:
                found_flag = True

            # If image found, overwriting next images on previous image, and deleting the last one
            if found_flag:
                if i != images_length - 1:
                    next_image_data = database.child('Images').child(str(i + 1)).get().val()

                    metadata = next_image_data['metadata']
                    name = next_image_data['name']
                    products = next_image_data['products']
                    img_url = next_image_data['url']
                    database.child('Images').child(str(i)).child('metadata').set(metadata)
                    database.child('Images').child(str(i)).child('name').set(name)
                    database.child('Images').child(str(i)).child("products").set(products)
                    database.child('Images').child(str(i)).child("url").set(img_url)
                else:
                    database.child('Images').child(str(i)).remove()
            i += 1

        return JsonResponse("Map Deleted", safe=False)


@csrf_exempt
def SaveMetadata(request, id=0):
    # Saving image metadata to firebase
    if request.method == 'POST':
        params = request.body.decode()
        params = json.loads(params)
        url = params["url"]
        metadata = params["metadata"]
        utc = str(datetime.utcnow())
        utc = utc.replace(":", ".")
        # Creating Metadata txt file
        file = open("ImageMetadata/metadata-" + utc + ".txt", "a")
        file.write(metadata)
        file.close()

        MetadataURL = uploadToFirebase("ImageMetadata/metadata-" + utc + ".txt")

        images = database.child('Images').get().val()

        i = 0
        for image in images:
            imageURL = image['url']
            if imageURL == url:
                database.child('Images').child(str(i)).child("metadata").set(MetadataURL)
            i += 1

        return JsonResponse(MetadataURL, safe=False)


@csrf_exempt
def SaveProducts(request, id=0):
    # Saving image product_list to firebase
    if request.method == 'POST':
        params = request.body.decode()
        params = json.loads(params)
        url = params["url"]
        products = params["products"]
        utc = str(datetime.utcnow())
        utc = utc.replace(":", ".")
        # Creating Products txt file
        file = open("ImageProducts/products-" + utc + ".txt", "a")
        file.write(products)
        file.close()

        ProductsURL = uploadToFirebase("ImageProducts/products-" + utc + ".txt")

        images = database.child('Images').get().val()

        i = 0
        for image in images:
            imageURL = image['url']
            if imageURL == url:
                database.child('Images').child(str(i)).child("products").set(ProductsURL)
            i += 1

        return JsonResponse(ProductsURL, safe=False)


@csrf_exempt
def FindPath(request, id=0):
    if request.method == 'POST':
        params = request.body.decode()
        params = json.loads(params)

        solution = params
        solution["Arrows"] = []
        paths_list = find_path(solution)
        print("Algorithm solution:", paths_list)

        for path in paths_list:
            for i in range(len(path) - 1):
                v1 = path[i]
                v2 = path[i + 1]
                solution["Arrows"].append([v1, v2])
                for j, edge in enumerate(solution["Connections"]):
                    if (edge["s"] == v1 and edge["t"] == v2) or (edge["s"] == v2 and edge["t"] == v1):
                        solution["Connections"][j]["color"] = "blue"

        del solution["Products"]

        return JsonResponse(solution, safe=False)


# The algorithm trick:
# 1. Get the order of products that got selected and find the ordered required vertices
# 2. Find the minimal weighted path from the starting point, through the required vertices in their given order
def find_path(data):
    vertices = data['Points']
    edges = data['Connections']
    products_list = data['Products']
    graph = defaultdict(list)

    for edge in edges:
        graph[edge['s']].append(edge['t'])
        graph[edge['t']].append(edge['s'])

    start_vertex = None
    for i, vertex in enumerate(vertices):
        if vertex['color'] == 'green':
            start_vertex = i
            break

    # Required assumption: There are no 2 or more vertices with the same products
    required_vertices = [start_vertex]
    for product in products_list:
        for i, vertex in enumerate(vertices):
            if product in vertex['products']:
                if i not in required_vertices:
                    required_vertices.append(i)

    print("Required vertices list:", required_vertices)
    visited_vertices = [start_vertex]
    paths = []
    last_vertex = start_vertex
    for i in range(len(required_vertices) - 1):
        if required_vertices[i + 1] in visited_vertices:
            print("Vertex: " + str(required_vertices[i + 1]) + " was already visited")
            continue
        min_path = Dijkstra(data, last_vertex, required_vertices[i + 1])[1]
        paths.append(min_path)
        last_vertex = required_vertices[i + 1]

        # Update visited vertices
        visited_vertices = list(set(visited_vertices + min_path))

    return paths


def Dijkstra(data, start, end):
    graph = defaultdict(list)
    for edge in data["Connections"]:
        x = edge['s']
        y = edge['t']
        z = distance_between(data["Points"][x], data["Points"][y])
        graph[x].append((y, z))
        graph[y].append((x, z))

    heap = [(0, start, [])]
    seen = set()
    while heap:
        (cost, node, path) = heapq.heappop(heap)
        if node in seen:
            continue
        path = path + [node]
        seen.add(node)
        if node == end:
            return cost, path
        for n, w in graph[node]:
            heapq.heappush(heap, (cost + w, n, path))

    return float("inf"), []


def distance_between(v1, v2):
    return ((v1['x'] - v2['x']) ** 2 + (v1['y'] - v2['y']) ** 2) ** 0.5
