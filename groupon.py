import requests
import sys
from multiprocessing import Pool
from urllib import parse


def prepare_urls(base_url, letter, start, end):
	urls = []
	for i in range(start, end):
		start+= 1
		urls.append(base_url + str(letter) + str(start))
	return urls

def try_code(url):
	login_url = 'https://www.groupon.com.ar/user_sessions/users/login'
	credentials = {
		'username': 'xeki@jbnote.com',
		'password': 'Videocorel12!'
	}
	session = requests.Session()
	session.post(login_url, data=credentials)
	response = session.get(url)
	parameters = (dict(parse.parse_qsl(parse.urlsplit(url).query)))
	promo_code = parameters['promo_code']
	if (response.status_code == 200):
		print ("ENCONTRAMOS UN CÓDIGO PARA TU GROUPON! " + promo_code)
		return promo_code
	else:
		if (promo_code.endswith('0')):
			print ("Aún no encontramos un código válido, código actual: " + promo_code)
	return False

if __name__ == '__main__':
	print ("Encontrá este script actualizado y un tutorial en: https://github.com/luchomatic/groupon_discount_finder")
	print()

	letter = input("Ingresá la letra de cupón que querés probar (letra por defecto L) : ") or "L"
	base_url = input("Pegá la URL de prueba de cupón del groupon que querés(copiá solo hasta promo_code=): ") or "https://www.groupon.com.ar/checkout/breakdowns/foodie-special-burger-hamburguesas-6-10?gift=false&quantity=1&pledge_id=1009104501&promo_code="
	login_url = 'https://www.groupon.com.ar/user_sessions/users/login'
	start = input("Ingresá el número mínimo de cupón (por ejemplo 1000): ") or "1000"
	end = input("Ingresá el número máximo de cupón (por ejemplo 3000): ") or "9999"
	username = input("Ingresá tu email de Groupon: ") or "lucho_mini_mania@hotmail.com"
	password = input("Ingresá tu contraseña de Groupon: ") or "videocorel12"
	procesos = input("AVANZADO - Ingresá la cantidad de procesos que querés que se ejecuten al mismo tiempo (tocar ENTER para dejar el valor por defecto 100): ") or "100"
	credentials = {
		'username': username,
		'password': password
	}
	print("")
	print("Letra: " + letter)
	print("URL de código de groupon: " + base_url)
	print("Número mínimo: " + start)
	print("Número máximo: " + end)
	print("Mail de groupon: " + username)
	print("Contraseña de groupon: " + password)
	print("")
	print ("Listo, ya se están probando los cupónes en tu órden cuando aparezca alguno debajo de este texto, usalo en la web")
	urls = prepare_urls(base_url, letter, int(start), int(end))
	session = requests.Session()
	session.post(login_url, data=credentials)
	p = Pool(int(procesos))
	results = p.map(try_code, urls)
	print ("")
	for result in results:
		if (result != False):
			print(result)