Welcome to the COPE Forum wiki!
# Quick Feature Overview 📑
### Forum: 
* Create, edit, and delete posts
* Posts will display images, pdfs, and videos in slides
* Comment on posts
* Posts are organized by date, can be found through years and months
* Search functionality, can find posts based on text/titles
### Users:
* Create users with different roles (Admin, Creator, Viewer)
* Available content and access to different parts of site are based on current logged in user
* Admins perform all functionality, can see all users and create new users, can set announcement tags for new posts that will show up in specific location on homepage
* Creators cannot manage users, but can manage their own posts
* Viewers can only see posts
* Password reset functionality available in profile or login page

# [Deployment 🚀](https://github.com/acebc-cope-forum/ace-bc/blob/main/documentation/Deployment.md)
Information regarding deployment and running the application

# [Documentation 📚](https://github.com/acebc-cope-forum/ace-bc/blob/main/documentation/Documentation.md)
Explanation of folder structure, what files are for, etc. 

# [Issues 🔍](https://github.com/acebc-cope-forum/ace-bc/blob/main/documentation/Issues.md)
List of known issues/bugs

# [Recommendations 💬](https://github.com/acebc-cope-forum/ace-bc/blob/main/documentation/Recommendations.md)
Features to work on, any miscellaneous recommendations for the project

# Tools/Links 🧰
* Django Documentation: https://docs.djangoproject.com/en/4.1/
* Bootstrap Documentation: https://getbootstrap.com/docs/5.2/getting-started/introduction/
* SQLite:  
To check the SQLite database, you can either use a VSCode extension: https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite  
Or DB Browser: https://sqlitebrowser.org/

# Feature Gallery
### Registration
Users require a role code provided by an admin to sign up for their respective role in the forum
![registration](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/registration.png)
### Home Page
The home page is populated with annoucements pinned at the top and the 10 most recent posts shown below.
![homepage](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/homepage.png)
### Post Creation
Posts can be created with attachments such as Youtube embeds, photos, and PDF files.
![create_post](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/create_post.png)
### Post View
Each post will show the text body as the first card. The next card button will show attachements such as images, Youtube embeds, or PDF files. The comment section is below. Comments can be posted, edited, and replied to. Admin users have the power to remove user comments.
![post_and_comments](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/post_and_comments.png)
### Post Attachments
The default card shown is the post text body. Going to the next card will show the attachments.
![post_attachments_1](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/post_attachments_1.png)
![post_attachments_2](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/post_attachments_2.png)
![post_attachments_3](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/post_attachments_3.png)
### Archives
All posts are sorted by year and month.
![archives_1](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/archives_1.png)
![archives_2](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/archives_2.png)
### Advanced Search Page
In addition to the basic search, Advanced search gives more parameters to find posts.
![advanced_search](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/advanced_search.png)
### Subscription
Users can subscribe to an email newsletter that show recent post summaries. Clicking the button again will unsubscribe the user from the mailing list.
![subscription](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/subscription.png)
### Manage Users Page
Admin users can access this page to manage users, manually register new users, and change the role codes.
![manage_users](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/manage_users.png)
### IT Admin Page
In addition to the Manage Users page, this page can be accessed to change the database.
![django_admin](https://github.com/livictor888/ACE-BC-Forum/blob/main/documentation/images/django_admin.png)


