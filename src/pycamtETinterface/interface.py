# Loadng libraries
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, GridBox, ButtonStyle, Dropdown
from IPython.display import display
from IPython.display import clear_output

# Loading functions 
from pycamtET import dataFunctions as dFu, plotFunctions as pFu
try:
    from pycamtET import _geodata
except:
    _geodata=False

if _geodata==True:
    from pycamtET import mapFunctions as mFu
    from pycamtET.supportMap import _adm1_d as adm1_d,_adm2_d as adm2_d,_adm_d as adm3_d
    regions = sorted(list(adm1_d.admin1Name.unique())) 
    zones = sorted(list(adm2_d.admin2Name.unique())) 
    districts = sorted(list(adm3_d.admin3Name.unique()))  

DrpDDict = {'station':{'description':'Station:','width':'350px'},
           'year':{'description':'Year:','width':'230px'},
           'season':{'description':'Season:','width':'230px'},
           'month':{'description':'Month:','width':'200px'},
           'dekadal':{'description':'Dekade:','width':'200px'},
           'region':{'description':'Region:','width':'230px'},
           'zone':{'description':'Zone:','width':'230px'},
           'district':{'description':'District:','width':'230px'}}

def DrpDSelect(options,DictSelect):
    DictOpts = DrpDDict[DictSelect]
    DrpD = widgets.Dropdown(options= options, description=DictOpts['description'], value=None, disabled=False, 
                               layout=Layout(width = DictOpts['width']))
    NameWid = widgets.Output()
    
    def on_change(change):
        NameWid.clear_output()   
        with NameWid:
            if change['type'] == 'change' and change['name'] == 'value':
                print(change['new'])
            else:
                display(options[options == change.new])
    DrpD.observe(on_change, names= 'value')
    return DrpD,NameWid

# to implement this below: remove widgetoutput-retrieval from pltBtn etc functions, use this function for any keys needed,
# and supply None to any not needed, and make eg pltBtnMp more flexible to also deal with dekadal, month or season none.
def getWidOutput(*widgetsIn):
    widgetsOut = []
    for widgetIn in widgetsIn:
        if widgetIn == None:
            widgetsOut.append(None)
            continue
        try:
            textIn = widgetIn.outputs[0]['text'].strip()
        except:
            print('Make selections in all drop-down menus before plotting.')
            return [None]*len(widgetsIn)
        if textIn.isnumeric():
            outVal = int(textIn)
        else:
            outVal = textIn
        widgetsOut.append(outVal)
    return widgetsOut

def pltBtn(dfAll,savePath,element,timeperiod,stationWid,yearWid):
    def clicked(pltEL):    
        stationName,year = getWidOutput(stationWid,yearWid)
        if stationName == None:
            return
        dfOne = dFu.locSelect(dfAll,stationName)
        dkData = dFu.timeData(dfOne,element,timeperiod)

        #Display plot
        df,fig = pFu.recentHistoric(dkData,year, savePath)

    plt_btn = widgets.Button(value=False, description='Plot')
    plt_btn.style.button_color = 'darkseagreen'
    plt_btn.on_click(clicked)
    return plt_btn

def pltBtnMp(dfAll,savePath,element,yearWid,seasonWid,monthWid,dekadeWid,regionWid,zoneWid,districtWid):
    def clicked(mpEL):   
        year,season,month,dekadal,region,adm2,adm3 = getWidOutput(yearWid,seasonWid,monthWid,dekadeWid,regionWid,zoneWid,districtWid)
        if year == None:
            return
        
        mapData = dFu.locData(dfAll,element,year=year,season=season,month=month,dekadal=dekadal)

        idwFigs = mFu.idwMap(mapData,region,savePath=savePath)
        idwFigs = mFu.idwMap(mapData,adm2=adm2,savePath=savePath)
        idwFigs = mFu.idwMap(mapData,adm3=adm3,savePath=savePath)

    mp_btn = widgets.Button(value=False, description='Display')
    mp_btn.style.button_color = 'darkseagreen'
    mp_btn.on_click(clicked)
    return mp_btn

def interfaceDk(dfAll,savePath):
    dfMeta = dFu.dataLoad(dfAll.filePath,dataChoice='metadata')
    
    station = sorted(list(dfMeta.STN_Name.unique()))
    yearsN = list(dfAll.sort_values(by=['YEAR'], ascending=False).YEAR.unique())
    seasonsN = sorted(list(dfAll.season.unique()))
    months = list(range(1,13))
    dekades = [1,2,3]
      
    #DISPLAYING DASHBOARD 
    
    # Station Name Selection
    #-----------------------------------------------------------
    stnDrpD,stationNameWid = DrpDSelect(station,'station')
    #======================================================================================
    #-------------------------------------------------------
    # Year Selection
    #-----------------------------------------------------------
    yrsDrpD,yearNeeded = DrpDSelect(yearsN,'year')
    #======================================================================================
    #-------------------------------------------------------
    # Season Selection
    #-----------------------------------------------------------
    ssnDrpD,seasonNeeded = DrpDSelect(seasonsN,'season')    
    #=================================================================================
    #-------------------------------------------------------
    # Month Selection
    #-----------------------------------------------------------   
    monthS,monthNeeded = DrpDSelect(months,'month')
    #-------------------------------------------------------
    # Dekade Selection
    #-----------------------------------------------------------
    dekadeS,dekadeNeeded = DrpDSelect(dekades,'dekadal')
    
    if _geodata==True:
        #-------------------------------------------------------
        # Region Selection
        #-----------------------------------------------------------
        regionDrpD,regionNeeded = DrpDSelect(regions,'region')    
        #-------------------------------------------------------
        # Zone Selection
        #-----------------------------------------------------------
        zoneDrpD,zoneNeeded = DrpDSelect(zones,'zone')        
        #-------------------------------------------------------
        # District Selection
        #-----------------------------------------------------------
        districtDrpD,districtNeeded = DrpDSelect(districts,'district')
    
    #====================================================================================
    #Previous event button 
    prev_button = widgets.Button(description='Previous', icon='backward')
    
    #The text year select display
    year_selectbox = widgets.Text(layout=Layout(width='10%'),value='2015')
    
    #Next event button 
    next_button = widgets.Button( description='Next', icon='forward')
    
    #RadioButton event Interpolation
    interpol_Radio = widgets.RadioButtons(
        description = 'Interpolation',
        options=['IDW Method', 'Kriging Method'],
        value='IDW Method', 
        layout={'width': 'max-content'},
        disabled=False
    )
    interpol_Radio
    
    #Plotting rf event button
    plt_rfbtn = pltBtn(dfAll,savePath,'PRECIP','dekadal',stationNameWid,yearNeeded)
    
    #Plotting tmax event button
    plt_tmaxbtn = pltBtn(dfAll,savePath,'TMPMAX','dekadal',stationNameWid,yearNeeded)
    
    #Plotting tmin event button
    plt_tminbtn = pltBtn(dfAll,savePath,'TMPMIN','dekadal',stationNameWid,yearNeeded)
        
    if _geodata==True:
        #==================================================================
        #Maping rf event button
        mp_rfbtn = pltBtnMp(dfAll,savePath,'PRECIP',yearNeeded,None,monthNeeded,dekadeNeeded,regionNeeded,zoneNeeded,districtNeeded)
        
        #Maping tmax event button
        mp_tmaxbtn = pltBtnMp(dfAll,savePath,'TMPMAX',yearNeeded,None,monthNeeded,dekadeNeeded,regionNeeded,zoneNeeded,districtNeeded)

        #Maping tmin event button
        mp_tminbtn = pltBtnMp(dfAll,savePath,'TMPMIN',yearNeeded,None,monthNeeded,dekadeNeeded,regionNeeded,zoneNeeded,districtNeeded)

        check_boxEth = widgets.Checkbox(value=False, description='Ethiopia', icon='check')
    
    #Label 
    label_iniSt = widgets.HTML("<b>Station Selection</b>")
    label_iniPlot = widgets.HTML("<b>Dekadal Rainfall, Maximum Temperature and Minimum Temperature Plotting</b>")
    label_iniHistRF = widgets.HTML("<b>Historical, Actual, Mean and Anomaly Dekadal Rainfall Distribution</b>")
    label_iniHistTMax = widgets.HTML("<b>Historical, Actual, Mean and Anomaly Dekadal Maximum Temperature Distribution</b>")
    label_iniHistTMin = widgets.HTML("<b>Historical, Actual, Mean and Anomaly Dekadal Minimum Temperature Distribution</b>")
    
    label_iniIniMap = widgets.HTML("<b>Initial Setting</b>")
    label_iniMap = widgets.HTML("<b>Dekadal Rainfall, Maximum Temperature and Minimum Temperature Map Analysis</b>")
    label_iniMapRF = widgets.HTML("<b>Actual, Mean and % of Normal Dekadal Rainfall</b>")
    label_iniMapTMax = widgets.HTML("<b>Actual, Mean and Anomaly Dekadal Maximum Temperature</b>")
    label_iniMapTMin = widgets.HTML("<b>Actual, Mean and Anomaly Dekadal Minimum Temperature</b>")
    
    #Defining a layout with tabs. 
    
    tab1P = VBox(children=[HBox(children=[label_iniHistRF]), HBox(children=[plt_rfbtn])])
    tab2P = VBox(children=[HBox(children=[label_iniHistTMax]), HBox(children=[plt_tmaxbtn])])
    tab3P = VBox(children=[HBox(children=[label_iniHistTMin]), HBox(children=[plt_tminbtn])])
    
    if _geodata==True:
        tab1M = VBox(children=[HBox(children=[label_iniMapRF]),HBox(children=[prev_button, year_selectbox, next_button, mp_rfbtn])])
        tab2M = VBox(children=[HBox(children=[label_iniMapTMax]),HBox(children=[prev_button, year_selectbox, next_button, mp_tmaxbtn])])
        tab3M = VBox(children=[HBox(children=[label_iniMapTMin]),HBox(children=[prev_button, year_selectbox, next_button, mp_tminbtn])])
    
    #=============================================================================================
    #Creating the tab instance with tabs
    tabPlot = widgets.Tab(children=[tab1P, tab2P, tab3P], layout=Layout(width = '880px'))
    tabPlot.set_title(0, 'Rainfall')
    tabPlot.set_title(1, 'Maximum Temp.')
    tabPlot.set_title(2, 'Minimum Temp.')
    
    if _geodata==True:
        tabMap = widgets.Tab(children=[tab1M, tab2M, tab3M], layout=Layout(width = '880px'))
        tabMap.set_title(0, 'Rainfall')
        tabMap.set_title(1, 'Maximum Temp.')
        tabMap.set_title(2, 'Minimum Temp.')
    
    #=========================================================================================
    # Plot GridBox
    plotGrid = GridBox(children=[stnDrpD, yrsDrpD],
            layout=Layout(
                width='auto',
                height='auto',
                grid_template_columns='370px 300px 280px',
                grid_template_rows='50px',
                )
           )
    
    plotGrid
    
    if _geodata==True:
        # Map GridBox
        mapGrid = GridBox(children=[check_boxEth, regionDrpD, zoneDrpD, districtDrpD, yrsDrpD, monthS, dekadeS, interpol_Radio],
                layout=Layout(
                    width='auto',
                    height='auto',
                    grid_template_columns='220px 220px 220px 250px',
                    grid_template_rows='50px 50px'
                )
               )
        mapGrid
    
    #The form contain VBox and HBox
    form_items1 = [ HBox(children=[label_iniSt]),
                    HBox(children=[plotGrid]),
                    HBox(children=[label_iniPlot]),
                    HBox(children=[tabPlot]),
                  ]
       
    form1 = VBox(form_items1, layout=Layout(
        width = '880px',
        align_items='center'
        ))
    
    if _geodata==True:
        form_items2 = [ HBox(children=[label_iniIniMap]),
                        HBox(children=[mapGrid]),
                        HBox(children=[label_iniMap]),
                        VBox(children=[tabMap])
                     ]

        form2 = VBox(form_items2, layout=Layout(
            width = '950px',
            align_items='center'
            ))
    
    #Adding the forms to accordion
    if _geodata==False:
        accordion = widgets.Accordion(children=[form1])
    else:
        accordion = widgets.Accordion(children=[form1,form2])
        accordion.set_title(1, 'Precipitation, Maximum Temperature and Minimum Temperature Map Analysis')
    accordion.set_title(0, 'Precipitation, Maximum Temperature and Minimum Temperature Plotting')
    print(_geodata)
    return accordion

def interfaceMonth(dfAll,dfWind,savePath):
    dfMeta = dFu.dataLoad(dfAll.filePath,dataChoice='metadata')
    
    station = sorted(list(dfMeta.STN_Name.unique()))
    yearsN = list(dfAll.sort_values(by=['YEAR'], ascending=False).YEAR.unique())
    seasonsN = sorted(list(dfAll.season.unique()))
    months = list(range(1,13))
    dekades = [1,2,3]

    #DISPLAYING DASHBOARD 
    
    # Station Name Selection
    #-----------------------------------------------------------
    stnDrpD,stationNameWid = DrpDSelect(station,'station')
    #======================================================================================
    #-------------------------------------------------------
    # Year Selection
    #-----------------------------------------------------------
    yrsDrpD,yearNeeded = DrpDSelect(yearsN,'year')
    #=================================================================================
    #-------------------------------------------------------
    # Month Selection
    #-----------------------------------------------------------
    monthS,monthNeeded = DrpDSelect(months,'month')
    #-------------------------------------------------------
    # Region Selection
    #-----------------------------------------------------------
    if _geodata==True:
        regionDrpD,regionNeeded = DrpDSelect(regions,'region')
        #-------------------------------------------------------
        # Zone Selection
        #-----------------------------------------------------------
        zoneDrpD,zoneNeeded = DrpDSelect(zones,'zone')        
        #-------------------------------------------------------
        # District Selection
        #-----------------------------------------------------------
        districtDrpD,districtNeeded = DrpDSelect(districts,'district')
    #====================================================================================
    #Previous event button 
    prev_button = widgets.Button(description='Previous', icon='backward')
    prev_button
    
    #The text year select display
    year_selectbox = widgets.Text(layout=Layout(width='10%'),value='2015')
    year_selectbox
    
    #Next event button 
    next_button = widgets.Button( description='Next', icon='forward')
    next_button
    
    #RadioButton event Interpolation
    interpol_Radio = widgets.RadioButtons(
        description = 'Interpolation',
        options=['IDW Method', 'Kriging Method'],
        value='IDW Method', 
        layout={'width': 'max-content'},
        disabled=False
    )
    interpol_Radio
    
    #Plotting rf event button
    #check_boxGrid = widgets.Checkbox(value = False, description='Grid', icon='check')
    #check_boxGrid
   
    def clicked(pltRf):    
        stationName,year = getWidOutput(stationNameWid,yearNeeded)
        if stationName == None:
            return
            
        dfOne = dFu.locSelect(dfAll,stationName)
       
        # Display selected element
        monthRF = dFu.timeData(dfOne,'PRECIP','month')
        monthRD = dFu.timeData(dfOne,'RD','month')
        yearRF = dFu.timeData(dfOne,'PRECIP','year')
    
        #Display plot
        #rfAllAnom = pFu.yearAnom(dkRF)
        rfAllAnom = pFu.yearAnom(yearRF)
        monthRFrecHis,fig6 = pFu.recentHistoric(monthRF,year,savePath)
        monthRFrecHis,fig7 = pFu.recentHistoric(monthRD,year,savePath)
        
    plt_rfbtn = widgets.Button(value=False, description='Plot')
    plt_rfbtn.style.button_color = 'darkseagreen'
    plt_rfbtn.on_click(clicked)
   
    #Plotting tmax event button
    plt_tmaxbtn = pltBtn(dfAll,savePath,'TMPMAX','month',stationNameWid,yearNeeded)    
    
    #Plotting tmin event button    
    plt_tminbtn = pltBtn(dfAll,savePath,'TMPMIN','month',stationNameWid,yearNeeded)
    
    #Plotting Windrose event button
    def clicked(pltWinrs):
        # Display selected station
        stationName,year,month = getWidOutput(stationNameWid,yearNeeded,monthNeeded)
        if stationName == None:
            return   
            
        df = dfWind
    
        wind = df[df.EG_EL == 'WINSPD'].drop_duplicates(subset=['STN_Name','dateTime']).set_index(['STN_Name','dateTime']).rename(columns={'value':'WINSPD'}).get(['season','seasonyear','dk','WINSPD'])
        wind.loc[:,'WINDIR'] = df[df.EG_EL == 'WINDIR'].drop_duplicates(subset=['STN_Name','dateTime']).set_index(['STN_Name','dateTime']).rename(columns={'value':'WINDIR'}).get(['WINDIR'])
        wind = wind.reset_index()
    
        #Display plot
        fig_winros=pFu.windRose(wind,stationName,year,month=month,savePath=savePath)
    
    plt_winrsbtn = widgets.Button(value=False, description='Plot')
    plt_winrsbtn.style.button_color = 'darkseagreen'
    plt_winrsbtn.on_click(clicked)

    if _geodata==True:
        #Maping rf event button
        def clicked(mpRf):
            year,month,region,adm2,adm3 = getWidOutput(yearNeeded,monthNeeded,regionNeeded,zoneNeeded,districtNeeded)
            if year == None:
                return
            
            mapmonRF = dFu.locData(dfAll,'PRECIP',year=year,month=month)
            mapmonRD = dFu.locData(dfAll,'RD',year=year,month=month)

            idwFigs = mFu.idwMap(mapmonRF,region,savePath=savePath)
            idwFigs = mFu.idwMap(mapmonRF,adm2=adm2,savePath=savePath)
            idwFigs = mFu.idwMap(mapmonRF,adm3=adm3,savePath=savePath)
            idwFigs = mFu.idwMap(mapmonRD,region,savePath=savePath)

        mp_rfbtn = widgets.Button(value=False, description='Display')
        mp_rfbtn.style.button_color = 'darkseagreen'
        mp_rfbtn.on_click(clicked)

        #Maping tmax event button       
        mp_tmaxbtn = pltBtnMp(dfAll,savePath,'TMPMAX',yearNeeded,None,monthNeeded,None,regionNeeded,zoneNeeded,districtNeeded)

        #Maping tmin event button
        mp_tminbtn = pltBtnMp(dfAll,savePath,'TMPMIN',yearNeeded,None,monthNeeded,None,regionNeeded,zoneNeeded,districtNeeded)

        check_boxEth = widgets.Checkbox(value=False, description='Ethiopia', icon='check')

    #Label 
    label_iniSt = widgets.HTML("<b>Station Selection</b>")
    label_iniPlot = widgets.HTML("<b>Monthly Rainfall, Maximum Temperature and Minimum Temperature Plotting</b>")
    label_iniHistRF = widgets.HTML("<b>Historical, Actual, Cumulative, Mean and Anomaly Monthly Rainfall Distribution</b>")
    label_iniHistTMax = widgets.HTML("<b>Historical, Actual, Mean and Anomaly Monthly Maximum Temperature Distribution</b>")
    label_iniHistTMin = widgets.HTML("<b>Historical, Actual, Mean and Anomaly Monthly Minimum Temperature Distribution</b>")
    label_iniWindrs = widgets.HTML("<b>Windrose Ploting </b>")
    
    if _geodata==True:
        label_iniIniMap = widgets.HTML("<b>Initial Setting</b>")
        label_iniMap = widgets.HTML("<b>Monthly Rainfall, Maximum Temperature and Minimum Temperature Map Analysis</b>")
        label_iniMapRF = widgets.HTML("<b>Actual, Mean and % of Normal Monthly Rainfall</b>")
        label_iniMapTMax = widgets.HTML("<b>Actual, Mean and Anomaly Monthly Maximum Temperature</b>")
        label_iniMapTMin = widgets.HTML("<b>Actual, Mean and Anomaly Monthly Minimum Temperature</b>")
    
    #Defining a layout with tabs. 
    
    tab1P = VBox(children=[HBox(children=[label_iniHistRF]), HBox(children=[plt_rfbtn])])
    tab2P = VBox(children=[HBox(children=[label_iniHistTMax]), HBox(children=[plt_tmaxbtn])])
    tab3P = VBox(children=[HBox(children=[label_iniHistTMin]), HBox(children=[plt_tminbtn])])
    
    if _geodata==True:
        tab1M = VBox(children=[HBox(children=[label_iniMapRF]),HBox(children=[prev_button, year_selectbox, next_button, mp_rfbtn])])
        tab2M = VBox(children=[HBox(children=[label_iniMapTMax]),HBox(children=[prev_button, year_selectbox, next_button, mp_tmaxbtn])])
        tab3M = VBox(children=[HBox(children=[label_iniMapTMin]),HBox(children=[prev_button, year_selectbox, next_button, mp_tminbtn])])

    #=============================================================================================
    #Creating the tab instance with tabs
    tabPlot = widgets.Tab(children=[tab1P, tab2P, tab3P], layout=Layout(width = '880px'))
    tabPlot.set_title(0, 'Rainfall')
    tabPlot.set_title(1, 'Maximum Temp.')
    tabPlot.set_title(2, 'Minimum Temp.')
    
    if _geodata==True:
        tabMap = widgets.Tab(children=[tab1M, tab2M, tab3M], layout=Layout(width = '880px'))
        tabMap.set_title(0, 'Rainfall')
        tabMap.set_title(1, 'Maximum Temp.')
        tabMap.set_title(2, 'Minimum Temp.')
    
    #=========================================================================================
    # Plot GridBox
    plotGrid = GridBox(children=[stnDrpD, yrsDrpD],
            layout=Layout(
                width='auto',
                height='auto',
                grid_template_columns='370px 280px',
                grid_template_rows='50px',
                )
           )
    
    plotGrid
    
    # Plot Windros Gridbox
    plotGridWin = GridBox(children=[stnDrpD, yrsDrpD, monthS, plt_winrsbtn],
            layout=Layout(
                width='auto',
                height='auto',
                grid_template_columns='220px 220x',
                grid_template_rows='50px 50px'
                )
           )
    
    plotGridWin
    
    # Map GridBox
    if _geodata==True:
        mapGrid = GridBox(children=[check_boxEth, regionDrpD, zoneDrpD, districtDrpD, yrsDrpD, monthS, interpol_Radio],
                layout=Layout(
                    width='auto',
                    height='auto',
                    grid_template_columns='220px 220px 220px 250px',
                    grid_template_rows='50px 50px'
                )
               )
        mapGrid
    
    #The form contain VBox and HBox
    form_items1 = [ HBox(children=[label_iniSt]),
                    HBox(children=[plotGrid]),
                    HBox(children=[label_iniPlot]),
                    HBox(children=[tabPlot]),
                  ]
       
    form1 = VBox(form_items1, layout=Layout(
        width = '880px',
        align_items='center'
        ))
    
    if _geodata==True:
        form_items2 = [ HBox(children=[label_iniIniMap]),
                        HBox(children=[mapGrid]),
                        HBox(children=[label_iniMap]),
                        VBox(children=[tabMap])
                     ]

        form2 = VBox(form_items2, layout=Layout(
            width = '950px',
            align_items='center'
            ))

    form_items3 = [ HBox(children=[label_iniWindrs]),
                    HBox(children=[plotGridWin])
                 ]
       
    form3 = VBox(form_items3, layout=Layout(
        width = '950px',
        align_items='center'
        ))
    
    form_items4 = [
                 ]
       
    form4 = HBox(form_items4, layout=Layout(
        width = '950px',
        align_items='center'
        ))
    
    #Adding the forms to accordion
    if _geodata==True:
        AccChildren = [form1,form2,form3,form4]
        AccPos = [0,1,2,3]
    else:
        AccChildren = [form1,form3,form4]
        AccPos = [0,None,1,2]
    accordion = widgets.Accordion(children=AccChildren)
    accordion.set_title(AccPos[0], 'Precipitation, Maximum Temperature and Minimum Temperature Plotting')
    if _geodata==True:
        accordion.set_title(AccPos[1], 'Precipitation, Maximum Temperature and Minimum Temperature Map Analysis')
    accordion.set_title(AccPos[2], 'Station Level Vector Wind Analysis and Monitoring')
    accordion.set_title(AccPos[3], 'Global Synoptic Systems Monitoring')
    return accordion

def interfaceSeason(dfAll,dfWind,savePath):
    dfMeta = dFu.dataLoad(dfAll.filePath,dataChoice='metadata')
    
    station = sorted(list(dfMeta.STN_Name.unique()))
    yearsN = list(dfAll.sort_values(by=['YEAR'], ascending=False).YEAR.unique())
    seasonsN = sorted(list(dfAll.season.unique()))
    months = list(range(1,13))
    dekades = [1,2,3]

    #DISPLAYING DASHBOARD 
    
    # Station Name Selection
    #-----------------------------------------------------------    
    stnDrpD,stationNameWid = DrpDSelect(station,'station')    
    #======================================================================================
    #-------------------------------------------------------
    # Year Selection
    #-----------------------------------------------------------
    yrsDrpD,yearNeeded = DrpDSelect(yearsN,'year')    
    #======================================================================================
    #-------------------------------------------------------
    # Season Selection
    #-----------------------------------------------------------
    ssnDrpD,seasonNeeded = DrpDSelect(seasonsN,'season')
    
    if _geodata==True:
        #-------------------------------------------------------
        # Region Selection
        #-----------------------------------------------------------
        regionDrpD,regionNeeded = DrpDSelect(regions,'region')
        #-------------------------------------------------------
        # Zone Selection
        #-----------------------------------------------------------
        zoneDrpD,zoneNeeded = DrpDSelect(zones,'zone')        
        #-------------------------------------------------------
        # District Selection
        #-----------------------------------------------------------
        districtDrpD,districtNeeded = DrpDSelect(districts,'district')
        #====================================================================================
    
    #Previous event button 
    prev_button = widgets.Button(description='Previous', icon='backward')
    prev_button
    
    #The text year select display
    year_selectbox = widgets.Text(layout=Layout(width='10%'),value='2015')
    year_selectbox
    
    #Next event button 
    next_button = widgets.Button( description='Next', icon='forward')
    next_button
    
    #RadioButton event Interpolation
    interpol_Radio = widgets.RadioButtons(
        description = 'Interpolation',
        options=['IDW Method', 'Kriging Method'],
        value='IDW Method', 
        layout={'width': 'max-content'},
        disabled=False
    )
    interpol_Radio
    
    #Plotting rf event button
    #check_boxGrid = widgets.Checkbox(value = False, description='Grid', icon='check')
    #check_boxGrid
    
    def clicked(pltRf):    
        stationName,year,season = getWidOutput(stationNameWid,yearNeeded,seasonNeeded)
        if stationName == None:
            return
        
        dfOne = dFu.locSelect(dfAll,stationName)
       
        # Display selected element
        seasonRF = dFu.timeData(dfOne,'PRECIP','season')
        yearRF = dFu.timeData(dfOne,'PRECIP','year')
        seasonRD = dFu.timeData(dfOne,'RD','season')
        
        #Display plot
        rfAllAnom = pFu.yearAnom(yearRF)
        seasonRFbar = pFu.seasonBar(seasonRF,year, savePath)
        seasonCumDay = pFu.cumulativeRFday(dfOne,year,season, savePath)
            
    plt_rfbtn = widgets.Button(value=False, description='Plot')
    plt_rfbtn.style.button_color = 'darkseagreen'
    plt_rfbtn.on_click(clicked)
    
    #Plotting tmax event button
    def clicked(pltTmax):
        # Display selected station and year
        stationName,year = getWidOutput(stationNameWid,yearNeeded)
        if stationName == None:
            return
        
        dfOne = dFu.locSelect(dfAll,stationName)                           # Display selected station   
        seasonTMAX = dFu.timeData(dfOne,'TMPMAX','season')                 # Display selected element
    
        #Display plot
        seasonTMAXbar = pFu.seasonBar(seasonTMAX,year,savePath)
           
    plt_tmaxbtn = widgets.Button(value=False, description='Plot')
    plt_tmaxbtn.style.button_color = 'darkseagreen'
    plt_tmaxbtn.on_click(clicked)
    
    #Plotting tmin event button
    def clicked(pltTmin):
        # Display selected station and year
        stationName,year = getWidOutput(stationNameWid,yearNeeded)
        if stationName == None:
            return
        
        dfOne = dFu.locSelect(dfAll,stationName)                           # Display selected station   
        seasonTMIN = dFu.timeData(dfOne,'TMPMIN','season')                 # Display selected element

        #Display plot
        seasonTMINbar = pFu.seasonBar(seasonTMIN,year,savePath)

    
    plt_tminbtn = widgets.Button(value=False, description='Plot')
    plt_tminbtn.style.button_color = 'darkseagreen'
    plt_tminbtn.on_click(clicked)
    
    #Plotting Windrose event button
    def clicked(pltWinrs):
        # Display selected station
        stationName,year,season = getWidOutput(stationNameWid,yearNeeded,seasonNeeded)
        if stationName == None:
            return    

        df = dfWind
    
        wind = df[df.EG_EL == 'WINSPD'].drop_duplicates(subset=['STN_Name','dateTime']).set_index(['STN_Name','dateTime']).rename(columns={'value':'WINSPD'}).get(['season','seasonyear','dk','WINSPD'])
        wind.loc[:,'WINDIR'] = df[df.EG_EL == 'WINDIR'].drop_duplicates(subset=['STN_Name','dateTime']).set_index(['STN_Name','dateTime']).rename(columns={'value':'WINDIR'}).get(['WINDIR'])
        wind = wind.reset_index()
    
        #Display plot
        fig_winros=pFu.windRose(wind,stationName,year,season,savePath=savePath)
    
    plt_winrsbtn = widgets.Button(value=False, description='Plot')
    plt_winrsbtn.style.button_color = 'darkseagreen'
    plt_winrsbtn.on_click(clicked)
    
    if _geodata==True:
        #==================================================================
        #Maping rf event button
        def clicked(mpRf):
            year,season,region,adm2,adm3 = getWidOutput(yearNeeded,seasonNeeded,regionNeeded,zoneNeeded,districtNeeded)
            if year == None:
                return
            
            mapSsnRF = dFu.locData(dfAll,'PRECIP',year,season)
            
            df2015BegaRD = dFu.locData(dfAll,'RD',2015,'Bega')
            stationDist = mFu.stationDistr(df2015BegaRD)
            
            idwFigs = mFu.idwMap(mapSsnRF,region,savePath=savePath)
            idwFigs = mFu.idwMap(mapSsnRF,adm2=adm2,savePath=savePath)
            idwFigs = mFu.idwMap(mapSsnRF,adm3=adm3,savePath=savePath)
                
        mp_rfbtn = widgets.Button(value=False, description='Display')
        mp_rfbtn.style.button_color = 'darkseagreen'
        mp_rfbtn.on_click(clicked)
        mp_rfbtn
        
        #Maping tmax event button
        mp_tmaxbtn = pltBtnMp(dfAll,savePath,'TMPMAX',yearNeeded,seasonNeeded,None,None,regionNeeded,zoneNeeded,districtNeeded)
       
        #Maping tmin event button
        mp_tminbtn = pltBtnMp(dfAll,savePath,'TMPMIN',yearNeeded,seasonNeeded,None,None,regionNeeded,zoneNeeded,districtNeeded)

    
    #SST Nino3.4 event button
    def clicked(sstNin):
        sstAnom = pFu.sstNoaa(years=(1995,2005,2015,2021))
        
    sstN_plot = widgets.Button(value=False, description='Display')
    sstN_plot.style.button_color = 'darkseagreen'
    sstN_plot.on_click(clicked)
    
    #Analogue years selection 1991-2000
    data = {"1991":"data_1", "1992":"data_2", "1993":"data_3", "1994":"data_4", "1995":"data_5", 
            "1996":"data_6", "1997":"data_7", "1998":"data_8", "1999":"data_9", "2000":"data_10"}
    
    names = []
    checkbox_objects = []
    for key in data:
        checkbox_objects.append(widgets.Checkbox(value=False, description=key))
        names.append(key)
    
    arg_dict = {names[i]: checkbox for i, checkbox in enumerate(checkbox_objects)}
    
    ui_91_00 = widgets.VBox(children=checkbox_objects)
    
    selected_data = []
    def select_data(**kwargs):
        selected_data.clear()
    
        for key in kwargs:
            if kwargs[key] is True:
                selected_data.append(key)
    
        print(selected_data)
    
    analogOut_91_00 = widgets.interactive_output(select_data, arg_dict)
    #display(ui, analogOut)
    
    #Analogue years selection 2001-2000    
    data = {"2001":"data_1", "2002":"data_2", "2003":"data_3", "2004":"data_4", "2005":"data_5", 
            "2006":"data_6", "2007":"data_7", "2008":"data_8", "2009":"data_9", "2010":"data_10"}
    
    names = []
    checkbox_objects = []
    for key in data:
        checkbox_objects.append(widgets.Checkbox(value=False, description=key))
        names.append(key)
    
    arg_dict = {names[i]: checkbox for i, checkbox in enumerate(checkbox_objects)}
    
    ui_01_10 = widgets.VBox(children=checkbox_objects)
    
    selected_data = []
    def select_data(**kwargs):
        selected_data.clear()
    
        for key in kwargs:
            if kwargs[key] is True:
                selected_data.append(key)
    
        print(selected_data)
    
    analogOut_01_10 = widgets.interactive_output(select_data, arg_dict)
    #display(ui, analogOut)
    
    #Analogue years selection 2011-2020
    data = {"2011":"data_1", "2012":"data_2", "2013":"data_3", "2014":"data_4", "2015":"data_5", 
            "2016":"data_6", "2017":"data_7", "2018":"data_8", "2019":"data_9", "2020":"data_20"}
    
    names = []
    checkbox_objects = []
    for key in data:
        checkbox_objects.append(widgets.Checkbox(value=False, description=key))
        names.append(key)
    
    arg_dict = {names[i]: checkbox for i, checkbox in enumerate(checkbox_objects)}
    
    ui_11_20 = widgets.VBox(children=checkbox_objects)
    
    selected_data = []
    def select_data(**kwargs):
        selected_data.clear()
    
        for key in kwargs:
            if kwargs[key] is True:
                selected_data.append(key)
    
        print(selected_data)
    
    analogOut_11_20 = widgets.interactive_output(select_data, arg_dict)
    #display(ui, analogOut)
    
    #=============================================================================
    #National Checkbox
    check_boxEth = widgets.Checkbox(value=False, description='Ethiopia', icon='check')
    check_boxEth
    
    #Label 
    label_iniSt = widgets.HTML("<b>Station Selection</b>")
    label_iniPlot = widgets.HTML("<b>Seasonal Rainfall, Maximum Temperature and Minimum Temperature Plotting</b>")
    label_iniHistRF = widgets.HTML("<b>Historical, Actual, Cumulative, Mean and Anomaly Seasonal Rainfall Distribution</b>")
    label_iniHistTMax = widgets.HTML("<b>Historical, Actual, Mean and Anomaly Seasonal Maximum Temperature Distribution</b>")
    label_iniHistTMin = widgets.HTML("<b>Historical, Actual, Mean and Anomaly Seasonal Minimum Temperature Distribution</b>")
    label_iniWindrs = widgets.HTML("<b>Windrose Ploting </b>")
    
    if _geodata==True:
        label_iniIniMap = widgets.HTML("<b>Initial Setting</b>")
        label_iniMap = widgets.HTML("<b>Seasonal Rainfall, Maximum Temperature and Minimum Temperature Map Analysis</b>")
        label_iniMapRF = widgets.HTML("<b>Actual, Mean and % of Normal Seasonal Rainfall</b>")
        label_iniMapTMax = widgets.HTML("<b>Actual, Mean and Anomaly Seasonal Maximum Temperature</b>")
        label_iniMapTMin = widgets.HTML("<b>Actual, Mean and Anomaly Seasonal Minimum Temperature</b>")
        
    #Defining a layout with tabs. 
    
    tab1P = VBox(children=[HBox(children=[label_iniHistRF]), HBox(children=[plt_rfbtn])])
    tab2P = VBox(children=[HBox(children=[label_iniHistTMax]), HBox(children=[plt_tmaxbtn])])
    tab3P = VBox(children=[HBox(children=[label_iniHistTMin]), HBox(children=[plt_tminbtn])])
    
    if _geodata==True:
        tab1M = VBox(children=[HBox(children=[label_iniMapRF]),HBox(children=[prev_button, year_selectbox, next_button, mp_rfbtn])])
        tab2M = VBox(children=[HBox(children=[label_iniMapTMax]),HBox(children=[prev_button, year_selectbox, next_button, mp_tmaxbtn])])
        tab3M = VBox(children=[HBox(children=[label_iniMapTMin]),HBox(children=[prev_button, year_selectbox, next_button, mp_tminbtn])])
        
    tab1sst = VBox(children=[HBox(children=[sstN_plot])])
    tab2sst = VBox(children=[HBox(children=[ui_91_00, analogOut_91_00, sstN_plot])])
    tab3sst = VBox(children=[HBox(children=[ui_01_10, analogOut_01_10, sstN_plot])])
    tab4sst = VBox(children=[HBox(children=[ui_11_20, analogOut_11_20, sstN_plot])])
    tab5sst = VBox(children=[HBox(children=[sstN_plot])])
                   
    #=============================================================================================
    #Creating the tab instance with tabs
    tabPlot = widgets.Tab(children=[tab1P, tab2P, tab3P], layout=Layout(width = '880px'))
    tabPlot.set_title(0, 'Rainfall')
    tabPlot.set_title(1, 'Maximum Temp.')
    tabPlot.set_title(2, 'Minimum Temp.')
    
    if _geodata==True:
        tabMap = widgets.Tab(children=[tab1M, tab2M, tab3M], layout=Layout(width = '880px'))
        tabMap.set_title(0, 'Rainfall')
        tabMap.set_title(1, 'Maximum Temp.')
        tabMap.set_title(2, 'Minimum Temp.')
    
    tabSST = widgets.Tab(children=[tab1sst, tab2sst, tab3sst, tab4sst, tab5sst], layout=Layout(width = '880px'))
    tabSST.set_title(0, 'Nino3.4 SST Anom')
    tabSST.set_title(1, 'A. Years Decade I')
    tabSST.set_title(2, 'A. Years Decade II')
    tabSST.set_title(3, 'A. Years Decade III')
    tabSST.set_title(4, 'Selected A. Years')
    
    
    #=========================================================================================
    # Plot GridBox
    plotGrid = GridBox(children=[stnDrpD, yrsDrpD, ssnDrpD],
            layout=Layout(
                width='auto',
                height='auto',
                grid_template_columns='370px 300px 280px',
                grid_template_rows='50px',
                )
            )
    
    plotGrid
    
    
    # Plot Windros Gridbox
    plotGridWin = GridBox(children=[stnDrpD, yrsDrpD,ssnDrpD,plt_winrsbtn],
            layout=Layout(
                width='auto',
                height='auto',
                grid_template_columns='220px 220x',
                grid_template_rows='50px 50px'
                )
           )
    
    plotGridWin
    
    # Map GridBox
    if _geodata==True:
        mapGrid = GridBox(children=[check_boxEth, regionDrpD, zoneDrpD, districtDrpD, yrsDrpD, ssnDrpD, interpol_Radio],
                layout=Layout(
                    width='auto',
                    height='auto',
                    grid_template_columns='240px 240px 220px 250px',
                    grid_template_rows='50px 50px'
                    )
                )
    
    #The form contain VBox and HBox
    form_items1 = [ HBox(children=[label_iniSt]),
                    HBox(children=[plotGrid]),
                    HBox(children=[label_iniPlot]),
                    HBox(children=[tabPlot]),
                    ]
       
    form1 = VBox(form_items1, layout=Layout(
        width = '880px',
        align_items='center'
        ))
    
    if _geodata==True:
        form_items2 = [ HBox(children=[label_iniIniMap]),
                        HBox(children=[mapGrid]),
                        HBox(children=[label_iniMap]),
                        VBox(children=[tabMap])
                        ]
           
        form2 = VBox(form_items2, layout=Layout(
            width = '950px',
            align_items='center'
            ))
    
    form_items3 = [ VBox(children=[tabSST])
        
                    ]
       
    form3 = VBox(form_items3, layout=Layout(
        width = '950px',
        align_items='center'
        ))
    
    form_items4 = [ HBox(children=[label_iniWindrs]),
                    HBox(children=[plotGridWin])   
                    ]
       
    form4 = VBox(form_items4, layout=Layout(
        width = '950px',
        align_items='center'
        ))
    
    form_items5 = [ 
                    ]
       
    form5 = VBox(form_items5, layout=Layout(
        width = '950px',
        align_items='center'
        ))
    
    #Adding the forms to accordion
    if _geodata==True:
        AccChildren = [form1, form2, form3, form4, form5]
        AccPos = [0,1,2,3,4]
    else:
        AccChildren = [form1,form3,form4,form5]
        AccPos = [0,None,1,2,3]
    
    accordion = widgets.Accordion(children=AccChildren)
    accordion.set_title(AccPos[0], 'Precipitation, Maximum Temperature and Minimum Temperature Plotting')
    if _geodata==True:
        accordion.set_title(AccPos[1], 'Precipitation, Maximum Temperature and Minimum Temperature Map Analysis')
    accordion.set_title(AccPos[2], 'Monitoring of Nino3.4 SST Anomaly and Selection of Analogue Years')
    accordion.set_title(AccPos[3], 'Station Level Vector Wind Analysis and Monitoring')
    accordion.set_title(AccPos[4], 'Global Synoptic Systems Monitoring')
    return accordion