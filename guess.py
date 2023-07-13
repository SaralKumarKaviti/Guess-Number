from flask import Flask,render_template,request, flash,redirect, url_for, jsonify
from config import client
from models import *
import datetime
import random



app = Flask(__name__)

app.secret_key='mygame'

def show_score():
    attempts_list=[]
    if len(attempts_list) <= 0:
        print("There is currently no high score, it's yours for the taking!")
    else:
        print("The current high score is {} attempts".format(min(attempts_list)))

@app.route("/",methods=['POST','GET'])
def playGame():
    return render_template("start_game.html")

@app.route("/gameRules",methods=['POST','GET'])
def gameRulesPage():
    return render_template('game_rules.html')

@app.route("/userDetails",methods=['POST','GET'])
def userDetailsPage():
    tokenNumber = random.randint(1000,9000)
    gameNumber = "gplayer"+str(tokenNumber)
    random_number = random.randint(1,20)
    name = request.form.get("name")
    createdOn = datetime.datetime.now()
    if request.method=='POST':
        player_details = UserDetails(
            name=name,
            gameNumber=gameNumber,
            randomNumber=random_number,
            createdOn=createdOn
            )
        player_info = player_details.save()
        if player_info:
            return redirect(url_for('playGamePage',gameNumber=gameNumber))
    else:
        return render_template('play_details.html')

@app.route("/playGame/<gameNumber>",methods=['POST','GET'])
def playGamePage(gameNumber):
    get_random_number = UserDetails.objects.get(gameNumber=gameNumber)
    number = request.form.get("number")
    attempts_list=[]    
    random_number=get_random_number.randomNumber
    if request.method=='POST':
        power=random_number*random_number        
        attempts = 0
        show_score()
        def correct():
            print("Nice! You got it!")
            attempts = 0
            attempts += 1
            attempts_list.append(attempts)
            # flash("It took you {} attempts".format(attempts))

        while True:
            if int(number)<=1 or int(number)>20:
                flash("Please Guess a number with in the given range")

            if int(number) == random_number:
                correct()
                return redirect(url_for('gameOverPage'))
                
            elif random_number % 5 == 0:
                if int(number) == random_number:
                    correct()

                elif int(number) > random_number:
                    flash("The number is Divisible by 5, and also less than {}".format(int(number)))
                    attempts += 1

                else:
                    flash("The number is Divisible by 5 ,But grater than {}".format(int(number)))

            elif random_number%2==0:
                if int(number) == random_number:
                    correct()
                elif int(number) > random_number:
                    flash("The number is Divisible by 2, and also less than {}".format(int(number)))
                    attempts += 1
                else:
                    flash("The number is Divisible by 2 ,But grater than {}".format(int(number)))

            elif random_number%3==0:
                if int(number)==random_number:
                    correct()
                elif int(number) > random_number:
                    flash("The number is Divisible by 3, and also less than {}".format(int(number)))
                    attempts += 1

                else:
                    flash("The number is Divisible by 3 ,But grater than {}".format(int(number)))

            elif power == 49:
                flash("The power of the random is 49")
                attempts += 1

            elif random_number ==  11 or 13 or 17 or 19 :
                flash("The number from 1 to 20, Except 2, 3, 5 prime numbers")
                attempts += 1

            elif int(number) > random_number:
                flash("It's Lower !!")
                attempts += 1
            elif int(number) < random_number:
                flash("It's Higher !!")
                attempts += 1
            return redirect(url_for('playGamePage',gameNumber=gameNumber))

    return render_template('guess_number.html')

@app.route("/gameOver",methods=['POST','GET'])
def gameOverPage():
    return render_template('game_over.html')

if __name__ == '__main__':
    app.run(debug=True)
