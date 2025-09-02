#renders to form to input text prompt
# will call generate_video_from_prompt function
# show succes or error message

from flask import Flask,render_template,request,flash,redirect,url_for
import os

from generate_video import generate_video_from_prompt
from dotenv import load_dotenv
app=Flask(__name__)
app.secret_key=os.getenv("GEMINI_KEY")

@app.route('/',methods=['GET','POST'])

def index():
    if request.method=='POST':
        prompt=request.form.get('prompt')
        if not prompt:
            flash("please enter a Prompt!","error")
            return redirect(url_for('index'))
        
        try:
            generate_video_from_prompt(prompt)
            flash("Video generated successfully! Check the Videos folder.","success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error generating video: {str(e)}","error")
            return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs("Videos", exist_ok=True)  # Ensure Videos folder exists
    app.run(debug=True)
