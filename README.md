# Supermarket Optimizer


## Description:

This project is a web application that allows users to create shopping lists and optimize them based on the user's preferences. \
The application will provide the user with the best route to take in the supermarket to minimize the time spent shopping.


## Admin/Debug User Interface:

The admin/debug UI is used for Supermarket Managers to update the store information which include:
- Handling the store layout.
- Managing the products availability and locations around the store.
- Test the application with different scenarios (As the customer would see it).

![AdminUI.png](assets%2FAdminUI.png)


## Customer User Interface:

The customer UI is used for customers to:
- Create a shopping list.
- Set the starting point in the supermarket (which is their current location).
- Active the optimizer to get the best route to take in the supermarket.

![CustomerUI.png](assets%2FCustomerUI.png)


## The Problem:

The problem that this application comes to solves is: \
Finding the shortest path in the supermarket, that goes through all the customer requested products locations.

This problem is also known as a variation of the Traveling Salesperson (TSP) problem which is known as NP-Hard problem and currently there are no efficient algorithms to solve this problem.

One of the available algorithms is `Held Karp algorithm` can find the optimal solution for our problem, but with a runtime of: `𝑶(|𝑽|!∗|𝑽|^𝟐)`. \
But for a web application, this runtime is not acceptable, so we had to find a more efficient algorithm to solve this problem.


## The Solution:

To solve this problem, we have come with a new algorithm: `Optimized Dijkstra`, with a runtime of: `𝑶((𝑬+𝑽)∗𝒍𝒐𝒈(𝑽))`.

Instead of finding the optimal solution, we monitor the order which the customer have selected the products,
and based on that we find the shortest path that: 
1. Start from selected starting.
2. Pass through all the selected products locations in the order they were selected.
3. If the path already passed through the product location, we skip it and move to the next product location.

![Path.png](assets%2FPath.png)


## Key Features:

The application comes with the following key features to help visualize the algorithm solution and provide UI for the user to interact with the application.


### Market Maps:

The market maps are used to display each store layout and can hold the following information:
- Points: The points are the different locations in the store where the products are located.
- Connections: The connections are the paths between the points that the customer can take to move around the store.
- Products: The products are the items that the customer can add to their shopping list.

From this menu, managers can create, update or delete the store maps. \
While customers can only switch between the available store maps.

![Market Maps.png](assets%2FMarket%20Maps.png)


### Product List:

The product list is used to display and filter the available products in the store and holds the following information:
- Name: The name of the product.
- Status: The status of the product (Available/Unavailable).
- Location: The location of the product in the store.

From this menu, managers can add, update or delete products from the store and test the algorithm that and test the algorithm that finds the best route to take in the store. \
While customers can add or remove products from their shopping list and finds the best route to take from the "Find Path" button.

![Product List.png](assets%2FProduct%20List.png)


### Options Bar:

The options bar is used to display the available options that the user can use to interact with the application.

![OptionsBar.png](assets%2FOptionsBar.png)


- `Edit Point Positions (Admin/Debug Only)`:
This option is used to edit the position of the points in the store layout.


- `Edit Point Products (Admin/Debug Only)`:
This option is used to edit the products in the selected point on the store layout. \
![EditPoint.png](assets%2FEditPoint.png)

- `Set Starting Point`:
This option is used to set the starting point in the store layout.

- `Unset Starting Point`:
This option is used to unset the starting point in the store layout.

- `Add Point (Admin/Debug Only)`:
This option is used to add a new point to the store layout.

- `Add Connection (Admin/Debug Only)`:
This option is used to add a new connection between two points in the store layout.

- `Remove Point (Admin/Debug Only)`:
This option is used to remove a point from the store layout.

- `Remove Connection (Admin/Debug Only)`:
This option is used to remove a connection between two points in the store layout.

- `Edit Metadata (Debug Only)`:
This option is used to edit the metadata of the store layout, directly from the JSON which holds all the data. \
![MetaDataEditor.png](assets%2FMetaDataEditor.png)

- `Save Metadata (Admin/Debug Only)`:
This option is used to save the metadata of the store layout, which include the points, connections and products.

- `Clear All (Admin/Debug Only)`:
This option is used to clear all the points, connections and products from the store layout.


## Requirements:

### Angular UI (Frontend)

- `anguler 13.3.0` or lower
- `node.js 18.16.0` or lower
- [package.json](angular-ui%2Fpackage.json)


### Django Firebase (Backend)

- `python3.8` or higher
- [requirements.txt](django-firebase%2Frequirements.txt)
