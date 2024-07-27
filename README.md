# MEAL TRACKING WEB-APP 

## VIDEO DEMO: 

URL - https://youtu.be/kUVQdyd_6Pc

## DESCRIPTION:

The idea of my project was to implement a full stack instance of a website to track people's meals.

### 1. The user

Upon entering the IP of the host server, users will be prompted to either log in or register an account with a valid username, email and password. After doing so, a check is done in the backend to ensure goals for the user have been set, else they will be prompted to do so quickly. Once done, the users can navigate the webpages to start recording their progress in terms of meals.

### 2. The meals

The website would be able to store the meals eaten on specific days, limiting users to **3 meals a day**.
The meals eaten had an **associated nutrition level stored within a table** of the database, containing information like calories, fats, carbs and protein. Each day's or week's nutrition intake can then be calculated for the user and **displayed in different formats on different pages** for the user to see.

### 3. The goals

This leads me to the next idea of helping users plan their nutrition intakes. **Goals can be set** by users upon registration or changed later on, where a **pre-set amount will be prompted** based on the target weight the users input. As users continue to record their daily meals and weights in respective tables, a **line chart can be used to track** the user's nutrition progress within the week, or weight progress within half a year. Of course, the line chart is responsive to any changes within the tracked meals of the user. Not to forget, a **circular progress chart** is shown to help users track their weekly macro-nutrients intake.

### 4. The friends

To motivate users to keep using the web and sticking to their goals, there is the functionality of **adding other users as friends**. A **dropdown** is provided to allow users to easily add other people as friends, and can also be **removed** as easily. These friendships are stored within a many to many table within the database.

### 5. The website

Ultimately, the website created was strongly focused on providing a **smooth and interactive user experience**, making use of **complementary colors, transitions and interactive buttons and features**. Each page is also consistently communicating with the backend to ensure **constant updates and little latency**.  

### 6. The backend

The backend code was split into **3 python files**, one main file for **all flask APIs** used by the font end, one **middleman controller** file for all calculations and ugly logic that needed to be reused or recycled, and one file solely to **communicate with the database**, selecting, inserting, updating or deleting data as requested.