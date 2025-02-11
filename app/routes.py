# app/routes.py
import requests
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils import (load_json_data, save_json_data, sanitize_input, 
                       check_disallowed_words, log_event)
from config import get_config

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def login():
    """
    Display login page and handle login submissions.
    We authenticate the user by checking the account number and password in data.json.
    """
    if request.method == 'POST':
        account_number = sanitize_input(request.form.get('account_number', ''))
        password = sanitize_input(request.form.get('password', ''))

        data = load_json_data()
        user_found = None
        for user in data['users']:
            if user['account_number'] == account_number and user['password'] == password:
                user_found = user
                break

        if user_found:
            session['user'] = user_found['account_number']
            log_event(f"User {user_found['account_number']} logged in.")
            return redirect(url_for('main_bp.dashboard'))
        else:
            flash("Invalid account number or password.", "error")
            log_event(f"Failed login attempt for account: {account_number}", "WARNING")

    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    """ Log out the current user. """
    user = session.pop('user', None)
    if user:
        log_event(f"User {user} logged out.")
    return redirect(url_for('main_bp.login'))

@main_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Show a dashboard page where the user can enter a story theme
    and choose a word count or other parameters.
    """
    if 'user' not in session:
        return redirect(url_for('main_bp.login'))
    return render_template('dashboard.html')

@main_bp.route('/generate-story', methods=['POST'])
def generate_story():
    if 'user' not in session:
        return redirect(url_for('main_bp.login'))

    cfg = get_config()
    data = load_json_data()

    theme = sanitize_input(request.form.get('theme', ''))
    requested_word_count = sanitize_input(request.form.get('word_count', '300'))

    # Validate word count
    try:
        requested_word_count = int(requested_word_count)
    except ValueError:
        requested_word_count = cfg.MAX_STORY_WORDS  # fallback to 300

    if requested_word_count > cfg.MAX_STORY_WORDS:
        requested_word_count = cfg.MAX_STORY_WORDS

    # Check disallowed words in theme
    disallowed_found = check_disallowed_words(theme)
    if disallowed_found:
        flash(f"Theme contains disallowed words: {', '.join(disallowed_found)}", "error")
        log_event(f"Disallowed words detected in theme: {disallowed_found}", "WARNING")
        return redirect(url_for('main_bp.dashboard'))

    # Construct request to DeepInfra API
    url = "https://api.deepinfra.com/v1/openai/chat/completions"  # updated endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg.DEEPINFRA_API_KEY}"
    }
    payload = {
        "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        "messages": [
            {
                "role": "user",
                "content": f"Generate a story with the theme '{theme}' using up to {requested_word_count} words. The story should be at a primary reading level with PM vocabulary."
            }
        ]
    }

    story_text = ""
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError if status != 200
        story_data = response.json()
        story_text = story_data.get("choices", [{}])[0].get("message", {}).get("content", "No story available.")
    except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
        print(f"DeepInfra API error: {e}")  # Debug output
        flash("Failed to generate story. Please try again later.", "error")
        log_event(f"API call error: {e}", "ERROR")
        return redirect(url_for('main_bp.dashboard'))

    # Save story to data.json
    new_story = {
        "user_account": session['user'],
        "theme": theme,
        "content": story_text
    }
    user_account = session.get('user')
    for user in data.get('users', []):
        if user.get('account_number') == user_account:
            user.setdefault('stories', [])
            user['stories'].append(new_story)
            break
    save_json_data(data)

    log_event(f"Story generated for user {session['user']} with theme '{theme}'.")
    return render_template('story.html', story=story_text)