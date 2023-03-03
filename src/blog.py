#!/usr/bin/env python3
"""Declare a Flask blueprint to register blog views.
"""

import flask
from markupsafe import Markup
from werkzeug.exceptions import abort

from db import get_db
from auth import login_required

bp = flask.Blueprint(  # declare new blueprint
    name='blog',
    import_name=__name__,
    template_folder='templates',
    url_prefix='/',
)


@bp.route('/')
def index():
    """Index view of the blog, fetch all blog posts and display them from
    newest to oldest.

    Returns (str): index view
    """
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return flask.render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Blog creation view. Answer a GET request with the creation form.
    Insert new post in db when a POST request occurs and return user to index
    page if everything went right, otherwise to the same view.

    Returns (str): create view or redirect to index page
    """
    tag1 = '<'
    tag2 = '>'

    if flask.request.method == 'POST':
        title = flask.request.form['title']
        body = Markup(flask.request.form['body'])  # use Markup to enable autoescaping
        error = None

        if not title:
            error = 'Title is required.'

        if body.__contains__(tag1 or tag2):
            error = "Pas d'injection svp mdr"

        if error is not None:
            flask.flash(error, 'error')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, flask.g.user["id"])  # la requête est maintenant préparée
            )
            db.commit()
            return flask.redirect(flask.url_for('blog.index'))

            # process the form data here
        return flask.render_template("blog/index.html", title=title, body=body, error=error)

    return flask.render_template('blog/create.html')


def get_post(post_id, check_author=True):
    """Return a blog post from the database from its id.
    If check_author is True, check if the current logged-in user is
    the owner of the post, raising HTTP 403 Forbidden error if they are not.

    Args:
        post_id: the post id to fetch
        check_author (bool): If True, check ownership of the post.
            Default to True.

    Returns: result from the queryset

    Raises:
        werkzeug.exceptions.NotFound: if the post id is not found
        werkzeug.exceptions.Forbidden: if check_author is True and current
            logged-in user is not author of the post
    """
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'  # la requête est maintenant préparée
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (post_id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    if check_author and post['author_id'] != flask.g.user['id']:
        abort(403)

    return post


@bp.route('/update/<int:post_id>', methods=('GET', 'POST'))
@login_required
def update(post_id):
    """Blog post update view. Display update form in the same way as the
    creation form. Answer POST update with an update in the database.

    Args:
        post_id: the id of the post to update

    Returns: update view or a redirect to the index page
    """

    tag1 = '<'
    tag2 = '>'

    post = get_post(post_id)

    if flask.request.method == 'POST':
        title = flask.request.form['title']
        body = Markup(flask.request.form['body'])
        error = None

        if not title:
            error = 'Title is required.'

        if body.__contains__(tag1 or tag2):
            error = "Pas d'injection svp mdr"

        if error is not None:
            flask.flash(error, 'error')
        else:
            db = get_db()
            
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?', (title, body, post_id) # la requête est maintenant préparée
            )
            db.commit()
            return flask.redirect(flask.url_for('blog.index'))

        # process the form data here
        return flask.render_template("blog/index.html", title=title, body=body, error=error)

    return flask.render_template('blog/update.html', post=post)


@bp.route('/delete/<int:post_id>', methods=('POST',))
@login_required
def delete(post_id):
    """POST method to delete a post by its id. Silently fails.

    Args:
        post_id: the post id to delete

    Returns: redirect to the index view
    """
    get_post(post_id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (post_id,))  # la requête est maintenant préparée
    db.commit()
    return flask.redirect(flask.url_for('blog.index'))


@bp.route('/detail/<int:post_id>')
def detail(post_id):
    """Post detail view. Display the blog post alone in a page.

    Args:
        post_id: the post id to display

    Returns: the view of the detailed post

    Raises:
        werkzeug.exceptions.NotFound: if the post id is not found
    """
    post = get_post(post_id, check_author=False)

    return flask.render_template('blog/detail.html', post=post)
