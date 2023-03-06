# Cyber security project

[Assignment](https://cybersecuritybase.mooc.fi/module-3.1)

Simple web application that allows users to create accounts and write publications (containing text) that are visible to everyone logged in to application.
Application has multiple security flaws and fixes are included in the code.


# Project report

REPOSITORY: https://github.com/matiasnisula/cyber-security-project-1 
 

Web application that allows users to create accounts and write publications (containing text) that are visible to everyone logged in to application. 

 

Flaws are from OWASP [top 10 list](https://owasp.org/www-project-top-ten/2017/Top_10.html) 2017. 

 

FLAW 1: SQL injection 

Link: https://github.com/matiasnisula/cyber-security-project-1/blob/main/mysite/messageapp/views.py#L26 

App inserts user input directly to SQL statement and executes it. In addition, statement “cursor.executescript(sql)” allows executing multiple SQL statements. For example, the malicious user can submit input like '); DELETE FROM messageapp_publication; --. Now the SQL statement to be executed is INSERT INTO messageapp_publication (published, publisher_id, content) VALUES ('2023-03-01 11:40:15.290540', 6, ''); DELETE FROM messageapp_publication; --'); This deletes everything from that table, which should not be allowed to do for basic user. 

 

Fixing this is simple. Django offers ORM-tools (Object-relational mapping) which allow safely insert objects to database. Remove or comment out lines 26-29 in views.py and remove comment mark from line: Publication.objects.create(publisher=request.user, content=content) 

 

FLAW 2: Cross site scripting (XSS) 

Link: https://github.com/matiasnisula/cyber-security-project-1/blob/main/mysite/templates/messageFrontPage.html#L25 

Template/html-file that shows all publications trusts input given to it. By default, Django templates escape specific characters which are particularly dangerous to HTML. That offers a good amount of protection from, for example, XSS (Cross site scripting) attacks. When it's turned off, the user can submit input that contains html or/and JavaScript, and it gets executed on other user’s machines that fetch the html-page. For example, someone can submit html-form, something like: 

<form action="add/" method="POST"> 

  <input type="hidden" name="content" value="I didn’t want to post this"/> 

  <input type="submit" value="Don’t' click this!"/> 

</form> 

 

This input is saved to the database table publications. When someone else fetches the html-page, html-form is rendered as it is. If user clicks the submit button, publication containing content “I didn’t want to post this” is sent to the server behalf of the user. This kind of flaw gives the attacker a lot of options. Html-tags <script> [insert JavaScript here] </script> can be used to get JavaScript code to be executed on user’s machine, which can be used to multiple malicious purposes, for example stealing user’s cookies. 

 

The solution to this is just simply change line {{pub.content|safe}} to {{pub.content}} which allows Django to use its character escaping protocol. 

 

FLAW 3: Broken access control 

Link: https://github.com/matiasnisula/cyber-security-project-1/blob/main/mysite/messageapp/views.py#L35 

Application has a functionality for user to delete their own publications. Functionality has a flaw that doesn’t check if the user that added the publication is the one who is deleting it. The delete button is only showing for the user that added the publication, but this does not prevent doing simply GET request to the backend URL host/messages/delete/<publication_id>. 

To fix the problem, the backend needs to check if the user that made the request is the same as the one who added the publication. Remove/comment out the line “publication.delete()” and remove comment marks from below that (“if ((request.user == publication.publisher) publication.delete()”) and from the beginning of the function “@login_required”. 

 

 

FLAW 4: Broken authentication 

Link: https://github.com/matiasnisula/cyber-security-project-1/blob/main/mysite/mysite/views.py#L23 

Application has a functionality for the user to create an account and login to application. Functionality for account creating does not have any restrictions for passwords. It is possible for users to create weak passwords that are relatively easy to crack with brute force. 

To fix this problem, the backend needs to use Django’s built-in signup form “UserCreationForm” and built-in function “authenticate”, which prevents creating an account with most of the weakest passwords. Remove or comment out the signup function and remove comment marks from the other signup function above. 

 

 

FLAW 5: Cross-site Request Forgery (CSRF) 

Link: https://github.com/matiasnisula/cyber-security-project-1/blob/main/mysite/messageapp/views.py#L17 

Application has a functionality for user to add (POST) publications. Function handling requests does not have any CSRF protection. OWASP describes CSRF as follows: “[Cross-Site Request Forgery](https://owasp.org/www-community/attacks/csrf) (CSRF) is an attack that forces an end user to execute unwanted actions on a web application in which they’re currently authenticated.” [1]. Successful CSRF attack usually requires user to perform some kind of action, for example, clicking a malicious link. Let’s imagine a situation where the user is logged in to the application and has received malicious link over email. Clicking the link renders a new html-page, which can contain, for example, html-form, which will make an unwanted POST request to the backend. 

<form action="add/" method="POST"> 

  <input type="hidden" name="content" value="CSRF ATTACK INCOMING"/> 

  <input type="submit" value="Click this to win 100$"/> 

</form> 

This requires user to click button, but it can be made to send content automatically with JavaScript. Because the user was logged in to the application, the user’s browser will include necessary authentication cookies with the request and the backend trusts that the request was made on purpose. 

 

To fix this problem, the backend needs to use Django’s built-in protection for CSRF attacks. Tag {% csrf_token %} needs to be included in the form-element. It’s already there, but the backend ignores it with decoration @csrf_exempt. Removing the decorator (@csrf_exempt) prevents attacks described previously. Now requests (POST) need to contain a secret cookie that server remembers. If an invalid cookie is submitted, server responses with an error message. 
