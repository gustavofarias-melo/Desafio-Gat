from datetime import datetime
from pymongo import MongoClient
from fastapi import FastAPI
from API.intelxapi import intelx

app = FastAPI()
client = MongoClient(host='mongodb://localhost:27017/')
db_logs = client['logs']
db_domains_emails = client['domains_emails']
db_requests = client['requests']

# API running
intelx = intelx('b6b10024-a60d-491c-8404-1a9cca46422a')
results = intelx.search('hackerone.com', maxresults=15)
print(results)

api = open("api.txt", "w")
api.write(str(results))
api.close()


def writeLog(parameters, request: str):
    with open('./logs/logs.txt', 'a') as logs:
        msg = datetime.now().strftime(f'[%d/%m/%y] Foi realizado um {request} '
                                      f'buscando por {parameters} [%H:%M:%S]\n')
        logs.write(datetime.now().strftime(msg))
        logs.close()
        # Added the database
        db_logs.logs.insert_one({"log": "{}".format(msg)})


# all datas
@app.get('/request/emails/domains')
def return_all():
    db_data = db_domains_emails['domain_email'].find({}, {"_id": 1, "domain": 1, "email": 1})
    each_data = []
    for data in db_data:
        each_data.append(data)
    writeLog(parameters='[todos dados]', request="[GET 200]")
    return {"Data": f"{each_data}"}


# only domains
@app.get('/request/domain/{domain_name}')
def search_domain(domain_name):
    if not db_domains_emails['domain_email'].find_one({"domain": "{}".format(domain_name)}):
        writeLog(domain_name, '[GET 404]')
        return {"Error": "Domínio não existe"}

    writeLog(domain_name, '[GET 200]')
    return {f'{domain_name}': 'encontrado'}


# only email
@app.get('/request/emails/{email_name}')
def search_email(email_name):
    if db_domains_emails['domain_email'].find_one({"email": "{}".format(email_name)}):
        writeLog(email_name, "[GET 200]")
        return {f"{email_name}": "encontrado"}

    writeLog(email_name, "[GET 404]")
    return {"Error": "E-mail não encontrado"}


# return domain and email
@app.get('/request/{domain_name}/{email}')
def search_domain_email(domain_name, email_name):
    data_exist = db_domains_emails['domain_email'].find_one(
        {"domain": f"{domain_name}", "email": f"{email_name}"}, {"_id": 0, "domain": 1, "email": 1})
    if data_exist:
        writeLog(parameters={'domain': f'{domain_name}', 'email': f'{email_name}'}, request='[GET 200]')
        return data_exist

    writeLog(domain_name, '[GET 404]')
    return {"Error": "Domínio e/ou Email não existe"}


@app.post('/insert/')
def insert_data(domain_name, email_name):
    if db_domains_emails['domain_email'].insert_one(
            {"domain": f"{domain_name}", "email": f"{email_name}"}):
        writeLog(request="[POST 200]", parameters={'domain': f'{domain_name}', 'email': f'{email_name}'})
        return {"Success": "Data OK"}
    return {"Error": "Unknown"}


@app.delete('/request/delete')
def delete_data(domain_name=None, email_name=None):
    if db_domains_emails['domain_email'].find_one_and_delete(
            {'domain': f'{domain_name}', 'email': f'{email_name}'}):
        writeLog({f'{domain_name}, {email_name} as removed'}, '[DELETE 200]')
        return {f'{domain_name}': 'removed with sucess'}

    writeLog({f'{domain_name}, {email_name} not found'}, '[DELETE 404]')
    return {"Error": "Not found"}


@app.put('/request/change/')
def change_data(domain_email, email_name, new_domain, new_email):
    data_exist = db_domains_emails['domain_email'].find_one_and_replace(
        {'domain': f'{domain_email}', 'email': f'{email_name}'}, {'domain': f'{new_domain}', 'email': f'{new_email}'})
    if data_exist:
        return {'Sucess': '200'}
    return {"Not Found"}
