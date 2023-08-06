# import libraries
import json
import sys
import time
from datetime import datetime

import numpy as np
import pandas as pd
import requests
import urllib3

pd.options.mode.chained_assignment = None
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DataAccess:

    def __init__(self, userID, url):
        self.userID = userID
        self.url = url

    def get_sensor_alias(self, device_id, df, raw_metadata):
        """

        :param raw_metadata: json of device metadata
        :param device_id: string
        :param df: Dataframe
        :return: dataframe with columns having sensor alias

        Maps sensor_alias/ sensor name with corresponding sensor ID
        replaces column names with sensor_alias_sensor_id

        """

        list1 = list(df['sensor'].unique())
        if len(raw_metadata) == 0:
            raw_metadata = DataAccess.get_device_metadata(self, device_id)
        sensor_spec = 'sensors'
        sensor_param_df = pd.DataFrame(raw_metadata[sensor_spec])
        for i in list1:
            sensor_param_df1 = sensor_param_df[sensor_param_df['sensorId'] == i]
            sensor_name = sensor_param_df1.iloc[0]['sensorName']
            sensor_name = sensor_name + " (" + i + ")"
            df['sensor'] = df['sensor'].replace(i, sensor_name)
        return df

    def get_caliberation(self, device_id, df_raw):
        """

        :param df_raw: Dataframe
        :param device_id: string
        :return: Calibrated dataframe

        Perform cal on original data
             y = mx + c
             if y is greater than max value replace y with max value
             if y is less than min value replace y with min value

        """

        df_raw.sort_values("sensor", inplace=True)
        raw_metadata = DataAccess.get_device_metadata(self, device_id)
        sensor_spec = 'params'
        header = ['sensorID', 'm', 'c', 'min', 'max', 'automation']
        sen_spec_data = raw_metadata[sensor_spec].keys()
        sen_spec_data_collect = []
        for sensor in sen_spec_data:
            m = c = min_ = max_ = automation = 0
            for name_value in raw_metadata[sensor_spec][sensor]:
                if name_value['paramName'] == 'm':
                    m = name_value['paramValue']
                if name_value['paramName'] == 'c':
                    c = name_value['paramValue']
                if name_value['paramName'] == 'min':
                    min_ = name_value['paramValue']
                if name_value['paramName'] == 'max':
                    max_ = name_value['paramValue']
                if name_value['paramName'] == 'automation':
                    automation = name_value['paramValue']
            sen_spec_data_collect.append([sensor, m, c, min_, max_, automation])
        sensor_param_df = pd.DataFrame(sen_spec_data_collect, columns=header)

        sensor_data_with_meta = df_raw.merge(sensor_param_df, left_on='sensor', right_on='sensorID').drop('sensor',
                                                                                                          axis=1)
        if sensor_data_with_meta['c'].values[0] == 0 and sensor_data_with_meta["max"].values[0] == 0 and \
                sensor_data_with_meta["min"].values[0] == 0:
            sensor_data_with_meta['final_value'] = sensor_data_with_meta["value"]
        else:
            # print(sensor_data_with_meta["value"])
            sensor_data_with_meta["value"] = sensor_data_with_meta["value"].replace('BAD 255', '-99999') \
                .replace('-', '99999').replace('BAD undefined', '-99999').replace('BAD 0', '-99999')
            sensor_data_with_meta["value"] = sensor_data_with_meta["value"].astype('float')
            sensor_data_with_meta["m"] = sensor_data_with_meta["m"].astype('float')
            sensor_data_with_meta["c"] = sensor_data_with_meta["c"].astype('int')
            sensor_data_with_meta["max"] = sensor_data_with_meta["max"].replace('-', '99999').replace(
                '1000000000000000000000000000', '99999').replace('100000000000', '99999')
            if type(sensor_data_with_meta["max"][0]) != int:
                sensor_data_with_meta["max"] = sensor_data_with_meta["max"].astype(float)
            sensor_data_with_meta["min"] = sensor_data_with_meta["min"].astype('int')
            # print(sensor_data_with_meta["value"],type((sensor_data_with_meta["value"].values[0])))
            # abssensor_data_with_meta["value"] = sensor_data_with_meta["value"].astype('str')
            sensor_data_with_meta["value"] = sensor_data_with_meta["value"].astype('float')

            # print(sensor_data_with_meta["value"],,type((sensor_data_with_meta["value"].values[0])))

            sensor_data_with_meta['final_value'] = (sensor_data_with_meta['value'] * sensor_data_with_meta['m']) + \
                                                   sensor_data_with_meta['c']

            # sensor_data_with_meta['final_value'] = sensor_data_with_meta['final_value'].astype('float')
            sensor_data_with_meta['final_value'] = np.where(
                sensor_data_with_meta["final_value"] > sensor_data_with_meta["max"], sensor_data_with_meta["max"],
                sensor_data_with_meta["final_value"]
            )
            sensor_data_with_meta['final_value'] = np.where(
                sensor_data_with_meta["final_value"] < sensor_data_with_meta["min"], sensor_data_with_meta["min"],
                sensor_data_with_meta["final_value"]
            )
        df = sensor_data_with_meta[['time', 'final_value', 'sensorID']]
        df.rename(columns={'time': 'time', 'final_value': 'value', 'sensorID': 'sensor'}, inplace=True)
        return df, raw_metadata

    def time_grouping(self, df, bands):
        """

        :param df: DataFrame
        :param bands: 05,1W,1D
        :return: Dataframe

        Group time series DataFrame
        Example: The values in Dataframe are at 30s interval we can group and change the 30s interval to 5 mins, 10 mins, 1 day or 1 week.
        The resultant dataframe contains values at given interval.
        """

        df['Time'] = pd.to_datetime(df['time'])
        df.sort_values("Time", inplace=True)
        df = df.drop(['time'], axis=1)
        df = df.set_index(['Time'])
        df.index = pd.to_datetime(df.index)
        df = df.groupby(pd.Grouper(freq=str(bands) + "Min", label='right')).mean()
        df.reset_index(drop=False, inplace=True)
        return df

    def get_cleaned_table(self, df):
        """

        :param df: Raw Dataframe
        :return: Pivoted DataFrame

        The raw dataframe has columns like time, sensor, values.
        The resultant dataframe will be time sensor alias - sensor id along with their corresponding values

        """

        df = df.sort_values('time')
        df.reset_index(drop=True, inplace=True)
        results = df.pivot(index='time', columns='sensor', values='value')
        results.reset_index(drop=False, inplace=True)
        return results

    def get_device_details(self):
        """

        :return: Details Device id and Device Name of a particular account

        Dataframe with list of device ids and device names.

        """
        try:
            url = "https://" + self.url + "/api/metaData/allDevices"
            header = {'userID': self.userID}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw)
            else:
                raw_data = json.loads(response.text)['data']
                df_raw = pd.DataFrame(raw_data)
                return df_raw

        except Exception as e:
            print('Failed to fetch device Details')
            print(e)

    def get_device_metadata(self, device_id):
        """

        :param device_id: string
        :return: Json

         Every detail related to a particular device like device added date, m,c,min,max values, sensor id, sensor alias and so on

        """
        try:
            url = "https://" + self.url + "/api/metaData/device/" + device_id
            header = {'userID': self.userID}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw)
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch device Metadata')
            print(e)

    def get_userinfo(self):
        """
        :return: Json

        Details like phone,name,gender,emailed etc are fetched
        """
        try:
            url = "https://" + self.url + "/api/metaData/user"
            header = {'userID': self.userID}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw)
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch user Information')
            print(e)

    def get_dp(self, device_id, sensors=['D29'], n=1, cal=True, end_time=datetime.now()):
        """

        :param device_id: string
        :param sensors: list of sensors. Sensors is not None
        :param n: number of data points
        :param cal: True/False
        :param end_time: 'year-month-day hours:minutes:seconds'
        :return: Dataframe with values

        Get Data Point fetches data containing values of last n data points of given sensor at given time.

        """

        try:
            # lim = n
            sub_list = []
            rawdata_res = []
            e_time = pd.to_datetime(end_time)
            en_time = int(round(e_time.timestamp()))
            header = {}
            cursor = {'end': en_time,'limit': n}

            if n == 1:
                if len(sensors) == 1:
                    url = "https://" + self.url + "/api/apiLayer/getLimitedDataMultipleSensors/?device=" + device_id + "&sensor=" + \
                          sensors[0] + "&eTime=" + str(en_time) + "&lim=" + str(cursor['limit']) + "&cursor=true"
                    payload = {}
                    param = 'GET'
                    response = requests.request(param, url, headers=header, data=payload, verify=False)
                    raw = json.loads(response.text)
                    if response.status_code != 200:
                        raise ValueError(raw)
                    if 'success' in raw:
                        raise ValueError(raw)
                    if len(json.loads(response.text)) == 0:
                        raise ValueError('No Data!')
                    else:
                        raw_data = json.loads(response.text)['data']
                        df_raw = pd.DataFrame(raw_data)
                        df_raw['time'] = pd.to_datetime(df_raw['time'], utc=False)
                        df_raw['time'] = df_raw['time'].dt.tz_convert('Asia/Kolkata')
                        df_raw['time'] = df_raw['time'].dt.tz_localize(None)
                        if cal or cal == 'true' or cal == "TRUE":
                            df, metadata = DataAccess.get_caliberation(self, device_id, df_raw)
                            df = DataAccess.get_sensor_alias(self, device_id, df, metadata)
                        else:
                            df = df_raw
                            metadata = {}
                            df = DataAccess.get_sensor_alias(self, device_id, df, metadata)
                    return df

                else:
                    payload = {"sensors": sensors}
                    url = "https://" + self.url + "/api/apiLayer/getLastDps?device=" + device_id
                    param = 'PUT'
                    response = requests.request(param, url, headers=header, data=payload, verify=False)
                    raw = json.loads(response.text)
                    if response.status_code != 200:
                        raise ValueError(raw)
                    if 'success' in raw:
                        raise ValueError(raw)
                    elif len(json.loads(response.text)) == 0:
                        raise ValueError('No Data!')
                    else:
                        raw = json.loads(response.text)
                        for i in raw[0]:
                            filtered = raw[0][i]
                            sub_list = sub_list + filtered
                        df_raw = pd.DataFrame(sub_list)
                        df_raw['time'] = pd.to_datetime(df_raw['time'], utc=False)
                        df_raw['time'] = df_raw['time'].dt.tz_convert('Asia/Kolkata')
                        df_raw['time'] = df_raw['time'].dt.tz_localize(None)
                        if cal or cal == 'true' or cal == "TRUE":
                            df, metadata = DataAccess.get_caliberation(self, device_id, df_raw)
                            df = DataAccess.get_sensor_alias(self, device_id, df, metadata)
                            df = df.sort_values('time')
                            df = df.pivot(index='time', columns='sensor', values='value')
                            df.reset_index(drop=False, inplace=True)
                        else:
                            metadata = {}
                            df = DataAccess.get_sensor_alias(self, device_id, df_raw, metadata)
                            df = df.sort_values('time')
                            df = df.pivot(index='time', columns='sensor', values='value')
                            df.reset_index(drop=False, inplace=True)
                        return df
            else:
                str1 = ","
                sensor_values = str1.join(sensors)
                payload = {}
                counter = 0
                while True:
                    for record in range(counter):
                        sys.stdout.write('\r')
                        sys.stdout.write("Approx Records Fetched %d" % (10000 * record))
                        sys.stdout.flush()
                    if counter == 0:
                        url = "https://" + self.url + "/api/apiLayer/getLimitedDataMultipleSensors/?device=" + device_id + "&sensor=" + \
                              sensor_values + "&eTime=" + str(en_time) + "&lim=" + str(cursor['limit']) + "&cursor=true"
                    else:
                        url = "https://" + self.url + "/api/apiLayer/getLimitedDataMultipleSensors/?device=" + device_id + "&sensor=" + \
                              sensor_values + "&eTime=" + str(cursor['end']) + "&lim=" + str(cursor['limit']) + "&cursor=true"
                    response = requests.request("GET", url, headers=header, data=payload)
                    raw = json.loads(response.text)
                    if response.status_code != 200:
                        raise ValueError(raw)
                    if 'success' in raw:
                        raise ValueError(raw)
                    if len(json.loads(response.text)['data']) == 0:
                        raise ValueError('No Data!')
                    else:
                        raw_data = json.loads(response.text)['data']
                        cursor = json.loads(response.text)['cursor']
                        rawdata_res = rawdata_res + raw_data
                        counter = counter + 1

                    if cursor['end'] is None:
                        break
                df_raw = pd.DataFrame(rawdata_res)
                df_raw['time'] = pd.to_datetime(df_raw['time'], utc=False)
                df_raw['time'] = df_raw['time'].dt.tz_convert('Asia/Kolkata')
                df_raw['time'] = df_raw['time'].dt.tz_localize(None)
                if cal or cal == 'true' or cal == "TRUE":
                    df, metadata = DataAccess.get_caliberation(self, device_id, df_raw)
                    df = DataAccess.get_sensor_alias(self, device_id, df, metadata)
                    df = DataAccess.get_cleaned_table(self, df)
                else:
                    metadata = {}
                    df = DataAccess.get_sensor_alias(self, device_id, df_raw, metadata)
                    df = DataAccess.get_cleaned_table(self, df)
            return df
        except Exception as e:
            print(e)

    def data_query(self, device_id, start_time, end_time=datetime.now(), sensors=None, cal=True, bands=None, echo=True):
        # df = pd.DataFrame()
        rawdata_res = []
        temp = ''
        s_time = pd.to_datetime(start_time)
        st_time = int(round(s_time.timestamp())) * 1000000000
        e_time = pd.to_datetime(end_time)
        en_time = int(round(e_time.timestamp())) * 1000000000
        header = {}
        payload = {}
        counter = 0
        cursor = {'start': st_time, 'end': en_time}
        while True:
            if echo:
                for record in range(counter):
                    sys.stdout.write('\r')
                    sys.stdout.write("Approx Records Fetched %d" % (10000 * record))
                    sys.stdout.flush()
            if sensors is None:
                url_api = "https://" + self.url + "/api/apiLayer/getDataByStEt?device="
                if counter == 0:
                    temp = url_api + device_id + "&sTime=" + str(st_time) + "&eTime=" + str(en_time) + "&cursor=true"
                else:
                    temp = url_api + device_id + "&sTime=" + str(cursor['start']) + "&eTime=" + str(
                        cursor['end']) + "&cursor=true"
            if sensors is not None:
                url_api = "https://" + self.url + "/api/apiLayer/getAllData?device="
                if counter == 0:
                    str1 = ","
                    sensor_values = str1.join(sensors)
                    temp = url_api + device_id + "&sensor=" + sensor_values + "&sTime=" + str(st_time) + "&eTime=" + str(
                        en_time) + "&cursor=true"
                else:
                    str1 = ","
                    sensor_values = str1.join(sensors)
                    temp = url_api + device_id + "&sensor=" + sensor_values + "&sTime=" + str(
                        cursor['start']) + "&eTime=" + str(cursor['end']) + "&cursor=true"

            response = requests.request("GET", temp, headers=header, data=payload)
            raw = json.loads(response.text)
            if response.status_code != 200:
                raise ValueError(raw)
            if 'success' in raw:
                raise ValueError(raw)
            if len(json.loads(response.text)['data']) == 0:
                raise ValueError('No Data!')
            else:
                raw_data = json.loads(response.text)['data']
                cursor = json.loads(response.text)['cursor']
                rawdata_res = rawdata_res + raw_data
                counter = counter + 1
            if cursor['start'] is None or cursor['end'] is None:
                break
        df_raw = pd.DataFrame(rawdata_res)
        df_raw['time'] = pd.to_datetime(df_raw['time'], utc=False)
        df_raw['time'] = df_raw['time'].dt.tz_convert('Asia/Kolkata')
        df_raw['time'] = df_raw['time'].dt.tz_localize(None)

        if len(df_raw.columns) == 2:
            df_raw['sensor'] = sensors[0]

        if cal == True or cal == 'true' or cal == "TRUE":
            # #qq=qq[~qq['value'].isin(['','BAD 255','BAD 0','BAD undefined','-'])]
            df, metadata = DataAccess.get_caliberation(self, device_id, df_raw)
            df = DataAccess.get_sensor_alias(self, device_id, df, metadata)
            df = DataAccess.get_cleaned_table(self, df)
        else:
            metadata = {}
            df = DataAccess.get_sensor_alias(self, device_id, df_raw, metadata)
            df = DataAccess.get_cleaned_table(self, df)
        if bands is not None:
            df = DataAccess.time_grouping(self, df, bands)
        return df

    def publish_event(self, title, message, meta_data, hover_data, event_tags, created_on):
        """

        :param title: string
        :param message: string
        :param meta_data: string
        :param hover_data: string
        :param event_tags: string
        :param created_on: date string
        :return: json

        Fetches Data of published events based on input parameters

        """
        raw_data = []
        try:
            url = "https://" + self.url + "/api/eventTag/publishEvent"
            header = {'userID': self.userID}
            payload = {
                "title": title,
                "message": message,
                "metaData": meta_data,
                "eventTags": [event_tags],
                "hoverData": "",
                "createdOn": created_on
            }
            response = requests.request('POST', url, headers=header, json=payload, verify=True)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw)
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch event Details')
            print(e)
        return raw_data

    def get_events_in_timeslot(self, start_time, end_time):
        """

        :param start_time: date string
        :param end_time: date string
        :return: Json

        Fetches events data in given timeslot

        """
        raw_data = []
        try:
            url = "https://" + self.url + "/api/eventTag/fetchEvents/timeslot"
            header = {'userID': self.userID}
            payload = {
                "startTime": start_time,
                "endTime": end_time
            }
            response = requests.request('PUT', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw)
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch event Details')
            print(e)

        return raw_data

    def get_event_data_count(self, end_time=time.time(), count=None):
        """

        :param end_time: date string
        :param count: integer
        :return: Json
        """
        raw_data = []
        try:
            url = "https://" + self.url + "/api/eventTag/fetchEvents/count"
            header = {'userID': self.userID}
            payload = {
                "endTime": end_time,
                "count": count
            }
            response = requests.request('PUT', url, headers=header, json=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw)
            else:
                raw_data = json.loads(response.text)
                return raw_data

        except Exception as e:
            print('Failed to fetch event Count')
            print(e)

        return raw_data

    def get_event_categories(self):
        """

        :return: Event Categories Details
        """
        raw_data = []
        try:
            url = "https://" + self.url + "/api/eventTag"
            header = {'userID': self.userID}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw)
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch event Count')
            print(e)

        return raw_data

