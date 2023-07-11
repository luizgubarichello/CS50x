import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

import time
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    symbols = db.execute("SELECT symbol FROM transactions WHERE id=? GROUP BY symbol", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
    total = cash
    remove_list = []
    for i, symbol in enumerate(symbols):
        shares_sum = db.execute("SELECT SUM(shares) AS sum FROM transactions WHERE id=? AND symbol=?", session["user_id"], symbol["symbol"])
        symbols[i]["shares"] = shares_sum[0]["sum"]
        symbols[i]["price"] = lookup(symbol["symbol"])["price"]
        symbols[i]["value"] = symbols[i]["shares"] * symbols[i]["price"]
        total += symbols[i]["value"]
        symbols[i]["value"] = usd(symbols[i]["value"])
        symbols[i]["price"] = usd(symbols[i]["price"])
        if int(shares_sum[0]["sum"]) <= 0:
            remove_list.append(symbols[i])
    for item in remove_list:
        symbols.remove(item)
    return render_template("index.html", symbols=symbols, cash=usd(cash), grand_total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        quoted = lookup(request.form.get("symbol"))

        # Ensure that the symbol is valid
        if not quoted:
            return apology("Invalid symbol", 400)

        # Ensure n of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide n of shares", 400)

        try:
            shares = float(request.form.get("shares"))
        except ValueError:
            return apology("Shares must be a positive integer", 400)

        # Ensure n of shares is a +int
        if shares != int(shares) or shares < 0:
            return apology("Shares must be a positive integer", 400)

        # Get cash of the current user
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

        # Calcute the price of the shares he is trying to byt
        cart = quoted["price"] * shares

        # Checking if the account balance is enough to buy the desired shares
        # If it isn't enough, don't update the user's balance
        if cart > cash:
            status = False
            return apology("Insufficient Balance", 400)

        # If it is enough, update the users balance
        else:
            cash -= cart
            db.execute("UPDATE users SET cash=? WHERE id=?", cash, session["user_id"])
            status = True

        # Inserting the transaction into db
        db.execute("INSERT INTO transactions (symbol, price, shares, transaction_date, id, status, trans_type) VALUES (?, ?, ?, ?, ?, ?, ?)", quoted["symbol"], quoted["price"], int(shares), time.time(), session["user_id"], status, "buy")

        if status == False:
            return apology("Insufficient Balance", 400)
        else:
            return redirect("/")

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("buy.html")
        

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get transactions history
    t_history = db.execute("SELECT symbol, price, shares, transaction_date FROM transactions WHERE id=?", session["user_id"])

    # Format a little bit
    for t in t_history:
        t["price"] = usd(t["price"])
        t["transaction_date"] = datetime.fromtimestamp(t["transaction_date"]).strftime("%d/%m/%y %H:%M:%S")

    # Render template
    return render_template("history.html", t_history=t_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        symbol = request.form.get("symbol")

        quoted = lookup(symbol)

        if not quoted:
            return apology("Invalid symbol", 400)

        return render_template("quoted.html", quoted=quoted)

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Password must be confirmed
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Checking if username already exists
        un_list = db.execute("SELECT username FROM users")
        for un in un_list:
            if un["username"] == request.form.get("username"):
                return apology("username already exists", 400)

        # Variables for username and password hash
        un = request.form.get("username")
        phash = generate_password_hash(request.form.get("password"))

        # Inserting into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", un, phash)

        # Redirect user to login
        return redirect("/login")

    else:

        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Getting the symbols the user has on his portfolio
    symbols = db.execute("SELECT symbol FROM transactions WHERE id=? GROUP BY symbol", session["user_id"])

    # Case Post
    if request.method == "POST":
        sell_symbol = request.form.get("symbol")
        sell_shares = int(request.form.get("shares"))

        # Ensure positive number of shares
        if sell_shares <= 0:
            return apology("Invalid number of shares", 400)

        # Checking users output
        for i, symbol in enumerate(symbols):

            # If symbol provided is in users portfolio
            if sell_symbol == symbols[i]["symbol"]:

                # Get number of shares and ensure user has enough shares to sell
                shares_sum = db.execute("SELECT SUM(shares) AS sum FROM transactions WHERE id=? AND symbol=?", session["user_id"], symbol["symbol"])
                if sell_shares > shares_sum[0]["sum"]:
                    return apology("Not enough shares owned to sell", 400)

                # Insert transaction into db and update users cash
                cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
                db.execute("INSERT INTO transactions (symbol, price, shares, transaction_date, id, status, trans_type) VALUES (?, ?, ?, ?, ?, ?, ?)", sell_symbol, lookup(symbol["symbol"])["price"], -sell_shares, time.time(), session["user_id"], True, "sell")
                price_sold = db.execute("SELECT price FROM transactions ORDER BY transaction_id DESC LIMIT 1")
                cash += sell_shares * float(price_sold[0]["price"])
                db.execute("UPDATE users SET cash=? WHERE id=?", cash, session["user_id"])

                return redirect("/")

        # If the shares coud not be sold
        return apology("Could not sell your shares", 400)

    # Case get
    elif request.method == "GET":
        remove_list = []
        for i, symbol in enumerate(symbols):
            shares_sum = db.execute("SELECT SUM(shares) AS sum FROM transactions WHERE id=? AND symbol=?", session["user_id"], symbol["symbol"])
            if int(shares_sum[0]["sum"]) <= 0:
                remove_list.append(symbols[i])
        for item in remove_list:
            symbols.remove(item)
        return render_template("sell.html", symbols=symbols)

