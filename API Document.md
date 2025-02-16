# API Document

## Account

### /register

**POST**

Call when an account is created.

#### Request body

```json
{
  "email": "string",
  "full_name": "string",
  "date_of_birth": 1731754271,
  "ethnicity": "string",
  "gender": "string"
}
```

#### Responses

```json
{
   "message": "string"
}
```



### /login

**POST**

Call when the user logs in.

Please save the token for authorization access.

#### Request body

```json
{
  "email": "string"
}
```

#### Responses

```json
{
   "token": "string"
}
```



### /get_user_info

**GET**

**Authorization**



#### Responses

```json
{
  "email": "string",
  "full_name": "string",
  "date_of_birth": 1731754271,
  "ethnicity": "string",
  "gender": "string"
}
```



### /update_user_info

**POST**

**Authorization**



#### Request body

```json
{
  "full_name": "string",
  "date_of_birth": 1731754271,
  "ethnicity": "string",
  "gender": "string"
}
```

#### Responses

```json
{
   "message": "string"
}
```



### /get_avatar

**GET**

**Authorization**



#### Responses

```json
{
    "avatar_url": "https://media.kungcorp.io/33/avatar/avatar.png",
    "avatar_thumbnail_url": "https://media.kungcorp.io/33/avatar/avatar_thumbnail.jpg"
}
```



### /upload_avatar

**POST**

**Authorization**



#### Request body

```json
Image file
```



#### Responses

```json
{
    "avatar_url": "https://media.kungcorp.io/33/avatar/avatar.png",
    "avatar_thumbnail_url": "https://media.kungcorp.io/33/avatar/avatar_thumbnail.jpg"
}
```



## User Detail

### /get_user_details

**GET**

**Authorization**



#### Responses

```json
{
  "face_shape": "string",
  "skin_tone": 0,
  "body_dimensions": "string",
  "real_world_measurements": "string",
  "hair_style": "string",
  "hair_color": "string"
}
```



### /update_user_details

**POST**

**Authorization**



#### Request body

```json
{
  "face_shape": "string",
  "skin_tone": 0,
  "body_dimensions": "string",
  "real_world_measurements": "string",
  "hair_style": "string",
  "hair_color": "string"
}
```



#### Responses

```json
{
   "message": "string"
}
```



## Generate

### /generate

**POST**

**Authorization**



body_dimensions is a list, you need to add the key-value pairs.



#### Request body

```json
{
  	"user_details": {
      "face_shape": "long",
      "skin_tone": 2,
      "pose":"I-Pose",
      "body_dimensions": [
              {"key": "b_{main}_muscular", "value": 0.5},
              {"key": "b_{main}_overweight", "value": 1},
              {"key": "b_{main}_skinny", "value": 0},
              {"key": "b_{Head}_Neck Thickness", "value": 0},
              {"key": "b_{Head}_Neck Length", "value": 1},
              {"key": "b_{Torso}_Shoulder Width", "value": 0.3},
              {"key": "b_{Torso}_Chest Width", "value": 0},
              {"key": "b_{Torso}_Breast Size", "value": 2},
              {"key": "b_{Torso}_Waist Thickness", "value": 0},
              {"key": "b_{Torso}_Belly Size", "value": 2},
              {"key": "b_{Torso}_Hips Size", "value": 0},
              {"key": "b_{Arms}_Upper Arm Length", "value": 0},
              {"key": "b_{Arms}_Upper Arm Thickness", "value": 0},
              {"key": "b_{Arms}_Forearm Length", "value": 1},
              {"key": "b_{Arms}_Forearm Thickness", "value": 0},
              {"key": "b_{Legs}_Thigh Length", "value": 0},
              {"key": "b_{Legs}_Thigh Thickness", "value": 1},
              {"key": "b_{Legs}_Shin Length", "value": 0},
              {"key": "b_{Legs}_Shin Thickness", "value": 0},
              {"key": "b_{Arms}_Hand Width", "value": 0},
              {"key": "b_{Arms}_Hand Thickness", "value": 0},
              {"key": "b_{Legs}_Foot Length", "value": 1}
          ],
          "body_dimension_lengths": [
              {"key": "spine", "value": {"x":1.1, "y":1.2, "z":1.1}}
          ],
          "hairstyle": "10",
          "hair_color": "6B4F30FF",
          "camera_view": "Front",
          "view_mode": 0,
          "expression": "Kiss",
          "background_color_hex": "FFE4DBFF",
          "gender": "Female"
      },
      "apparel_details": {
          "brand": "brand",
          "item_id": "LongSleeve",
          "color": "Black",
          "size": "M",
          "size2": "L"
      },
      "image_options":{
          "quality": 100,
          "thumbnail_width": 128
      }
}
```



#### Responses

```json
{
   "task_id": "string"
}
```



### /generate_video

**POST**

**Authorization**



body_dimensions is a list, you need to add the key-value pairs.



#### Request body

```json
{
  	"user_details": {
      "face_shape": "long",
      "skin_tone": 2,
      "pose":"I-Pose",
      "body_dimensions": [
              {"key": "b_{main}_muscular", "value": 0.5},
              {"key": "b_{main}_overweight", "value": 1},
              {"key": "b_{main}_skinny", "value": 0},
              {"key": "b_{Head}_Neck Thickness", "value": 0},
              {"key": "b_{Head}_Neck Length", "value": 1},
              {"key": "b_{Torso}_Shoulder Width", "value": 0.3},
              {"key": "b_{Torso}_Chest Width", "value": 0},
              {"key": "b_{Torso}_Breast Size", "value": 2},
              {"key": "b_{Torso}_Waist Thickness", "value": 0},
              {"key": "b_{Torso}_Belly Size", "value": 2},
              {"key": "b_{Torso}_Hips Size", "value": 0},
              {"key": "b_{Arms}_Upper Arm Length", "value": 0},
              {"key": "b_{Arms}_Upper Arm Thickness", "value": 0},
              {"key": "b_{Arms}_Forearm Length", "value": 1},
              {"key": "b_{Arms}_Forearm Thickness", "value": 0},
              {"key": "b_{Legs}_Thigh Length", "value": 0},
              {"key": "b_{Legs}_Thigh Thickness", "value": 1},
              {"key": "b_{Legs}_Shin Length", "value": 0},
              {"key": "b_{Legs}_Shin Thickness", "value": 0},
              {"key": "b_{Arms}_Hand Width", "value": 0},
              {"key": "b_{Arms}_Hand Thickness", "value": 0},
              {"key": "b_{Legs}_Foot Length", "value": 1}
          ],
          "body_dimension_lengths": [
              {"key": "spine", "value": {"x":1.1, "y":1.2, "z":1.1}}
          ],
          "hairstyle": "10",
          "hair_color": "6B4F30FF",
          "camera_view": "Front",
          "view_mode": 0,
          "expression": "Kiss",
          "background_color_hex": "FFE4DBFF",
          "gender": "Female"
      },
      "apparel_details": {
          "brand": "brand",
          "item_id": "LongSleeve",
          "color": "Black",
          "size": "M",
          "size2": "L"
      },
      "video_options":{
          "video_live": false,
          "duration": 5,
          "negative_prompt": "",
          "prompt": "",
          "seed": 0
      }
}
```



#### Responses

```json
{
   "task_id": "string"
}
```



### /upscale

**POST**

**Authorization**



#### Request body

```json
{
   "video_url": "string"
}
```



#### Responses

```json
{
   "task_id": "string"
}
```





### /generate/{task_id}

**GET**

**Authorization**



#### Responses

```json
{
   "status": int,
   "position": int
}
```



```python
# In queue 
status=0

# Processing 
status=1

# Completed 
status=2

# Failed 
status=3

# Not in the queue
position = -1

# In process
position = 0

# There's one more task ahead
position = 1

# There are two more tasks ahead
position = 2

# There are n tasks ahead
position = n
```



## Gallery

### /get_gallery

**GET**

**Authorization**



#### Responses

```json
{
    "gallery_urls": [
        {
            "source_url": "https://media.kungcorp.io/33/gallery/3aa38a43-631e-44f4-ae1a-de16d9843cad_upscale.mp4",
            "thumbnail_url": "https://media.kungcorp.io/33/gallery/3aa38a43-631e-44f4-ae1a-de16d9843cad_upscale_thumbnail.jpg",
            "last_modified": 1739678557
        },
        {
            "source_url": "https://media.kungcorp.io/33/gallery/fa398b2c-d6c4-4e81-b58e-8585b37cbebc.mp4",
            "thumbnail_url": "https://media.kungcorp.io/33/gallery/fa398b2c-d6c4-4e81-b58e-8585b37cbebc_thumbnail.jpg",
            "last_modified": 1739678440
        },
        {
            "source_url": "https://media.kungcorp.io/33/gallery/fa398b2c-d6c4-4e81-b58e-8585b37cbebc.jpg",
            "thumbnail_url": "https://media.kungcorp.io/33/gallery/fa398b2c-d6c4-4e81-b58e-8585b37cbebc_thumbnail.jpg",
            "last_modified": 1739678350
        }
    ]
}
```



### /remove_gallery_file/{file_name}

**DELETE**

**Authorization**



#### Responses

```json
{
   "message": "string"
}
```



## Clothes

### /upload_clothes

**POST**



#### Excel Example

| URL                   | Brand  | Gender | Name   | Colors         | Colors Hex              | Sizes       |
| --------------------- | ------ | ------ | ------ | -------------- | ----------------------- | ----------- |
| https://example.com/1 | BrandA | Male   | Cloth1 | Red,Blue,Green | #FF0000,#0000FF,#008000 | S,M,L       |
| https://example.com/2 | BrandB | Female | Cloth2 | Black,White    | #000000,#FFFFFF         | XS,S,M,L,XL |
| https://example.com/3 | BrandC | Female | Cloth3 | Yellow,Purple  | #FFFF00,#800080         | M,L,XL,XXL  |



#### Request body

```json
*.xls *.xlsx
```



#### Responses

```json
{
   "message": "string"
}
```



### /get_clothes

**POST**



#### Request body

```json
{
    "url":"https://example.com/1",
    "name":"cloth1"
}
```



#### Responses

```json
{
    "gender": "Male",
    "colors": [
        "Red",
        "Blue",
        "Green"
    ],
    "sizes": [
        "S",
        "M",
        "L"
    ],
    "name": "Cloth1",
    "brand": "BrandA",
    "colors_hex": [
        "#FF0000",
        "#0000FF",
        "#008000 "
    ]
}
```



# API Call Example

1. /register
2. /login
3. /update_user_details
4. /upload_avatar
5. /generate
6. Poll the **/generate/{taskid}** every 5 seconds using the task id
7. When status is 2, go next step
8. /get_gallery
9. Use task id to match the image
10. /get_gallery_image/{url}

