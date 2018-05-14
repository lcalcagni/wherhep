def read_from_shower(angle, type, number, data):
  
  file = open('dlearning_shower/data/MissingAngle'+angle+type+'_'+number+'.lgf', 'r')

  for line in file:
    global prim_type
	global prim_egy
    
    if  (data == 'Primary particle' and data in line):
        prim_type = line.split(':')[-1].strip()
        prim_type = prim_type.split('^')[0]
    return prim_type
        
    if  (data == 'Primary energy' and data in line) :
        prim_egy = line.split(':')[-1].strip()
        prim_egy = prim_egy.replace(' ','')
    return prim_egy

   
