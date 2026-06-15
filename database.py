import sqlite3

DB_PATH = 'resources.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            topic_tags TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            format TEXT NOT NULL,
            url TEXT NOT NULL,
            rating REAL
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM resources')
    if cursor.fetchone()[0] == 0:
        populate_db(cursor)

    conn.commit()
    conn.close()

def populate_db(cursor):
    resources = [
        # Python
        ("Python for Beginners — Python.org",
         "Official Python tutorial covering variables, data types, control flow, functions and modules.",
         "python, programming, basics, variables, functions, beginner, tutorial",
         "Beginner", "Tutorial", "https://docs.python.org/3/tutorial/"),

        ("Python Functions — W3Schools",
         "Guide to defining and calling Python functions, parameters, return values and scope.",
         "python, functions, parameters, return values, scope, beginner",
         "Beginner", "Article", "https://www.w3schools.com/python/python_functions.asp"),

        ("Python Lists and Data Structures — Real Python",
         "Comprehensive guide to Python lists, tuples, dictionaries and sets with examples.",
         "python, lists, data structures, dictionaries, tuples, sets",
         "Beginner", "Tutorial", "https://realpython.com/python-data-structures/"),

        ("Python Object-Oriented Programming — Real Python",
         "Introduction to classes, objects, inheritance and encapsulation in Python.",
         "python, OOP, classes, objects, inheritance, object-oriented",
         "Intermediate", "Tutorial", "https://realpython.com/python3-object-oriented-programming/"),

        ("Advanced Python: Decorators and Generators — CS Dojo",
         "Video tutorial covering lambda functions, decorators, generators and higher-order functions.",
         "python, decorators, generators, lambda, advanced, functions",
         "Advanced", "Video", "https://www.youtube.com/c/CSDojo"),

        # Flask
        ("Flask Quickstart — Flask Documentation",
         "Official Flask quickstart guide covering routing, templates, request handling and responses.",
         "flask, web development, routing, templates, HTTP, Python, web application",
         "Beginner", "Documentation", "https://flask.palletsprojects.com/quickstart/"),

        ("Flask Web Application Tutorial — Real Python",
         "Step-by-step tutorial to build a web application with Flask including forms and databases.",
         "flask, web application, forms, database, Python, tutorial",
         "Intermediate", "Tutorial", "https://realpython.com/flask-by-example-part-1-project-setup/"),

        ("Flask REST API Tutorial — freeCodeCamp",
         "Building RESTful APIs with Flask including GET, POST, PUT and DELETE endpoints.",
         "flask, REST, API, HTTP, endpoints, JSON, web services",
         "Intermediate", "Tutorial", "https://www.freecodecamp.org/"),

        ("Jinja2 Templating — Flask Documentation",
         "Guide to Jinja2 templates in Flask covering template inheritance, variables and control structures.",
         "flask, jinja2, templates, HTML, rendering, frontend",
         "Intermediate", "Documentation", "https://flask.palletsprojects.com/templating/"),

        # Machine Learning
        ("Machine Learning Crash Course — Google",
         "Google's introduction to machine learning concepts including regression, classification and neural networks.",
         "machine learning, neural networks, classification, regression, AI, Google",
         "Beginner", "Tutorial", "https://developers.google.com/machine-learning/crash-course"),

        ("Scikit-learn User Guide",
         "Official documentation covering supervised learning, unsupervised learning, model evaluation and preprocessing.",
         "scikit-learn, machine learning, supervised, classification, clustering, Python",
         "Intermediate", "Documentation", "https://scikit-learn.org/stable/user_guide.html"),

        ("TF-IDF Vectorisation — Scikit-learn",
         "Documentation and examples for TF-IDF text vectorisation using TfidfVectorizer.",
         "TF-IDF, text processing, vectorisation, NLP, natural language processing, scikit-learn",
         "Intermediate", "Documentation", "https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html"),

        ("Cosine Similarity Explained — Towards Data Science",
         "Visual explanation of cosine similarity for measuring similarity between text documents and vectors.",
         "cosine similarity, vectors, NLP, text similarity, machine learning, mathematics",
         "Intermediate", "Article", "https://towardsdatascience.com/"),

        ("Neural Networks — 3Blue1Brown",
         "Visual video series explaining how neural networks learn using gradient descent and backpropagation.",
         "neural networks, deep learning, gradient descent, backpropagation, AI, mathematics",
         "Intermediate", "Video", "https://www.youtube.com/c/3blue1brown"),

        ("Recommender Systems — Towards Data Science",
         "Overview of content-based filtering, collaborative filtering and hybrid recommender system approaches.",
         "recommender systems, content-based filtering, collaborative filtering, recommendation engine, AI",
         "Intermediate", "Article", "https://towardsdatascience.com/"),

        ("Convolutional Neural Networks — Stanford CS231n",
         "Stanford course notes on CNNs for image recognition and computer vision applications.",
         "CNN, convolutional neural networks, image recognition, deep learning, computer vision",
         "Advanced", "Article", "https://cs231n.github.io/"),

        # Databases
        ("SQLite Tutorial — SQLite.org",
         "Official SQLite documentation covering database creation, SQL queries, tables and transactions.",
         "SQLite, database, SQL, queries, tables, relational database",
         "Beginner", "Documentation", "https://www.sqlite.org/docs.html"),

        ("SQL for Beginners — W3Schools",
         "Interactive SQL tutorials covering SELECT, INSERT, UPDATE, DELETE, JOIN and GROUP BY.",
         "SQL, database, queries, SELECT, JOIN, relational database, beginner",
         "Beginner", "Tutorial", "https://www.w3schools.com/sql/"),

        ("Database Design Fundamentals",
         "Introduction to relational database design including ER diagrams, normalisation and schemas.",
         "database design, relational database, ER diagrams, normalisation, schema, SQL",
         "Intermediate", "Tutorial", "https://www.coursera.org/"),

        # Web Development
        ("HTML and CSS Basics — MDN Web Docs",
         "Mozilla's guide to HTML structure, CSS styling, layouts and responsive web design.",
         "HTML, CSS, web development, responsive design, layouts, frontend",
         "Beginner", "Documentation", "https://developer.mozilla.org/en-US/docs/Learn"),

        ("JavaScript Fundamentals — JavaScript.info",
         "Modern JavaScript tutorial covering variables, functions, DOM manipulation and events.",
         "JavaScript, web development, DOM, events, functions, frontend, programming",
         "Beginner", "Tutorial", "https://javascript.info/"),

        ("RESTful API Design",
         "Guide to designing RESTful web services including HTTP methods, status codes and resource naming.",
         "REST API, web services, HTTP, API design, endpoints, JSON, client-server",
         "Intermediate", "Article", "https://restfulapi.net/"),

        # Networking and Cloud
        ("Computer Networking — Khan Academy",
         "Introduction to networking concepts including IP addresses, DNS, TCP/IP and the OSI model.",
         "networking, IP addresses, DNS, TCP/IP, OSI model, computer networks",
         "Beginner", "Video", "https://www.khanacademy.org/computing/computers-and-internet"),

        ("AWS Cloud Fundamentals — AWS Training",
         "Amazon Web Services introduction covering cloud computing, EC2, S3 and core AWS services.",
         "AWS, cloud computing, Amazon Web Services, EC2, S3, cloud architecture",
         "Intermediate", "Tutorial", "https://aws.amazon.com/training/"),

        # Git
        ("Git Basics — Git Documentation",
         "Official Git guide covering repository setup, commits, branches, merging and remote repositories.",
         "git, version control, GitHub, branches, commits, repository",
         "Beginner", "Documentation", "https://git-scm.com/doc"),
    ]

    cursor.executemany('''
        INSERT INTO resources (title, description, topic_tags, difficulty, format, url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', resources)
    print(f"Inserted {len(resources)} resources into database.")

if __name__ == '__main__':
    init_db()
    print("Database initialised successfully.")