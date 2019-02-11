from flask_restful import Resource 
from flask import Flask
from pymongo import MongoClient
from flask import request


conn = MongoClient()
db = conn.mypropertydb
data_table = db.properties


class Page(Resource):
    def get(self):

        if 'feed_ratio' in request.args and 'page' in request.args:
            feed = request.args['feed_ratio']
            page = request.args['page']
            feed = eval(feed)
            feed_11  = feed[0]['ratio']
            feed_12  = feed[1]['ratio']
            feed_16  = feed[2]['ratio']

            lst_11 = []
            lst_12 = []
            lst_16 = []

            for item in data_table.find():
                if item['feed'] == "11":
                    lst_11.append({'property_name': item['property_name'], 'Feed': item['feed'], 'Price': item['price']})
                
                elif item['feed'] == "12":
                    lst_12.append({'property_name': item['property_name'], 'Feed': item['feed'], 'Price': item['price']})
                
                else: 
                    lst_16.append({'property_name': item['property_name'], 'Feed': item['feed'], 'Price': item['price']})
            
            output = []
            position_11 = (int(page) - 1) * feed_11
            position_12 = (int(page) - 1) * feed_12
            position_16 = (int(page) - 1) * feed_16

            limit_11 = position_11 + feed_11
            limit_12 = position_12 + feed_12
            limit_16 = position_16 + feed_16

            count_11 = 0
            count_12 = 0
            count_16 = 0
            if len(lst_11) < limit_11:
                count_11 = limit_11 - len(lst_11)
                limit_11 = len(lst_11)

            if len(lst_12) < limit_12:
                count_12 = limit_12 - len(lst_12)
                limit_12 = len(lst_12)

            if len(lst_16) < limit_16:
                count_16 = limit_16 - len(lst_16)
                limit_16 = len(lst_16)


            for i in range(position_11, limit_11):
                output.append(lst_11[i])
            
            for i in range(position_12, limit_12):
                output.append(lst_12[i])

            for i in range(position_16, limit_16):
                output.append(lst_16[i])


            if len(output) < 48 and len(output) > 0 :
                count = 48 - len(output)
                x = max(len(lst_11), len(lst_12), len(lst_16))

                if x == len(lst_11) :
                    temp = count_12 + count_16
                    new_position_11 = limit_11+temp
                    if new_position_11 > len(lst_11):
                        for i in range(new_position_11, len(lst_11)):
                            output.append(lst_11[i])
                            count-=1
                            if count == 0:
                                break
                        if len(output) < 48:
                            if len(lst_12) > len(lst_16):
                                new_position_12 = len(lst_11) - new_position_11
                                for i in range(new_position_12, len(lst_12)):
                                    output.append(lst_12[i])
                                    count -= 1
                                    if count == 0:
                                        break
                            elif len(lst_16) > len(lst_12) and len(lst_16) > limit_16:
                                new_position_16 = len(lst_11) - new_position_11
                                for i in range(new_position_12, len(lst_12)):
                                    output.append(lst_16[i])
                                    count-=1
                                    if count == 0:
                                        break
                    else:
                        if len(lst_12) > len(lst_16):

                            new_position_12 = len(lst_11) - new_position_11
                            for i in range(new_position_12, len(lst_12)):
                                output.append(lst_12[i])
                                count -= 1
                                if count == 0:
                                    break
                        elif len(lst_16) > len(lst_12) and len(lst_16) > limit_16:
                            for i in range(limit_16, len(lst_16)):
                                output.append(lst_16[i])
                                count -= 1
                                if count == 0:
                                    break

                elif x == len(lst_12) :
                    temp = count_11 + count_16
                    new_position_12 = limit_12+temp
                    if new_position_12 > len(lst_12):
                        for i in range(new_position_12, len(lst_12)):
                            output.append(lst_12[i])
                            count-=1
                            if count == 0:
                                break
                        if len(output) < 48:
                            if len(lst_11) > len(lst_16):

                                for i in range(limit_11, len(lst_11)):
                                    output.append(lst_11[i])
                                    count-=1
                                    if count == 0:
                                        break
                            elif len(lst_16) > len(lst_11) and len(lst_16) > limit_16:
                                for i in range(limit_16, len(lst_16)):
                                    output.append(lst_16[i])
                                    count-=1
                                    if count == 0:
                                        break
                    else:
                        if len(lst_12) > len(lst_16):

                            new_position_12 = len(lst_11) - new_position_11
                            for i in range(new_position_12, len(lst_12)):
                                output.append(lst_12[i])
                                count -= 1
                                if count == 0:
                                    break
                        elif len(lst_16) > len(lst_12) and len(lst_16) > limit_16:
                            for i in range(limit_16, len(lst_16)):
                                output.append(lst_16[i])
                                count -= 1
                                if count == 0:
                                    break
                # elif x == len(lst_12):
                #     temp = count_11 + count_16
                #     new_position_12 = limit_12 + temp
                #     for i in range(new_position_12, len(lst_12)):
                #         output.append(lst_12[i])
                #         count-=1
                #         if count == 0:
                #             break
                #     if len(output) < 48:
                #         if len(lst_11) > len(lst_16) and len(lst_11) > limit_11:
                #             for i in range(limit_11, len(lst_11)):
                #                 output.append(lst_11[i])
                #                 count-=1
                #                 if count == 0:
                #                     break
                #         elif len(lst_16) > len(lst_11) and len(lst_16) > limit_16:
                #             for i in range(limit_16, len(lst_16)):
                #                 output.append(lst_16[i])
                #                 count-=1
                #                 if count == 0:
                #                     break
                #
                # elif x == len(lst_16):
                #     temp = count_11 + count_12
                #
                #     for i in range(limit_16+temp, len(lst_16)):
                #         output.append(lst_16[i])
                #         count-=1
                #         if count == 0:
                #             break
                #     if len(output) < 48:
                #         if len(lst_11) > len(lst_12) and len(lst_11) > limit_11:
                #             for i in range(limit_11, len(lst_11)):
                #                 output.append(lst_11[i])
                #                 count-=1
                #                 if count == 0:
                #                     break
                #         elif len(lst_12) > len(lst_11) and len(lst_12) > limit_12:
                #             for i in range(limit_12, len(lst_12)):
                #                 output.append(lst_12[i])
                #                 count-=1
                #                 if count == 0:
                #                     break

          
            return {'result': output}



        elif 'page' not in request.args and 'feed_ratio' not in request.args :
            output = []
            for item in data_table.find():
                output.append({'property_name': item['property_name'], 'Feed': item['feed'], 'Price': item['price']})
            return {'result': output}


        elif 'page' in request.args and 'feed_ratio' not in request.args:
            page_number = request.args['page']
            output = []
            x = (int(page_number) - 1) * 48
            for item in data_table.find().skip(x).limit(48):
                output.append({'property_name': item['property_name'], 'Feed': item['feed'], 'Price': item['price']})
            return {'result': output}


    
