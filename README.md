## The Requirements

1. ### The User Requirements

   - The website should have `three roles` for user instead of than guest
     1. Owner
         - `Add` his mobiles on the website
         - `Show` his mobiles
         - `Delete` his mobiles on the website
         - `Active/Inactive` his own mobiles
         - `Add a Seller` for access some of his mobiles 
         - `Show all the listed mobiles` in the home page
         - `Filtering the listed mobiles` in the home page
     2. Seller
         - `Active/Inactive the available` owner mobiles 
         - `Show all the listed mobiles` in the home page
         - `Filtering the listed mobiles` in the home 
     3. Customer 
         - `Buy mobiles` 
         - `Show all the listed mobiles` in the home page
         - `Filtering the listed mobiles` in the home
     4. Guest
        - `Show all the listed mobiles` in the home page
        - `Filtering the listed mobiles` in the home

   - There is `login` page for Owner, Seller and Customer
   - There is `registration` page for create Owner or Customer account
   - Create Seller account by the owner `each owner just has one seller`
   - The user can `change his own password`
   - The user can `filtering the mobiles` in the home page depend on
      - Price `List the mobiles in range minimum price and maximum price`
      - Category `List all mobiles under this category`
         ```
               X: M1, M2
               | > Y: M3, M4 
               | > Z: M5, M6
     
          Here there is category 'X' has M1, M2 mobiles under it
          also it has two subcategory under it Y, Z which have its own mobiles (M3, M4, M5, M6)
          so when filter by category 'X' we should list all the mobiles on level 'X' and its childrens
          then the result is (M1, M2, M3, M4, M5, M6)
            
         ```
   - Each mobile should have its own `mobile detail page`
   - The customer can `buy any mobile` available in the home page under some conditions
     1. The money in the customer wallet bigger than the mobile price
     2. The amount of a mobile is one or more 
   - The mobile should be Inactive when the amount is zero `especially when the customer buy all the amount of that mobile `
   - The mobiles should be listed in `pagging` for scroll between them not just one page for all mobiles
   - The user can `logout` from his account

2. ### System Requirements
   
   - Clone the repository 
   - Create python virtual environments on the same level of manage.py file
        ```
        python -m venv myenv
        ```
   - Create the requirements.txt file on the same level of manage.py file if not exist
        ```
        asgiref==3.5.2
        Babel==2.10.3
        Django==4.0.6
        django-money==3.0.0
        Pillow==9.2.0
        psycopg2==2.9.3
        py-moneyed==2.0
        pytz==2022.1
        sqlparse==0.4.2
        typing-extensions==4.3.0
        tzdata==2022.1
        ```
   - run this command in the terminal  
        ```
        pip install -r requirements.txt
        ```
   - Create the Dockerfile `optional`
   - You can use this command for create user on your administration page
        ```
        python manage.py createsuperuser
        ```
   - Run this command for open the server connection on localhost
        ```
        python manage.py runserver
        ```
   



