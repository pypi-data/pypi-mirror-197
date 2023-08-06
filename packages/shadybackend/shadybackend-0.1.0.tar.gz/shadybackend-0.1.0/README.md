# SHADY Stack

As the name implies, this is a less than kosher web stack based of the SWAG
stack. I developed it for my projects as I am in university and web hosting can
be expensive. The shady stack consists of the following:

1. A **S**tatic site hosted (GitHub Pages, GitLab Pages, etc.) 
2. Simplistic pages that communicate to the backend via a already existing web-app's Web
   **H**ooks (Slack, Discord, Gsuit, GitHub Actions, etc.).  
3. An **A**plication Bridge program that can read the calls to the webhooks and
   pass them to the next component. 
4. A Backend **D**eamon that acutely presses the requests from the webhooks and
   updates a local copy of the site tree as needed.  
5. An application that regularly s**Y**ncs the local tree
   with the remote tree served as the static site in step 1.

## Documentation

For more information, see the [official documentation](https://user-1103.github.io/shady-stack/).
