import var

var.items = {'11':{'name':'dirt','solid':True,'type':'solid','life':2,'tile':11},
	'13':{'name':'gold','solid':False,'type':'ore','tile':13,'price':15},
	'14':{'name':'coal','solid':False,'type':'ore','tile':14,'price':2},
	'17':{'name':'meat','solid':False,'type':'food','tile':17,'price':8},
	'18':{'name':'chest','solid':True,'type':'storage','items':[],'tile':18,'price':25},
	'19':{'name':'pickaxe','solid':False,'type':'weapon','damage':3,\
		'status':None,'rank':1,'sharp':True,'tile':19,'price':15},
	'20':{'name':'bronze','solid':False,'type':'ore','tile':20,'price':1},
	'21':{'name':'carrot (seed)','solid':False,'type':'seed','tile':21,'price':2,\
		'growth':0,'growth_max':2,'growth_time':0,'growth_time_max':30,'image_index':0,\
		'images':['i','I','Y'],'makes':22},
	'22':{'name':'carrot','solid':False,'type':'food','tile':22,'price':4,'cook_time':10,\
		'makes':25},
	'23':{'name':'hoe','solid':False,'type':'weapon','damage':1,'recipe':['iron'],\
		'status':None,'material':'iron','speed':6,'rank':1,'sharp':True,'tile':23,'price':9},
	'24':{'name':'stove','solid':False,'type':'stove','tile':24,'price':50,'cooking':None},
	'25':{'name':'steamed carrot','solid':False,'type':'cooked food','tile':25,'price':8},
	'26':{'name':'single bed','solid':False,'type':'bed','owner':None,'tile':26,'price':35},
	'27':{'name':'pot','solid':False,'type':'cup','contains':None,'tile':27,'price':15,
		'volume':0,'volume_max':10,'material':'clay'},
	'28':{'name':'barrel','solid':False,'type':'container','contains':None,'tile':28,'price':40},
	'30':{'name':'forge','solid':False,'type':'forge','tile':30,'price':100,'forging':None,
		'forge_time':0},
	'31':{'name':'iron','solid':False,'type':'ore','tile':31,'price':16}}

var.tile_map = {'0':{'icon':'#','color':['gray','darkgray']},
	'1':{'icon':' ','color':['black','darkgray']},
	'2':{'icon':'.','color':['silver','darkgray']},
	'3':{'icon':'<','color':['white','darkgray']},
	'4':{'icon':'>','color':['white','darkgray']},
	'5':{'icon':' ','color':['white','green']},
	'6':{'icon':';','color':['altlightgreen','lightgreen']},
	'7':{'icon':'\\','color':['lightgreen','altlightgreen']},
	'8':{'icon':';','color':['lightsand','sand']},
	'9':{'icon':',','color':['altlightgreen','green']},
	'10':{'icon':'o','color':['blue','blue']},
	'11':{'icon':';','color':['sand','brown']},
	'12':{'icon':'#','color':['sand','brown']},
	'13':{'icon':'1','color':['sand','gold']},
	'14':{'icon':'c','color':['darkgray','darkergray']},
	'15':{'icon':'#','color':['white','brown']},
	'16':{'icon':'.','color':['brown','sand']},
	'17':{'icon':'F','color':['red','lightsand']},
	'18':{'icon':'#','color':['brown','lightsand']},
	'19':{'icon':'/','color':['silver',None]},
	'20':{'icon':'b','color':['gray','brown']},
	'21':{'icon':'i','color':['sand',None]},
	'22':{'icon':'Y','color':['brown',None]},
	'23':{'icon':'L','color':['silver',None]},
	'24':{'icon':'#','color':['gray','darkergray']},
	'25':{'icon':'i','color':['brown',None]},
	'26':{'icon':'#','color':['white','red']},
	'27':{'icon':'u','color':['brown','darkbrown']},
	'28':{'icon':'8','color':['brown','darkbrown']},
	'29':{'icon':'.','color':['sand','darkishbrown']},
	'30':{'icon':'#','color':['white','black']},
	'31':{'icon':'i','color':['gray','darkgray']}}

var.solid = [0,11,15]
var.blocking = [10]

var.DIRT = [28,29]
var.GRASS = [6,7,9]