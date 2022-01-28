import pandas as pd
import numpy as np
import math
from scipy.stats import norm
from Vraag2 import Vraag
import copy

alpha_numeric_dict = {"A": 0,
                      "B": 1,
                      "C": 2,
                      "D": 3,
                      "E": 4,
                      "F": 5,
                      "G": 6,
                      "H": 7,
                      "I": 8,
                      "J": 9,
                      "K": 10,
                      "L": 11,
                      "M": 12,
                      "N": 13,
                      "O": 14,
                      "P": 15,
                      "Q": 16,
                      "R": 17,
                      "S": 18,
                      "T": 19,
                      "U": 20,
                      "V": 21,
                      "W": 22,
                      "X": 23,
                      "Y": 24,
                      "Z": 25}

numeric_alpha_dict = {value : key for (key, value) in alpha_numeric_dict.items()}

def check_sort_answers_RC_NPS2(df, values):
    
    # Bereken de (N)
    N = pd.Series([df['a'].count()], index=["(N)"])
    
    # Bereken de percentages 
    percentages = (df['a'].value_counts()/df['a'].count())
    
    # Voeg totaal rij toe 
    percentages = percentages.append(N)

    # Convert percentages naar dataframe
    data_tuples = list(zip(percentages.index, percentages.values))
    data = pd.DataFrame.from_records(data_tuples, columns=['Properties (%)', 'Totaal'])
    
    #Vergeten answers toevoegen
    given_answers = list(data['Properties (%)'][0:-1])
    missing_answers = list(set(values) - set(given_answers))

    # Voeg vergeten antwoorden toe met 0% responserate
    for missing in missing_answers:
        lengte = len(data)
        line = pd.DataFrame({'Properties (%)': missing, "Totaal": 0.0}, index=[lengte])
        data = pd.concat([data.iloc[:lengte-1], line, data.iloc[lengte-1:]]).reset_index(drop=True)
    
    return data

def check_sort_answers_RC_NPS(base, column, values):
    
    given_answers = list(base[column][0:-1])
    missing_answers = list(set(values) - set(given_answers))
    
    # Voeg missing answers rows toe
    for missing in missing_answers:
        base.loc[len(base)] = 0
        base[column][len(base)-1] = missing
        n = base.loc[len(base)-2]
        base = base.drop([len(base)-2])
        base = base.reset_index(drop=True)
        base.loc[len(base)] = n
        
    columns = []
    new_data = pd.DataFrame( columns=columns)
    # Goeie order antwoorden showen
    for element in values:
        
        x = base.loc[base[column].astype(str) == element]
        new_data = new_data.append(x)
        
    x = base.loc[base[column] == "(N)"]
    new_data = new_data.append(x)
    new_data = new_data.reset_index(drop=True) 
    
    return new_data

def check_sort_answers_NV2(data, column):
    
    #Vergeten answers toevoegen
    given_answers = [str(x) for x in data['Properties (%)'][0:-1]]
    missing_answers = list(set(Vraag.syntax[column].antwoorden) - set(given_answers))

    # Voeg niet gekozen antwoorden toe met een response van 0%  
    for missing in missing_answers:
        lengte = len(data)
        line = pd.DataFrame({'Properties (%)': missing, "Totaal": 0.0}, index=[lengte])
        data = pd.concat([data.iloc[:lengte-1], line, data.iloc[lengte-1:]]).reset_index(drop=True)
        
    order = Vraag.syntax[column].antwoorden
    columns = ['Properties (%)', 'Totaal']
    new_data = pd.DataFrame( columns=columns)
    
    # Als er een volgorde is
    if len(order) != 0:
        # Voeg 1 voor 1 toe in de volgorde aan nieuw dataframe
        for element in order:
            
            x = data.loc[data['Properties (%)'].astype(str) ==  element]
            new_data = new_data.append(x)
        
        # Voeg totaal rij toe 
        x = data.loc[data['Properties (%)'] == "(N)"]
        new_data = new_data.append(x)
        new_data = new_data.reset_index(drop=True)
        return new_data
            
    else:
        
        data2 = data[0:-1]
        data2 = data2.sort_values(by=['Properties (%)'])
        x = data.loc[data['Properties (%)'] == "(N)"]
        data2 = data2.append(x)
        data2 = data2.reset_index(drop=True)
        return data2
    
def check_sort_answers_NV(base, column):
    
    # Definieer missing answers rows toe
    given_answers =  [str(x) for x in base[column][0:-1].tolist()]
    missing_answers = list(set(Vraag.syntax[column].antwoorden) - set(given_answers))
 
    # Voeg missing answers rows toe
    for missing in missing_answers:
        base.loc[len(base)] = 0
        base[column][len(base)-1] = missing
        n = base.loc[len(base)-2]
        base = base.drop([len(base)-2])
        base = base.reset_index(drop=True)
        base.loc[len(base)] = n
    
    columns = []
    new_data = pd.DataFrame( columns=columns)
    
    if len(Vraag.syntax[column].antwoorden) != 0:
    # Goeie order antwoorden showen
        for element in Vraag.syntax[column].antwoorden:
            
            x = base.loc[base[column].astype(str) == element]
            new_data = new_data.append(x)
            
        x = base.loc[base[column] == "(N)"]
        new_data = new_data.append(x)
        new_data = new_data.reset_index(drop=True) 
        
        new_data = new_data.rename(columns={column: 'Properties (%)', 'All': 'Totaal'})
        return new_data
        
    else:
        base = base.rename(columns={column: 'Properties (%)', 'All': 'Totaal'})
        return base

def dataverwerking(column, df):
    
    # Bereken de (N)
    N = pd.Series([df[column].count()], index=["(N)"])
        
    # Bereken de percentages 
    percentages = (df[column].value_counts()/df[column].count())
    
    # Voeg totaal rij toe 
    percentages = percentages.append(N)
    
    # Convert percentages naar dataframe
    data_tuples = list(zip(percentages.index, percentages.values))
    data = pd.DataFrame.from_records(data_tuples, columns=['Properties (%)', 'Totaal'])
        
    return data

def create_crosstabs(df, kruisvariabelen, data):
    
    column = df.columns[0]
    kv_list = []

    # Maak KV Tabellen
    for i in range(len(kruisvariabelen)):
        
        if i != (len(kruisvariabelen) - 1):
            kv_list.append(pd.crosstab(index = df[column], columns = data[kruisvariabelen[i]]))
            
        elif i == (len(kruisvariabelen) - 1):
            kv_list.append(pd.crosstab(index = df[column], columns = data[kruisvariabelen[i]], margins = True))
            
    # Voeg missing column answers toe aan KV's met 0% responserate
    for kv in kv_list:
 
        missing_answers = list(set(Vraag.syntax[kv.columns.name].antwoorden) - set(kv.columns))
 
        for missing in missing_answers:
            kv[missing] = 0
            
    # Zet columns in de goede volgorde
    for i in range(len(kv_list)):
        
        if i != len(kv_list) - 1:
             kv_list[i] = kv_list[i][Vraag.syntax[kv_list[i].columns.name].antwoorden]
             
        elif i == len(kv_list) - 1:
            kv_list[i] = kv_list[i][Vraag.syntax[kv_list[i].columns.name].antwoorden].join(kv_list[i]['All'])
            
    base = kv_list[0]
    duplicate_counter = 0
    
    # Combineer de kv's
    for kv in kv_list[1:]:
        for col in kv:
            if col in base.columns:
                duplicate_counter = duplicate_counter + 1
                base.insert(len(base.columns), (col+(duplicate_counter*' ')), kv[col])
            else:
                base.insert(len(base.columns), col, kv[col])

    if len(kruisvariabelen) == 1:  
        base = base[base.index != 'All']
        
    total = base.sum()
    total.name = '(N)'
    base = base.append(total.transpose())

    # Bereken percentages
    for col in base.columns[:-1]:
        if base[col][:-1].sum() == 0:
            continue
        elif base[col][:-1].sum() != 0:
            base[col][:-1] = base[col][:-1] / base[col]['(N)']

    # if column == 'V3':
    #     print(base)

    for i in base.index:
        x = df[df[column] == i].shape[0]
        base['All'][i] = x

    # if column == 'V3':
    #     print(base)

    tot = copy.copy(base['All'][:-1].sum())
    base['All'][:-1] = base['All'][:-1] / base['All'][:-1].sum()
    #base['All'][:-1] = base['All'][:-1] / len(df[column])

    # if column == 'V3':
    #     print(base)
        #raise SystemExit

    # Move total column to the front
    base = base[ ['All'] + [ col for col in base.columns if col != 'All' ] ].reset_index(drop=False)
    #base['All'][len(base)-1] = len(df[column])
    base['All'][len(base)-1] = tot

    # if column == 'V3':
    #     print(base)


    return base

def NV(df, kruisvariabelen, data):
    
    dataframe_list = []
    
    # definieer column name 
    column = df.columns[0]

    if len(kruisvariabelen) != 0:
        
        base = create_crosstabs(df, kruisvariabelen, data)
        new_data = check_sort_answers_NV(base, column)
        dataframe_list.append((new_data, 'NV'))
        print(new_data)
        raise SystemExit
        
        sign_df = sign(new_data, kruisvariabelen)

        dataframe_list.append((sign_df, 'SIG'))
     
    else:
        
        data = dataverwerking(column, df)
        new_data = check_sort_answers_NV2(data, column)
        dataframe_list.append((new_data, 'NV'))
        
            
    return dataframe_list

def NV_GEM(df, kruisvariabelen, data):

    dataframe_list = []
    
    # definieer column name 
    column = df.columns[0]
    
    if len(kruisvariabelen) != 0:

        base = create_crosstabs(df, kruisvariabelen, data)
       
        # Bereken Gem
        row_list = ['Gemiddelde']
        
        for col in base.columns[1:]:
            x = (base[col][:-1]*base[column][:-1]).sum()
            row_list.append(x)
        
        gem_df = pd.DataFrame([row_list], columns=base.columns)
        gem_df = gem_df.append(base.loc[len(base)-1])
        gem_df = gem_df.reset_index(drop=True)
        
        new_data = check_sort_answers_NV(base, column)
        dataframe_list.append((new_data, 'NV'))
        gem_df = gem_df.rename(columns={column: 'Gemiddelde', 'All': 'Totaal'})
        dataframe_list.append((gem_df, 'GEM'))      
    
    else:
        
        data = dataverwerking(column, df)
        new_data = check_sort_answers_NV2(data, column)
        dataframe_list.append((new_data, 'NV'))
        
        #gemiddelde dataframe aanmaken en toevoegen
        avg = [('Gemiddelde',df[column].mean())]
        data2 = pd.DataFrame.from_records(avg, columns=['Gemiddelde', 'Totaal'])
        data2.loc[len(df)]=['(N)',df[column].count()] 
        data2 = data2.reset_index(drop=True)
        dataframe_list.append((data2, 'GEM'))
        
    return dataframe_list

def NPS(df, kruisvariabelen, data):
    
    dataframe_list = []
    
    # definieer column name 
    column = df.columns[0]
    
    if len(kruisvariabelen) != 0:
    
        # Verdeel antwoordopties in categorieen 
        criteria = [df[column].between(0, 6), df[column].between(7,8), df[column].between(9,10)]
        values = ['Detractor','Passive','Promoter']
        df['a'] = np.select(criteria, values, 0)
        
        # Wissel columns van positie
        df = df[ ['a'] + [ col for col in df.columns if col != 'a' ] ].reset_index(drop=True)
        
        
        if len(kruisvariabelen) != 0:
    
            base = create_crosstabs(df, kruisvariabelen, data)
            base = base.rename(columns={'a': column})
            
            new_data = check_sort_answers_RC_NPS(base, column, values)    
            
            # Bereken Promter / Detractor / NPS
            promoter_score = new_data['All'][2]
            detractor_score = new_data['All'][0]
            NPS = round((promoter_score - detractor_score)*100, 0)
            
            NPS_list = ['NPS']
            
            for col in new_data.columns[1:]:
                promoter_score = new_data[col][2]
                detractor_score = new_data[col][0]
                NPS = round((promoter_score - detractor_score)*100, 0)
                NPS_list.append(NPS)
            
            line = pd.DataFrame([NPS_list], columns=base.columns, index=[len(new_data)])
            new_data = pd.concat([new_data.iloc[:len(new_data)-1], line, new_data.iloc[len(new_data)-1:]]).reset_index(drop=True)
            
            new_data = new_data.rename(columns={column: 'Net Promotor Score', 'All': 'Totaal'})
            dataframe_list.append((new_data, 'NPS'))

    else:
        
         # Verdeel antwoordopties in categorieen 
        criteria = [df[column].between(0, 6), df[column].between(7,8), df[column].between(9,10)]
        values = ['Detractor','Passive','Promoter']
        df['a'] = np.select(criteria, values, 0)
        
        data = check_sort_answers_RC_NPS2(df, values)
        
        # Bereken Promoter / Detractor / NPS
        promoter_score = data.loc[data['Properties (%)'] == 'Promoter', 'Totaal'].sum()
        detractor_score = data.loc[data['Properties (%)'] == 'Detractor', 'Totaal'].sum()
        NPS = round((promoter_score - detractor_score)*100, 0)
        
        # Zet NPS row op ena laatste plek in het Dataframe
        line = pd.DataFrame({'Properties (%)': 'NPS', "Totaal": NPS}, index=[len(data)])
        data = pd.concat([data.iloc[:len(data)-1], line, data.iloc[len(data)-1:]]).reset_index(drop=True)

        columns = ['Properties (%)', 'Totaal']
        new_data = pd.DataFrame( columns=columns)

        # Zet antwoordopties in de goede volgorde
        order = ['Promoter', 'Passive', 'Detractor', 'NPS']
        
        for element in order:
            
            x = data.loc[data['Properties (%)'].astype(str) ==  element]
            new_data = new_data.append(x)
            
        x = data.loc[data['Properties (%)'] == "(N)"]
        new_data = new_data.append(x)
        new_data = new_data.reset_index(drop=True)

        # Voeg dataframes toe aan lijst
        new_data = new_data.rename(columns={'Properties (%)': 'Net Promotor Score'})
        dataframe_list.append((new_data, 'NPS'))

    return dataframe_list

def RC_GEM(df, kruisvariabelen, data):
    
    dataframe_list = []
    
    # definieer column name 
    column = df.columns[0]
    
    if len(kruisvariabelen) != 0:
        
        base = create_crosstabs(df, kruisvariabelen, data)
        
        # Bereken Gemiddelde
        row_list = ['Gemiddelde']
        
        for col in base.columns[1:]:
            x = (base[col][:-1]*base[column][:-1]).sum()
            row_list.append(x)
        
        gem_df = pd.DataFrame([row_list], columns=base.columns)
        gem_df = gem_df.append(base.loc[len(base)-1])
        gem_df = gem_df.reset_index(drop=True)
        
    
        # Verdeel antwoordopties in categorieen 
        criteria = [df[column].between(0, 5), df[column].between(6,7), df[column].between(8,10)]
        values = ['Onvoldoende (5 of lager)','Voldoende (6 of 7)','Goed (8 of hoger)']
        df['a'] = np.select(criteria, values, 0)
        
         # Wissel columns van positie
        df = df[ ['a'] + [ col for col in df.columns if col != 'a' ] ].reset_index(drop=True)
        
        if len(kruisvariabelen) != 0:
    
            base = create_crosstabs(df, kruisvariabelen, data)
            raise SystemExit
            base = base.rename(columns={'a': column})
            
            new_data = check_sort_answers_RC_NPS(base, column, values)  

            new_data = new_data.rename(columns={column: 'Properties (%)', 'All': 'Totaal'})
            gem_df = gem_df.rename(columns={column: 'Gemiddelde', 'All': 'Totaal'})
            dataframe_list.append((new_data, 'RC'))
            dataframe_list.append((gem_df, 'GEM'))
            
    else:
        
        # Verdeel antwoordopties in categorieen 
        criteria = [df[column].between(0, 5), df[column].between(6,7), df[column].between(8,10)]
        values = ['Onvoldoende (5 of lager)','Voldoende (6 of 7)','Goed (8 of hoger)']
        df['a'] = np.select(criteria, values, 0)
        
        data = check_sort_answers_RC_NPS2(df, values)

        columns = ['Properties (%)', 'Totaal']
        new_data = pd.DataFrame( columns=columns)

        # Zet antwoordopties in de goede volgorde
        for element in values:
            
            x = data.loc[data['Properties (%)'].astype(str) ==  element]
            new_data = new_data.append(x)
            
        x = data.loc[data['Properties (%)'] == "(N)"]
        new_data = new_data.append(x)
        new_data = new_data.reset_index(drop=True)

        # Voeg dataframes toe aan lijst
        dataframe_list.append((new_data, 'RC'))
        
        #gemiddelde dataframe aanmaken en toevoegen
        avg = [('Gemiddelde',df[column].mean())]
        data2 = pd.DataFrame.from_records(avg, columns=['Gemiddelde', 'Totaal'])
        data2.loc[len(df)]=['(N)',df[column].count()] 
        data2 = data2.reset_index(drop=True)
        dataframe_list.append((data2, 'GEM'))
        #print(data2)
        
    return dataframe_list

def MV(df_list, kruisvariabelen, data):
    dataframe_list = []
    tuple_list = []
    mv_list = []
    n = 0
    
    if len(kruisvariabelen) != 0:
    
        for df in df_list:
            for column in df:
            
                base = create_crosstabs(df, kruisvariabelen, data)
                
                base = base.rename(columns={column: 'Properties (%)'})
                base.name = column
                n = base.loc[base['Properties (%)'] == '(N)'].iloc[0]
                mv_list.append(base)
        
        new_data = pd.DataFrame( columns=mv_list[0].columns)
        
    
        for element in mv_list:
            df = element.loc[element['Properties (%)'] == 1]
            df = df.reset_index(drop=True)
            df.name = element.name
            df['Properties (%)'][0] = Vraag.syntax[element.name].antwoorden[0]
            #print(df)
            
            if len(df) != 0:
                new_data = new_data.append(df.iloc[0])
                new_data = new_data.reset_index(drop=True)
            elif len(df) == 0:
                data = pd.DataFrame({"Properties (%)": Vraag.syntax[df.name].antwoorden[0]}, index=[len(new_data)])
                new_data = new_data.append(data)
                new_data = new_data.reset_index(drop=True)
         
        new_data = new_data.replace(np.nan, 0)
        new_data = new_data.append(n)
        new_data = new_data.reset_index(drop=True)
        
        dataframe_list.append((new_data, 'MR'))
        sign_df = sign(new_data, kruisvariabelen)
        dataframe_list.append((sign_df, 'SIG'))
        
        
    elif len(kruisvariabelen) == 0:

        for df in df_list:
            for column in df:
                answer_label = Vraag.syntax[column].antwoorden[0]
                tuple_list.append((answer_label, df[column].sum()/df[column].count()))
    
        data = pd.DataFrame.from_records(tuple_list, columns=['Properties (%)', 'Totaal'])
        data.loc[len(df)]=['(N)',df[column].count()]
        data = data.reset_index(drop=True)
    
        dataframe_list.append((data, 'MR'))
        #print(data)
        
    return dataframe_list

def top2Bot2(df, kruisvariabelen, data):
    
    
    dataframe_list = []
    
    # definieer column name 
    column = df.columns[0]
    
    if len(kruisvariabelen) != 0:
        
        base = create_crosstabs(df, kruisvariabelen, data)
        new_data = check_sort_answers_NV(base, column)
        dataframe_list.append((new_data, 'NV'))
        
        sign_df = sign(new_data, kruisvariabelen)
        dataframe_list.append((sign_df, 'SIG'))
        
        top1 = int(Vraag.syntax[column].soort.split("'")[1][0]) - 1 
        top2 = int(Vraag.syntax[column].soort.split("'")[1][-1])
        
        bot1 = int(Vraag.syntax[column].soort.split("'")[3][0]) - 1
        bot2 = int(Vraag.syntax[column].soort.split("'")[3][-1])
        
        #top2bot aanmaken
        top2bot2_list = []
        
        # Bereken top2
        top2 = new_data.iloc[top1:top2].sum()[1:].to_frame().transpose()
        
        # Bereken bot2
        bot2 = new_data.iloc[bot1:bot2].sum()[1:].to_frame().transpose()
        
        top2 = top2.append(bot2)
        top2['Properties (%)'] = ['Top-2', 'Bottom-2']
        
        # Move total column to the front
        top2 = top2[ ['Properties (%)'] + [ col for col in top2.columns if col != 'Properties (%)' ] ].reset_index(drop=True)
        
        top2.loc[len(top2)]=new_data.loc[len(new_data)-1]

        dataframe_list.append((top2, 'Top2Bot2'))
        
        sign_df = sign(top2, kruisvariabelen)
        dataframe_list.append((sign_df, 'SIG'))
        
     
    else:
        
        data = dataverwerking(column, df)
        new_data = check_sort_answers_NV2(data, column)
        dataframe_list.append((new_data, 'NV'))
        
        top1 = int(Vraag.syntax[column].soort.split("'")[1][0]) - 1 
        top2 = int(Vraag.syntax[column].soort.split("'")[1][-1])
        
        bot1 = int(Vraag.syntax[column].soort.split("'")[3][0]) - 1
        bot2 = int(Vraag.syntax[column].soort.split("'")[3][-1])
        
        #top2bot aanmaken
        top2bot2_list = []
        
        # Bereken top2
        top2 = new_data['Totaal'][top1]+new_data['Totaal'][top2]
        top2bot2_list.append(('Top-2', top2))
        
        # Bereken bot2
        bot2 = new_data['Totaal'][bot1]+new_data['Totaal'][bot2]
        top2bot2_list.append(('Bottom-2', bot2))
        
        tb2 = pd.DataFrame.from_records(top2bot2_list, columns=['Properties (%)', 'Totaal'])
        tb2.loc[len(tb2)]=['(N)',df[column].count()] 
        dataframe_list.append((tb2, 'Top2Bot2'))
    
    return dataframe_list


def sign(data, kruisvariabelen):
    
    #print(kruisvariabelen)
    
    dataa = data.copy()
    data_df = dataa[dataa.columns[2:]]
    start = 0

    for kv in kruisvariabelen:
        
        einde = start + len(Vraag.syntax[kv].antwoorden)
        
        kv_df = data_df[data_df.columns[start:einde]]
        #print(kv_df)
        #raise SystemExit
        saved_columns = kv_df.columns
        for c in range(len(kv_df.columns)):
            
            kv_df = kv_df.rename(columns={kv_df.columns[c]:numeric_alpha_dict[c]})
        
        kv_df2 = pd.DataFrame(index=kv_df.index, columns=kv_df.columns)
        
        for i in range(len(kv_df.columns)):
            
            columns = list(kv_df.columns[0:i]) + list(kv_df.columns[i+1:len(kv_df.columns)])
            
            for k in range(len(kv_df)-1):
                for col in columns:
                    
                    x = kv_df[kv_df.columns[i]][k]
                    xn = kv_df[kv_df.columns[i]][len(kv_df)-1]
                    
                    y = kv_df[col][k]
                    yn = kv_df[col][len(kv_df)-1]
                    
                    if x != 0 and x != 1 and y!= 0 and y != 1:
                        
                        proportion = (x*xn+y*yn)/(xn+yn)
                        z_value = (x-y)/(math.sqrt((proportion*(1-proportion))*(1/xn+1/yn)))
                        inv = norm.ppf(0.025)
                        
                        if (z_value > inv*-1):
                            kv_df2[kv_df2.columns[i]][k] = str(kv_df2[kv_df2.columns[i]][k]) + col
                        elif (z_value < inv):
                            kv_df2[kv_df2.columns[i]][k] = str(kv_df2[kv_df2.columns[i]][k]) + col
                        else:
                            pass
                            
                    
        
        for k in range(len(kv_df2)):
            for col in kv_df2.columns:
                if 'nan' in str(kv_df2[col][k]):
                    kv_df2[col][k] = str(kv_df2[col][k]).replace("nan", "")
                
        
        for c in range(len(kv_df2.columns)):
            kv_df2 = kv_df2.rename(columns={kv_df2.columns[c]:saved_columns[c]})    
        
        for col in kv_df2.columns:
            dataa[col] = kv_df2[col]
        start = einde
    
    return dataa
    
    