# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this for production

# Sample blog posts data
blog_posts = [
    {
        'id': 1,
        'title': '10 Ways to Reduce Plastic Waste',
        'content': 'Here are practical tips to cut down on plastic in your daily life...',
        'author': 'Eco Team',
        'date': '2023-05-15',
        'image': 'plastic-waste.jpg'
    },
    {
        'id': 2,
        'title': 'Sustainable Gardening Tips',
        'content': 'Learn how to create an eco-friendly garden that supports biodiversity...',
        'author': 'Green Thumb',
        'date': '2023-06-22',
        'image': 'sustainable-garden.jpg'
    }
]

@app.route('/')
def home():
    return render_template('index.html', posts=blog_posts[:3])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=blog_posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    else:
        flash('Post not found', 'error')
        return redirect(url_for('blog'))

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        try:
            electricity = float(request.form.get('electricity', 0))
            gas = float(request.form.get('gas', 0))
            car_mileage = float(request.form.get('car_mileage', 0))
            flights = float(request.form.get('flights', 0))
            
            # Simple carbon footprint calculation (kg CO2)
            carbon_footprint = (electricity * 0.85) + (gas * 2.3) + (car_mileage * 0.4) + (flights * 0.18)
            
            # Eco-friendly tips based on footprint
            tips = []
            if carbon_footprint > 10000:
                tips.append("Consider switching to renewable energy sources for your home.")
                tips.append("Reduce meat consumption - try meatless Mondays!")
            elif carbon_footprint > 5000:
                tips.append("Use public transportation or carpool to reduce emissions.")
                tips.append("Unplug electronics when not in use to save energy.")
            else:
                tips.append("Great job! Share your eco-friendly habits with others.")
                tips.append("Consider planting trees to offset your remaining footprint.")
            
            return render_template('calculator_result.html', 
                                 carbon_footprint=round(carbon_footprint, 2),
                                 tips=tips)
        except ValueError:
            flash('Please enter valid numbers', 'error')
            return redirect(url_for('calculator'))
    
    return render_template('calculator.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Here you would typically save to database or send email
        # For now, we'll just flash a message
        flash(f'Thank you {name}! Your message has been received. We\'ll contact you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)