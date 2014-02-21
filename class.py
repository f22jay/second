#!/usr/bin/python 
class book:
	author=''
	name='xxxx'
	pages=0
	price=0
	def __init__(self,pages,price,name):
		self.pages=pages
		self.price=price
		self.namne=name
	def show(self):
		print "price is " ,self.price
		print "pages is " ,self.pages
		print "name is " ,self.name

books=book(360,15,"wori")
books.show()
