#Function read_from_shower: Read data from shower. 
def read_from_shower(angle, type_p, number, data):
    filename = 'dlearning_shower/data/MissingAngle'+angle+type_p+'_'+number+'.lgf'
    file = open(filename, 'r')

    for line in file:
    
      if  (data == 'Primary particle' and data in line):
          prim_type = line.split(':')[-1].strip()
          prim_type = prim_type.split('^')[0]
          return prim_type
        
      if  (data == 'Primary energy' and data in line) :
          prim_egy = line.split(':')[-1].strip()
          prim_egy = prim_egy.replace(' ','')
          return prim_egy
 


#Function read_from_table: Read table and extract.         
def read_from_table(angle, type_p, number, table):
     
    tablename = 'MissingAngle'+angle+type_p+'_'+number+'.'+table
    df = pd.read_table(tablename, delim_whitespace = True, skiprows = 32, skipfooter = 1, engine = 'python', header = None)


 
   
