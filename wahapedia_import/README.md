# wh40kdata

## Rough steps

Install `mysql 8`, if not already installed, make a database called `wahapedia`

Create `config.py` based on `example.config.py` and populate with your credentials

Install `python 3` and run `python3 updateInputData.py`

Run `python3 ingestion.py` to populate your local db

Install node ~15, then navigate to `cd exportion` and run `npm i` to install node modules

From `exportion/`, run `npm start` to start the server, then navigate to [http://localhost:3000/](http://localhost:3000/)

Click a faction and then, in the browser’s network inspector, copy the returned object to paste into a rulebook’s (im/ex)port window