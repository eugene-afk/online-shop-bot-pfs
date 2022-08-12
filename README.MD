## Demo
Demo available at [@OnlineShopDemoBot](https://t.me/online_shop_demo_bot)<br/>
[Stripe testing cards](https://stripe.com/docs/testing#cards)<br/>
## Test data
Testing data for products uploading available at `.../test-data/products.json`<br />
To upload data use command /load_data in running tg bot.

## How to run

### With Docker
1. Edit database init file *.../data/mysql/init/database.sql*
2. Edit docker compose file *.../docker-compsoe.yml*, it includes comments for environment variables.
3. Run docker-compose <br/>
`sudo docker-compose up` or `sudo docker compose up` *starting time after build ~1 minute*

### Without Docker

#### Backend

1. Edit settings *.../backend/settings.py*
2. Open your terminal in `backend` folder. <br/>
3. Install virtual environment. <br/>
`python3 -m venv env`<br/>
4. Activate virtual environment.<br/>
`source env/bin/activate` on linux or `env\Scripts\activate` on windows<br/>
5. Install requirement packages.<br/>
`pip install -r requirements.dev.txt`<br/>
6. Run telegram bot first (on startup it's creating tables and writing starting data).<br/>
`python3 manage.py run_bot`<br/>
7. Edit REST API service settings at `.../backend/rest/settings.py`
8. Run REST API service.
`python3 manage.py run_rest` swagger docs available at `/docs`<br/>

*For Windows you may need run this command: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` before activate virtual environment*

#### Frontend

1. Open your terminal in `web` folder. <br/>
2. Edit REST API url at `.../web/src/api/baseUrl.js`
3. Run npm install. <br/>
`npm install`<br/>
4. Run application.<br/>
`npm start`<br/>