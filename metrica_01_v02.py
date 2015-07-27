#!/c/Python25 python
import sys, os, numpy #sys, os, PIL, numpy, Image, ImageEnhance
import grass.script as grass
import os


os.chdir(r'E:\data_2015\Ju_coelho\grass_2\txt-saidas')
rast_hex='hex1kmteste2_rast'
mapa_veg='areateste_rast_cat'
mapa_eucdist='hex1kmteste2_shp_centroid_rast_mwsi_15Val_euddist'

grass
x=grass.read_command('r.stats',input=rast_hex)
y=x.split('\n')
del y[-1]
del y[-1]



txt_hex=open('txt_dist_min.txt','w')
cabecalho='HEXID'',''EucDistMin \n'
txt_hex.write(cabecalho)
y_trava=y[200:250]
for i in y_trava:

    
    grass.run_command('g.region',rast=rast_hex)
    #expressao1='hexmask=if('+rast_hex+'=='+i+','+rast_hex+',null())'
    
    grass.mapcalc(expressao1, overwrite = True, quiet = True)
    #grass.run_command('r.mask',input='hexmask')
    #grass.run_command('g.region',rast='hexmask')
    
    #expressao2="vegcompltemp="+mapa_veg
    #grass.mapcalc(expressao2, overwrite = True, quiet = True) 
    stats_veg=grass.read_command('r.stats',input=mapa_veg)
    
    stats_veg_split=stats_veg.split('\n')
    del stats_veg_split[-1]
    del stats_veg_split[-1]
    listmapa_contruir=[]
   
    print len(stats_veg_split)
    
    if len(stats_veg_split) != 0:
        for stvg in stats_veg_split:
            print stvg
            #expressao3='vegunique=if(vegcompltemp=='+stvg+',1,null())'
            
            
            #grass.mapcalc(expressao3, overwrite = True, quiet = True) 
            
            #expressao4='vegunique_euc=vegunique*'+mapa_eucdist
            #grass.mapcalc(expressao4, overwrite = True, quiet = True) 
            
            #univar=grass.read_command('r.univar',map='vegunique_euc',fs="comma")
            #univar_split=univar.split('\n')
            #mean_univar=univar_split[9].replace('mean: ','')
            
            #mean_univar_flt=float(mean_univar)
           
            ##reclassificando com o valor da media
            #expressao5='vegunique_euc_mean'+stvg+'=if(vegunique_euc >= 0,'+`mean_univar_flt`+',null())'
            #grass.mapcalc(expressao5, overwrite = True, quiet = True) 
            #listmapa_contruir.append('vegunique_euc_mean'+stvg)
            
          
        #grass.run_command('r.series',input=listmapa_contruir,out='mapa_reconstruido',method='sum',overwrite = True)
        #for rm in listmapa_contruir:   
            #grass.run_command('g.remove', flags='f',rast=rm)    
        #grass.run_command('g.region',rast='mapa_reconstruido')
        #univar=grass.read_command('r.univar',map='mapa_reconstruido',fs="comma")
        #univar_split=univar.split('\n')
        #univar_minimum=univar_split[6].replace('minimum: ','')
        #print univar_minimum
        #txt_hex.write(i+','+univar_minimum+'\n')
        
       
    
    
    
    #grass.run_command('r.mask',flags='r')
    
    
    


txt_hex.close()