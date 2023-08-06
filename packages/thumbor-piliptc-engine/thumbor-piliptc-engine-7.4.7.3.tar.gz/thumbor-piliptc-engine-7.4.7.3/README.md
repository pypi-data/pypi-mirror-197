# thumbor-piliptc-engine

thumbor-piliptc-engine is a patched version from the legacy Pil imaging engine for [thumbor](https://github.com/thumbor/thumbor).

![](/thumbor-piliptc-engine.png?raw=true)

## IPTC tags :
JPEG IPTC (International Press Telecommunications Council) tags are a set of metadata that can be embedded into JPEG image files to provide information about the image content, including ownership and copyright information. These tags can be used by photographers, artists, and publishers to identify their work and protect their intellectual property rights. By including IPTC tags in their JPEG images, creators can ensure that their ownership and copyright information is attached to their work and remains with it as it is shared and distributed across the internet. This can be particularly important for photographers and other creators who rely on their work to generate income, as it can help deter unauthorized use and ensure that they are properly credited for their work. In this way, JPEG IPTC tags can play an essential role in protecting the intellectual property of creators and maintaining the integrity of their work.


In Europe, image copyright is protected by various laws and regulations, such as the Berne Convention for the Protection of Literary and Artistic Works and the Directive on the harmonization of certain aspects of copyright and related rights in the information society. These laws provide creators with exclusive rights over their works, including photographs and images, and require that any use of these works by others be authorized or licensed by the creator.


The use of JPEG IPTC tags can be particularly helpful in enforcing these copyright laws. **In fact, some countries in Europe, such as France and Germany, have enacted specific laws that require the use of IPTC tags on certain types of images, such as those used in advertising and editorial content.** These laws require that the copyright owner's name and contact information be included in the IPTC tags, making it easier for potential infringers to identify and contact the owner for permission to use the image.



## Thumbor :

this project is related with this issue : [Preserve IPTC metadata #1301](https://github.com/thumbor/thumbor/issues/1301)
> [kkopachev](https://github.com/kkopachev) This is not possible now with default Pillow engine, as Pillow itself does not have a way to save IPTC/XMP data.

> [scorphus](https://github.com/scorphus) You can try and use thumbor-wand-engine, which is a new engine built on top of ImageMagick with support to IPTC/XMP data.

So we must choose between legacy  engine 'thumbor.engines.pil' (Pillow) or 'thumbor_wand_engine' (imagemagick) if you want to preserve original image IPTC tags.

I tried the thumbor_wand_engine : it works fine ! it's maybe slower than "pil" but "thumbor" generated image contains iptc tags.

![](/pil-vs-wand-2.png?raw=true)

**We need this feature for european/french laws compliance" about copyright.**

I don't want to speak here about avantage/disavantage from each engine : speed, memory consumption, image rendering/quality ...

**I wanted to stay on "pil" engine and provide IPTC preservation : so i start this small project.**


In a near futur, i will try to "merge request" this feature on thumbor official project but it can be rejected because i add a new package dependance with [iptcinfo3](https://github.com/james-see/iptcinfo3).

## Releases:

v0.1.0 : pre-release : just a proof of concept : working version but not ready for production

**v0.2.0 : remove [iptcinfo3](https://github.com/james-see/iptcinfo3) package requirement : write my own iptc raw copy class to optimize usage within thumbor**

**v1.0.0 : add [JpegIPTC](https://github.com/gdegoulet/JpegIPTC) package**

**v7.4.7 : new version modele**

## Try it !

[https://hub.docker.com/repository/docker/gdegoulet/thumbor_piliptc_engine/general](https://hub.docker.com/repository/docker/gdegoulet/thumbor_piliptc_engine/general)

```
docker run --rm -it gdegoulet/thumbor_piliptc_engine:latest      pip list | egrep -i "(thumbor|iptc|jpeg|pillow)"
JpegIPTC               1.1
libthumbor             2.0.2
Pillow                 9.4.0
thumbor                7.4.7
thumbor-piliptc-engine 7.4.7
thumbor-plugins        0.2.4
thumbor-plugins-gifv   0.1.2
thumbor-wand-engine    0.1.1

docker run --rm -it -p8902:8000 \
  -e LOG_LEVEL=DEBUG \
  -e ENGINE=thumbor_piliptc_engine \
  -e PRESERVE_EXIF_INFO=True \
  -e FILE_LOADER_ROOT_PATH=/data/thumbor/tmp \
  -e FILE_STORAGE_ROOT_PATH=/data/thumbor/storage \
  -e RESULT_STORAGE_FILE_STORAGE_ROOT_PATH=/data/thumbor/result_storage \
  -e RESULT_STORAGE_STORES_UNSAFE=True \
  docker.io/gdegoulet/thumbor_piliptc_engine
```

```
wget -O test.jpg "http://localhost:8902/unsafe/x200/filters:quality(70)/i.f1g.fr/media/cms/1936x527_cropupscale/2023/03/11/1a1f02bd710b9768995d58a5e2cdbeb8e89be7fa7215476a8ea55e8c4951ceac.jpg"

iptc test.jpg | head
test.jpg:
 Tag      Name                 Type      Size  Value
 -------- -------------------- --------- ----  -----
 1:000    Model Version        Short        2  2
 1:020    File Format          Short        2  1
 1:022    File Version         Short        2  2
 1:030    Service Identifier   String       9  AFP-PHOTO
 1:040    Envelope Number      NumString    8  12345678
 1:060    Envelope Priority    NumString    1  5
 1:070    Date Sent            Date         8  20230311
```

## Installation

You can install the package from this repository with `pip`:

    $ pip install git+https://github.com/gdegoulet/thumbor-piliptc-engine@v7.4.7.1

    or

    pip install thumbor-piliptc-engine==7.4.7.1

### Requirements
-   Python 3.7 or higher
-   Thumbor (same version than thumbor-piliptc-engine )
-   git (for now, you can only install from github repository )
-   iptcinfo3 (configured as dependance)

```
root@44171bd2df65:/src# pip install     --no-cache-dir     --prefix="${PYTHONUSERBASE}" git+https://github.com/gdegoulet/thumbor-piliptc-engine

Processing ./thumbor-piliptc-engine
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Collecting JpegIPTC@ git+https://github.com/gdegoulet/JpegIPTC@v1.2
  Cloning https://github.com/gdegoulet/JpegIPTC (to revision v1.2) to /tmp/pip-install-q_46r3la/jpegiptc_ef90d167450740b397ed6774fca992e2
  Running command git clone --filter=blob:none --quiet https://github.com/gdegoulet/JpegIPTC /tmp/pip-install-q_46r3la/jpegiptc_ef90d167450740b397ed6774fca992e2
  Resolved https://github.com/gdegoulet/JpegIPTC to commit 88d2433d1eb1e27d3dbe8267cb595d06fb36e092
  Preparing metadata (setup.py) ... done
Requirement already satisfied: thumbor>=7.1 in /app/lib/python3.11/site-packages (from thumbor-piliptc-engine==1.1.0) (7.4.7)
Requirement already satisfied: pillow>=9.0 in /app/lib/python3.11/site-packages (from thumbor-piliptc-engine==1.1.0) (9.4.0)
Requirement already satisfied: colorama==0.*,>=0.4.3 in /app/lib/python3.11/site-packages (from thumbor>=7.1->thumbor-piliptc-engine==1.1.0) (0.4.6)
Requirement already satisfied: derpconf==0.*,>=0.8.3 in /app/lib/python3.11/site-packages (from thumbor>=7.1->thumbor-piliptc-engine==1.1.0) (0.8.3)
Requirement already satisfied: libthumbor==2.*,>=2.0.2 in /app/lib/python3.11/site-packages (from thumbor>=7.1->thumbor-piliptc-engine==1.1.0) (2.0.2)
Requirement already satisfied: piexif==1.*,>=1.1.3 in /app/lib/python3.11/site-packages (from thumbor>=7.1->thumbor-piliptc-engine==1.1.0) (1.1.3)
Requirement already satisfied: pytz>=2019.3.0 in /app/lib/python3.11/site-packages (from thumbor>=7.1->thumbor-piliptc-engine==1.1.0) (2022.7.1)
Requirement already satisfied: statsd==3.*,>=3.3.0 in /app/lib/python3.11/site-packages (from thumbor>=7.1->thumbor-piliptc-engine==1.1.0) (3.3.0)
Requirement already satisfied: tornado==6.*,>=6.0.3 in /app/lib/python3.11/site-packages (from thumbor>=7.1->thumbor-piliptc-engine==1.1.0) (6.2)
Requirement already satisfied: thumbor-plugins-gifv==0.*,>=0.1.2 in /app/lib/python3.11/site-packages (from thumbor>=7.1->thumbor-piliptc-engine==1.1.0) (0.1.2)
Requirement already satisfied: webcolors==1.*,>=1.10.0 in /app/lib/python3.11/site-packages (from thumbor>=7.1->thumbor-piliptc-engine==1.1.0) (1.11.1)
Requirement already satisfied: six in /app/lib/python3.11/site-packages (from derpconf==0.*,>=0.8.3->thumbor>=7.1->thumbor-piliptc-engine==1.1.0) (1.16.0)
Building wheels for collected packages: thumbor-piliptc-engine, JpegIPTC
  Building wheel for thumbor-piliptc-engine (pyproject.toml) ... done
  Created wheel for thumbor-piliptc-engine: filename=thumbor_piliptc_engine-1.1.0-py3-none-any.whl size=16750 sha256=94a8fc46f363d22a3bd2c1f15989952bcbbde53ec116dc5db9c9a9e262112a57
  Stored in directory: /tmp/pip-ephem-wheel-cache-tjp9zvzc/wheels/f0/21/40/0e8f20f4be68abb8d80c9cf2fe548f6f3cfd352df72825930c
  Building wheel for JpegIPTC (setup.py) ... done
  Created wheel for JpegIPTC: filename=JpegIPTC-1.1-py3-none-any.whl size=7268 sha256=37a3edbbe2c6ab462aa7c65a83ed0e6be7b67f26c09a05c75d591283fb51dbaa
  Stored in directory: /tmp/pip-ephem-wheel-cache-tjp9zvzc/wheels/c3/f2/e5/05cf3aa7051cf5d7db96fa57f2b7bd453d867f448b016c70c3
Successfully built thumbor-piliptc-engine JpegIPTC
Installing collected packages: JpegIPTC, thumbor-piliptc-engine
  Attempting uninstall: thumbor-piliptc-engine
    Found existing installation: thumbor-piliptc-engine 0.3.0
    Uninstalling thumbor-piliptc-engine-0.3.0:
      Successfully uninstalled thumbor-piliptc-engine-0.3.0
Successfully installed JpegIPTC-1.1 thumbor-piliptc-engine-1.1.0
```


## Usage

To use this engine with thumbor, define `thumbor_piliptc_engine` as the imaging
engine in `thumbor.conf`:

```python
ENGINE = "thumbor_piliptc_engine"
```


## Example


```
wget https://i.f1g.fr/media/cms/509x286_crop/2022/11/21/76bde3fc961f0fa8733756922d1e2ed06311d804ec38b89dc60d6ba36d30e046.jpg


iptc 76bde3fc961f0fa8733756922d1e2ed06311d804ec38b89dc60d6ba36d30e046.jpg
76bde3fc961f0fa8733756922d1e2ed06311d804ec38b89dc60d6ba36d30e046.jpg:
 Tag      Name                 Type      Size  Value
 -------- -------------------- --------- ----  -----
 1:000    Model Version        Short        2  2
 1:020    File Format          Short        2  1
 1:022    File Version         Short        2  2
 1:030    Service Identifier   String       9  AFP-PHOTO
 1:040    Envelope Number      NumString    8  12345678
 1:060    Envelope Priority    NumString    1  5
 1:070    Date Sent            Date         8  20221120
 1:080    Time Sent            Time        11  210118+0000
 1:090    Coded Character Set  Binary       3  1b 2d 41
 1:100    Unique Name of Objec String      11  AFP_32PC4R2
 2:000    Record Version       Short        2  2
 2:005    Object Name          String      27  UKRAINE-RUSSIA-WAR-CONFLICT
 2:010    Urgency              NumString    1  5
 2:012:00 Subject Reference    String      45  IPTC:16009000:unrest, conflicts and  war:war:
 2:012:01 Subject Reference    String      41  IPTC:16000000:unrest, conflicts and  war:
 2:015    Category             String       3  WAR
 2:020    Supplemental Categor String       3  war
 2:025:00 Keywords             String       3  war
 2:025:01 Keywords             String      10  Horizontal
 2:055    Date Created         Date         8  20221120
 2:060    Time Created         Time        11  152935+0300
 2:062    Digital Creation Dat Date         8  20221120
 2:063    Digital Creation Tim Time        11  152935+0300
 2:065    Originating Program  String      22  g2mapping/libg2 3.9.39
 2:070    Program Version      String       6  3.9.15
 2:080    By-line              String      12  BULENT KILIC
 2:085    By-line Title        String       3  STF
 2:090    City                 String      12  Chornobaivka
 2:100    Country Code         String       3  UKR
 2:101    Country Name         String       7  Ukraine
 2:110    Credit               String       3  AFP
 2:115    Source               String       3  AFP
 2:116    Copyright Notice     String      16  AFP or licensors
 2:120    Caption/Abstract     String     242  A Ukrainian soldier walks in front of a destroyed building of the International Airport of Kherson in the village of Chornobaivka, outskirts of Kherson, on November 20, 2022, amid the Russian invasion of Ukraine. (Photo by BULENT KILIC / AFP)
 2:135    Language Identifier  String       2  EN



wget -O test.jpg "http://localhost:8901/unsafe/filters:quality(60)/i.f1g.fr/media/cms/509x286_crop/2022/11/21/76bde3fc961f0fa8733756922d1e2ed06311d804ec38b89dc60d6ba36d30e046.jpg"
--2023-03-09 19:05:53--  http://localhost:8901/unsafe/filters:quality(60)/i.f1g.fr/media/cms/509x286_crop/2022/11/21/76bde3fc961f0fa8733756922d1e2ed06311d804ec38b89dc60d6ba36d30e046.jpg
Resolving localhost (localhost)... 127.0.0.1
Connecting to localhost (localhost)|127.0.0.1|:8901... connected.
HTTP request sent, awaiting response... 200 OK
Length: 31970 (31K) [image/jpeg]
Saving to: 'test.jpg'

test.jpg                                                  100%[===================================================================================================================================>]  31,22K  --.-KB/s    in 0s

2023-03-09 19:05:53 (348 MB/s) - 'test.jpg' saved [31970/31970]

iptc test.jpg
test.jpg:
 Tag      Name                 Type      Size  Value
 -------- -------------------- --------- ----  -----
 1:000    Model Version        Short        2  2
 1:020    File Format          Short        2  1
 1:022    File Version         Short        2  2
 1:030    Service Identifier   String       9  AFP-PHOTO
 1:040    Envelope Number      NumString    8  12345678
 1:060    Envelope Priority    NumString    1  5
 1:070    Date Sent            Date         8  20221120
 1:080    Time Sent            Time        11  210118+0000
 1:090    Coded Character Set  Binary       3  1b 2d 41
 1:100    Unique Name of Objec String      11  AFP_32PC4R2
 2:000    Record Version       Short        2  2
 2:005    Object Name          String      27  UKRAINE-RUSSIA-WAR-CONFLICT
 2:010    Urgency              NumString    1  5
 2:012:00 Subject Reference    String      45  IPTC:16009000:unrest, conflicts and  war:war:
 2:012:01 Subject Reference    String      41  IPTC:16000000:unrest, conflicts and  war:
 2:015    Category             String       3  WAR
 2:020    Supplemental Categor String       3  war
 2:025:00 Keywords             String       3  war
 2:025:01 Keywords             String      10  Horizontal
 2:055    Date Created         Date         8  20221120
 2:060    Time Created         Time        11  152935+0300
 2:062    Digital Creation Dat Date         8  20221120
 2:063    Digital Creation Tim Time        11  152935+0300
 2:065    Originating Program  String      22  g2mapping/libg2 3.9.39
 2:070    Program Version      String       6  3.9.15
 2:080    By-line              String      12  BULENT KILIC
 2:085    By-line Title        String       3  STF
 2:090    City                 String      12  Chornobaivka
 2:100    Country Code         String       3  UKR
 2:101    Country Name         String       7  Ukraine
 2:110    Credit               String       3  AFP
 2:115    Source               String       3  AFP
 2:116    Copyright Notice     String      16  AFP or licensors
 2:120    Caption/Abstract     String     242  A Ukrainian soldier walks in front of a destroyed building of the International Airport of Kherson in the village of Chornobaivka, outskirts of Kherson, on November 20, 2022, amid the Russian invasion of Ukraine. (Photo by BULENT KILIC / AFP)
 2:135    Language Identifier  String       2  EN
```

## Logs


```
root@44171bd2df65:/src# thumbor --port=8000 --conf=/usr/src/app/thumbor.conf -l DEBUG
2023-03-11 16:22:52 root:DEBUG thumbor starting at 0.0.0.0:8000
2023-03-11 16:22:52 asyncio:DEBUG Using selector: EpollSelector
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: response.count:1
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: response.none_smart:1
2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: response.none_smart:0
2023-03-11 16:23:07 thumbor:DEBUG [RESULT_STORAGE] getting from /data/thumbor/result_storage/default/16/10/fc6d87db0af8192db5a48d82b016d4c28918
2023-03-11 16:23:07 thumbor:DEBUG [RESULT_STORAGE] image not found at /data/thumbor/result_storage/default/16/10/fc6d87db0af8192db5a48d82b016d4c28918
2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: result_storage.incoming_time:0
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: result_storage.miss:1
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: storage.miss:1
2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: original_image.fetch.200.i_f1g_fr:59
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: original_image.fetch.200.i_f1g_fr:1
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: original_image.status.200:1
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: original_image.status.200.i_f1g_fr:1
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: original_image.response_bytes:38698
2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: iptc_passthrough_create_image.time:0
2023-03-11 16:23:07 thumbor:DEBUG creating tempfile for i.f1g.fr/media/cms/509x286_crop/2022/11/21/76bde3fc961f0fa8733756922d1e2ed06311d804ec38b89dc60d6ba36d30e046.jpg in /data/thumbor/storage/c8/a265b39d5bec5b40ca5a3714d34fbc04be5aae.e65963ced7774178a74318dfcc414161...
2023-03-11 16:23:07 thumbor:DEBUG moving tempfile /data/thumbor/storage/c8/a265b39d5bec5b40ca5a3714d34fbc04be5aae.e65963ced7774178a74318dfcc414161 to /data/thumbor/storage/c8/a265b39d5bec5b40ca5a3714d34fbc04be5aae...
2023-03-11 16:23:07 thumbor:DEBUG No image format specified. Retrieving from the image extension: .jpg.
2023-03-11 16:23:07 thumbor:DEBUG Content Type of image/jpeg detected.
2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: iptc_passthrough_read.time:0
2023-03-11 16:23:07 tornado.access:INFO 200 GET /unsafe/filters:quality(60)/i.f1g.fr/media/cms/509x286_crop/2022/11/21/76bde3fc961f0fa8733756922d1e2ed06311d804ec38b89dc60d6ba36d30e046.jpg (10.201.2.1) 99.44ms
2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: response.time:98
2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: response.time.200:98
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: response.status.200:1
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: response.not_smart.count:1
2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: response.not_smart.latency:98
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: response.format.jpg:1
2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: response.time.jpg:98
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: response.bytes.jpg:32132
2023-03-11 16:23:07 thumbor:DEBUG [RESULT_STORAGE] putting at /data/thumbor/result_storage/default/16/10/fc6d87db0af8192db5a48d82b016d4c28918 (/data/thumbor/result_storage/default/16/10)
2023-03-11 16:23:07 thumbor:DEBUG METRICS: inc: result_storage.bytes_written:32132
2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: result_storage.outgoing_time:0

```

**2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: iptc_passthrough_create_image.time:0**

...

**2023-03-11 16:23:07 thumbor:DEBUG METRICS: timing: iptc_passthrough_read.time:0**
