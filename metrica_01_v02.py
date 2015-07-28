#!/c/Python25 python
import sys, os, numpy #sys, os, PIL, numpy, Image, ImageEnhance
import grass.script as grass
import os

grass.run_command('r.mask',flags='r')
os.chdir(r'E:\data_2015\Ju_coelho\grass_2\txt-saidas')
rast_hex='hex1kmteste2_rast'
mapa_veg='areateste_rast_cat'


"""
neste bloco estou criando uma lista com os valores dos hexagonos
Com isso o algoritimo percorrera todos os heganos armazenando em uma tabela de atributos 
O valor medio das menores distancia dos fragmento, o numero do hexagono e a area em M2


"""
x=grass.read_command('r.stats',input=rast_hex)
y=x.split('\n')
del y[-1]
del y[-1]



txt_hex=open('txt_dist_min.txt','w')
cabecalho='HEXID'',''ISOMEAN'',''Area_M2' ',''DistMinFrag \n'
txt_hex.write(cabecalho)
y_trava=y[200:203]

# esse contadoR auxilia no acumulador, uma vez que preciso saber se eh o primeiro hexagono
contador_hexagono=0





list_map_rm=[]
for i in y_trava:

    
    grass.run_command('g.region',rast=rast_hex)
    
    #mapa hexmask, recebe cada hexago
    expressao1='hexmask=if('+rast_hex+'=='+i+','+rast_hex+',null())'
    grass.mapcalc(expressao1, overwrite = True, quiet = True)
    
    """
    o mapa dist_from_HEX, eh a matriz de distancia gerada a partir do hexagono 
    extraido no passo anterior
    """
    grass.run_command("r.grow.distance", input="hexmask",distance='dist_from_HEX',overwrite = True)
    
    
    
    """
    multiplicando a matriz de distancia pelo mapa binario
    a cada hexagono a matriz muda e o mapa de vegunique_euc tambem.
    Nesse passo os valores das distancias passam para os valores dos
    fragmentos.
    mapa gerado nesse passo: vegunique_euc 
    """
    expressao4='vegunique_euc=areateste_rast_bin*dist_from_HEX'
    grass.mapcalc(expressao4, overwrite = True, quiet = True) 
    
    
    #removendo valores menores que 0 do mapa de vegetacao com valores de distancias
    # mapa gerado nesse passo: vegunique_euc_apoio
    
    
    expressao5='vegunique_euc_apoio=if(vegunique_euc>0,vegunique_euc,null())'
    grass.mapcalc(expressao5, overwrite = True, quiet = True)


    # definindo a regiao para copiar o mapa de vegetacao
    #mapa gerado nesse passo: vegcompltemp 
    grass.run_command('g.region',rast=mapa_veg)
    expressao2="vegcompltemp="+mapa_veg
    grass.mapcalc(expressao2, overwrite = True, quiet = True) 
    
    
    """
    Neste passo foi criado uma lista com os valores de cada fragemto.
    """
    stats_veg=grass.read_command('r.stats',input=mapa_veg)
    
        
    stats_veg_split=stats_veg.split('\n')
    del stats_veg_split[-1]
    del stats_veg_split[-1]
    listmapa_contruir=[]    
    
    #trava
    stats_veg_split=stats_veg_split[0:100]
    cont_frag_veg=0
    
    """
    neste laco o programa ira percorrer por todos os fragmentos, reclassificando um a um com os valores das menores distancia
    Ex: poligono pode ter varios valores, sendo que esse mapa foi gerado a partir de uma multiplicacao da mattriz de distcia euclidiana
    e o mapa binario de fragmentos. Para cada um desse fragmentos prcisamos saber qual eh pixel com o menor valor e reclassificar todo o fragemento com
    com esse valor
    
    """
    for stvg in stats_veg_split:
        
        """
        definindo o tamanho da regiao para criar o mapa de frag mask
        esse mapa mask servira para fechar a janela de processamento apenas para o fragemto da vez.
        mapa gerado nesse processo:veg_mask 
        """ 
        #
        grass.run_command('g.region',rast="vegcompltemp")
        expressao3='veg_mask=if(vegcompltemp=='+stvg+',1,null())'
        grass.mapcalc(expressao3, overwrite = True, quiet = True)
        
        # criando mascara a partir do mapa fragmento
        grass.run_command('r.mask',flags='r')
        grass.run_command('r.mask',input='veg_mask')
        
        #definindo a regiao com mapa fragmento
        grass.run_command('g.region',rast="veg_mask")
        
        """
        Como nossa jabela esta reduzida e a unica area visivel no mento eh
        a area do fragmento, faremos uma extracao do mapa "vegunique_euc_apoio".
        O mapa gerado nesse processo tera a penas os valores visiveis ignorando todo o 
        restante
        mapa criado nesse processo:"'frag_'+stvg+'"
        """
        expressao4='frag_'+stvg+'=vegunique_euc_apoio'
        grass.mapcalc(expressao4, overwrite = True, quiet = True)
        
        #definindo a regiao para extrair o valor mininum
        grass.run_command('g.region',rast='frag_'+stvg)
        univar=grass.read_command('r.univar',map='frag_'+stvg,fs="comma")
        univar_split=univar.split('\n')
        list_map_rm.append('frag_'+stvg)

            
        
        
        """
        Se o tamanho da lista statisticas for menor que zero, significa que 
        o mapa esta vazio, com isso nao executa esse bloco
        Se for maior entra no bloco
        """
        if len(univar_split)!=0:
            
            """
            Extraindo o menor valor de todos os pixels deste fragmento
            """
            
            #subistituindo a string para tranforma pra float
            mim_univar=univar_split[6].replace('minimum: ','')
            
            mim_univar_flt=float(mim_univar)  
            
            # se o valor do frag for maio que zero, retorna o valor do minimo
            expressao5='frag_'+stvg+'min=int(if('+'frag_'+stvg+'!=0,'+`mim_univar_flt`+'))'
            grass.mapcalc(expressao5, overwrite = True, quiet = True)
            
            
            # incrementando a lista para criar o mapa contruido
            listmapa_contruir.append('frag_'+stvg+'min')
            
            #criando a lista para remover no final
            list_map_rm.append('frag_'+stvg+'min')
            
            
        #removendo a mascra    
        grass.run_command('r.mask',flags='r')
     
     
            
    #'mapa_reconstruido', Este bloco faz a juncao de todos os fragmentos ja reclassificados com o valor da menor distancia
    """
    Foi nescessaio criar uma segunda lista de apoio: listmapa_contruir_apoio, na primeira tentativa o programa
    nao aguentou cruzar todos os mapas, foi preciso dividir em etapas
    
    """
    listmapa_contruir_apoio=[]
    x=0
    grass.run_command('g.region',rast=rast_hex)
    listmapa_contruir_apoio=listmapa_contruir
    while(len(listmapa_contruir_apoio)>0):
        if x==0:
            expressao20='mapa_reconstruido='+listmapa_contruir_apoio[x]
            grass.mapcalc(expressao20, overwrite = True, quiet = True)    
            del listmapa_contruir_apoio[x]
            x=x+1
        else:
            listmapa_contruir_apoio_2=listmapa_contruir_apoio[0:3]
            listmapa_contruir_apoio_2.append('mapa_reconstruido')
            grass.run_command('r.patch',input=listmapa_contruir_apoio_2,out='temp',overwrite = True)
            expressao9='mapa_reconstruido=temp'
            grass.mapcalc(expressao9, overwrite = True, quiet = True)   
            #grass.run_command('g.remove', flags='f',rast='temp')
            del listmapa_contruir_apoio[0:3]
        
       
    
    #expressao9='mapa_reconstruido=temp'
    #grass.mapcalc(expressao9, overwrite = True, quiet = True)     
    univar_mapa_contruido=grass.read_command('r.univar',map='temp',fs="comma")
    univar_mapa_contruido_split=univar_mapa_contruido.split('\n') 
    mim_univar_mapa_contruido_split=univar_mapa_contruido_split[6].replace('minimum: ','')
    mim_univar_mapa_contruido_split_flt=int(mim_univar_mapa_contruido_split)
    
    
    
    
    #print mim_univar_mapa_contruido_split_flt
    
    
    
    
    #esse mapa vai guardar o fragmento mais proximo do hexagono para pegar o ncell
    expressao6='frag_min_dis_HEX=if(temp=='+`mim_univar_mapa_contruido_split_flt`+','+`mim_univar_mapa_contruido_split_flt`+',null())'
    grass.mapcalc(expressao6, overwrite = True, quiet = True)    
    
    
    
    
    
    #pegando o Ncel
    univar_Ncel=grass.read_command('r.univar',map='frag_min_dis_HEX',fs="comma")
    univar_Ncel_split=univar_Ncel.split('\n')
    univar_Ncel_split=univar_Ncel_split[5].replace('n: ','')
    mean_univar_flt=int(univar_Ncel_split)
    #print "N pixel = ", mean_univar_flt
    area_ha_frag_mais_prox=30*30
    
    area_ha_frag_mais_prox=area_ha_frag_mais_prox*mean_univar_flt
    
    
    
    
    
    #pagando o mean do mapa geral
    
    univar=grass.read_command('r.univar',map='temp',fs="comma")
    univar_split=univar.split('\n')
    mean_univar=univar_split[9].replace('mean: ','')
    
    mean_univar_flt=float(mean_univar)
    txt_hex.write(i+','+mean_univar+','+`area_ha_frag_mais_prox`+','+`mim_univar_mapa_contruido_split_flt`+'\n')
    grass.run_command('g.remove', flags='f',rast='mapa_reconstruido')
    #for rm in list_map_rm:   
        #grass.run_command('g.remove', flags='f',rast=rm)    

          
txt_hex.close()
#grass.run_command('g.remove', flags='f',rast='hexmask,veg_mask,vegcompltemp,vegunique_euc,vegunique_euc_apoio,dist_from_HEX')
    
    
    
    
    
    
    
    
        
            
    
    
  
  
  
  
  
  
  
  
  
  
  