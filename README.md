**The requirements:**

1. There are four roles:

    The owner: who can add, delete, filtering, update, show and delete the mobiles

    The seller: who can show and filtering the mobiles, and make inactive for mobiles
    
    The customer: who can buy the available mobiles 
    
    The guest: who can just see the mobiles

2. Add mobiles under categories 
3. Listing the topic mobiles in the main page (/, /home), and making paging 10 mobiles on each page (/listing/?page=<int:page_num>)
4. Listing the mobiles depend on price range - between (a, b) -
5. Listing the mobiles depend on categories
6. Make a detail page for each mobile (/mobile/<int:pk>):
    
    a. Show the name, photo, category, price, size and about the mobile
    
    b. Box for show the amount of the available mobiles   
    
    c. Button to let the customer buy the mobile so the amount will decrease by one, the lowest value is zero he can’t buy if the amount is zero 

7. Registration and login pages for the customers  
8. Convert between coins

