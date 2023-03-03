from program.config import MAP_API_KEY
import requests
import json


# 簡化(get first 10) 算距離 照片url 連結url 做成carousel
def simplify_resp(resp:dict)->list:
    output = []
    if len(resp['results']) > 10:
        carousel_len = 10
    else:
        carousel_len = len(resp['results'])
    for i in range(carousel_len):
        element = resp['results'][i]
        new_dict = {}
        new_dict['name'] = element['name']
        new_dict['address'] = element['vicinity']
        # lat, lng in string
        new_dict['coords'] = [str(element['geometry']['location']['lat']), str(element['geometry']['location']['lng'])]
        new_dict['place_id'] = element['place_id']
        new_dict['photo_reference'] = element['photos'][0]['photo_reference']
        if 'rating' in element.keys():
            new_dict['rating'] = element['rating']
        else:
            new_dict['rating'] = '???'
        output.append(new_dict)
    return output

def get_distance(place_list:list, origin_coords:list)->list:
    # distance matrix api
    destinations_str = ''
    for i in range(len(place_list)):
        destinations_str += (place_list[i]['coords'][0] + '%2C' + place_list[i]['coords'][1])
        if i != len(place_list)-1:
            destinations_str += '%7C'
    
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&key={}&language=zh-TW".format(
        origin_coords[0] + '%2C' + origin_coords[1], destinations_str, MAP_API_KEY
    )
    response = requests.request('GET', url)
    resp_to_dict = json.loads(response.text)
    dist_element_list = resp_to_dict['rows'][0]['elements']
    # desired list is a list of dict
    distances = []
    for element in dist_element_list:
        distances.append(element['distance']['text'])
    # add back into place list
    for i in range(len(place_list)):
        place_list[i]['distance'] = distances[i]

    return place_list

def make_photo_url(place_list:list)->list:
    for place in place_list:
        photo_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=300&photo_reference={}&key={}'.format(
            place['photo_reference'], MAP_API_KEY
        )
        place['photo_url'] = photo_url
    return place_list
    
def make_place_url(place_list:list)->list:
    for place in place_list:
        url = 'https://www.google.com/maps/search/?api=1&query={}%2C{}&query_place_id={}'.format(
            place['coords'][0], place['coords'][1], place['place_id']
        )
        place['place_url'] = url
    return place_list

def create_carousel(place_list)->dict:
    contents = {}
    contents['type'] = 'carousel'
    bubbles = []
    for place in place_list:
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": place['photo_url'],
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": place['name'],
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "地點",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": place['address'],
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "評價",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": str(place['rating'])+' ★',
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "距離",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": place['distance'],
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "在 google map 中查看",
                    "uri": place['place_url']
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                }
                ],
                "flex": 0
            }
        }
        bubbles.append(bubble)
    contents['contents'] = bubbles
    return contents

def resp_to_carousel(resp_dict:dict, lat_lng:list)->dict:
    place_list = simplify_resp(resp_dict)
    # 經度 緯度
    place_list = get_distance(place_list, lat_lng)
    place_list = make_photo_url(place_list)
    place_list = make_place_url(place_list)
    carousel = create_carousel(place_list)
    return carousel
    
init_msg = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "哈囉！請從以下選項開始查詢",
        "weight": "bold",
        "size": "lg"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "附近有甚麼餐廳",
          "text": "附近有甚麼餐廳"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "附近有甚麼咖啡廳",
          "text": "附近有甚麼咖啡廳"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "附近有甚麼酒吧",
          "text": "附近有甚麼酒吧"
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": []
      }
    ],
    "flex": 0,
    "borderWidth": "bold"
  }
}

init_msg2 = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "請從以下選項重新開始查詢",
        "weight": "bold",
        "size": "lg"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "附近有甚麼餐廳",
          "text": "附近有甚麼餐廳"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "附近有甚麼咖啡廳",
          "text": "附近有甚麼咖啡廳"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "附近有甚麼酒吧",
          "text": "附近有甚麼酒吧"
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": []
      }
    ],
    "flex": 0,
    "borderWidth": "bold"
  }
}