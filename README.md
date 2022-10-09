# Calendar of your Life

A simple to help generate a calendar of your life. I made this to specifically
help figure out what circles to highlight for the  **Kurzgesagt's Calendar of
your Life** infographic poster.

## Usage

```bash
./main.py ${PATH_TO_CALENDAR_FILE}
```


## Sample Calendar File

Setup a `yaml` file like the one below which contains event ranges.

```yaml
birthday: 1995-11-08
events:
  - name: "2y"
    color: green
    start: 1995-11-08
    end: 1997-11-08
  - name: "2y"
    color: red
    start: 1997-11-08
    end: 1999-10-09
  - name: "test"
    color: blue 
    start: 1999-10-09
    end: 2005-07-31
```
