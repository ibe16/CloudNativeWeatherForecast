import os
import unittest

import sys
sys.path.append("/home/irene/MEGA/CC2/Practica2/src")
import Api_V1 
app = Api_V1.app.test_client()

class ApiV1Test(unittest.TestCase):
    """Test unitarios para la versión 1 de la API"""

    def test_24hours_endpoint(self):
        """ Comprobamos que la API nos devuelve un OK """

        response = app.get('/servicio/v1/prediccion/hours24')
        self.assertEqual(response.status_code, 200)

    def test_48_hours_endpoint(self):
        """ Comprobamos que la API nos devuelve un OK """

        response = app.get('/servicio/v1/prediccion/hours48')
        self.assertEqual(response.status_code, 200)

    def test_72_hours_endpoint(self):
        """ Comprobamos que la API nos devuelve un OK """

        response = app.get('/servicio/v1/prediccion/hours72')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()