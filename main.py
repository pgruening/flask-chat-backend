import multiprocessing as mp
import app
import time


class Reader():
    def __init__(self):
        self.receive_qu = app.send_qu

    def run(self):
        print('Starting reader')
        while True:
            if not self.receive_qu.empty():
                data = self.receive_qu.get()
                print('found data')
                print(data)
                data['message'] = 'My answer!'
                print(data)
                app.receive_qu.put(data)

            else:
                time.sleep(1.)


if __name__ == '__main__':

    app_process = mp.Process(target=app.app.run)
    app_process.start()

    reader = Reader()
    read_process = mp.Process(target=reader.run)
    read_process.start()
