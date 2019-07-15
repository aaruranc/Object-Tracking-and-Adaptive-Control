














# Create csv of labelled data
df = pd.read_csv('structured_data.csv')

names = []
for index, series in df.iterrows():
    print(index)
    print(len(names))
    print('')
    obj_class = df['Class'][index]
    if pd.isna(obj_class): 
#         print('here')
        names.append(None)
        
    else:
        num = df['Image'][index]
        if pd.isna(num):
            temp = index
            while (pd.isna(num)):
#                 print('here')
                temp = temp - 1
                num = df['Image'][temp]
#         print(num)
        num = num - 2524
                
        info = data[obj_class]
        found = False
        for name in info:
            past = False
            for frame in info[name]:
                for key in frame:
#                     print('Key:')
#                     print(key)
#                     print('Num:')
#                     print(num)
#                     print(frame[key]['Score'])
#                     print(df['Score'][index])
                    if key == int(num):
                        if (frame[key]['Score'] - df['Score'][index] == 0):
#                             print('here too')
                            names.append(name)
                            found = True
                    elif key > num:
                        past = True
                
                if found or past:
                    break
                    
            if found:
                break







# Create a csv with all of the corresponding imputed data 

# Expand data first

new_data = {}
for obj_type in data:
    info = data[obj_type]
#     print(info)
    d = {}
    for obj in info:
        print(obj)
        entries = len(info[obj])        
        needs_imputed = False
        if entries > 1:
            first = True
            curr = 0
            for obj_dict in info[obj]:
                for key in obj_dict:                
                    stats = obj_dict[key]
                    if first:
                        curr = stats['frame']
                        first = False
                        continue
                    frame = stats['frame']
                    if (frame - curr) > 1:
                        needs_imputed = True
                        print('needs imputed')
                        break
                    else:
                        curr = frame
                if needs_imputed:
                    break
                    
         
        if needs_imputed:
            indices = []
#             print(info[obj])
            for entry in info[obj]:
                index = list(entry.keys())[0]
                indices.append(index)
            length = len(indices)


            temp = indices[0] + 1
            end = indices[length-1]
            prev_frame = indices[0]
            next_frame = indices[1]
            
            counter = 0
            dummy = 1
            dd = {indices[0]: info[obj][0]}
#             print('DD:')
#             print(dd)
            while (temp != end):
#                 print(temp)
                if temp not in indices:
                    next_frame = indices[counter+1]

                    while temp > next_frame:
                        counter = counter + 1
                        next_frame = indices[counter+1]
                    
                    prev_frame = indices[counter]
                    past = info[obj][counter]
                    future = info[obj][counter+1]
                    
                    window_diff = next_frame - prev_frame
                    scale = (temp - prev_frame) / window_diff
                    diff = {'Score': future[next_frame]['Score'] - past[prev_frame]['Score'],
                            'xmin': future[next_frame]['xmin'] - past[prev_frame]['xmin'],
                            'xmax': future[next_frame]['xmax'] - past[prev_frame]['xmax'],
                            'ymin': future[next_frame]['ymin'] - past[prev_frame]['ymin'],
                            'ymax': future[next_frame]['ymax'] - past[prev_frame]['ymax']}
                    
                    imputation = {'Score': past[prev_frame]['Score'] + scale*diff['Score'],
                                  'xmin': past[prev_frame]['xmin'] + scale*diff['xmin'],
                                  'xmax': past[prev_frame]['xmax'] + scale*diff['xmax'],
                                  'ymin': past[prev_frame]['ymin'] + scale*diff['ymin'],
                                  'ymax': past[prev_frame]['ymax'] + scale*diff['ymax'],
                                  'prev': prev_frame, 'next': next_frame
                                 }
                    imp = {temp: imputation}
                    
#                     dd.append()
                    dd[temp] = imputation
                    
#                     print(past)
#                     print(imp)
#                     print(future)
#                     print('')
                elif temp in indices:
                    dd[temp] = info[obj][dummy]
                    dummy = dummy + 1
                temp = temp + 1   
#             print(dd)
            d[obj] = dd
        else:
            d[obj] = info[obj]
    
    print(d)
#     print('')
    new_data[obj_type] = d
#     print(new_data)
    print('')
    print('')

# print(new_data)















k = len(ground) - 1
ground[str(k)]

imputed_ground = {}

for obj_class in new_data:
    for obj in new_data[obj_class]:
        x = new_data[obj_class][obj]
        if isinstance(x, list):
#             print('LIST')

            for i in x:
                for key in i:
                    if key in imputed_ground:
                        imputed_ground[key][obj] = i[key]
                    else:
                        imputed_ground[key] = {obj: i[key]}
                        
        elif isinstance(x, dict):
#             print('DICT')
            
            for i in x:                
                data = 0
                if i in x[i]:
                    data = x[i][i]
                else:
                    data = x[i]
                    
                if i in imputed_ground:
                    imputed_ground[i][obj] = data
                else:
                    imputed_ground[i] = {obj: data}

















df4 = pd.DataFrame(columns=['NumDetected', 'Score', 'xmin', 'xmax', 'ymin', 'ymax', 'Name'])

nums = range(0, 12762)
for i in nums:
    print(i)
    print(imputed_ground[i])
    count = 0
    for key in imputed_ground[i]:
        count = count + 1
    print(count)
    
    d= {}
    if count == 0:
        d = {'NumDetected': 0, 'Score': None, 'xmin': None, 'xmax': None, 'ymin': None, 'ymax': None, 'Name': None}
        df4 = df4.append(d, ignore_index=True)
    else:
        first = True
        for key in imputed_ground[i]:
            if count == 0:
                break
            
            obj = imputed_ground[i][key]
            if first:
                d = {'NumDetected': count, 'Score': obj['Score'], 'xmin': obj['xmin'], 'xmax': obj['xmax'], 
                     'ymin': obj['ymin'], 'ymax': obj['ymax'], 'Name': key}
                df4 = df4.append(d, ignore_index=True)
                first = False
            else:
                d = {'NumDetected': None, 'Score': obj['Score'], 'xmin': obj['xmin'], 'xmax': obj['xmax'], 
                     'ymin': obj['ymin'], 'ymax': obj['ymax'], 'Name': key}
                df4 = df4.append(d, ignore_index=True)
            
            count = count - 1


