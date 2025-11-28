import json, unittest, datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


# interpret location into a nested object by extracting the 5 parts of the location string  separated by /
# Then organise the following operation status and temp into a nested object called data  with the keys status and temperature


def convertFromFormat1 (jsonObject):

   location_parts = jsonObject['location'].split('/')

    result = {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': location_parts[0],
            'city': location_parts[1],
            'area': location_parts[2],
            'factory': location_parts[3],
            'section': location_parts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }

    return result



# parse timestamp from ISO 8601 to Unix timestamp and remap the fields to match the result.json
# https://stackoverflow.com/questions/60442518/invalid-format-string-when-parsing-iso-8601-only-in-windows 


def convertFromFormat2 (jsonObject):
    
    iso_timestamp = jsonObject['timestamp']
    dt = datetime.datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
    timestamp_ms = int(dt.timestamp() * 1000)

    result = {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp_ms,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': {
            'status': jsonObject['data']['status'],
            'temperature': jsonObject['data']['temperature']
        }
    }

    return result


def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
