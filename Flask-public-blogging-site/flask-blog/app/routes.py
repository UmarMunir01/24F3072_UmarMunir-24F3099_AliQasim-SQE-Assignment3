from flask import Blueprint, render_template, redirect, request, url_for, flash, abort
from app import db
from app.models import Post, Comment
from app.forms import PostForm
from flask_login import login_required, current_user
# from . import main

main = Blueprint('main', __name__)

#app/routes.py

@main.route('/')
def index():
    # show all public posts (exclude private posts by others if using is_private)
    if current_user.is_authenticated:
        # posts = Post.query.order_by(Post.timestamp.desc()).all()
        posts = Post.query.filter(
            db.or_(
                Post.is_private == False,
                Post.author_id == current_user.id
            )
        ).order_by(Post.timestamp.desc()).all()
    else:
        # for anonymous users, hide private posts
        posts = Post.query.filter_by(is_private=False).order_by(Post.timestamp.desc()).all() if hasattr(Post, 'is_private') else Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts, view='all')

@main.route('/my_posts')
@login_required
def my_posts():
    posts = Post.query.filter_by(author_id=current_user.id).order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts, view='mine')

@main.route('/others_posts')
@login_required
def others_posts():
    # exclude current user's posts and (optionally) exclude private posts
    q = Post.query.filter(Post.author_id != current_user.id)
    if hasattr(Post, 'is_private'):
        q = q.filter_by(is_private=False)
    posts = q.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts, view='others')

@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    # comments = post.comments

    # deny access if the post is marked private and current user is not the author
    if getattr(post, 'is_private', False) and (not current_user.is_authenticated or post.author_id != current_user.id):
        abort(404)

    comments = post.comments.order_by(Comment.timestamp.asc()).all() if hasattr(post.comments, 'order_by') else post.comments
    if request.method == 'POST':
        if current_user.is_authenticated:
            content = request.form.get('content').strip()
            if not content:
                flash('Comment cannot be empty.', 'warning')
                # return redirect(url_for('main.post_detail', post_id=post.id))
            else:
                comment = Comment(content=content, post_id=post.id, author_id=current_user.id)
                db.session.add(comment)
                db.session.commit()
                flash('Comment added successfully!', 'success')
                return redirect(url_for('main.post_detail', post_id=post.id))
        else:
            flash('You must be logged in to comment.', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('post_detail.html', post=post, comments=comments)

@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author_id=current_user.id, is_private=form.is_private.data if hasattr(Post, 'is_private') else False)
        db.session.add(post)
        db.session.commit()
        flash('Post created Successfully!', 'success')
        return redirect(url_for('main.post_detail', post_id=post.id))
    return render_template('post_form.html', form=form)