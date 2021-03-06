import var

var.items = {'11':{'name':'dirt','solid':True,'type':'solid','life':2,'tile':11},
	'13':{'name':'gold','solid':False,'type':'ore','tile':13,'price':15},
	'14':{'name':'coal','solid':False,'type':'ore','tile':14,'price':2},
	'17':{'name':'meat','solid':False,'type':'food','tile':17,'price':8},
	'18':{'name':'chest','solid':False,'type':'storage','items':[],'tile':18,'price':25},
	'19':{'name':'pickaxe','solid':False,'type':'weapon','damage':3,\
		'status':None,'rank':1,'sharp':True,'tile':19,'price':15},
	'20':{'name':'bronze','solid':False,'type':'ore','tile':20,'price':1},
	'21':{'name':'carrot (seed)','solid':False,'type':'seed','tile':21,'price':2,\
		'growth':0,'growth_max':2,'growth_time':0,'growth_time_max':5,'image_index':0,\
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
	'31':{'name':'iron','solid':False,'type':'ore','tile':31,'price':16},
	'32':{'name':'tree','solid':True,'type':'tree','tile':32,'price':-1},
	'33':{'name':'dagger','solid':False,'type':'weapon','damage':4,\
		'status':None,'rank':1,'sharp':True,'material':'steel','tile':19,'price':15}}

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
	'15':{'icon':'#','color':['palebrown','brown']},
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
	'31':{'icon':'i','color':['gray','darkgray']},
	'32':{'icon':'#','color':['brown','darkbrown']},
	'33':{'icon':'#','color':['darkishbrown','darkbrown']},
	'34':{'icon':'.','color':['gray','kindadarkgray2']},
	'35':{'icon':';','color':['gray','kindadarkgray']},
	'36':{'icon':';','color':['sand','lightsand']},
	'37':{'icon':';','color':['sand','lightersand']},
	'38':{'icon':'.','color':['blue','darkerblue']}}

var.color_codes = {'black':(0,0,0),
	'white':(255,255,255),
	'gray':(128,128,128),
	'red':(255,0,0),
	'green':(0,130,0),
	'blue':(0,0,255),
	'darkerblue':(0,0,230),
	'purple':(128,0,128),
	'silver':(192, 192, 192),
	'darkgray':(86, 86, 86),
	'darkergray':(46, 46, 46),
	'altgray':(148, 148, 148),
	'kindadarkgray':(90,90,90),
	'kindadarkgray2':(80,80,80),
	'lightgreen':(0, 150, 0),
	'altlightgreen':(0, 140, 0),
	'palebrown':(255, 197, 115),
	'sand':(255, 197, 138),
	'lightsand':(255, 211, 148),
	'lightersand':(255, 224, 179),
	'brown':(205, 133, 63),
	'darkbrown':(129, 84, 0),
	'darkishbrown':(111,72,0),
	'gold':(253, 233, 16)}

var.solid = [0,11,15,33]
var.blocking = [10,38]

var.WATER = [10,38]
var.DIRT = [28,29]
var.GRASS = [6,7,9]
var.STONE = [1,34,35]