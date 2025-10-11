from flask import Flask
from flask import render_template
from flask import request

app=Flask(__name__)

login_main='''
            
        <div class="container">
        <div class="row">

            <div class="col" >
                <img src="../../static/left_login_img.svg">
            </div>

            <div class="col col-6">

                <form  novalidate>

                    <fieldset>
                        <legend>Login</legend>

                        <label for="username" class="form-label">Username</label>
                        <input type="text" id="username" class="form-control form-control-lg mt-3" required />


                        <label for="password" class="form-label mt-3">Password</label>
                        <input type="password" id="password" class="form-control form-control-lg mt-3" required />


                        <button class="mt-3" type="submit">Submit</button>

                        <p class="mt-3">If you don't have an account, <a href="register"> register </a></p>

                    </fieldset>

                </form>

            </div>
            <div class="col">
            <!--
            <img src="../../static/right_login_img.svg">
            -->
            </div>
        </div>
    </div>

            '''

register_main = '''
                
                 
        <div class="container">
        <div class="row">

            <div class="col" >
                <img src="../../static/left_login_img.svg">
            </div>

            <div class="col col-6">

                <form  novalidate>

                    <fieldset>
                        <legend>Register</legend>

                        <label for="username" class="form-label">Username</label>
                        <input type="text" id="username" class="form-control form-control-lg mt-3" required />


                        <label for="password" class="form-label mt-3">Password</label>
                        <input type="password" id="password" class="form-control form-control-lg mt-3" required />


                        <button class="mt-3" type="submit">Submit</button>

                        <p class="mt-3">Already have an account? <a href="login"> login </a></p>

                    </fieldset>

                </form>

            </div>
            <div class="col">
            <!--
            <img src="../../static/right_login_img.svg">
            -->
            </div>
        </div>
        </div>
         

                    '''


script = '''
                
        const form = document.querySelector("form");

        form.addEventListener('submit', e => {
            if (!form.checkValidity()){
                e.preventDefault()
            }
            form.classList.add('was-validated')
        })

                '''



@app.route("/")
@app.route("/login")
def login():
    return render_template('auth_info/pages.html', page_name="Login",main=login_main, log_active="active")

@app.route("/register")
def register():
    return render_template('auth_info/pages.html', page_name="Register" ,main=register_main, log_active="active")

@app.route("/help")
def help():
    return render_template('auth_info/pages.html', page_name="Help", main="WILL FILL POST DEVELOPMENT", help_active="active")

@app.route("/about")
def about():
    return render_template('auth_info/pages.html', page_name="about", main="A PROJECT WEB APP FOR HOSPITAL MANAGEEMENT, IIT MADRAS", about_active="active")


if __name__=="__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
    
