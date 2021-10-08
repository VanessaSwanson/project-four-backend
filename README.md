General Assembly Project 4: Kollektiv
![](https://lh5.googleusercontent.com/-pOiURiW1xFvf3XAHLvHdY-LRbh3ia-lzYYaVdefpAyz4qBzzVvXfp2nRADWaA4fFiP6Bh4RhX8t7Wrz2A4w3r5TIfQOMRGWvGQ9RTh7ac_L5N7dnTp3Ve0aveCtifuR4lSnsk0=s0)
====================================================================================================================================================================================================

# Table of Contents

1. [Overview](#overview)

2. [Project Brief](#projectbrief)

3. [Kollektiv](#kollektiv)

4. [Getting Started](#gettingstarted)

5. [Process](#process)

    1.[Planning](#planning)

    2.[Backend](#backend)

      1. [Posts](#posts)

      2. [Users](#users)

      3. [Authentication](#authentication)

      4. [Password confirmation](#passwordconfirmation)

    3.[Frontend](#frontend)

     1. [Explore page](#explore)

     2. [Home Page](#home)

     3. [Post Show Page](#post)

     4. [User Show Page](#user)

     5. [React hooks](#reacthooks)

     6. [Messaging](#messaging)

6. [Known Bugs](#bugs)

7. [Wins](#wins)

8. [Challenges](#challenges)

9. [Key Learnings](#learnings)

10. [Future Content](#futurecontent)

Overview <a name="overview"></a>
========

This was my final project as part of the General Assembly immersive Software Engineering course, in which I built an Instagram clone using Django and React.

🔗 [Deployed site](https://kollektiv-sei.netlify.app)

Project Brief <a name="projectbrief"></a>
=============

Build a full stack app using Django and React.

Timeframe: 7 days (although I gave myself an extra 24 hours to continue working on my messaging feature)

Technologies used:

-   React.js

-   React-router-dom

-   Python

-   Django

-   Django REST framework

-   SCSS

-   Bootstrap React

-   pyJWT

-   Axios

-   Git + GitHub

Kollektiv <a name="kollektiv"></a>
=========

For my final project I decided to work on my own, to really test my understanding of building a full stack application from start to finish with Django and React, especially as we had only very recently learned Python, SQL and Django so I really wanted to solidify my learning.

Inspired by the Musée D'Orsay, and their [2020 Instagram artist-in-residence, Jean-Philippe Delhomme](https://news.artnet.com/art-world/musee-dorsay-instagram-artist-residency-1747413), I decided to build an Instagram clone with a twist, by imagining that all of the site's users were famous artists. I called it Kollektiv and used bold, primary Bauhaus colours to fit with the theme.

You can see the deployed site [here](https://kollektiv-sei.netlify.app/) or click the image below, which will take you to a video showing an overview of the site's functionality.

[<img width="883" alt="Screenshot 2021-10-07 at 18 55 20" src="https://user-images.githubusercontent.com/78015278/136437989-89445b29-6a52-4ab2-abe9-e7c40151ca49.png">](https://www.youtube.com/watch?v=NUz4eILoBDM)


Getting Started <a name="gettingstarted"></a>
===============

-   Clone or download the repo

-   Backend:

-   `pipenv shell` to navigate into the virtual environment

-   `python3 manage.py loaddata jwt_auth/seeds.json` to run the users seeds

-   `python3 manage.py loaddata posts/seeds.json` to run the posts seeds

-   `python3 manage.py runserver` to run the server on localhost:8000

-   Frontend:

-   `npm i` to install any dependencies

-   `npm run dev` to launch the client site on localhost:3000

Process <a name="process"></a>
=======

# Planning <a name="planning"></a>
--------

I started by investigating Instagram web (as opposed to the mobile app) to see what each step of the user journey looked like. I used this to build detailed wireframes of each page, and a list of features and functions I wanted to include.

My MVP features included:

-   Users are able to post one photo at a time.

-   Users are able to comment on posts and delete their own comments.

-   Users are able to like and unlike posts.

-   Users are able to follow and unfollow other users.

-   A home page which shows only posts from users that the current user follows.

-   An 'explore' page which shows all posts from across the Kollektiv site, which can be searched and filtered.

-   A user show and personal profile page which shows only posts from the relevant user.

-   Users can edit their profile.

My stretch features included:

-   An image uploader tool for images as opposed to just using a url link in the create post form.

-   The ability for users to add multiple photos to posts, which would then need to be shown using an image carousel.

-   The ability to comment on comments (nested comments).

-   The ability to like comments.

-   Messaging between users.

-   Private accounts.

-   Media query to make the site fit to mobile screens.

Once I had my key features and wireframes, I created an entity relationship diagram (ERD) to map out how I thought my different django models would relate to each other. In the end, my relationships ended up being a bit more simplistic than this, but I thought it would be good to plan for stretch goals to better prepare myself.

![](https://lh3.googleusercontent.com/yTIRLKYT8Ej2AK421QGYYWXKuQRyt3bESL27Bbahp2PPU84AU06XFEKqNbSu4bx8j3nH79gm6mIZ-3LGRtNTGv4EtiDW2pOfkT-zRveP7KBzita9aDxbrAMpZu2LpqrbGItXcZk=s0)

I then built a Trello board, which I would use to track my tasks and keep me on schedule. This is an example of what the Trello board looked like further into the project. As you can see, I had a daily to do and bits to tidy list, as well as a traffic light system while testing the backend requests.

![](https://lh6.googleusercontent.com/nvWkk3DlxLltWYvYqLoJd62NCeqny0qgz1beLhW32NSp7NZEkymmeWAtoy65yugxJ3xXJyv8GVPBfCAar9Mv78RlNhYov2gxI-ieo5kjVcKmp3c7iiKUF5qZ4qVsWQFtOAFZ5iU=s0)

## Backend <a name="backend"></a>

### Posts <a name="posts"></a>

After setting up my backend, I began working on my posts model, which would have a one to many relationship with the comments model, like so:


```
class  Post(models.Model):

   title = models.CharField(max_length=50, blank=True)

   caption = models.TextField(max_length=1000)

   created_at = models.DateTimeField(auto_now_add=True)

   image = models.CharField(max_length=300)

   liked_by = models.ManyToManyField(

       'jwt_auth.User',

       related_name='liked_posts',

       blank=True

   )

   owner = models.ForeignKey(

       'jwt_auth.User',

       related_name='posts_made',

       on_delete=models.CASCADE

   )

   def  __str__(self):

       return  f'{self.title} - {self.id}'

class  Comment(models.Model):

   text = models.TextField(max_length=300)

   created_at = models.DateTimeField(auto_now_add=True)

   post = models.ForeignKey(

       Post,

       related_name='comments',

       on_delete=models.CASCADE

   )

   owner = models.ForeignKey(

       'jwt_auth.User',

       related_name='comments_made',

       on_delete=models.CASCADE

   )

   def  __str__(self):

       return  f'{self.post} - {self.id}'
```


I then created views for posts using Django REST framework for all key requests such as creating, editing and deleting posts, as well as creating and deleting comments, and liking posts (which was a toggle function).

I also created serializers for displaying all necessary data fields for the relevant views, these were updated and added to after creating the user model and testing on the front end, which would inevitably reveal certain details I had forgotten to populate in my serializers.

### Users <a name="users"></a>

Then I moved onto my users, which are always more complicated due to passwords and authentication. I created a custom user model, by extending Django's own AbstractUser class:

```

class  User(AbstractUser):

   full_name = models.CharField(max_length=30)

   email = models.CharField(max_length=50)

   bio = models.TextField(max_length=150)

   profile_image = models.CharField(max_length=300)

   is_private = models.BooleanField(default=False)

   followed_by = models.ManyToManyField(

       'jwt_auth.User',

       related_name='following',

       blank=True,

   )
 ```

The user model had a many to many relationship with itself to represent followers and following. In the final 36 hours of the project, I ended up having some time to spare, so started on my stretch goal of messaging, which meant I then added a one to many relationship of many messages to one user like so:

```
class  Message(models.Model):

   message = models.TextField(max_length=1000)

   created_at = models.DateTimeField(auto_now_add=True)

   sender = models.ForeignKey(

       User,

       related_name='messages_made',

       on_delete=models.CASCADE

   )

   receiver = models.ForeignKey(

       User,

       related_name='messages_received',

       on_delete=models.CASCADE

   )
```

A message could have both one sender and one receiver, which had related names of messages_made and messages_received on the user model.

For the user views, I made use of some of the generic Django views, as well as creating some bespoke views, such as the following view, which worked as a toggle function:

```

class  UserFollowView(APIView):

   ''' Follow / unfollow toggle '''

   permission_classes = (IsAuthenticated, )

   def  post(self, request, user_pk):

       try:

           user_to_follow = User.objects.get(pk=user_pk)

       except  User.DoesNotExist:

           raise  NotFound()

       if  request.user in  user_to_follow.followed_by.all():

           user_to_follow.followed_by.remove(request.user.id)

       else:

           user_to_follow.followed_by.add(request.user.id)

       serialized_user = UserSerializer(user_to_follow)

       return  Response(serialized_user.data, status=status.HTTP_202_ACCEPTED)
```

### Authentication <a name="authentication"></a>

To set up authentication for users - to essentially recreate the secure routing from my previous Express API project - I followed the instructions we were taught in class to create a bespoke piece of middleware for JSON Web Tokens. This was needed because, while Django REST framework comes with a number of authentication methods built in, it doesn't utilise JSON tokens, which works well with the frontend React framework.

First, I installed pyJWT, then I created a new file, authentication.py to write the middleware:

```
class  JWTAuthentication(BasicAuthentication):

   def  authenticate(self, request):

       header = request.headers.get('Authorization')

       if  not  header:

           return  None

       if  not  header.startswith('Bearer'):

           raise  PermissionDenied({'detail': 'Invalid Auth Header'})

       token = header.replace('Bearer ', '')

       try:

           payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

           user = User.objects.get(pk=payload.get('sub'))

       except  jwt.exceptions.InvalidTokenError:

           raise  PermissionDenied({'detail': 'Invalid Token'})

       except  User.DoesNotExist:

           raise  PermissionDenied({'detail': 'User Not Found'})

       return (user, token)
       
 ```

This essentially checks for the authorisation header and throws an error if it is either missing or malformed. If there is a valid authorisation header, the token is extracted and decoded to give us the payload, including the current user's ID. This is returned as a tuple, with the user as the first element and the token as the second.

### Password confirmation <a name="passwordconfirmation"></a>

To check the user password against password confirmation, I then had to build a custom user serializer:

```

class  UserRegisterSerializer(serializers.ModelSerializer):

   password = serializers.CharField(write_only=True)

   password_confirmation = serializers.CharField(write_only=True)

   def  validate(self, data):

       password = data.pop('password')

       password_confirmation = data.pop('password_confirmation')

       if  password != password_confirmation:

           raise  ValidationError({'password_confirmation': 'does not match'})

       try:

           validation.validate_password(password=password)

       except  ValidationError  as  err:

           raise  ValidationError({'password': err.messages})

       data['password'] = make_password(password)

       return  data
```

As you can see, this is quite straightforward and simply checks that the password and password_confirmation fields match, otherwise it throws an error. It then uses Django's built-in validate_password method to check the strength of the password (I commented this out while working on the site to make it easier to test) and Django's make_password method to hash the password before saving to the database.

I tested all of my requests using Insomnia as I went along, installing djangorestframework-camel-case to ensure formatting was correct on both applications, and created seed files for my posts and users apps.

## Frontend <a name="frontend"></a>
--------

### Explore page <a name="explore"></a>

![](https://lh3.googleusercontent.com/4Ktnla7D5KAEhikuSGVxf8_1zlaEIL7q1NbYzI4wtQK2n5L9Am0wI0176kYTcjoPKi2ZOgKIARQWFIko78kgAMwjF_-O2uLTmQ5kkAB94fpf8JBZFICvQuv5d8bvwQaZv_g7m8c=s0)

I started by building the explore page, as this was the simplest data request - a simple get all posts, sorted by the time the post was created. Posts were shown using minimalist postCard components, which linked to the postShow page.

The explore page also includes a search function, which allows users to search by full name, username or post caption, and selected search term buttons in case users need some inspiration.

### Home Page <a name="home"></a>

The home page shows only posts from users that the current logged in user follows, sorted in time order. 

On the right hand side of the page, there is a "Suggestions for you" section, which shows a selection of other Kollektiv users to follow. These suggestions are accounts that are followed by the people that the logged in user follows. This was achieved through pure JavaScript fundamentals, with the array of unique suggestions being created like so using spread operators:

```

 // These lines filter users for your suggestions. It suggests accounts that people you follow 
 are following.

 const  key = 'username'

 const  followingAccounts = []

 const  suggestions = []

 user?.following.map(account  => (

   followingAccounts.push(account)

 ))

 followingAccounts.map(account  => (

   suggestions.push(...account.following)

 ))

 const  arrayUniqueByKey = [...new  Map(suggestions.map(item  =>

   [item[key], item])).values()]
   
   ```

Further down in the JSX, I then clarify that only accounts that the logged in user doesn't already follow should be shown:
```

{arrayUniqueByKey.length > 0 &&

                   arrayUniqueByKey.map(suggestion=>(

                     suggestion.id === user.id || suggestion.followedBy.some(follower  => (follower.id === user.id)) ?

                       ''

                       :

. . .

```

### Post Show Page <a name="post"></a>

![](https://lh4.googleusercontent.com/aI7zFfNzYC7hG7AfcGfl_8Bq0IGsGOQB1AlQG5nR58db5ngR1dGzF8e49ircNJDNg1IEMwMRfJ1gYkNCmkTYGS_t9DFcfLWvy-8fPjFkhzcyyKUItO0pncHg24w6md8mXKFPGZ4=s0)

The post show page is where most of the site's key features take place: commenting, liking, following and, if you are the creator of the post, the ability to delete the post entirely.

I was really proud of myself for being able to get all of these features so neatly onto one page, mimicking the Instagram web app. It was difficult at first to make the page rerender after new requests as they were all taking place at the same url, but this was achieved eventually by awaiting new requests in my various submit functions and setting state again.

As you can see in the screenshot above, the comments section is scrollable, again inspired by the Instagram web app.

### User Show Page <a name="user"></a>

The user show page displays a user's key information, along with a wall of posts that they've created. It conditionally renders, so if it is your own profile, you see an edit profile button, but if it is another user's profile, you see a follow/unfollow button.

I was really pleased with the edit profile form in the end, as I was able to pre-populate it with the user's current information to aid the user experience, including their profile image, allowing them to only edit what is necessary:

![](https://lh6.googleusercontent.com/hCpeoAoocpboh4x1V7ZkA9nRk-kyfn7enAKfN-J3wOfrFhcrNj40hysRbWuQYOtgzI86gg1v1STx2v8kGaOVSiTt7_yCoKjuk95o9fHWrut67EwZf9xlSy_PKtXdplDsIyojhsc=s0)

### React hooks <a name="reacthooks"></a>

We had been taught about React hooks right before the start of Project 4 and given the example of forms as a good use case, so I knew I wanted to include this in my project to get a basic introduction to this useful feature of React.

My useForm hook below allows me to reuse common form functions such as handleChange and handleUploadedImage:

```

function  useForm(intialFormState) {

 const [formData, setFormData] = React.useState(intialFormState)

 const [formErrors, setFormErrors] = React.useState(intialFormState)

 const  handleUploadedImage = (imageUrl, fieldName) => {

   setFormData({ ...formData, [fieldName]:  imageUrl })

 }

 const  handleChange = (event) => {

   const  updatedFormData = { ...formData, [event.target.name]:  event.target.value }

   const  updatedErrors = { ...formErrors, [event.target.name]:  '' }

   setFormData(updatedFormData)

   setFormErrors(updatedErrors)

 }

 return {

   formData,

   handleUploadedImage,

   handleChange,

   setFormData,

   formErrors,

   setFormErrors,

 }

}
```

### Messaging <a name="messaging"></a>

![](https://lh5.googleusercontent.com/T_tkErPr8Y0CXGYbRD84G5OQef1euUHdj6MZWGvrIiF3Xhk6sLOWTArwWQMytRZZsVlJFLCyPaGDF3ZaDNp9p7CiLjk5r_rIXRHAjGO5gEw38N8zUs0LGB30PnuWXCeoIGfip3s=s0)

Messaging was a stretch goal, which I started implementing in the final 36 hours of my project (front and backend). In this time, I was able to get a really basic inbox together, which sorted the logged in user's sent and received messages into separate arrays based on the user they were chatting with - I call these 'threads' or 'chats'.

This involved some really tricky JavaScript. I knew from reading online that I needed a reduce function, but the generic reduce functions I found to sort arrays by certain object keys (in my case username) online were not sufficient as the data I was accessing was so deeply nested. In the interest of time, I sought help from my course tutors and Jack May, the lead teacher ended up giving me and the teaching assistants a master class, the code from which is outlined below:

```

// Reduce function that loops through each message the user has made and sorts them by recipient/threads

 const  currentChatUser = currentUser?.username

 const  createdChats = mergedChats?.reduce((chats, currentMessage) => {

   const  isSender = currentMessage.sender.username === currentChatUser

   const  currentChat = chats.find(chat  => {

     return (

       chat.user.username === currentMessage.receiver.username ||

       chat.user.username === currentMessage.sender.username

     )

   })

   if (!currentChat) {

     const  user = isSender ? currentMessage.receiver : currentMessage.sender

     return [...chats, { user, messages: [{ message:  currentMessage.message, createdAt:  currentMessage.createdAt, sender:  currentMessage.sender,

       receiver:  currentMessage.receiver, isSender }] }]

   }

   return  chats.map(chat  => {

     if (chat !== currentChat) return  chat

      return {

       ...chat,

       messages: [

         ...chat.messages,

         {

           message:  currentMessage.message,

           createdAt:  currentMessage.createdAt,

           sender:  currentMessage.sender,

           receiver:  currentMessage.receiver,

           isSender,

         }

       ],

     }

   })

 }, [])
 
 ```

This provided me with an array of chat objects, each of which included a user object and a messages array. I then sorted this array of chats in alphabetical order by username to display the chats alphabetically down the left hand side of the page, and when mapping the messages in the individual chats, I sorted them by time.

By the project deadline, I had not completed the full messaging functionality, only a very rough version of the inbox, so I gave myself an extra 24 hours. In this time I added the create message functionality in the inbox, a create message button and form on the user show page, and conditional styling in the inbox which displayed messages from the receiver and sender on different sides of the chat (as shown in the screenshot above).

Known Bugs <a name="bugs"></a>
==========

-   These aren't so much bugs as things I would improve with more time:

-   At the moment in the 'more posts by...' section on the user show page, it includes the current post being shown, so I would filter to remove this.

-   As I only gave myself an extra 24 hours to finish messaging, there are lots of things I would improve here:

-   I would show chats in time order rather than alphabetically.

-   I would link to user show pages when clicking on users' profile images on the inbox page (this was surprisingly difficult when using the Bootstrap-React tabs).

-   At the moment, when clicking on the send message button on the user show page, it opens up a send message form. In an ideal world, I would find a way for this button to instead open up the inbox and either create a new chat thread to send a message in, or find an existing chat to join in the inbox, as happens on Instagram web.

Wins <a name="wins"></a>
====

-   I was really pleased with how much I achieved in this solo project in the given time.

-   In particular, it was really satisfying when the post show page was complete with full functionality working smoothly on the same page.

-   It was also really satisfying to achieve my stretch goal of messaging between users as I thought that this wouldn't be possible in the timeframe.

Challenges <a name="challenges"></a>
==========

-   Django definitely took some getting used to having learned it so quickly on the course and I ended up over complicating the backend set up of models, mainly due to being nervous and overly cautious I think. 

-   The sorting and filtering of data was a great JavaScript fundamentals workout! Especially in the messaging.

Key Learnings <a name="learnings"></a>
=============

-   Following this project I feel much more comfortable with Django, python and SQL databases.

-   It was a great introduction to React hooks, even if I only used it very minimally in this project.

Future Content <a name="futurecontent"></a>
==============

-   Allowing users to upload multiple images.

-   Allowing users to upload videos.

-   Enabling nested comments/comment threads.

-   Styling for mobile screens.

-   Improved messaging feature.

-   I'm not sure how one would create the Instagram stories feature exactly, but that would be a really interesting thing to look into for my own learning and development.

