# jma-atomfeed-reader
- Atom Feed XML reader for JMA.
- JMA is Japan Meteorological Agency.

## Use data source

- http://xml.kishou.go.jp/xmlpull.html
- Atom Feed Pattern (total 8 patterns)
    - Data retention period
        - High frequency update Type (include least 10 minutes data)
        - A hour update type (include least a few days data)
    - Date update timing
        - On Time
        - Immediately
        - Eeathquake and volcano
        - Other

## How to install

`pip install -r requirements.txt`

## How to use

```
cd jmaatomfeed
python3 reader.py https://www.data.jma.go.jp/developer/xml/feed/regular.xml
```

## How to config

- see config.py.
