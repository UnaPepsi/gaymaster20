from random import randint,choice

lower_case = "abcdefghijklmnopqrstuvwxyz"
upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = "!#$%&/()=[+*]^|-_:;{}.,<>?¿¡'\"\\"


def pass_gen(lower: bool,upper: bool,number: bool,symbol: bool,long: int):
	if long > 1000:
		return "Why would you need a password that long?"
	options = {}
	password = ""
	options.update({lower_case:lower})
	options.update({upper_case:upper})
	options.update({numbers:number})
	options.update({symbols:symbol})
	for value in list(options):
		if not options.get(value):
			del options[value]
	for i in range(long):
		element = choice(list(options))
		password += element[randint(0,len(element)-1)]
	return password