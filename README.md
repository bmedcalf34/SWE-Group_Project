# SWE-Group_Project
https://swe-group-project.herokuapp.com/

SWE Project Readme  

Our application is the food app nutrionia which is purposed for the task of providing recipes, nutritional and dietary advice to users. Our application encompasses a multi-page web app that features dietary information, recipe and nutrition look ups. 

<strong> Software Dependencies: </strong>

Please see our repository's requirements.txt for a list of update python libraries and requirements. 

<strong> User Stories Sprint I </strong>

<em> User Story I </em>

Implemented by Maryam Botrus

My revised user story would be for a typical end-user Joe 
Joe is an overweight man who wants to lose weight and is unable to do so. He finds his way to our application and makes an account

Username: Joe password: Lose weight

Joe wants to understand how he can lose weight via dieting so he navigates to the Diet Selection button on the main screen after creating his account.
From this Joe can get suggested meals from either the water weight or lose weight diet recommendations.
Joe is happy with our application and goes on to lose 100 lbs from his new water diet. He also develops acute malnutrition as our diet recommendations are not the best.
This functionality encompasses over 300 lines of code across signup.html, login.html, index.html the required database code in app.py and the diet selection and diet_selection.html screens.

<em> User Story II </em>

Implemented by Maryam Botrus and Able Saw

Michael Phillips (no relation to Michael Phelps) is an Olympic swimmer who cares quite a bit about his macros. He also has poor eyesight and is unable to read food labels. After navigating to the Nutritiona app he wants to be able to count the macros of everything he is eating. Fortunately for Michael he keeps good track of all his ingredients and meals.
Michael visits the front page of the app and navigates to the nutrition menu. From here he searches the calories and nutritional value for 1 whole chicken, an apple and a sack of flour.
Michael then adds the macros in his excel spreadsheet and calculates his vitamin and caloric balance for his daily meal.
With his new found knowledge in hand Michael was able to better track his macros and win the United States gold at the Olympics.

This user story consists of the app.route("/nutrition") method from app.py along with the nutrition.html document and several lines of code on the main page that enable Michael to navigate through

<em> User Story III </em>

Implemented by Shaunniel Reid

Cameron Payne wants him and his wife to eat healthier. He wants to have the ability to eat his favorite foods but still maintain a healthy diet. He finds the Nutritiona Web App and signs up and creates a personal account. He is now able to search for his favorite foods and always finds the healthiest option with the nutrition filter options. He can also save all his favorite foods to view every time he logs back into the site. His wife can also make her own account and search for her favorite foods and save them. Now Cameron Payne and his wife are eating healthier and are still able to enjoy their favorite types of food. The functionality in this user story is made by the @app.route("/login"), @app.route("/logout"), @app.route("/signup"), @app.route("/recipes"), @app.route("/favorite") @app.route("/unfavorite") methods.


<em> User Story IV </em>

Implemented by Ben Medcalf

Stephen wants to get better at cooking from home so that he can eat out less and save money. He doesn't have a great idea how to start so he navigates to the Nutritiona app. From the main page, he is able to login or sign up to a new account so that he can save recipes that he likes. In order to find some recipes, Stephen goes to the "Recipes" section of the app. From here, he can enter an ingredient and an amount of recipes he would like to see. 
Looking into his cupboard, Stephen sees that he has a good amount of potatoes, so he searches for 10 potato recipes. He can then view these recipes and sasve them for later on his account.
This app funcionality is made up of the search.py file, which contains the search algorithm, as well as the signup.html, login.html, index.html, and recipes.html files for signing up, logging in, and navigating to the recipe functionality.

<em> User Story V </em>
   
Implemented by Maryam and Able 

Mitchell wants to plan his meals for the week so that he can organize his schedule and spend less time thinking about what to eat. He found his way to the nutriona app through the miracle of the google search engine. Mitchell navigates to the meal planner where he starts putting in his caloric needs and the type of foods he is interested in. Mitchell is a rather strange man who only eats nuts and so Nutritiona is the perfect app for him as it allows him to search up his favorite nut based dishes like almonds, cashews, water chestnuts ect... The meal suggestions give him calorie and carb counts to help him monitor his diet and meet his weekly caloric needs. Mitchell was very thankful that he found nutritiona so that he could pursue his nut based lifestyle. 

Main Page -> Get a Meal Plan -> Meal Plan Calendar 

<em> User Story VI </em>
   
Implemented by ...


<em> User Story VII </em>
   
Implemented by ...


<em> User Story VIII </em>
   
Implemented by ...
