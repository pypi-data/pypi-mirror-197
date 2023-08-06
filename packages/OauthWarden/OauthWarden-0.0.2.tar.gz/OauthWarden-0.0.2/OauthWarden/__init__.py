from .warden import TokenChecker, Log, check_token

def checktoken(textfile):
    with open(textfile, "r") as f:
        tokens = [line.strip() for line in f]

    checker = TokenChecker(tokens)
    checker.check()
