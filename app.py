import random
import string
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# This will store the URL mappings in a dictionary
url_database = {}

# This is a function for creating the short URL
def create_short_url():
    """Create a random 6-character short URL"""
    # This will count ascii letters and also the digits
    characters = string.ascii_letters + string.digits
    # This will generate the random 6 character URL
    return ''.join(random.choice(characters) for _ in range(6))

def commit_short_url(main_url):
    """Shorten the given URL"""
    # URL guidelines
    # Make sure its either: "http://" or "https//"
    if not main_url.startswith(('http://', 'https://')):
        main_url = 'http://' + main_url

    # Make sure if the URL already exits
    for short_url, long_url in url_database.items():
        # This will allow the long URL to be converted into a smaller URL
        if long_url == main_url:
            return short_url

    # Create short URL
    short_url = create_short_url()
    # If and while short url is in the database
    while short_url in url_database:
        # Then create a short URL
        short_url = create_short_url()

    # We can store the URL mapping
    url_database[short_url] = main_url
    return short_url

# This uses the flask library which we imported previously
@app.route('/', methods=['GET', 'POST'])
def point():
    # Initialize these outside the POST condition
    shortened_url = None
    error = None
    main_input = None

    # This will request the method POST
    if request.method == 'POST':
        # This will request the url and strip is to remove any possible whitespace
        main_url = request.form.get('url', '').strip()
        # This will make sure the original url is the same
        main_input = main_url

        if main_url:
            try:
                # Generate short URL
                short_code = commit_short_url(main_url)
                # Construct full short URL
                shortened_url = request.host_url + short_code
            except Exception as e:
                error = "Error occured when creating the URL"
        else:
            error = "Can you enter a valid URL"
    #This will allow the program to detect the html file folder
    return render_template('index.html',
                           shortened_url=shortened_url,
                           error=error,
                           main_input=main_input)
#Simply will direct to the oringal page
@app.route('/<small_code>')
def direct_to_url(small_code):
    """Direct the page to the original URL"""
    original_url = url_database.get(small_code)
    #Important - if the URL has any issues it will let the user know that the link was not found with 404 error
    if original_url:
        return redirect(original_url)
    return "The URL was not found", 404

#This will run the program on port 5000 in a special web browser interface
if __name__ == '__main__':
    #Run it on port 5000 in a local browser through terminal
    app.run(host='0.0.0.0', port=5000, debug=True)








