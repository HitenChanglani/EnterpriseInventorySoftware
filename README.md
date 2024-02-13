# EnterpriseInventorySoftware
This is an implementation of Django REST API framework for Inventory Management. 

# REST API DOCS
The REST APIs are implemented with the authorization token and only authorized requests are served. The authorization token can be obtained by initially calling the login POST endpoint with valid username and password. A new user can be created by calling register POST endpoint. All other API requests need this authorization token in the header. 

## Create New User

This endpoint creates a new authorized user.

### Required fields in form data body

| username | string |
| password | string |
| email    | string | 


### Request
`POST /register/`

`curl --location 'http://127.0.0.1:8000/register/' \
--header 'Cookie: csrftoken=4XcXKlJs2hmpHV1i1yHJAf9bfRcjW4Sy' \
--form 'username="TestUser"' \
--form 'password="TestPassword"' \
--form 'email="testuser@test.com"'`

### Response
`{
    "id": 1,
    "username": "TestUser",
    "email": "testuser@test.com"
}`

## Login 
This endpoint authenticates the username and password and gives an authorization token as the response if the user is authenticated.

### Required fields in form data body
| Key      | Value  |
| -------- | ------ |
| username | string |
| password | string |

### Request
`POST /login/`

`curl --location 'http://127.0.0.1:8000/login/' \
--header 'Cookie: csrftoken=4XcXKlJs2hmpHV1i1yHJAf9bfRcjW4Sy' \
--form 'username="TestUser"' \
--form 'password="TestPasword"'`

### Response
`{
    "token": "a85483e4ee642020924d99888f4928efff59ac46"
}`

## Logout
This endpoint revokes the access for the authorization token provided in the request.

### Required fields in Header

| Key           | Value         |
| ------------- | ------------- |
| Authorization | Token xxxxxxx |

### Request
`POST /logout/`

`curl --location --request POST 'http://127.0.0.1:8000/logout/' \
--header 'Authorization: Token a85483e4ee642020924d99888f4928efff59ac46' \
--header 'Cookie: csrftoken=4XcXKlJs2hmpHV1i1yHJAf9bfRcjW4Sy'`

### Response
`{"message":"Successfully logged out."}`

## Create New Category
This endpoint creates new category for the items.

### Required fields in Header

| Key           | Value         |
| ------------- | ------------- |
| Authorization | Token xxxxxxx |

### Required fields in form data body

| Key  | Value  |
| -----| ------ |
| name | string |

### Request

`POST /items/category/`

`curl --location 'http://127.0.0.1:8000/items/category/' \
--header 'Authorization: Token a85483e4ee642020924d99888f4928efff59ac46' \
--header 'Cookie: csrftoken=4XcXKlJs2hmpHV1i1yHJAf9bfRcjW4Sy' \
--form 'name="drinks"'`

### Response
`{"name":"drinks"}`

## View all Categories
This endpoint returns all the category for the items.

### Required fields in Header

| Key           | Value         |
| ------------- | ------------- |
| Authorization | Token xxxxxxx |

### Request

`GET /items/category/`

`curl --location 'http://127.0.0.1:8000/items/category/' \
--header 'Authorization: Token eee83252db017561cd56c121fdca2eb8eeaf2e66' \
--header 'Cookie: csrftoken=4XcXKlJs2hmpHV1i1yHJAf9bfRcjW4Sy'`

### Response
`[
    {
        "name": "drinks"
    }
]`


## Create new Item
This endpoint creates a new item and stores it in the database

### Required fields in Header

| Key           | Value         |
| ------------- | ------------- |
| Authorization | Token xxxxxxx |


### Required fields in form data body

| Key  | Value  |
| -----| ------ |
| sku | string |
| name | string |
| availableStock | number |
| category | string |
| tags | list of string |


### Request
`POST /items/item/`

`curl --location 'http://127.0.0.1:8000/items/item/' \
--header 'Authorization: Token eee83252db017561cd56c121fdca2eb8eeaf2e66' \
--header 'Cookie: csrftoken=4XcXKlJs2hmpHV1i1yHJAf9bfRcjW4Sy' \
--form 'sku="COKE"' \
--form 'name="Coke"' \
--form 'availableStock="25"' \
--form 'category="drinks"' \
--form 'tags="['\''cold'\'', '\''liquid'\'']"'`

### Response
`{"sku":"COKE","name":"Coke","availableStock":25,"status":"IN_STOCK","category":{"name":"drinks"},"tags":[{"name":"cold"},{"name":"liquid"}],"createdAt":"2024-02-13","updatedAt":"2024-02-13"}`



## View all Items
This endpoint returns all the items when no query parameters are provided

### Required fields in the header

| Key           | Value         |
| ------------- | ------------- |
| Authorization | Token xxxxxxx |

### Request
`GET /items/item/`

`curl --location 'http://127.0.0.1:8000/items/item/' \
--header 'Authorization: Token eee83252db017561cd56c121fdca2eb8eeaf2e66' \
--header 'Cookie: csrftoken=4XcXKlJs2hmpHV1i1yHJAf9bfRcjW4Sy'`

### Response
`[{"sku":"COKE","name":"Coke","availableStock":25,"status":"IN_STOCK","category":{"name":"drinks"},"tags":[{"name":"cold"},{"name":"liquid"}],"createdAt":"2024-02-13","updatedAt":"2024-02-13"}]`


## View filtered items
This API endpoint accepts query parameters for filtering. All the parameters provided are used with a AND clause and the filtered set is returned. 

### Required fields in the header

| Key           | Value         |
| ------------- | ------------- |
| Authorization | Token xxxxxxx |

### Accepted Query Parameters
| Key     | Value |
| -- | -- |
| category | string |
| status | 'IN_STOCK'/'OUT_OF_STOCK'|
| fromDate | date |
| toDate | date |


### Request
`GET /items/item/`

`curl --location 'http://127.0.0.1:8000/items/item/?category=drinks&status=IN_STOCK' \
--header 'Authorization: Token eee83252db017561cd56c121fdca2eb8eeaf2e66' \
--header 'Cookie: csrftoken=4XcXKlJs2hmpHV1i1yHJAf9bfRcjW4Sy'`


### Response
`[{"sku":"COKE","name":"Coke","availableStock":25,"status":"IN_STOCK","category":{"name":"drinks"},"tags":[{"name":"cold"},{"name":"liquid"}],"createdAt":"2024-02-13","updatedAt":"2024-02-13"}]`
