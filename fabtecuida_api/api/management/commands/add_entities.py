from django.core.management import BaseCommand
import sys,os
import csv
from fabtecuida_api import settings
from fabtecuida_api.api.models import User, Entity

import sys

base_dir = settings.BASE_DIR

class Command(BaseCommand):
	# Show this when the user types help
	help = u"Cargar entidades desde archivo csv"

	# A command must define handle()
	def handle(self, *args, **options):
		
		csv_filepathname= u'%s/fabtecuida_api/excel/consolidado.csv' % base_dir 
		
		dataReader = csv.reader(open(csv_filepathname, 'r', encoding="utf-8"), delimiter=',', quotechar='"')
		
		user = User.objects.get(pk=1)

		
		x = 0
		for row in dataReader:
			if x > 1:
				entity = Entity.objects.create(
					location = row[1] + ',' + row[0],
					name=row[3]
				)

				entity.manager.add(user)

				print("GUARDADO %s" % entity)
			x = x + 1

		self.stdout.write("\n**** Proceso Terminado ****")
