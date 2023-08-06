# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bcrpy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'bcrpy',
    'version': '0.1.0',
    'description': 'Un cliente API para la extraccion, consulta y analisis de la base de datos BCRPData del Banco Central de Reserva del Peru (BCRP)',
    'long_description': '# bcrpy\n\nUn cliente API para la extraccion, consulta y analisis de la base de datos [BCRPData](https://estadisticas.bcrp.gob.pe/estadisticas/series/) del [Banco Central de Reserva del Peru (BCRP)](https://www.bcrp.gob.pe/) escrito para Python. Este cliente es un _wrapper_ de la [API para Desarrolladores](https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api) del BCRP.\n\n![](img/logo-bcrp.png)\n\n\n\n# Installation and Local Usage\n\nTo import this repository to your local environment and access it (on terminal):\n\n```ruby\nvirtualenv venv\nsource venv/bin/activate\npip install bcrpy\n```\n\n# Examples\n#### [In]\n```ruby\nimport bcrpy\n\nbanc = bcrpy.Marco()\t\t\t# cargar objeto\n\nbanc.get_metadata()\t\t\t# obtener todos los metadatos del BCRPData \nprint(banc.metadata)\t\t# imprimir metadatos obtenidos\n```\n\n#### [Out]\n| | Código de serie      |          Categoría de serie  | ... | Memo Unnamed: 13 |\n| -----------           | -----------           | -----------                |-----------  | -----------  |\n|0 |          PN00001MM |  Sociedades creadoras de depósito |  ... | NaN |        NaN |\n|1 |          PN00002MM |  Sociedades creadoras de depósito |  ... | NaN |        NaN |\n|2 |          PN00003MM |  Sociedades creadoras de depósito |  ... | NaN |        NaN |\n|3 |          PN00004MM |  Sociedades creadoras de depósito |  ... | NaN |        NaN |\n|4 |          PN00005MM |  Sociedades creadoras de depósito |  ... | NaN |        NaN |\n| ... |              ... |                             | ... | ... | ... |        ... |\n| 14853 |      PD39791AM  |      Expectativas Empresariales | ... | NaN |        NaN |\n| 14854  |     PD39792AM  |      Expectativas Empresariales | ... | NaN |        NaN |\n| 14855  |     PD39793AM  |      Expectativas Empresariales | ... | NaN |        NaN |\n| 14856  |     PD39794AM  |      Expectativas Empresariales | ... | NaN |        NaN |\n| 14857  |     PD39795AM  |      Expectativas Empresariales | ... | NaN |        NaN |\n\n#### [In]\n```ruby\nimport bcrpy\n\nbanc = bcrpy.Marco()\t\t\t# cargar objeto\n\n#hacer una consulta del codigo de serie predeterminado de este metodo (actualmente \'PD39793AM\') con el API del BCRPData\nbanc.query()\t\t\t\n\n#hacer otra consulta, pero para el codigo de serie \'PN00015MM\'\nbanc.query(\'PN00015MM\')\t\t\n```\n\n#### [Out] \n\nrunning query for PD39793AM...\n\nPD39793AM es indice 14855 en metadatos\n```json\n{\n        "Código de serie": "PD39793AM",\n        "Categoría de serie": "Expectativas Empresariales",\n        "Grupo de serie": "Expectativas empresariales sectoriales",\n        "Nombre de serie": "Índice de expectativas del sector a 12 meses - Servicios",\n        "Fuente": NaN,\n        "Frecuencia": "Mensual",\n        "Fecha de creación": "2023-02-28",\n        "Grupo de publicación": "Expectativas macroeconómicas y de ambiente empresarial",\n        "Área que publica": "Departamento de Indicadores de la Actividad Economía",\n        "Fecha de actualización": "2023-02-28",\n        "Fecha de inicio": "Abr-2010",\n        "Fecha de fin": "Sep-2022",\n        "Memo": NaN\n}\n```\nrunning query for PN00015MM...\n\nPN00015MM es indice 14 en metadatos\n```json\n{\n        "Código de serie": "PN00015MM",\n        "Categoría de serie": "Sociedades creadoras de depósito",\n        "Grupo de serie": "Cuentas monetarias de las sociedades creadoras de depósito",\n        "Nombre de serie": "Activos Internos Netos - Crédito al Sector Privado - ME (millones US$)",\n        "Fuente": "BCRP",\n        "Frecuencia": "Mensual",\n        "Fecha de creación": "2022-03-24",\n        "Grupo de publicación": "Sistema financiero y empresas bancarias y expectativas sobre condiciones crediticias",\n        "Área que publica": "Departamento de Estadísticas Monetarias",\n        "Fecha de actualización": "2023-02-24",\n        "Fecha de inicio": "Abr-1992",\n        "Fecha de fin": "Sep-2022",\n        "Memo": NaN\n}\n```\n\n#### [In]\n```ruby\nimport bcrpy\nimport matplotlib.pyplot as plt \n\nbanc = bcrpy.Marco()\t#cargar objeto\n\n#escoger los inputs de los datos que se desean extraer del BCRPData (otros datos como banc.idioma (=\'ing\') son predeterminados, pero tambien se pueden cambiar)\nbanc.codigos = [\'PN01288PM\',\'PN01289PM\',\'PN00015MM\']\nbanc.fechaini = \'2020-1\'\nbanc.fechafin = \'2023-1\'\n\nbanc.state_inputs()\t\t\t# mostrar el estado actual de los inputs escogidos \n\ndf = banc.GET(\'GET.csv\')\t# obtener informacion de los inputs escogidos (arriba) con el API del BCRP y guardarlas como un archivo con el nombre \'GET.csv\'\n\n#graficos (plots)\nfor name in df.columns:\n    plt.figure(figsize=(9, 4))\n    banc.plot(df[name],name,\'plot\')\n    plt.show()\nplt.show()\n```\n\n#### [Out]\n\n\nrunning current inputs state...\n\n        self.metadata = \\<vacio>\n        self.codigos = [\'PN01288PM\', \'PN01289PM\', \'PN00015MM\']\n        self.formato = json\n        self.fechaini = 2020-1\n        self.fechafin = 2023-1\n        self.idioma = ing\n\nhttps://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01288PM-PN01289PM-PN00015MM/json/2020-1/2023-1/ing\n\n![](img/Figure_1.png)\n![](img/Figure_2.png)\n![](img/Figure_3.png)\n\n',
    'author': 'andrewrgarcia',
    'author_email': 'garcia.gtr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
