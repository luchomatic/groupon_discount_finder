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

def request_min_and_max_values():
	start = input("Ingresá el número mínimo de cupón (por ejemplo 1000): ") or "1000"
	while len(start) != 4:
		print("Asegurate de escribir sólo números y de 4 dígitos de longitud, ejemplo: 4450")
		start = input("Ingresá el número mínimo de cupón (por ejemplo 1000): ") or "1000"
	end = input("Ingresá el número máximo de cupón (por ejemplo 3000): ") or "9999"
	while len(end) != 4:
		print("Asegurate de escribir sólo números y de 4 dígitos de longitud, ejemplo: 5500")
		end = input("Ingresá el número máximo de cupón (por ejemplo 3000): ") or "9999"
	while (int(start) > int(end)):
		print("Asegurate de que el número de inicio sea menor que el de fin")
		start = input("Ingresá el número mínimo de cupón (por ejemplo 1000): ") or "1000"
		end = input("Ingresá el número máximo de cupón (por ejemplo 3000): ") or "9999"
		while len(start) != 4:
			print("Asegurate de escribir sólo números y de 4 dígitos de longitud, ejemplo: 4450")
			start = input("Ingresá el número mínimo de cupón (por ejemplo 1000): ") or "1000"
		while len(end) != 4:
			print("Asegurate de escribir sólo números y de 4 dígitos de longitud, ejemplo: 5500")
			end = input("Ingresá el número máximo de cupón (por ejemplo 3000): ") or "9999"
	values = {}
	values['min'] = start
	values['max'] = end
	return values

def try_code(url):
	login_url = 'https://www.groupon.com.ar/user_sessions/users/login'
	credentials = {
		'username': 'xeki@jbnote.com',
		'password': 'PASSWORD'
	}
	session = requests.Session()
	session.post(login_url, data=credentials)
	response = session.get(url)
	parameters = (dict(parse.parse_qsl(parse.urlsplit(url).query)))
	promo_code = parameters['promo_code']
	if (response.status_code == 200):
		response = session.get(url).json()
		try:
			coupon = "Cupón: " + promo_code + " " + response['adjustments'][0]['name'] + " Precio del groupon con el descuento aplicado: " + response['subtotal']['formattedAmount']
			print ("ENCONTRAMOS UN CÓDIGO PARA TU GROUPON! " + promo_code)
			return coupon
		except KeyError:
			return False
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
	minMaxValues = request_min_and_max_values()
	start = minMaxValues['min']
	end = minMaxValues['max']
	username = input("Ingresá tu email de Groupon: ") or "EMAIL"
	password = input("Ingresá tu contraseña de Groupon: ") or "PASSWORD"
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
	found = False
	for result in results:
		if (result != False):
			found = True
			print(result)
	if (found == False):
		print("Lo sentimos, no encontramos ningún cupón para tu groupon, aquí van algunos consejos para mayor efectividad")
		print("Asegurate de que la cuenta que utilizaste tiene al menos dos días de creada")
		print("En lo posible elegí grupones de la sección 'En tu ciudad'")
		print("En lo posible no elijas cupones de la categoria productos o viajes")