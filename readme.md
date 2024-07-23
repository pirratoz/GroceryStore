# REST-API Service "Grocery Store"

## Deployment

1. Downloading a project from Github
```sh
git clone https://github.com/pirratoz/GroceryStore
```
2. Populating ENVIRONMENT in docker-compose.yaml. The exception is [minio] (ACCESS_KEY, SECRET_KEY)
3. Certs generate
```sh
openssl genrsa -out ./grocery/certs/jwt-private.pem 2048
openssl rsa -in ./grocery/certs/jwt-private.pem -outform PEM -pubout -out ./grocery/certs/jwt-public.pem
```
4. Raise containers
```sh
docker-compose up
```
5.  Go to the minio-web interface, authenticate, create “bucket”, “accsess_key”, “secret_key”, fill out docker-compose.yaml again and restart containers.

RESTAPI: http://127.0.0.1:8001/docs
MINIO: http://127.0.0.1:9001/login

## Examples

### Create Product
1. Create user with admin role  

\- POST /users/  
\- data={
  "email": "user@example.com",
  "password": "string",
  "role": "admin"
}

2. Authorization using jwt  

\- POST /jwt/auth  
\- data={
  "email": "user@example.com",
  "password": "string"
}

3. Copy "access_token" and authorize yourself in the upper right corner

4. Uploading images for products, categories and subcategories  

\- POST /api/images/

5. Creating a category, image_id (id) must be taken from step 4  

\- POST /categories/  
\- data={
  "title": "Бакалея",
  "slug": "grocery",
  "image_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}

6. Creating a subcategory, image_id must be taken from step 4, category_id from step 5 

\- POST /subcategories/  
\- data={
  "category_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "крупы",
  "slug": "cereals",
  "image_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}

7. Product creation (price 10000 ~ 100.00 RUB, weight 1000 ~ 1kg)

\- POST /products/  
\- data={
  "subcategory_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Гречка",
  "slug": "buckwheat",
  "image_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "price": 10000,
  "weight_gramm": 1000
}

### Working with the cart
1. It is assumed that the user has been created and authorized

2. Add a product to cart  

\- POST /cart/  
\- data={
  "product_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "count": 10
}

3. Updating the quantity of goods

\- POST /cart/  
\- data={
  "product_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "count": 3
}

4. Removing an product from the cart

\- POST /cart/  
\- data={
  "product_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "count": 0
}

5. Emptying the Trash completely

\- DELETE /cart/  

### Getting product information by slug
1. All parameters are slug fields  
\- GET /products/{product}?category={category}&subcategory={subcategory}  


### View with pagination
1. Paginated views are available on the following endpoints:

\- GET /users/  
\- GET /categories/  
\- GET /subcategories/  
\- GET /products/  