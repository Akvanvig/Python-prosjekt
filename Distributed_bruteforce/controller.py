"""
Venter på innkommende meldinger som enten gir oppgaver å jobbe med, eller etterspør et rom å søke gjennom

Tar inn "Kode" som skal knekkes, samt rom det skal søkes i, (muligens størrelse på hver enkelt arbeidoppgave?) og eventuell hashing-algoritme.

Fordeler arbeidoppgaver ved å motta en forespørsel, og sender ut "Kode", tegn, arbeidsnodens søkerom, samt hashing-algoritme.

Tar inn resultater (enten svar, eller beskjed om at koden ikke er i søkerommet den ble gitt), og slutter å dele ut oppgaver basert på den koden om den er funnet (returnerer svar til den som sendte dette inn).

All kommunikasjon skal foregå via JSON api-kall
"""
#Webserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

#Other needed packages
import json
from random import random
from math import floor

#Required variables
tasks = []

#Settings
port = 80
address = 'localhost'

def main():
    #def __init__(self, start_point, end_point, keyword, chars, searchwidth, algorithm, id):
    tasks.append(Task('a','dddd','dddc','abcde',10, 'none', gen_task_id(tasks)))
    tasks.append(Task('0','5555','300','012345',10, 'none', gen_task_id(tasks)))

    #Starting webServer
    print('Starting Webserver on {}:{}'.format(address, port))
    httpd = HTTPServer((address, port), webServer)
    httpd.serve_forever()

def get_next_job():
    for task in tasks:
        job = task.get_task_worker()
        if not job['finished']:
            if job['free_block']:
                return job
            else:
                task.set_finished()
    return {
        'finished':True,
        'free_block':False,
        'keyword':'',
        'chars':'',
        'algorithm':'',
        'start_point':'',
        'end_point':''
    }

def get_next_job_json():
    return json.dumps(get_next_job())

def gen_task_id(tasks):
    task_id_unique = False
    temp_id = floor(random()*10000)
    while not task_id_unique:
        task_id_unique = True
        temp_id = floor(random()*10000)
        for task in tasks:
            if task.id == temp_id:
                task_id_unique = False
    return temp_id

class Task:
    def __init__(self, start_point, end_point, keyword, chars, searchwidth, algorithm, id):
        self.start_point = start_point  # Where to start searching
        self.end_point = end_point      # Where to end the search
        self.keyword = keyword          # What you're searching for
        self.chars = chars              # Characters that can be used
        self.searchwidth = searchwidth  # How large blocks will each worker-node be given at a time
        self.algorithm = algorithm      # How is keyword hashed/encrypted
        self.id = id                    #ID to connect results to tasks

        self.current_point = self.start_point # Will be increased as workers are given blocks to search through
        self.finished = False
        self.keyword_found = ""

    def get_task(self):
        return {
            'id':self.id,
            'finished':self.finished,
            'algorithm':self.algorithm,
            'start_point':self.start_point,
            'end_point':self.end_point,
            'keyword':self.keyword,
            'chars':self.chars,
            'searchwidth':self.searchwidth,
            'current_point':self.current_point,
            'keyword_found':self.keyword_found
        }

    def get_task_worker(self):
        """
        Retrieves all info needed for worker and puts it into a dictionary
        """
        start, end = self.get_block()
        return {
            'task_id':self.id,
            'finished':self.finished,
            'free_block':(start != end),
            'keyword':self.keyword,
            'chars':self.chars,
            'algorithm':self.algorithm,
            'start_point':start,
            'end_point':end
        }

    def get_block(self):
        """
        Retrives the next block to be worked on and updates current_point
        """
        current_value = self.get_value(self.current_point)
        endpoint_value = self.get_value(self.end_point)
        worker_start = self.current_point
        if (endpoint_value - current_value) > self.searchwidth:
            worker_end = self.get_word_from_value(current_value + self.searchwidth - 1)
            self.current_point = self.get_word_from_value(current_value + self.searchwidth)
        else:
            worker_end = self.end_point
            self.current_point = worker_end

        return worker_start, worker_end

    def get_value(self, str):
        """
        Beregner verdien fra base x-tall til base 10-tall
        Bruker variablene:
            str         = ordet som det skal beregnes verdi for
            self.chars  = alle tegnene som brukes (f.eks. "0123456789")
        """
        base = len(self.chars)
        base_placement = len(str) - 1
        value = 0
        for symbol in str:
            valueChar = self.chars.find(symbol)
            value += valueChar * (base ** base_placement)
            base_placement -= 1
        return value

    def get_word_from_value(self, value):
        """
        Beregner base-x ordet gitt base-10 verdien, og returnerer denne
        Variabler
            value       = base-10 verdien av kodeordet
            str         = verdiene kodeordet skal beregnes fra
            self.chars  = alle tegnene som brukes (f.eks. "abcdefghij")
        """
        base = len(self.chars)
        str = ""
        while value != 0:
            remainder = value % base
            value = int((value - remainder) / base)
            str = self.chars[remainder] + str
        return str

    def set_finished(self):
        self.finished = True

class webServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Handles standard GET-requests and get_job-requests
        """
        path = self.path
        status_code, res = webServer.handle_get_msg(path)
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(res.encode())

    def handle_get_msg(path):
        if path == "/get_job":
            #return 200, get_next_job_json()
            job = {'job':get_next_job_json()}
            return 200, webServer.add_json_successfull_status(job)
        elif path == "/get_tasks":
            res = []
            for task in tasks:
                res.append(task.get_task())
            return 200, json.dumps(res)
        else:
            return 404, 'Hello, world! \n{}'.format(path)


    def do_POST(self):
        """
        Handles all POST-requests, message is decoded in handle_post_msg()
        """
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        response = BytesIO()
        try:
            res = webServer.handle_post_msg(body)
            print(res)
            self.send_response(200)
        except Exception as e:
            print(e)
            res = str(e)
            self.send_response(500)
        self.end_headers()
        response.write(res.encode())
        self.wfile.write(response.getvalue())

    def handle_post_msg(body):
        """
        Takes in a request, converts to dictionary and handles request according to type specified in request
        Required
            type
            subtype
        Types/subtypes:
            get
                job
                tasks
            post
                result
            create
                task
            test
                post
        """
        request = json.loads(body)
        type = request['type']
        subtype = request['subtype']
        if type == 'get':
            if subtype == 'job':
                job = {'job':get_next_job()}
                return webServer.add_json_successfull_status(job)
            elif subtype == 'tasks':
                res = []
                for task in tasks:
                    res.append(task.get_task())
                res = {'tasks':res}
                return webServer.add_json_successfull_status(res)

        elif type == 'post':
            if subtype == 'result':
                start_point = request['start_point']
                end_point = request['end_point']
                found_keyword_bool = request['found_keyword_bool']
                keyword_found = request['keyword_found']
                task_id = request['task_id']
                if found_keyword_bool:
                    for task in tasks:
                        if task.id == task_id:
                            task.set_finished()
                            task.keyword_found = keyword_found
                            return webServer.make_json_status(1, "Result delivered successfully")
                    return webServer.make_json_status(0, "Couldn't find task")

        elif type == 'create':
            if subtype == 'task':
                start_point = request['start_point']
                end_point = request['end_point']
                keyword = request['keyword']
                chars = request['chars']
                searchwidth = request['searchwidth']
                algorithm = request['algorithm']
                tasks.append(Task(start_point,end_point,keyword,chars,searchwidth,algorithm,gen_task_id(tasks)))
                return webServer.make_json_status(1, "Successfully created new task")

        elif type == 'test':
            if subtype == 'post':
                return webServer.make_json_status(1, "Successful")

        #If correct type cannot be found
        return webServer.make_json_status(0, "Task Failed")

    def make_json_status(status_code, message):
        return json.dumps({"status_code":status_code, "status":message})
    def add_json_successfull_status(res):
        res['status_code'] = 1
        res['status'] = 'Successful'
        res = json.dumps(res)
        return res



if __name__=='__main__':
    main()
